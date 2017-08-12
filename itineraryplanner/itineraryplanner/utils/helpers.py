# -*- coding: utf-8 -*-
import itertools
import os
import pprint
import re
import subprocess
import time
from random import randrange

from django.conf import settings
from django.template.defaultfilters import slugify

APPS_DIR = settings.APPS_DIR.root

def write_pddl_file(file_contents, file_name="itinerary_problem.pddl"):
    """
    Creates the directory if it doesn't exist and the files needed

    """
    try:
        os.chdir(APPS_DIR + "/pddl_files")
    except OSError:
        os.mkdir("pddl_files")
        os.chdir("pddl_files")
    try:
        os.chdir("user_files")
    except FileExistsError:
        os.mkdir("user_files")
        os.chdir("user_files")
    except FileNotFoundError:
        os.mkdir("user_files")
        os.chdir("user_files")
    pddl_file = open(file_name, "w+")
    pddl_file.write(file_contents)
    pddl_file.close()


def _slug_strip(value, separator=None):
    """
    Cleans up a slug by removing slug separator characters that occur at the
    beginning or end of a slug. A separator may occur at the end of a slug if
    for example a slug generated by django has been shortened and the end of
    the shortened slug happens to be a separator. (e.g. slug=test-slug,
    slug[:5] would result in the slug 'test-')

    If an alternate separator has been supplied, any instances of the default
    '-' separator will be replaced with the new separator.
    """
    if separator == '-' or not separator:
        re_sep = '-'
    else:
        re_sep = '(?:-|%s)' % re.escape(separator)
        value = re.sub('%s+' % re_sep, separator, value)
    return re.sub(r'^%s+|%s+$' % (re_sep, re_sep), '', value)


def unique_slugify(instance, value, slug_field_name='slug', queryset=None,
                   slug_separator='-'):
    """
    Calculates a unique slug of ``value`` for an instance.
    ``slug_field_name`` should be a string matching the name of the field to
    store the slug in (and the field to check against for uniqueness).
    ``queryset`` usually doesn't need to be explicitly provided - it'll default
    to using the ``.all()`` queryset from the model's default manager.
    """

    # Grab an instance of the slug field for the working model based on the
    # name of the slug field for that model. Default is 'slug'
    slug_field = instance._meta.get_field(slug_field_name)
    # Get the slug field of the model instance to work on. This is the value
    # we'd like to set.
    slug = getattr(instance, slug_field.attname)
    max_length = slug_field.max_length

    # Generate an initial slug using the django helper slugify(). Chop the
    # generated slug down to our max_length value if necessary
    slug = slugify(value)
    if max_length:
        slug = slug[:max_length]
    slug = _slug_strip(slug, slug_separator)
    original_slug = slug

    # Create a queryset, excluding the current instance.
    if not queryset:
        queryset = instance.__class__._default_manager.all()
        if instance.pk:
            queryset = queryset.exclude(pk=instance.pk)

    # Find a unique slug. If one matches, at '-2' to the end and try again
    # (then '-3', etc).
    for x in itertools.count(1):
        if not queryset.filter(**{slug_field_name: slug}).exists():
            break

        # Truncate the original slug dynamically. Minus 1 for the hyphen.
        slug = "%s-%d" % (original_slug[:max_length - len(str(x)) - 1], x)

    setattr(instance, slug_field.attname, slug)


