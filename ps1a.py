###########################
# 6.0002 Problem Set 1a: Space Cows 
# Name:
# Collaborators:
# Time:

from ps1_partition import get_list_partitions
import time

#================================
# Part A: Transporting Space Cows
#================================

# Problem 1
def load_cows(filename):
    """
    Read the contents of the given file.  Assumes the file contents contain
    data in the form of comma-separated cow name, weight pairs, and return a
    dictionary containing cow names as keys and corresponding weights as values.

    Parameters:
    filename - the name of the data file as a string

    Returns:
    a dictionary of cow name (string), weight (int) pairs
    """
    cows = dict()
    with open(filename) as f:
        for cow in f:
            cow_name, cow_weight = cow.split(",")
            cows[cow_name] = int(cow_weight)
    return cows

# Problem 2
def greedy_cow_transport(cows,limit=10):
    """
    Uses a greedy heuristic to determine an allocation of cows that attempts to
    minimize the number of spaceship trips needed to transport all the cows. The
    returned allocation of cows may or may not be optimal.
    The greedy heuristic should follow the following method:

    1. As long as the current trip can fit another cow, add the largest cow that will fit
        to the trip
    2. Once the trip is full, begin a new trip to transport the remaining cows

    Does not mutate the given dictionary of cows.

    Parameters:
    cows - a dictionary of name (string), weight (int) pairs
    limit - weight limit of the spaceship (an int)
    
    Returns:
    A list of lists, with each inner list containing the names of cows
    transported on a particular trip and the overall list containing all the
    trips
    """
    # assumes each value in cows.values() <= limit
    flipped_cows = _flip_dict(cows)
    
    return _greedy_cow_recursive(flipped_cows, limit)

######## helper methods ###########
def _flip_dict(dict_):
    """
    Flips a dictionary such that the keys become values and values become keys
    Example:
    dict_ = {"Jesse": 6, "Alan": 3, "Maybel": 3, "Callie": 2, "Maggie": 5}
    flipped_dict = {2: ['Callie'], 3: ['Alan', 'Maybel'], 5: ['Maggie'], 6: ['Jesse']}

    Requires all dict_.values() to be hashable.
    Does not mutate dict_.
    """
    flipped_dict = dict()
    for k,v in dict_.items():
        flipped_dict[v] = flipped_dict.get(v, []) + [k]
    return flipped_dict

def _greedy_cow_recursive(flipped_cows, limit,
                          total_selected_weight=0, selected_names=None,
                          ignored=None, all_trips=None):
    #google-style-guide: Do not use mutable objects as default values in the function or method definition.
    if selected_names is None:
        selected_names = []
    if ignored is None:
        ignored = set()
    if all_trips is None:
        all_trips = []
        
    cow_weights = set(flipped_cows.keys())
    current_limit = limit - total_selected_weight
    
    def _append_trip_if_not_empty():
        """
        Appends selected_names to all_trips if and only if
        selected_names is not empty
        """
        if selected_names:
            all_trips.append(selected_names)
            
    if not flipped_cows:
        _append_trip_if_not_empty()
            
        return all_trips

    elif current_limit == 0 or (current_limit > 0 and cow_weights == ignored):
        _append_trip_if_not_empty()
        
        return _greedy_cow_recursive(flipped_cows, limit, 0, [], set(), all_trips)
        
    largest_weight = max(cow_weights.difference(ignored))

    if largest_weight > current_limit:
        ignored.add(largest_weight)
    else:
        cows_with_largest_weight = flipped_cows[largest_weight]
        try:
            selected_names += [cows_with_largest_weight.pop()]
            total_selected_weight += largest_weight
            
            if not cows_with_largest_weight:
                flipped_cows.pop(largest_weight)
        except IndexError:
            flipped_cows.pop(largest_weight)

    return _greedy_cow_recursive(flipped_cows, limit, total_selected_weight, selected_names, ignored, all_trips)
##################################
        
    


# Problem 3
def brute_force_cow_transport(cows,limit=10):
    """
    Finds the allocation of cows that minimizes the number of spaceship trips
    via brute force.  The brute force algorithm should follow the following method:

    1. Enumerate all possible ways that the cows can be divided into separate trips 
        Use the given get_partitions function in ps1_partition.py to help you!
    2. Select the allocation that minimizes the number of trips without making any trip
        that does not obey the weight limitation
            
    Does not mutate the given dictionary of cows.

    Parameters:
    cows - a dictionary of name (string), weight (int) pairs
    limit - weight limit of the spaceship (an int)
    
    Returns:
    A list of lists, with each inner list containing the names of cows
    transported on a particular trip and the overall list containing all the
    trips
    """
    cow_names = list(cows.keys())
    cow_weights = list(cows.values())
    
    def _names_from_weights(trip,names,weights):
        """
        Effectively removes all weights and names carried in
        trip. Any item removed from weights must be removed from names
        and vice versa.
        """        
        this_trip = []
        for x in trip:
            name = names.pop(weights.index(x))
            weights.remove(x)
            this_trip.append(name)
        return this_trip
    
    least_num_trips = len(cow_weights)#worst-case scenario is we carry one cow
                                      #each trip
    best_journey = None
    
    for journey in get_list_partitions(cow_weights):
        names = cow_names[:]
        weights = cow_weights[:]
        all_trips = []
        
        for trip in journey:
            #if in any one trip in this journey the weight is exceeded, disqualify journey
            if sum(trip) > limit:
                all_trips = []
                break
            this_trip = _names_from_weights(trip,names,weights)                
            all_trips.append(this_trip)
        
        if not all_trips:
            continue
        
        num_of_trips = len(all_trips)
        
        if (num_of_trips < least_num_trips):
            best_journey = all_trips
            least_num_trips = num_of_trips
            
    return best_journey if best_journey is not None else [[x] for x in cow_names]
        
# Problem 4
def compare_cow_transport_algorithms():
    """
    Using the data from ps1_cow_data.txt and the specified weight limit, run your
    greedy_cow_transport and brute_force_cow_transport functions here. Use the
    default weight limits of 10 for both greedy_cow_transport and
    brute_force_cow_transport.
    
    Print out the number of trips returned by each method, and how long each
    method takes to run in seconds.

    Returns:
    Does not return anything.
    """
    cows = load_cows("ps1_cow_data.txt")
    
    start = time.time()
    trips_greedy = greedy_cow_transport(cows)
    end = time.time()
    time_greedy = end - start
    
    start = time.time()
    trips_brute = brute_force_cow_transport(cows)
    end = time.time()
    time_brute = end - start

    num_trips_greedy = len(trips_greedy)
    num_trips_brute = len(trips_brute)

    print("least num of trips from greedy: ", num_trips_greedy)
    print("least num of trips from brute: ", num_trips_brute)
    print("time taken by brute: \t%.4f seconds " % time_brute)
    print("time taken by greedy: \t%.4f seconds" % time_greedy)
    print("brute - greedy = \t%.4f seconds" % (time_brute - time_greedy))

if __name__ == "__main__":
##    cows = {"Jesse": 6, "Alan": 3, "Maybel": 3, "Callie": 2, "Maggie": 5}
    compare_cow_transport_algorithms()
