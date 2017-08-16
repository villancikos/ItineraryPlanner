from django.conf.urls import url

from .views import ReactAttempt, ExamplesMenu, AutoCompleteExample, DistancesExample, SearchBoxExample, SearchAttempt

urlpatterns = [
    url(regex=r"^$",
        view=ExamplesMenu.as_view(),
        name="menu"),
    url(regex=r"^autocomplete/",
        view=AutoCompleteExample.as_view(),
        name="autocomplete"),
    url(regex=r"^distances/",
        view=DistancesExample.as_view(),
        name="distances"),
    url(regex=r"^searchbox/",
        view=SearchBoxExample.as_view(),
        name="searchbox"),
    url(regex=r"^attempt/",
        view=SearchAttempt.as_view(),
        name="attempt"),
    url(regex=r"^react/",
        view=ReactAttempt.as_view(),
        name="react"),
]