def create_pddl_problem(itinerary,output_plan=False):
    """ Helper function that forms the pddl file of th given itinerary.
    The customization in each pddl file will be created using the
    preferences properties inside the Preference table attached to each
    itinerary (i.e. each itinerary contains preferences at least for
    one place and at most one for each of the places involced)
    """
    tabs = {
        1: '\t',
        2: '\t\t',
        3: '\t\t\t',
        4: '\t\t\t\t',
        5: '\t\t\t\t\t',
    }
    initial_location = itinerary.initialPOI
    ending_location = itinerary.endingPOI
    places = itinerary.get_itinerary_places()
    steps = itinerary.steps.all()
    travel_methods = itinerary.get_all_travel_methods()
    print("............creating objects....")
    header = "(define (problem itinerary-{})\n\
        (:domain touristinfo)".format(itinerary.slug)
    objects = "\n\t(:objects "
    init = "\t(:init \n"
    times = ""
    goals = "{0}(:goal\n{1}(and\n".format(tabs[1], tabs[2])
    if initial_location:
        tourist_starting_location = "{0}(at tourist1 {1})\n".format(
            tabs[2], initial_location.slug)
    if ending_location:
        tourist_ending_location = "{0}(at tourist1 {1})\n".format(
            tabs[3], ending_location.slug)
        goals += tourist_ending_location
    else:
        goals += "{0}{1}".format(tabs[1], tourist_starting_location)
    paths = ""
    traveltimes = ""
    visit_for = ""
    constraints = "{0}(:constraints\n{1}(and\n".format(tabs[1], tabs[2])
    metrics = "\n{0}(:metric minimize\n{1}(+\n{2}(total-time)\n{3}(* {4}\
    \n{5}(+\n".format(tabs[1], tabs[2], tabs[3], tabs[3], 1000, tabs[4])
    for step in steps:
        # first we get the paths
        # if step.origin.slug != place:
        origin = step.origin.slug
        destination = step.destination.slug
        method = step.get_travel_method()
        camel_case = step.origin.get_camelCase()
        # we need the duration in minutes rounded
        duration = round(step.duration / 60, 2)
        paths += "{0}(path {1} {2})\n".format(tabs[2], origin, destination)
        # afterwards we need to get the traveltimes per traveling method
        # for travel_method in travel_methods:
        traveltimes += "{0}(=(traveltime {1} {2} {3}){4})\n".format(
            tabs[2], method, origin, destination, duration)
    for place in places:
        # Getting all the preferences added by the user on each place
        place_preferences = itinerary.itinerary_preference.filter(
            place__slug=place).get()
        # we make sure to get the slug and camel case for the constraints and goals
        slug = place_preferences.place.slug
        camel_case = place_preferences.place.get_camelCase()
        opens = place_preferences.place.opens
        closes = place_preferences.place.closes
        # adding each of the places to the object declaration of the pddl program
        objects += "{0} ".format(place)
        # getting the duration of the visits.
        if place_preferences:
            # get the opening and closing times if they exist otherwise opens at 0
            if opens and closes:
                # Normal Escenario with opening and closing times
                times += "{0}(at {1} (open {2}))\n".format(
                    tabs[2], opens, slug)
                times += "{0}(at {1} (not (open {2})))\n".format(
                    tabs[2], closes, slug)
            elif opens:
                # scenario where place opens 24 hours so no closing.
                if opens == '0000':
                    # means that the place opens 24 hours
                    times += "{0}(at {1} (open {2}))\n".format(
                        tabs[2], 0, slug)
            else:
                times += "{0}(at {1} (open {2}))\n".format(
                    tabs[2], 0, slug)
            # getting the constraints
            # which places does the user wants to visit
            # TODO: make sure the constraints don't overlap everything else (overkill)
            # probably constraints are the place for must.
            constraints += "{0}(preference {1} (at end (visited tourist1 {2})))\n".format(
                tabs[3], camel_case, slug)
            # amount of time the user wants to spend in each place.
            visit_for += "{0}(=(visitfor {1} tourist1){2})\n".format(
                tabs[2], place, place_preferences.visitFor)
            # the user may say a place is a MUST in his list.
            # Therefore we evauate these preferences.
            if place_preferences.must_visit:
                goals += "{0}(preference {1} (visited tourist1 {2}))\n".format(
                    tabs[3], camel_case, slug)
                metrics += "{0}(is-violated {1})\n".format(tabs[5], camel_case)

    visit_for += "\t)\n"  # ending of visit_for
    goals += "\t\t)\n\t)\n"  # ending of goals
    constraints += "{0})\n{1})".format(tabs[2], tabs[1])
    metrics += "{0})\n{1})\n{2})\n{3})\n)".format(
        tabs[4], tabs[3], tabs[2], tabs[1])
    objects += " - location tourist1 - tourist bus walk - mode)\n"
    # print(header, objects, init, times, tourist_starting_location,
    #      paths, traveltimes, visit_for, goals, constraints, metrics)
    file_contents = header + objects + init + times + tourist_starting_location + \
        paths + traveltimes + visit_for + goals + constraints + metrics
    # Print the plan in the console if true...
    if output_plan:
        print(file_contents)
    return file_contents


