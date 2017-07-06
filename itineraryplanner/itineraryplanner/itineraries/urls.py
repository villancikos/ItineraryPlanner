from django.conf.urls import url

from .views import PlacesOfInterestView

urlpatterns = [
    url(regex=r"^$",
        view=PlacesOfInterestView.as_view(),
        name="itineraryPicker"),
]
