from City import City
from City import create_cities
from City import tour_distance

import time

def travel_next(city, city_list, tour, all_tours):
    """Searches onward recursively
    Searches recursively and saves a full tour
    when the endconditions are met.
    
    Arguments:
        city (City): current location
        city_list (list): the full searchfield
        all_tours (list): a list of all tours
    """
    city.traversed = 1
    tour.append(city)
    is_end = True
    
    for next_city in city_list:
        if(next_city.traversed is not 1):
            travel_next(next_city, city_list, tour, all_tours)
            next_city.traversed = 0
            is_end = False
    if(is_end):
        endtour = tour.copy()
        all_tours.append(endtour)
    tour.remove(city)

def recursive_travel(city_list):
    """Start the recursive search
    
    Arguments:
        city_list (list): list of cities
    Returns:
        all_tours (list): list of tours
    """
    tour = []
    all_tours = []

    for city in city_list:
            travel_next(city, city_list,tour, all_tours)
            city.traversed = 0
    return all_tours

def shortest_tour(all_tours):
    """Returns the shortest tour from a list of all_tours
    
    Arguments:
        all_tours (list): List of all tours
    Returns:
        shortest (list)          : Shortest tour
    """
    shortest = all_tours[0]
    
    for tour in all_tours:
        if tour_distance(shortest) > tour_distance(tour):
            shortest = tour
    return shortest

def exhaustive_search(city_list,until):
    """Runs exhaustive search for a given amount of cities
    
    Arguments:
        city_list (list): list of cities
        until (integer) : amount of cities to search
    """
    all_tours = recursive_travel(city_list[0:until])
    shortest = shortest_tour(all_tours)
    return shortest

def brute_force(city_list):
    """Runs the exhaustive search and collects data
    
    Arguments:
        city_list (list): list of cities
    """
    start = time.time()*1000
    shortest = exhaustive_search(city_list,6)
    stop = time.time()*1000
    print("Shortest tour for 6 first cities:", tour_distance(shortest))
    print ("Time spent on 6 first cities:", "%.2f" % (stop-start), "ms")
    print("-")
    
    start = time.time()*1000
    shortest = exhaustive_search(city_list,7)
    stop = time.time()*1000
    print("Shortest tour for 7 first cities:", tour_distance(shortest))
    print ("Time spent on 7 first cities:", "%.2f" % (stop-start), "ms")
    print("-")
    
    start = time.time()*1000
    shortest = exhaustive_search(city_list,8)
    stop = time.time()*1000
    print("Shortest tour for 8 first cities:", tour_distance(shortest))
    print ("Time spent on 8 first cities:", "%.2f" % (stop-start), "ms")
    print("-")
    
    start = time.time()*1000
    shortest = exhaustive_search(city_list,9)
    stop = time.time()*1000
    print("Shortest tour for 9 first cities:", tour_distance(shortest))
    print ("Time spent on 9 first cities:", "%.2f" % (stop-start), "ms")
    print("-")
    
    start = time.time()*1000
    shortest = exhaustive_search(city_list,10)
    stop = time.time()*1000
    print("Shortest tour for 10 first cities:", tour_distance(shortest))
    print ("Time spent on 10 first cities:", "%.2f" % (stop-start), "ms")
    print(" ")