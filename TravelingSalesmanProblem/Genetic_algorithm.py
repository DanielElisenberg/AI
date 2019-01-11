from City import City
from City import tour_distance
from City import generate_random_tour

import random

class Salesman:
    """Class representing a salesman
    A salesman has a given tour and a fitness-value
    that represents the length of the tour. A lower
    fitness value is considered better.
    
    Attributes:
        tour (list)     : A list of cities
        fitness (double): The length of the tour
    """
    
    def __init__ (self, tour):
        self.tour = tour
        self.fitness = tour_distance(self.tour)
        
    def update_fitness(self):
        """Updates the fitness of salesman
        """
        self.fitness = tour_distance(self.tour)
        
        
def untraverse(tour):
    """Resets traversal of a tour
    Goes through each city in tour and
    set the traverse value to 0.
    
    Arguments:
        tour (list): List of cities
    """
    for city in tour:
        city.traversed = 0
        
def traverse_by_name(tour,name):
    """Traverses a city in a tour
    Looks for a city in the tour with the
    given name and sets its traverse value
    to 1.
    
    Arguments:
        tour (list)  : List of cities
        name (String): Name of city to be found 
    """
    for city in tour:
        if(city.name == name):
            city.traversed = 1
            return
    
def get_next_index(tour,name):
    """Gets the next appropriate city
    Searches the tour for the first city
    after the one with the responding name
    and finds the next city in the tour with
    a traverse value of 0.
    
    Arguments:
        tour (list)  : List of cities
        name (String): Name of city to be found
    Returns:
        j (integer): Index of next appropriate city
    """
    j = 0
    for i in range(0, len(tour)):
        if(tour[i].name == name):
            j=i+1
            if(j>len(tour)-1):
                j = 0
            while(tour[j].traversed == 1):
                    j += 1
                    if(j>len(tour)-1):
                        j = 0
    return j
    
def cycle_crossover(tour1, tour2):
    """Cycle crossover operation
    Takes in two tours and creates two children
    that has information merged from both tours.
    
    Arguments:
        tour1 (list): List of cities
        tour2 (list): List of cities
    Returns:
        child1 (list): Product of crossover
        child2 (list): Product of crossover
    """
    child1_tour = []
    child1_tour.append(tour1[0])
    tour1[0].traversed = 1
    traverse_by_name(tour2,tour1[0].name)
    
    for i in range(1,len(tour1)):
        if(i%2 == 0):
            j = get_next_index(tour1, child1_tour[i-1].name)
            child1_tour.append(tour1[j])
            tour1[j].traversed = 1
            traverse_by_name(tour2, tour1[j].name)
        else:
            j = get_next_index(tour2, child1_tour[i-1].name)
            child1_tour.append(tour2[j])
            tour2[j].traversed = 1
            traverse_by_name(tour1, tour2[j].name)
    untraverse(tour1)
    untraverse(tour2)

    child2_tour = []
    child2_tour.append(tour2[0])
    tour2[0].traversed = 1
    traverse_by_name(tour1,tour2[0].name)
    
    for i in range(1,len(tour1)):
        if(i%2 == 0):
            j = get_next_index(tour2, child2_tour[i-1].name)
            child2_tour.append(tour2[j])
            tour2[j].traversed = 1
            traverse_by_name(tour1, tour2[j].name)
        else:
            j = get_next_index(tour1, child2_tour[i-1].name)
            child2_tour.append(tour1[j])
            tour1[j].traversed = 1
            traverse_by_name(tour2, tour1[j].name)
    untraverse(tour1)
    untraverse(tour2)
    untraverse(child1_tour)
    untraverse(child2_tour)
    

    child1 = Salesman(child1_tour)
    child2 = Salesman(child2_tour)
    return child1, child2

def crossover(parents):
    """Starts all crossover operations
    Takes a list of parent-tours and picks
    two and two random parents from the list
    to create offspring until we have an equal
    amount of children to parent ratio.
    
    Arguments:
        parents (list): List of salesmen
    Returns:
        children (list): List of salesmen
    """
    children = []
    
    for x in range(0,int(len(parents)/2)):
        parent1 = random.choice(parents)
        parent2 = random.choice(parents)
        child1,child2 = cycle_crossover(parent1.tour, parent2.tour)
        children.append(child1)
        children.append(child2)
    return children

def random_sequence_mutation(tour):
    """
    """
    i = random.randint(0,int(len(tour)-2))
    j = random.randint(0,len(tour)-1)
    while j<=i:
        j = random.randint(0,len(tour)-1)
    newtour = tour[0:i]
    c = j
    while c >= i:
        newtour.append(tour[c])
        c -= 1
    newtour.extend(tour[j+1:len(tour)])
    return newtour
    
def mutation(salesmen):
    """Mutates a list of salesmen
    Every salesman in the list has
    a 10% chance to be mutated.
    
    Arguments:
        salesmen (list): a list of salesmen
    """
    for salesman in salesmen:
        if random.uniform(0.0,1.0) <= 0.1:
            salesman.tour = random_sequence_mutation(salesman.tour)

def genetic_algorithm(city_list, population, generations):
    """Runs the genetic algorithm
    Runs the genetic algorithm with the given
    population and generations.
    
    Arguments:
        city_list (list)     : List of cities to be explored
        population (integer) : Size of population
        generations (integer): Number of generations
    Returns:
        fittest (list): The lowest fitness from each generation
    """
    salesmen = []
    fittest = []
    
    for i in range(0, population):
            salesmen.append(Salesman(generate_random_tour(city_list)))
    
    salesmen.sort(key=lambda x: x.fitness)
    fittest.append(salesmen[0].fitness)
    
    for i in range(1,generations):
        topfit = salesmen[0:int(len(salesmen)*0.3)]
        newgen = salesmen[0:int(len(salesmen)*0.7)]
        children = crossover(topfit)
        mutation(children)
        newgen.extend(children)
        salesmen = newgen
        for salesman in salesmen:
            salesman.update_fitness()
        salesmen.sort(key=lambda x: x.fitness)
        fittest.append(salesmen[0].fitness)
    return fittest
        