import json
from django.shortcuts import render
from django.views.generic.edit import FormView
from .forms import PlacesOfInterestForm
from django.core.urlresolvers import reverse, reverse_lazy

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
        import ipdb; ipdb.set_trace()
        if form.is_valid():
            return self.form_valid(form)
        else:
            return self.form_invalid(form)

    def form_invalid(self, form):
        print("oh noes!!!")
        print(form)
        return super(PlacesOfInterestView, self).form_invalid(form)

    def form_valid(self, form):
        # This method is called when valid form data has been POSTed.
        # It should return an HttpResponse.
        print("oh yeas!!!")
        print(form.cleaned_data['placesToVisit'])
        return super(PlacesOfInterestView, self).form_valid(form)