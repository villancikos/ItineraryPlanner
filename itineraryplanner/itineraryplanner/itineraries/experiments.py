#from ..utils.helpers import create_pddl_problem
#from .models import Itinerary, ItineraryStep
from itineraryplanner.utils.helpers import create_pddl_problem,write_pddl_file, run_subprocess,convert_plan

awaken_times = { 'awaken': 480, 'not_awaken':1260}
experiment_slug = '2113b73a-fc05-4596-a70b-63a0dfc34343'
itinerary = Itinerary.objects.get(slug=experiment_slug)
problem_content = create_pddl_problem(itinerary, awaken_times, True)
# now that we have the problem we write it to a file.
file_name = "{0}-{1}.{2}".format("itinerary", str(itinerary.slug), "pddl")
write_pddl_file(problem_content, file_name)
# get the output in this plan_result variable
plan_result = run_subprocess(itinerary.slug, sleep_for=5)

plan_dict = convert_plan(plan_result)

""" Plan file with solution found 
itinerary-0af37403-7c33-474f-afbe-d22855bcb042
Noting that the total-time metric was removed. 
"""


