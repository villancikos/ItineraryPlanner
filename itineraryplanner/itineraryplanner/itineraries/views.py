"""
This view receives the input from the user. 
Validates it and creates a POI or updates it.
Then creates the ItineraryStep for each possible combination.
Adds everything to the Itinerary model and sends it to the 
server to compute the desired TOUR.
"""
# pylint: disable=E1101
import json
import pprint
import re

import googlemaps
from django.core.urlresolvers import reverse_lazy
from django.http import HttpResponse, JsonResponse
from django.views.generic.edit import FormView

from ..utils.helpers import (convert_plan, create_pddl_problem, run_subprocess,
                             write_pddl_file)
from .forms import PlacesOfInterestForm
from .models import Itinerary, ItineraryStep, PlaceOfInterest, Preferences

#gmaps = googlemaps.Client(key='AIzaSyBucexwP3IjpafwcJVPR3KtRnhqk-1sa00')
gmaps = googlemaps.Client(key='AIzaSyAxJ5w-FZlmrRB6VGyQdD2U18Oqr0QTLxs')


class PlacesOfInterestView(FormView):
    """
    View for receiving the user input and convert
    it to a POI object for the database.
    1. Checks if the POI exists or create it.
    2. Also gets the distances between each point between them.
    3. Saves both PlacesOfInterest and ItineraryStep models.
    4. Also saves everything to the Itinerary model to run it.
    """
    template_name = 'itineraries/index.html'
    form_class = PlacesOfInterestForm
    success_url = reverse_lazy('itineraries:itineraryPicker')

    def render_to_json_response(self, context, **response_kwargs):
        """Render a json response of the context."""

        data = json.dumps(context)
        response_kwargs['content_type'] = 'application/json'
        return HttpResponse(data, **response_kwargs)

    def get_context_data(self, **kwargs):
        context = super(PlacesOfInterestView,
                        self).get_context_data(**kwargs)
        context['success_url'] = self.success_url
        return context

    def post(self, request, *args, **kwargs):
        """
        TBD
        """
        form = self.get_form()
        if form.is_valid():
            return self.form_valid(form)
        else:
            return self.form_invalid(form)

    def form_invalid(self, form):
        print("oh noes!!!")
        print(form)
        return super(PlacesOfInterestView, self).form_invalid(form)

    def form_valid(self, form):
        response = super(PlacesOfInterestView, self).form_valid(form)
        # This method is called when valid form data has been POSTed.
        # It should return an HttpResponse.

        #places_to_visit_json = form.cleaned_data['placesToVisit']
        places_to_visit = json.loads(form.cleaned_data['placesToVisit'])
        preferences = json.loads(form.cleaned_data['preferences'])
        properties = json.loads(form.cleaned_data['properties'])
        # Get the user preferente for running the Plan.
        # Make sure to get a Valid Int before hand, else parse a 5 second parameter.

        run_plan_for = int(properties['runFor'])
        awaken_times = {
            'awaken': properties['wakeUpTime'],
            'not_awaken': properties['sleepTime']
        }
        transporation_methods = properties['methods']
        print("Printing Properties.\n", properties)
        print("Printing Run For.\n", run_plan_for)
        #distanceMatrixJson = form.cleaned_data['distanceMatrix']
        #distanceMatrixObject = json.loads(distanceMatrixJson)
        created_places = []
        for place in places_to_visit:
            # To DEBUG remove comments
            # print("Place with id: {0} and title: {2} \n Coordinates lat:{3},lng:{4}.\
            # \n Opens at:{5} and Closes at:{6}  ".format(
            #     place['place_id'],
            #     place['is_hotel'],
            #     place['name'],
            #     place['lat'],
            #     place['lng'],
            #     place['opens'],
            #     place['closes']
            # ))
            # we first try update the place in case it exists.
            # otherwise we just create it and carry on with the
            # relations with other Models in the database
            opens = place['opens'] or ""
            closes = place['closes'] or ""
            obj, created = PlaceOfInterest.objects.update_or_create(  # pylint: disable=W0612
                place_id=place['place_id'],
                defaults={
                    "is_hotel": place['is_hotel'],
                    "name": place['name'],
                    "lat": place['lat'],
                    "lng": place['lng'],
                    "opens": opens,
                    "closes": closes,
                }
            )
            # TODO:not the most elegant solution for the preference problem
            created_places.append(obj)
            # To DEBUG remove comments
            # if created:
            #     print("'{}' was created successfully".format(obj.name))
            # else:
            #     print("'{0}' was already in the database with id={1}".format(
            #         obj.name, obj.place_id))
            # print(obj, ", was created?: ", created)
        # Create an Itinerary Object to hold the tour.
        itinerary = Itinerary()
        # Initialize start and end at variables to store the itinerary initial and ending
        start_at = ''
        end_at = ''
        # get the mentioned places from the preferences
        for key, value in preferences.items():
            if value['startAt'] != False:
                start_at = value['startAt']
            if value['endAt'] != False:
                end_at = value['endAt']
        # set the initial and ending POI
        itinerary.initialPOI = PlaceOfInterest.objects.get(place_id=start_at)
        itinerary.endingPOI = PlaceOfInterest.objects.get(place_id=end_at)
        itinerary.save()
        for place in created_places:
            visit_for = preferences[place.place_id]['visitFor']
            priority = preferences[place.place_id]['priority']
            Preferences.objects.create(
                itinerary=itinerary,
                place=place,
                visitFor=visit_for,
                priority=priority,
            )
        # TODO: Fix this as it runs more than needed.
        # Traverse all the possible origins
        for origin in places_to_visit:
            # Traverse all the possible destinations
            for destination in places_to_visit:
                # for each destination check that is not the same as origin
                # then save the object as an Itinerary Step and compute duration of trip
                if destination != origin:
                    origin_poi = PlaceOfInterest.objects.get(place_id=origin['place_id'])
                    destination_poi = PlaceOfInterest.objects.get(place_id=destination['place_id'])
                    # Call Google distance matrix with user's parameters
                    if transporation_methods:
                        for key, value in transporation_methods.items():
                            if value:
                                method_choice = {
                                    'walking': ItineraryStep.METHOD_CHOICES.WALK,
                                    'bicycling': ItineraryStep.METHOD_CHOICES.BIKE,
                                    'driving': ItineraryStep.METHOD_CHOICES.CAR,
                                    'transit': ItineraryStep.METHOD_CHOICES.TUBE,
                                }
                                dmx = gmaps.distance_matrix(
                                    origins='place_id:{}'.format(origin['place_id']),
                                    destinations='place_id:{}'.format(destination['place_id']),
                                    mode=key,
                                    language="english"
                                )
                                print("End of the API call.")
                                it_step = ItineraryStep.objects.create(
                                    origin=origin_poi,
                                    destination=destination_poi,
                                    itinerary=itinerary,
                                    # TODO: (driving, walking, bicycling, transit)
                                    method=method_choice[key]
                                )
                                duration = dmx['rows'][0]['elements'][0]['duration']['value']
                                it_step.duration = duration
                                it_step.save()

                # To DEBUG remove comments
                # else:
                #     print("Destination:{0} and Origin:{0} are the same".format(destination, origin))

        '''
        all_distances = itinerary.get_distance_matrix_places_format()
        dmx = gmaps.distance_matrix(
            origins=all_distances,
            destinations=all_distances,
            mode='walking',
            language='english'
        )
        print("Got distances. {} Elements.\n{}".format(len(dmx),dmx))
        for outer in enumerate(all_distances):
            for inner in enumerate(all_distances):
                if not outer[1] == inner[1]:
                    it_step = ItineraryStep.objects.get(itinerary=itinerary,origin__place_id=outer[1][9:],destination__place_id=inner[1][9:])
                    it_step.duration = dmx['rows'][outer[0]]['elements'][inner[0]]['duration']['value']
                    it_step.save()
                    #print("FROM ", outer[1][9:]," TO ",inner[1][9:])
                    #print(dmx['rows'][outer[0]]['elements'][inner[0]]['duration']['value'])
        '''
        # one liner to print steps just to verify
        # [print(step) for step in itinerary.steps.all()]
        # create the string that will be embeded in the problem file.
        file_contents = create_pddl_problem(itinerary, awaken_times, output_plan=False)
        file_name = "{0}-{1}.{2}".format("itinerary", str(itinerary.slug), "pddl")
        # add contents to file.
        write_pddl_file(file_contents, file_name)
        try:
            # run optic, save output to a txt file and pass the final plan to plan var.
            plan = run_subprocess(itinerary.slug, sleep_for=run_plan_for)
            # from the plan variable convert the plan to an actual python dictionary.
            plan_dict = convert_plan(plan)
        except TypeError:
            data = {
                'message': 'An error occurred whilst running the itinerary.'
            }
            return JsonResponse(data, status=400)
        except:
            data = {
                'message': 'The server didn\'t come up with a feasible plan, sorry!'
            }
            return JsonResponse(data, status=400)
        """
        Example of Dict that we will generate.
        {0: 
            {'index': 0, 
            'visitFor': '30', 
            'place': 'place_id'}
        },
        {1:
            {'index': 1,
            'visitFor': '40',
            'place': 'place_id'}
        }

        for index in enumerate(visit_plan_dict):
            place_preference = itinerary.itinerary_preference.filter(
                place__slug=visit_plan_dict[index[0]]
            ).get()
            place_preference.index = visit_plan_dict[index[0]]['index']
            place_preference.save()
        """
        for index in enumerate(plan_dict):
            current_index = index[0]
            if plan_dict[current_index]['method'] == 'visit':
                # we have a visit instruction, let's update properties.
                place_preference = itinerary.itinerary_preference.filter(
                    place__slug=plan_dict[current_index]['place']
                ).get()
                place_preference.index = plan_dict[current_index]['index']
                place_preference.save()
                # add Google's place_id to dictionary.
                plan_dict[current_index]['visitPlaceId'] = place_preference.place.place_id
            else:
                # means we have a moving instruction.
                method_string = plan_dict[current_index]['method'].upper()
                method_value = getattr(ItineraryStep.METHOD_CHOICES, method_string)
                current_step_qs = itinerary.steps.filter(
                    origin__slug=plan_dict[current_index]['from']
                ).filter(
                    destination__slug=plan_dict[current_index]['to']
                ).filter(
                    method=method_value
                ).get()
                current_step_qs.index = plan_dict[current_index]['index']
                current_step_qs.save()
                # add Google's place_id to dictionary.
                plan_dict[current_index]['fromPlaceId'] = current_step_qs.origin.place_id
                plan_dict[current_index]['toPlaceId'] = current_step_qs.destination.place_id
        pprint.pprint(plan_dict)
        plan_json = json.dumps(plan_dict, ensure_ascii=False)
        if self.request.is_ajax():
            # Request is ajax, send a json response
            data = {
                'final_plan': plan_json
            }
            return JsonResponse(data, status=200)
        return response
