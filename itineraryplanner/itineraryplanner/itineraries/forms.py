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
    preferences = forms.CharField()
    properties = forms.CharField()

    def clean_properties(self):
        """ used to validate that the properies json
        comes with all the needed properties.
        The properties dictionary is expecting this:
        {
            "sleepTime":"2100",
            "wakeUpTime":"0800",
            "runFor":105,
            "methods":{
                "driving":true,
                "walking":false,
                "bicycling":false,
                "transit":false
            }
        }
        Thus, validation is needed as follows...
        """
        properties_raw = self.cleaned_data['properties']
        # try to get the json if not, then something is wrong.
        try:
            properties_json_data = json.loads(properties_raw)
        except:
            raise forms.ValidationError("Invalid property")
        # now clean the runFor parameter to avoid malicious code.
        try:
            run_for = int(properties_json_data['runFor'])
            if (run_for > 60 or run_for < 0):
                # default value to 5 to avoid overwhelming the server.
                run_for = 5
        except ValueError:
            raise ValidationError("runFor parameter must be an int.")
        properties_json_data['runFor'] = run_for
        properties = json.dumps(properties_json_data)
        return properties



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
        # TODO: Implement a cleansing method for the json
        places_to_visit_raw = self.cleaned_data['placesToVisit']
        preferences_raw = self.cleaned_data['preferences']
        properties_raw = self.cleaned_data['properties']

        # distance_matrix_raw = self.cleaned_data['distanceMatrix']

        try:
            # validate raw data
            places_json_data = json.loads(places_to_visit_raw)
            preferences_json_data = json.loads(preferences_raw)
            properties_json_data = json.loads(properties_raw)
        except:
            raise forms.ValidationError("Invalid data in the Json")

        if properties_json_data['runFor'] > 50 or properties_json_data['runFor'] < 0:
            properties_json_data['runFor'] = 5
            print("se limpio json data")
            print(properties_json_data)
        json_data.append(places_json_data,
                         preferences_json_data, properties_json_data)
        return json_data
