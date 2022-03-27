from operator import itemgetter
import json

def make_guess(request:any) -> str:
    def result_is_lower(o:dict) -> bool:
        return o["result"] == "lower"
    def result_is_higher(o:dict) -> bool:
        return o["result"] == "higher"
    #extract json object
    state:dict = request.get_json()
    #set function defaults
    min:int = state["minimum"]
    max:int = state["maximum"]
    guess:int = (min + max) // 2
    history:list = state["history"]
    # base case: initial guess
    if not history: return json.dumps(guess)
    #sort by secondary keys: results in reverse to obtain prefered order
    secondary_sort:list = list(sorted(history, key=itemgetter('result'), reverse=True))
    #sort by primary keys: guesses in order by value
    primary_sort:list = list(sorted(secondary_sort, key=itemgetter('guess')))
    #highest guess by default is max
    h:int = max
    #filter for results that are lower
    higher_results:list = list(filter(result_is_lower, primary_sort))
    #max becomes the lowest `lower` guess from the higher_results
    if higher_results: h = higher_results[0].get("guess") #obtain guess value
    #lowest guess by default is min
    l:int = min
    #filter for results that are higher
    lower_results:list = list(filter(result_is_higher, primary_sort))
    #min becomes the highest `higher` guess from the lower_results
    if lower_results: l = lower_results[-1].get("guess") #obtain guess value
    # evaluate guess based on the adjusted range
    guess = (l+h) // 2
    #return guess as a json string
    return json.dumps(guess)
