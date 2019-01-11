
import csv
from random import shuffle

class City:
    """Class representing a city
    City class containing a name identifying a city,
    a number that is used when constructing all the
    cities, and a dictionary of distances to other
    cities where the keys are the names of the other
    cities.
    The traversed variable is used in most of the 
    algorithms as a marker to avoid using a city
    twice in a given tour.
    
    Attributes:
        name    (String)      : The city name
        city_nr (Integer)     : The identifying number
        traversed (integer)   : Used as a boolean marker
        distances (dictionary): Distances to other cities
    """
    def __init__ (self, name, city_nr):
        self.name = name
        self.city_nr = city_nr
        self.traversed = 0
        self.distances = {}

    def add_distance(self, city, distance):
        """Adds distance to the dictionary
        
        Attributes:
            city (String)   : Name of city 
            distance (float): Distance to city
        """
        self.distances[city] = distance

    def distance_to(self, city):
        """Returns distance to a given city
        
        Returns:
            city (String): Name of city
        """
        return self.distances[city]
    
    def __str__(self):
        """String representation of object
        
        Returns:
            name (String): Name of city
        """
        return self.name
    
    def __repr__(self):
        """String representation of object
        
        Returns:
            name (String): Name of city
        """        
        return self.name

def create_cities ():
    """Creates a list of cities from cvs file
    Creates a list of complete city objects from
    a cvs files constructing the cities and
    filling their dictionaries with the correct
    distances to other cities.
    
    Returns:
        city_list (list): list of constructed cities
    """
    city_list = []
    counter = 0
    
    with open("european_cities.csv", "r") as f:
        data = list(csv.reader(f, delimiter=';'))
    
    for city in data[0]:
        city_list.append(City(city,counter))
        counter += 1

    distances = data[1:]
    for city in city_list:
        counter = 0
        for distance in distances[city.city_nr]:
            city.add_distance(city_list[counter].name, distance)
            counter += 1
    return city_list

def tour_distance (tour):
    """Calculates the distance of a tour
    Calculates a distance of a tour by summing
    the distances from each city to the next and
    finally adding on the distance from the end to
    the start.
    
    Arguments:
        tour (list)     : list of cities
    Returns:
        distance (float): distance of entire tour
    """
    next_city = 1
    distance = 0.0

    for city in tour:
        try:
            distance += float(city.distance_to(tour[next_city].name))
            next_city += 1
        except:
           distance += float(city.distance_to(tour[0].name))
    return distance

def generate_random_tour(city_list):
    """Generates a random tour
    Generates a random permutation of
    the given list of cities as a tour.
    
    Arguments:
        city_list (list): list of cities
        tour (list)     : list of cities
    """
    tour = []
    
    for city in city_list:
        tour.append(city)
    
    shuffle(tour)
    return tour