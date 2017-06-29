"""
    PlacesOfInteresForm used to receive the JSON from the Front-End.
"""
import json
import re

from django import forms
from django.forms import ValidationError


class PlacesOfInterestForm(forms.Form):
    """ This form will receive the war data JSON
    containing all the places the user wants to visit.
    """
    placesToVisit = forms.CharField()

    def clean_places(self):
        """
        Although the django CharField validation will verify that the
        correct type of data has been submitted to the form, we want
        to take that a step further and verify that the data we receieve
        from the front-end is of the correct format.
        The JSON should come in a format similar to :
        0: {
            "place_id": "ChIJrQCmO9IEdkgRyoqlpJ3K8n8",
            "is_hotel":false,
            "name": "LEGO® Store Leicester Square",
            "lat": 51.51042579999999,
            "lng": -0.1309333000000379,
        },
        1: {
            "place_id":"ChIJlzV3vysFdkgRo0fQHE0mBRk",
            "is_hotel":false,
            "name":"Leica Store Mayfair",
            "lat":51.5108555,
            "lng":-0.14509050000003754
        } ...
        """
        #TODO: Implement a cleansing method for the json
        raw_data = self.cleaned_data['placesToVisit']
        try:
            # validate raw data
            json_data = json.loads(raw_data)
        except:
            raise forms.ValidationError("Invalid data in the Json")
        return json_data
