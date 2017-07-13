# -*- coding: utf-8 -*-
import copy
import calendar
import datetime
import itertools
import os
from random import randrange
import re
import uuid
from django.template.defaultfilters import slugify


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


def create_pddl_problem(itinerary):
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
    header = "(define (problem {})\n\
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
    constraints = "{0}(:constraints\n{1}(and\n".format(tabs[1],tabs[2])
    metrics = "\t(:metric minimize\n\t\t(+\n\t\t\t(total-time)\n\t\t\t(* {}\
    \n\t\t\t\t(+\n".format(1000)
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
        # then we get the opening and closing times if they exist. otherwise none
        if step.origin.opens != "":
            times += "{0}(at {1} (open {2}))\n".format(
                tabs[2], step.origin.opens, step.origin.slug)
            times += "{0}(at {1} (not (open {2})))\n".format(
                tabs[2], step.origin.closes, step.origin.slug)

        metrics += "\t\t\t\t\t(is-violated {})\n".format(camel_case)
    metrics += "\t\t\t\t)\n\t\t\t)\n\t\t)\n\t)\n)"
    for place in places:
        place_preferences = itinerary.itinerary_preference.filter(
            place__slug=place).get()
        objects += "{} ".format(place)
        # getting the duration of the visits.
        if place_preferences:
            # getting the constraints
            constraints += "{0}(preference {1} (at end (visited tourist1 {2})))\n".format(tabs[3], camel_case, origin)
            visit_for += "{0}(=(visitfor {1} tourist1){2})\n".format(
                tabs[2], place, place_preferences.visitFor)
            if place_preferences.must_visit:
                goals += "{0}(preference {1} (visited tourist1 {2}))\n".format(
                    tabs[3], place_preferences.place.get_camelCase(), place)

    visit_for += "\t)\n"  # ending of visit_for
    goals += "\t\t)\n\t)\n"  # ending of goals
    constraints += "{0})\n{1})".format(tabs[2], tabs[1])
    objects += " - location tourist1 - tourist bus walk - mode)\n"
    print(header, objects, init, times, tourist_starting_location,
          times, paths, traveltimes, visit_for, goals, constraints)