def read_optic_output(itinerary_slug):
    """ This method will get the itinerary output
    file and convert it into a big string.
    After that other functions can use the entire plan.
    """
    outputs_dir = "/pddl_files/outputs/itinerary-{}.txt".format(itinerary_slug)
    file_loc = APPS_DIR+outputs_dir
    # immediately need to run read otherwise is lost...
    file = open(file_loc, 'r')
    # plan should be a string.
    plan = file.read()
    # look for the "with open..." code to avoid manual close.
    file.close()
    return convert_plan(plan)
    #raise NotImplementedError()

def convert_plan(plan):
    """ This method receives the plan as a string.
    Then it runs through the regex compiler to produce a set of instructions.
    After this it returns a dictionary with the name of the place as the key,
    and both the index (order in which the planner suggest to visit the place)
    and the duration of the 'task' as values.
    """
    # import pdb;pdb.set_trace()
    instruction_set = {}
    # Using python raw string to avoid multiple escape chars '/'.
    # import ipdb;ipdb.set_trace()
    regex = re.compile(
        r"^\d+.\d+: \({1}[a-z0-9 -]*\){1}  \[[0-9.]*\]$", re.MULTILINE)
    find_goals = re.compile(r"(?<=; Plan found with metric )\d+.\d+",re.MULTILINE)
    last_result_index = None
    # TODO: Improve this iteration as right now seems prone to errors.
    
    for last_result_index in find_goals.finditer(plan):
        pass
    if not last_result_index:
        raise(TypeError)
    planner_steps = regex.findall(plan,last_result_index.span()[1])
    counter = 0
    for instruction in planner_steps:
        moving_instruction = re.findall(r"\(move.+\)", instruction)
        print("Moving Instructions: ", moving_instruction)
        for move in moving_instruction:
            splitter = []  #  will hold each bit of each instruction
            starting = move.find("(") + 1
            ending = move.find(")")
            splitter = move[starting:ending].split()
            instruction_set[counter] = {
                'method': splitter[-1],
                'from': splitter[-3],
                'to': splitter[-2],
                'index': counter,
            }
            counter = counter+1
    print(instruction_set)
    return instruction_set

def run_subprocess(itinerary_slug, sleep_for=None, domain_file=None):
    """
    Receives the itinerary_slug of a tourist and runs it in Optic with the
    given domain file. If no domain file is given, then the default domain
    file is used. If no sleep_for time is given then we stop at 2 seconds.
    """
    if itinerary_slug is None:
        raise IOError
    if sleep_for is None or sleep_for == 0:
        sleep_for = 2.0
    problem_file = APPS_DIR + "/pddl_files/user_files/itinerary-{}.pddl".format(itinerary_slug)
    if not domain_file:
        domain_file = APPS_DIR + "/pddl_files/domain.pddl"
    commands = ['optic-cplex',
                domain_file,
                problem_file]
    proc = subprocess.Popen(commands, stdout=subprocess.PIPE)
    time.sleep(sleep_for)
    proc.terminate()
    text = proc.stdout.read().decode("UTF-8")
    print(freeze_output_file(itinerary_slug,text))
    pprint.pprint(text)
    return text

def freeze_output_file(itinerary_slug, text):
    """ This methods saves the output from the planner into a
    file inside the outputs folder. That way we can test if something went
    wrong or if the plan wasn't as accurate as we would wanted it to be.
    """
    file_name = "itinerary-{}.txt".format(itinerary_slug)
    file_loc = APPS_DIR+"/pddl_files/outputs/"
    pddl_file = open(file_loc+file_name,'w')
    pddl_file.write(text)
    pddl_file.close()
    return file_name