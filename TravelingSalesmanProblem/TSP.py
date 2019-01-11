import csv

import time

from City import City
from City import create_cities
from City import tour_distance
from City import generate_random_tour
from Hillclimb import hill_climber
from Exhaustive import brute_force
from Genetic_algorithm import genetic_algorithm

import time
import statistics
import matplotlib.pyplot as plt
import sys

def run_hillclimber (city_list):
    """Runs the hillclimber module
    
    Attributes:
        city_list(list): list of cities
    """
    print ("--------------HILL CLIMBING--------------")
    hill_climber(city_list)

def run_exhaustive(city_list):
    """Runs the exhaustive search module
    
    Attributes:
        city_list(list): list of cities
    """
    print ("------------EXHAUSTIVE SEARCH------------")
    brute_force(city_list)

def GA_graph(city_list):
    """Creates a figure of the GA
    
    Attributes:
        city_list(list): list of cities
    """
    fitness_lists = []
    for i in range(0,20):
        fittest = genetic_algorithm(city_list, 50, 1000)
        fitness_lists.append(fittest)
    accumulated = [0.0] * 1000
    for fittest in fitness_lists:
        counter = 0
        for fit_value in fittest:
            accumulated[counter] += fit_value
            counter += 1
    averages= [i/20.0 for i in accumulated]
    plt.plot(averages, label = "pop: 50")
    plt.legend(bbox_to_anchor=(0., 1.02, 1., .102), loc=3,ncol=2, mode="expand", borderaxespad=0.)
    
    fitness_lists = []
    for i in range(0,20):
        fittest = genetic_algorithm(city_list, 100, 1000)
        fitness_lists.append(fittest)
    accumulated = [0.0] * 1000
    for fittest in fitness_lists:
        counter = 0
        for fit_value in fittest:
            accumulated[counter] += fit_value
            counter += 1
    averages= [i/20.0 for i in accumulated]
    plt.plot(averages, label = "pop: 100")
    plt.legend(bbox_to_anchor=(0., 1.02, 1., .102), loc=3,ncol=2, mode="expand", borderaxespad=0.)
    
    
    fitness_lists = []
    for i in range(0,20):
        fittest = genetic_algorithm(city_list, 200, 1000)
        fitness_lists.append(fittest)
    accumulated = [0.0] * 1000
    for fittest in fitness_lists:
        counter = 0
        for fit_value in fittest:
            accumulated[counter] += fit_value
            counter += 1
    averages= [i/20.0 for i in accumulated]
    plt.plot(averages, label = "pop: 200")
    plt.legend(bbox_to_anchor=(0., 1.02, 1., .102), loc=3,ncol=2, mode="expand", borderaxespad=0.)
  
    plt.show()

def GA_stats(city_list):
    """Prints data of the GA
    
    Attributes:
        city_list(list): list of cities
    """
    print ("----------------GA DATA----------------")
    fitness_list = []
    for i in range(0,20):
        fittest = genetic_algorithm(city_list, 50, 1000)
        fitness_list.append(fittest[len(fittest)-1])
    fitness_list.sort()
    print ("-----pop: 50 - gen: 1000-----")
    print ("Mean:               %.2f" % statistics.mean(fitness_list))
    print ("Shortest tour:      %.2f" % fitness_list[0])
    print ("Longest tour:       %.2f" % fitness_list[len(fitness_list)-1])
    print ("Standard Deviation: %.2f" % statistics.stdev(fitness_list))
    
    fitness_list = []
    for i in range(0,20):
        fittest = genetic_algorithm(city_list, 100, 1000)
        fitness_list.append(fittest[len(fittest)-1])
    fitness_list.sort()
    print ("-----pop: 100 - gen: 1000-----")
    print ("Mean:               %.2f" % statistics.mean(fitness_list))
    print ("Shortest tour:      %.2f" % fitness_list[0])
    print ("Longest tour:       %.2f" % fitness_list[len(fitness_list)-1])
    print ("Standard Deviation: %.2f" % statistics.stdev(fitness_list))
    
    fitness_list = []
    for i in range(0,20):
        fittest = genetic_algorithm(city_list, 200, 1000)
        fitness_list.append(fittest[len(fittest)-1])
    fitness_list.sort()
    print ("-----pop: 200 - gen: 1000-----")
    print ("Mean:               %.2f" % statistics.mean(fitness_list))
    print ("Shortest tour:      %.2f" % fitness_list[0])
    print ("Longest tour:       %.2f" % fitness_list[len(fitness_list)-1])
    print ("Standard Deviation: %.2f" % statistics.stdev(fitness_list))
    
def GA_time(city_list):
    """Times the GA runtime
    
    Attributes:
        city_list(list): list of cities
    """
    print ("----------------GA TIME----------------")
    start = time.time()*1000
    fittest = genetic_algorithm(city_list[0:10], 200, 1000)
    stop = time.time()*1000
    print ("10 cities:")
    print ("    * Time:    %.2f ms" % (stop-start))
    print ("    * Fittest: %.2f" % fittest[len(fittest)-1])
    
    start = time.time()*1000
    fittest = genetic_algorithm(city_list, 200, 1000)
    stop = time.time()*1000
    print ("All cities:")
    print ("    * Time:    %.2f ms" % (stop-start))
    print ("    * Fittest: %.2f" % fittest[len(fittest)-1])
    
def main():
    """Main-function of TSP
    
    Generates all city objects and then runs requested
    amount of algorithms for solving the travelling salesman
    problem.
    Runs the module requested in the system argument.
    
    Arguments:
    {test_exhaustive | test_hillclimbing | test_GA_time | test_GA_graph | test_GA_data}
    """
    city_list = create_cities()
    
    if len(sys.argv) > 1:
        if sys.argv[1] == "test_exhaustive":
            run_exhaustive(city_list)
        elif sys.argv[1] == "test_hillclimb":
            run_hillclimber(city_list)
        elif sys.argv[1] == "test_GA_graph":
            GA_graph(city_list)
        elif sys.argv[1] == "test_GA_time":
            GA_time(city_list)
        elif sys.argv[1] == "test_GA_data":
            GA_stats(city_list)
        else:
            print ("Invalid argument supplied.")
            print ("TSP.py {test_exhaustive | test_hillclimbing | test_GA_time | test_GA_graph | test_GA_data}")          
    else:
        print ("Invalid amount of system arguments given.")
        print ("TSP.py {test_exhaustive | test_hillclimbing | test_GA_time | test_GA_graph | test_GA_data}")


if __name__ == '__main__': main()


