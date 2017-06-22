from django.db import models
from model_utils import Choices

from model_utils.models import TimeStampedModel
class Itinerary(TimeStampedModel):
    pass

class ItineraryStep(TimeStampedModel):
    origin = models.CharField(
        _('origin'),
        max_length=255
    )

class PlaceOfInterest():
    name = models.CharField(
        _('place'),
        max_length= 255
    )
    lat = models.DecimalField(
        _('latitude'),
        max_digits=9, 
        decimal_places=6
    )
    lng = models.DecimalField(
        _('longitude'),
        max_digits=9, 
        decimal_places=6
    )

