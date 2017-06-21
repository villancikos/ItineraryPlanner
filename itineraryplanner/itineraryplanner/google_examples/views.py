from django.views.generic import TemplateView
# Create your views here.
class ExamplesMenu(TemplateView):
    template_name = 'google-examples/menu.html'

class AutoCompleteExample(TemplateView):
    template_name = 'google-examples/autocomplete.html'

class DistancesExample(TemplateView):
    template_name= 'google-examples/distances.html'

class SearchBoxExample(TemplateView):
    template_name = 'google-examples/searchbox.html'