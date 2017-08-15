"""
This view receives the input from the user. 
Validates it and creates a POI or updates it.
Then creates the ItineraryStep for each possible combination.
Adds everything to the Itinerary model and sends it to the 
server to compute the desired TOUR.
"""
# pylint: disable=E1101
import json
import re
from random import randrange

import googlemaps
from django.core.urlresolvers import reverse_lazy
from django.http import HttpResponse, JsonResponse
from django.views.generic.edit import FormView

from .forms import PlacesOfInterestForm
from .models import Itinerary, ItineraryStep, PlaceOfInterest, Preferences
from ..utils.helpers import create_pddl_problem, write_pddl_file,run_subprocess,convert_plan

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
        #import ipdb;ipdb.set_trace()
        response = super(PlacesOfInterestView, self).form_valid(form)
        # This method is called when valid form data has been POSTed.
        # It should return an HttpResponse.

        #places_to_visit_json = form.cleaned_data['placesToVisit']
        places_to_visit = json.loads(form.cleaned_data['placesToVisit'])
        preferences = json.loads(form.cleaned_data['preferences'])
        print(preferences)
        for key,value in preferences.items():
            print(key, value)
        
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
        # TODO: Remove this default initial place of interest.
        # in the near future we want the user to select his desired starting point
        # e.g. the HOTEL or another initial Place of Interest
        random_place = created_places[randrange(0, len(created_places))]
        itinerary.initialPOI = random_place
        itinerary.save()
        for place in created_places:
            Preferences.objects.create(
                itinerary=itinerary,
                place=place,
                visitFor=randrange(30, 90)
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
                    it_step = ItineraryStep.objects.create(
                        origin=origin_poi,
                        destination=destination_poi,
                        itinerary=itinerary,
                        # TODO: each transportation Method from Google api (driving, walking, bicycling, transit)
                        method=ItineraryStep.METHOD_CHOICES.WALK
                    )
                    '''
                    dmx = gmaps.distance_matrix(
                        origins='place_id:{}'.format(origin['place_id']),
                        destinations='place_id:{}'.format(destination['place_id']),
                        mode="walking",
                        language="english"
                    )
                    '''
                    # Testing using different mode (transit)
                    # dmy = gmaps.distance_matrix(
                    #     origins='place_id:{}'.format(origin['place_id']),
                    #     destinations='place_id:{}'.format(destination['place_id']),
                    #     mode='transit',
                    #     language="english")
                    # print(dmy)
                    #duration = dmx['rows'][0]['elements'][0]['duration']['value']
                    #duration = 10
                    #it_step.duration = duration
                    #it_step.save()

                # To DEBUG remove comments
                # else:
                #     print("Destination:{0} and Origin:{0} are the same".format(destination, origin))

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
        # one liner to print steps just to verify
        # [print(step) for step in itinerary.steps.all()]
        # create the string that will be embeded in the problem file.
        file_contents = create_pddl_problem(itinerary,output_plan=False)
        file_name = "{0}-{1}.{2}".format("itinerary", str(itinerary.slug), "pddl")
        # add contents to file.
        write_pddl_file(file_contents, file_name)
        try: 
            plan = run_subprocess(itinerary.slug,sleep_for=2)
            plan_dict = convert_plan(plan)
        except TypeError:
            data = {
                'message':'An error occurred whilst running the itinerary.'
            }
            return JsonResponse(data, status=400)
        except:
            data = {
                'message':'The server didn\'t come up with a feasible plan, sorry!'
            }
            return JsonResponse(data, status=400)
        #submittable = plan_dict
        for index in enumerate(plan_dict):
            current_step_qs = itinerary.steps.all().filter(
                origin__slug=plan_dict[index[0]]['from']
            ).filter(
                destination__slug=plan_dict[index[0]]['to']
            ).get()
            # ).filter(
            #     method=ItineraryStep.METHOD_CHOICES[plan_dict[]]
            # ).get()
            current_step_qs.index = plan_dict[index[0]]['index']
            print(current_step_qs.origin.place_id)
            print(current_step_qs.destination.place_id)
            plan_dict[index[0]]['fromPlaceId']=current_step_qs.origin.place_id
            plan_dict[index[0]]['toPlaceId']=current_step_qs.destination.place_id
            current_step_qs.save()
            print(current_step_qs.index,":",current_step_qs.origin,"->",current_step_qs.destination,":",current_step_qs.method)
        plan_json = json.dumps(plan_dict, ensure_ascii=False)
        if self.request.is_ajax():
            # Request is ajax, send a json response
            data = {
                'final_plan': plan_json
            }
            return JsonResponse(data, status=200)
        return response
