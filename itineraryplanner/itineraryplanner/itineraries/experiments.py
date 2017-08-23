#from ..utils.helpers import create_pddl_problem
#from .models import Itinerary, ItineraryStep
from itineraryplanner.utils.helpers import create_pddl_problem

awaken_times = { 'awaken': 480, 'not_awaken':1260}
experiment_slug = '2113b73a-fc05-4596-a70b-63a0dfc34343'
itinerary = Itinerary.objects.get(slug=experiment_slug)
create_pddl_problem(itinerary, awaken_times, True)

""" Plan file with solution found 
itinerary-0af37403-7c33-474f-afbe-d22855bcb042
Noting that the total-time metric was removed. 
"""


