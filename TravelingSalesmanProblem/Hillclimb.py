from City import tour_distance
from City import generate_random_tour

import statistics
import time

def run_hillclimb (tour, swap_distance):
    """Run the hillclimb algorithm on a given tour
    
    Arguments:
        tour (list)            : list of cities
        swap_distance (integer): distance of swap_distance
    Returns:
        tour (list): hillclimbed tour of cities
    """
    counter = 1

    for city in tour[0:(len(tour)-1-swap_distance)]:
        change = tour.copy()
        swapcity = change[counter]
        change[counter] = change[counter+swap_distance]
        change [counter+swap_distance] = swapcity
        
        if (tour_distance(tour)>tour_distance(change)):
            tour = change
            if(swap_distance > 1):
                tour = run_hillclimb(tour,swap_distance-1)
        counter += 1
    return tour

def hill_climber(city_list):
    """Runs the hillclimbing and collects stats
    Runs the hillclimbing 20 times for 10 cities,
    and 20 times for all the cities, Thereafter
    reporting the requested data.
    
    Arguments:
        city_list (list): list of cities
    """
    distances = []
    print(" ")
    print("Data for 10 cities:")
    for x in range(0,20):
        tour = generate_random_tour(city_list[0:10])
        run_hillclimb(tour,int((len(tour)-2)/2))
        distances.append(tour_distance(tour))
    distances.sort()
    print ("Mean:               %.2f" % statistics.mean(distances))
    print ("Shortest tour:      %.2f" % distances[0])
    print ("Longest tour:       %.2f" % distances[len(distances)-1])
    print ("Standard Deviation: %.2f" % statistics.stdev(distances))
    
    distances =[]
    print("-")
    print("Data for all cities:")
    for x in range(0,20):
        tour = generate_random_tour(city_list)
        run_hillclimb(tour,int((len(tour)-2)/2))
        distances.append(tour_distance(tour))
    distances.sort()
    print ("Mean:               %.2f" % statistics.mean(distances))
    print ("Shortest tour:      %.2f" % distances[0])
    print ("Longest tour:       %.2f" % distances[len(distances)-1])
    print ("Standard Deviation: %.2f" % statistics.stdev(distances))
   
        