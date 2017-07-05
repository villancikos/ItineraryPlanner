"""
    Key model inside the ItineraryPlanner that handles
    Itineraries, Places of Interest and their relationships.
"""
import uuid

from django.conf import settings
from django.db import models
from django.utils.translation import ugettext_lazy as _
from model_utils import Choices
from model_utils.models import TimeStampedModel


"""
######################################################
############# placeId ################################
######################################################
https://developers.google.com/maps/documentation/javascript/3.exp/reference#MarkerPlace

Type:  string
The place ID of the place (such as a business or point of interest).
The place ID is a unique identifier of a place in the Google Maps database.
Note that the placeId is the most accurate way of identifying a place.
If possible, you should specify the placeId rather than a placeQuery.
A place ID can be retrieved from any request to the Places API,
such as a TextSearch.
Place IDs can also be retrieved from requests to the Geocoding API.
"""


class PlaceOfInterest(TimeStampedModel):
    """
    A PlaceOfInterest (POI) is a location in the Google Map
    that the tourist wants to visit. Only when the POI
    is the HOTEL will result in the is_hotel flag True.
    To see more fields available go to:
    https://developers.google.com/maps/documentation/javascript/reference#PlaceResult

    """
    place_id = models.CharField(
        max_length=255,
    )
    is_hotel = models.BooleanField(
        default=False,
    )
    name = models.CharField(
        max_length=255,
    )
    lat = models.DecimalField(
        _('latitude'),
        max_digits=13,
        decimal_places=10
    )
    lng = models.DecimalField(
        _('longitude'),
        max_digits=13,
        decimal_places=10
    )

    # Meta and String
    def __str__(self):
        return '{0}'.format(self.name)


class Itinerary(TimeStampedModel):
    """
    Its whole purpose is to hold a complete run of an itinerary.
    """
    STATUS_CHOICES = Choices(
        (0, 'PENDING', 'pending'),
        (1, 'COMPLETED', 'completed'),
        (2, 'RUNNING', 'running'),
        (3, 'ERROR', 'error'),
    )
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
    )
    status = models.PositiveSmallIntegerField(
        _('status'),
        choices=STATUS_CHOICES,
        default=STATUS_CHOICES.PENDING,
        editable=False,
    )
    slug = models.UUIDField(
        _('slug'),
        default=uuid.uuid4,
        editable=False
    )


class ItineraryStep(TimeStampedModel):
    """
    Will contain all the possible combinations of the
    Places of Interest inside one itinerary.
    """
    METHOD_CHOICES = Choices(
        (0, 'WALK', 'walk'),
        (1, 'BUS', 'bus'),
        (2, 'CAR', 'car'),
        (3, 'TUBE', 'tube'),
    )
    origin = models.ForeignKey(
        PlaceOfInterest,
        related_name="origin",
        verbose_name="the origin place",
        null=False,
    )
    destination = models.ForeignKey(
        PlaceOfInterest,
        related_name="destination",
        verbose_name="the destination place",
        null=False,
    )
    itinerary = models.ForeignKey(
        Itinerary,
        on_delete=models.CASCADE,
        related_name="steps",
        verbose_name=_("itinerary"),
    )
    method = models.PositiveSmallIntegerField(
        choices=METHOD_CHOICES,
        default=METHOD_CHOICES.WALK,
    )
    duration = models.PositiveIntegerField(
        default=0,
    )
    index = models.PositiveSmallIntegerField(
        default=0,
    )

    # Meta and String
    class Meta:
        verbose_name = _("Itinerary Step")
        verbose_name_plural = _("Itinerary Steps")
        ordering = ["index", "created"]

    def __str__(self):
        return 'Itinerary step from {0} to {1}. Duration:{2}'.format(
            self.origin, self.destination, self.duration)
