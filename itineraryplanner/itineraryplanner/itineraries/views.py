"""
This view receives the input from the user. 
Validates it and creates a POI or updates it.
Then creates the ItineraryStep for each possible combination.
Adds everything to the Itinerary model and sends it to the 
server to compute the desired TOUR.
"""
import json
import googlemaps

from django.core.urlresolvers import reverse, reverse_lazy
from django.http import HttpResponse
from django.views.generic.edit import FormView

from .forms import PlacesOfInterestForm
from .models import PlaceOfInterest, ItineraryStep, Itinerary
gmaps = googlemaps.Client(key='AIzaSyBucexwP3IjpafwcJVPR3KtRnhqk-1sa00')

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

        placesToVisitJson = form.cleaned_data['placesToVisit']
        placesToVisitObject = json.loads(placesToVisitJson)
        distanceMatrixJson = form.cleaned_data['distanceMatrix']
        distanceMatrixObject = json.loads(distanceMatrixJson)

        for place in placesToVisitObject:
            print("Place with id: {0} and title: {2} \n Coordinates lat:{3},lng:{4}".format(
                place['place_id'],
                place['is_hotel'],
                place['name'],
                place['lat'],
                place['lng']
            ))

            # we first try update the place in case it exists.
            # otherwise we just create it and carry on with the
            # relations with other Models in the database
            obj, created = PlaceOfInterest.objects.update_or_create(
                place_id=place['place_id'],
                defaults={
                    "is_hotel": place['is_hotel'],
                    "name": place['name'],
                    "lat": place['lat'],
                    "lng": place['lng']
                }
            )
            if created:
                print("'{}' was created successfully".format(obj.name))
            else:
                print("'{0}' was already in the database with id={1}".format(
                    obj.name, obj.place_id))
            print(obj, ", was created?: ", created)
        
        # import pdb
        # pdb.set_trace()
        # Placeholder Itinerary. TODO
        # Create an Itinerary Object to hold the tour.
        itinerary = Itinerary.objects.create()
        # Traverse all the possible origins
        for origin in placesToVisitObject:
            # Traverse all the possible destinations
            for destination in placesToVisitObject:
                # for each destination check that is not the same as origin
                # then save the object as an Itinerary Step and compute duration of trip
                if destination != origin:
                    origin_poi = PlaceOfInterest.objects.filter(place_id=origin['place_id']).get()
                    destination_poi = PlaceOfInterest.objects.filter(place_id=destination['place_id']).get()
                    it_step = ItineraryStep.objects.create(
                        origin = origin_poi,
                        destination = destination_poi,
                        itinerary = itinerary,
                        method = ItineraryStep.METHOD_CHOICES.WALK
                    )
                    dmx = gmaps.distance_matrix(
                        origins='place_id:{}'.format(origin['place_id']),
                        destinations='place_id:{}'.format(destination['place_id']),
                        mode="walking",
                        language="english"
                        )
                    duration = dmx['rows'][0]['elements'][0]['duration']['value']
                    it_step.duration = duration
                    it_step.save()
                else:
                    print("Destination:{0} and Origin:{0} are the same".format(destination, origin))

        if self.request.is_ajax():
            # Request is ajax, send a json response
            data = {
                'message:': 'Whatevs'
            }
            return self.render_to_json_response(data)
        return response
