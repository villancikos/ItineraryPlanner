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

from ..utils.helpers import unique_slugify

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
    slug = models.SlugField(
        _('slug'),
        max_length=255,
        unique=True
    )
    opens = models.CharField(
        max_length=4,
        blank=True,
    )
    closes = models.CharField(
        max_length=4,
        blank=True,
    )
    # Meta and String
    def __str__(self):
        return '{0}'.format(self.name)

    def save(self, *args, **kwargs):
        # Generate a slug for a new model instance before saving it.
        if self.pk is None:
            unique_slugify(self, self.name)
        super(PlaceOfInterest, self).save(*args, **kwargs)
  
    def get_camelCase(self):
        return "Visit"+''.join(x.capitalize() or '-' for x in self.slug.split('-'))


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
    initialPOI = models.ForeignKey(
        PlaceOfInterest,
        null=False,
        related_name="starting_point_for_itinerary",
    )
    endingPOI = models.ForeignKey(
        PlaceOfInterest,
        null=True,
        related_name="ending_point_for_itinerary"
    )
    def get_itinerary_places(self):
        """ this method will return 
        all the places that the user wants to visit
        in a whole itinerary plan."""
        places = []
        last_place = None
        for step in self.steps.all():
            if not last_place == step.origin:
                last_place = step.origin
                places.append(step.origin.slug)
        return places


    def get_all_travel_methods(self):
        """ small helper to get all travel methods 
        available inside an itinerary """
        steps = self.steps.all()
        methods = []
        for step in steps:
            if step.get_travel_method() not in methods:
                methods.append(step.get_travel_method())
        return methods


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

    def get_travel_method(self):
        """ helper function to return travel method in readable format"""
        return self.METHOD_CHOICES[self.method]
        
    # Meta and String
    class Meta:
        verbose_name = _("Itinerary Step")
        verbose_name_plural = _("Itinerary Steps")
        ordering = ["index", "created"]

    def __str__(self):
        return 'Itinerary step from {0} to {1}. Method: {2}. Duration:{3}'.format(
            self.origin, self.destination, self.METHOD_CHOICES[self.method], self.duration)


class Preferences(TimeStampedModel):
    """
    Each user will have many preferences
    for each itinerary.
    """
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
    )
    itinerary = models.ForeignKey(
        Itinerary,
        on_delete=models.CASCADE,
        related_name="itinerary_preference",
        verbose_name=_("itinerary preferences"),
    )
    place = models.ForeignKey(
        PlaceOfInterest,
        related_name="place_preference",
        verbose_name="place to visit preference",
        null=False,
    )
    visitFor = models.PositiveIntegerField(
        default=30,
        blank=False,
    )
    must_visit = models.BooleanField(
        default=True,
    )

    class Meta:
        verbose_name = _("Itinerary Preference")
        verbose_name_plural= _("Itinerary Preferences")

    def __str__(self):
        return 'Visit {0} for {1}mins on Itinerary:{2}'.format(self.place,self.visitFor, self.itinerary.slug)