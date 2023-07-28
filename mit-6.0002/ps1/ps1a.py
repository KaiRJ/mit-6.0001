###########################
# 6.0002 Problem Set 1a: Space Cows 
# Name:
# Collaborators:
# Time:

from ps1_partition import get_partitions
import time

import typing
Cows = dict[str,int]
Trips = list[list[str]]

#================================
# Part A: Transporting Space Cows
#================================

# Problem 1
def load_cows(filename : str) -> Cows:
    """
    Read the contents of the given file.  Assumes the file contents contain
    data in the form of comma-separated cow name, weight pairs, and return a
    dictionary containing cow names as keys and corresponding weights as values.

    Parameters:
    filename - the name of the data file as a string

    Returns:
    a dictionary of cow name (string), weight (int) pairs
    """
    cows = {}
    with open(filename) as file:
        for line in file:
            name, weight  = line.split(',')
            cows[name] = int(weight)
            
    return cows

# Problem 2
def greedy_cow_transport(cows : Cows, limit : int = 10) -> Trips:
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
    # create list of tuples, sorted by weight from cows dict.
    cows_sorted = sorted(cows.items(), key=lambda x: x[1], reverse=True)
    trips = [[]]
    trips_weight = [0]
    
    for name, weight in cows_sorted:
        # check if cow will fit on a current trip
        for i in range(len(trips)):
            if trips_weight[i] + weight <= limit:
                trips[i].append(name)
                trips_weight[i] += weight
                break
        else: # cow didnt fit on any current trips, try make new one 
            if weight < limit:
                trips.append([name])
                trips_weight.append(weight)
                
    return trips        

# Problem 3
def brute_force_cow_transport(cows : Cows,limit : int = 10) -> Trips:
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
    best_partition = [[]]
    for partition in get_partitions(cows):
        if len(partition) < len(best_partition) or best_partition == [[]]:
            for trip in partition:
                trip_weight = 0
                for cow in trip:
                    trip_weight += cows[cow]
                if trip_weight > limit:
                    break # over the limit therefore skip this trip
            else:
                # all trips in this partition under limit and fewer trips than current best
                best_partition = partition
    return best_partition
                
# Problem 4
def compare_cow_transport_algorithms(filename : str) -> None:
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
    greedy_trips = greedy_cow_transport(cows)
    end = time.time()

    print("greedy_cow_transport:")
    print(f"\tTrips : {greedy_trips}")
    print(f"\tTotal trips : {len(greedy_trips)}")
    print(f"\tTotal time  : {end - start}")

    start = time.time()
    brute_force_trips = brute_force_cow_transport(cows)
    end = time.time()

    print("brute_force_cow_transport:")
    print(f"\tTrips : {brute_force_trips}")
    print(f"\tTotal trips : {len(brute_force_trips)}")
    print(f"\tTotal time  : {end - start}")

if __name__ == '__main__':
    compare_cow_transport_algorithms("ps1_cow_data.txt")
