"""
MPCS 51042 Assignment 3
Ming Liu

These programs were written without discussing them with anyone.
"""

# Problem 2

import math
import webbrowser
import csv

class Coordinate:
    """
    The Coordinate class.
    """
    def __init__(self, latitude, longitude):
        """
        Constructor for coordinate numbers.
        """
        self.latitude = latitude
        self.longitude = longitude
    # self defined functions to make things from one to the other
    def toDegree(radian):
        """
        Converts radians to degrees
        """
        return radian*180/math.pi
    def toRadian(degree):
        """
        Converts degrees to radians
        """
        return degree*math.pi/180
    @classmethod
    def fromdegrees(cls, latitude, longitude):
        """
        Class method constructor? Takes inputs in degrees and creates a Coordinate object, storing them in radians.
        """
        # Had to go look it up: https://www.programiz.com/python-programming/methods/built-in/classmethod
        return cls(Coordinate.toRadian(latitude), Coordinate.toRadian(longitude))
    def distance(self, coord):
        """
        Calculates the absolute distance between two coordinates using the Haversine formula.
        """
        return 2*3961*math.asin(math.sqrt(math.sin((coord.latitude-self.latitude)/2)**2+math.cos(coord.latitude)*math.cos(self.latitude)*math.sin((coord.longitude-self.longitude)/2)**2))
    def as_degrees(self):
        """
        Returns a tuple of a coordinate, in degrees.
        """
        return (Coordinate.toDegree(self.latitude), Coordinate.toDegree(self.longitude))
    def show_map(self):
        """
        Opens Google Maps to the coordinate. Note: Python doesn't really have a method of closing the page, so don't call this too much.
        """
        # source: https://docs.python.org/3/library/webbrowser.html
        lat = Coordinate.toDegree(self.latitude)
        long = Coordinate.toDegree(self.longitude)
        url = "http://maps.google.com/maps?q="+str(lat)+","+str(long)
        webbrowser.open_new(url)

class School:
    def __init__(self, data):
        """
        Constructor for the School object. Takes in a dictionary (data) and extracts from it individual values.
        """
        self.id = int(data.get("School_ID"))
        self.name = str(data.get("Short_Name"))
        self.network = str(data.get("Network"))
        self.address = str(data.get("Address"))
        self.zip = str(data.get("Zip"))
        self.phone = str(data.get("Phone"))
        self.grades = data.get("Grades").split(", ")
        self.location = Coordinate.fromdegrees(float(data.get("Lat")), float(data.get("Long")))
        # depreciated function to get the coordinates directly from the csv, if I so wanted
        # self.coords = data.get("the_geom")
    def distance(self, coord):
        """
        Returns the distance between a school and any given pair of coordinates.
        """
        return Coordinate.distance(self.location, coord)
    def full_address(self):
        """
        Prints a multiline with the school's full address.
        Obviously all schools are in Chicago, right?
        """
        return str(self.address+"\nChicago, IL, "+self.zip)

class CPS:
    def __init__(self, fileName):
        """
        Reads in inputs from a .csv file containing all of the CPS data, and calls the School constructor on each line.
        """
        self.schools = []
        with open(fileName, 'r') as file:
            # nice of them to make DictReader: https://docs.python.org/3/library/csv.html#csv.DictReader
            # this takes the first line and automatically makes it the keys for a dictionary, constructed with each other line
            commas = csv.DictReader(file, quotechar='"', delimiter=',')
            for row in commas:
                self.schools.append(School(row))
    def nearby_schools(self, coord, radius=1.0):
        """
        Returns all nearby schools within a specified radius; default is 1 mile (which is really quite short for a school).
        """
        nearby = []
        for i in self.schools:
            dist = Coordinate.distance(i.location, coord)
            if dist <= radius:
                nearby.append(i)
        return nearby
    def get_schools_by_grade(self, *grades):
        """
        Gets school by grade. Returns all schools that teach ALL grades given as input.
        """
        gradeList = list(grades)
        matches = []
        for i in self.schools:
            # convert list to set so that we may use set logic on it, since the list of grades taught is entirely unique elements
            if set(gradeList).issubset(set(i.grades)):
                matches.append(i)
        # trim duplicates (don't know if any exist, but doing it anyways)
        matches = list(dict.fromkeys(matches))
        return matches
    def get_schools_by_network(self, network):
        """
        Checks to see if the school is in the correct network.
        """
        inNetwork = []
        for i in self.schools:
            # cleans up the input, just in case there was any capitalization mistakes
            # does not account for other forms of user error such as typos
            if network.upper() == i.network.upper():
                inNetwork.append(i)
        return inNetwork
