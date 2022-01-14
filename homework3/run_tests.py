import unittest
import math
from itertools import zip_longest

try:
    from problem1 import *
except ImportError:
    pass

try:
    from problem2 import *
except ImportError:
    pass

try:
    from gradescope_utils.autograder_utils.decorators import number, weight
except ImportError:
    # Copied from gradescope_utils source code

    class number(object):
        def __init__(self, val):
            self.val = val

        def __call__(self, func):
            func.__number__ = self.val
            return func


    class weight(object):
        def __init__(self, val):
            self.val = val

        def __call__(self, func):
            func.__weight__ = self.val
            return func

class TestProblem1(unittest.TestCase):

    @number("1.1")
    @weight(2)
    def test_1_1(self):
        """ Testing: vectorize(str.upper)() """
        expected = []
        actual = vectorize(str.upper)()

        if expected != actual:
            msg = "Found incorrect output: \n"
            for f in failures:
                msg += f"\t{f}\n\t\tExpected: {expected}\n\t\tActual:   {actual}\n"
            self.fail(msg)  


    @number("1.2")
    @weight(3)
    def test_1_2(self):
        """ Testing: vectorize(str.upper)("a") """
        expected = ["A"]
        actual = vectorize(str.upper)("a")

        if expected != actual:
            msg = "Found incorrect output: \n"
            for f in failures:
                msg += f"\t{f}\n\t\tExpected: {expected}\n\t\tActual:   {actual}\n"
            self.fail(msg)

    @number("1.3")
    @weight(3)
    def test_1_3(self):
        """ Testing: vectorize(str.upper)("a", "A", "b") """
        expected = ["A", "A", "B"]
        actual = vectorize(str.upper)("a", "A", "b")

        if expected != actual:
            msg = "Found incorrect output: \n"
            for f in failures:
                msg += f"\t{f}\n\t\tExpected: {expected}\n\t\tActual:   {actual}\n"
            self.fail(msg)  

    @number("1.4")
    @weight(2)
    def test_1_4(self):
        """ Testing: vectorize(math.sqrt)() """
        expected = []
        actual = vectorize(math.sqrt)()

        if expected != actual:
            msg = "Found incorrect output: \n"
            for f in failures:
                msg += f"\t{f}\n\t\tExpected: {expected}\n\t\tActual:   {actual}\n"
            self.fail(msg)  


    @number("1.5")
    @weight(2)
    def test_1_5(self):
        """ Testing: actual = vectorize(math.sqrt)(1) """
        expected = [1.0]
        actual = vectorize(math.sqrt)(1)

        if expected != actual:
            msg = "Found incorrect output: \n"
            for f in failures:
                msg += f"\t{f}\n\t\tExpected: {expected}\n\t\tActual:   {actual}\n"
            self.fail(msg)

    @number("1.6")
    @weight(3)
    def test_1_6(self):
        """ Testing: actual = vectorize(math.sqrt)(1, 1, 1, 1) """
        expected = [1.0, 1.0, 1.0, 1.0]
        actual = vectorize(math.sqrt)(1, 1, 1, 1)

        if expected != actual:
            msg = "Found incorrect output: \n"
            for f in failures:
                msg += f"\t{f}\n\t\tExpected: {expected}\n\t\tActual:   {actual}\n"
            self.fail(msg) 

class TestProblem2(unittest.TestCase):

    @number("2.1")
    @weight(3)
    def test_2_1(self):
        """ Testing Coordinate attributes """
        actual_coordinate = Coordinate(100, 200)

        # latitude
        expected = 100
        actual = actual_coordinate.latitude
        if expected != actual:
            msg = "Found incorret latitude: \n"
            msg += f"\tExpected: {expected}\n\tActual:   {actual}\n"
            self.fail(msg) 

        # longitude
        expected = 200
        actual = actual_coordinate.longitude
        if expected != actual:
            msg = "Found incorret longitude: \n"
            msg += f"\tExpected: {expected}\n\tActual:   {actual}\n"
            self.fail(msg) 

    @number("2.2")
    @weight(3)
    def test_2_2(self):
        """ Testing Coordinate fromdegrees """
        EPSILON = 0.001
        actual_coordinate = Coordinate.fromdegrees(2000, -1000)

        # latitude
        expected = 34.90658503988659
        actual = actual_coordinate.latitude
        if not ((expected - EPSILON <= actual) and (actual <= expected + EPSILON)):
            msg = "Found incorret latitude: \n"
            msg += f"\tExpected: {expected}\n\tActual:   {actual}\n"
            self.fail(msg) 

        # longitude
        expected = -17.453292519943297
        actual = actual_coordinate.longitude
        if not ((expected - EPSILON <= actual) and (actual <= expected + EPSILON)):
            msg = "Found incorret longitude: \n"
            msg += f"\tExpected: {expected}\n\tActual:   {actual}\n"
            self.fail(msg) 

    @number("2.3")
    @weight(3)
    def test_2_3(self):
        """ Testing Coordinate distance """
        EPSILON = 0.001
        coordinate1 = Coordinate(100, 200)
        actual_distance = coordinate1.distance(coordinate1)

        expected = 0
        actual = actual_distance
        if not ((expected - EPSILON <= actual) and (actual <= expected + EPSILON)):
            msg = "Found incorret distance: \n"
            msg += f"\tExpected: {expected}\n\tActual:   {actual}\n"
            self.fail(msg) 

    @number("2.4")
    @weight(3)
    def test_2_4(self):
        """ Testing Coordinate distance """
        EPSILON = 0.001
        coordinate1 = Coordinate(100, 200)
        coordinate2 = Coordinate(-100, -300)
        actual_distance = coordinate1.distance(coordinate2)

        expected = 10785.502296746728
        actual = actual_distance
        if not ((expected - EPSILON <= actual) and (actual <= expected + EPSILON)):
            msg = "Found incorret distance: \n"
            msg += f"\tExpected: {expected}\n\tActual:   {actual}\n"
            self.fail(msg) 

    @number("2.5")
    @weight(3)
    def test_2_5(self):
        """ Testing Coordinate as_degrees """
        EPSILON = 0.001
        coordinate1 = Coordinate(100, 200)
        actual_degrees = coordinate1.as_degrees()

        # latitude
        expected = 5729.5779513082325
        actual = actual_degrees[0]
        if not ((expected - EPSILON <= actual) and (actual <= expected + EPSILON)):
            msg = "Found incorret latitude in degrees: \n"
            msg += f"\tExpected: {expected}\n\tActual:   {actual}\n"
            self.fail(msg) 

        # longitude
        expected = 11459.155902616465
        actual = actual_degrees[1]
        if not ((expected - EPSILON <= actual) and (actual <= expected + EPSILON)):
            msg = "Found incorret longitude in degrees: \n"
            msg += f"\tExpected: {expected}\n\tActual:   {actual}\n"
            self.fail(msg) 

    # Test show_map by hand

    @number("2.6")
    @weight(7)
    def test_2_6(self):
        """ Testing School attributes """
        EPSILON = 0.001
        school_dict = {'School_ID': '610566', 
                       'Network': 'Options', 
                       'Short_Name': 'MAGIC JOHNSON - N LAWNDALE HS', 
                       'the_geom': 'POINT (-87.70660367604683 41.86647785082858)', 
                       'Address': '3222 W ROOSEVELT RD', 
                       'Zip': '60624', 
                       'Governance': 'ALOP', 
                       'Grade_Cat': 'HS', 
                       'Grades': '9, 10, 11, 12', 
                       'Lat': '41.8664778516', 
                       'Long': '-87.706603676', 
                       'Phone': '1(773)826-1137', 
                       'GeoNetwork': '5', 
                       'COMMAREA': 'NORTH LAWNDALE', 
                       'WARD_15': '24', 
                       'ALD_15': 'Michael D. Chandler'}

        actual_school = School(school_dict)

        # id
        actual = actual_school.id
        expected = 610566
        if expected != actual:
            msg = "Found incorret id: \n"
            msg += f"\tExpected: {expected}\n\tActual:   {actual}\n"
            self.fail(msg) 

        # name
        actual = actual_school.name
        expected = 'MAGIC JOHNSON - N LAWNDALE HS'
        if expected != actual:
            msg = "Found incorret name: \n"
            msg += f"\tExpected: {expected}\n\tActual:   {actual}\n"
            self.fail(msg) 

        # network
        actual = actual_school.network
        expected = 'Options'
        if expected != actual:
            msg = "Found incorret network: \n"
            msg += f"\tExpected: {expected}\n\tActual:   {actual}\n"
            self.fail(msg) 

        # address
        actual = actual_school.address
        expected = '3222 W ROOSEVELT RD'
        if expected != actual:
            msg = "Found incorret address: \n"
            msg += f"\tExpected: {expected}\n\tActual:   {actual}\n"
            self.fail(msg) 

        # zip
        actual = actual_school.zip
        expected = '60624'
        if expected != actual:
            msg = "Found incorret zip: \n"
            msg += f"\tExpected: {expected}\n\tActual:   {actual}\n"
            self.fail(msg) 

        # phone
        actual = actual_school.phone
        expected = '1(773)826-1137'
        if expected != actual:
            msg = "Found incorret phone: \n"
            msg += f"\tExpected: {expected}\n\tActual:   {actual}\n"
            self.fail(msg) 

        # grades
        actual = actual_school.grades
        expected = ['9', '10', '11', '12']
        if expected != actual:
            msg = "Found incorret grades: \n"
            msg += f"\tExpected: {expected}\n\tActual:   {actual}\n"
            self.fail(msg) 

        # location
        actual_location = actual_school.location

        # latitude
        expected = 0.730707884723702
        actual = actual_location.latitude
        if not ((expected - EPSILON <= actual) and (actual <= expected + EPSILON)):
            msg = "Found incorret school latitude: \n"
            msg += f"\tExpected: {expected}\n\tActual:   {actual}\n"
            self.fail(msg) 

        # longitude
        expected = -1.530769009887962
        actual = actual_location.longitude
        if not ((expected - EPSILON <= actual) and (actual <= expected + EPSILON)):
            msg = "Found incorret school longitude: \n"
            msg += f"\tExpected: {expected}\n\tActual:   {actual}\n"
            self.fail(msg) 

    @number("2.7")
    @weight(7)
    def test_2_7(self):
        """ Testing School distance """
        EPSILON = 0.001
        school_dict = {'School_ID': '610566', 
                       'Network': 'Options', 
                       'Short_Name': 'MAGIC JOHNSON - N LAWNDALE HS', 
                       'the_geom': 'POINT (-87.70660367604683 41.86647785082858)', 
                       'Address': '3222 W ROOSEVELT RD', 
                       'Zip': '60624', 
                       'Governance': 'ALOP', 
                       'Grade_Cat': 'HS', 
                       'Grades': '9, 10, 11, 12', 
                       'Lat': '41.8664778516', 
                       'Long': '-87.706603676', 
                       'Phone': '1(773)826-1137', 
                       'GeoNetwork': '5', 
                       'COMMAREA': 'NORTH LAWNDALE', 
                       'WARD_15': '24', 
                       'ALD_15': 'Michael D. Chandler'}

        actual_school = School(school_dict)
        coordinate = Coordinate(1, -1.5)

        expected = 1069.4978721896794
        actual = actual_school.distance(coordinate)
        if not ((expected - EPSILON <= actual) and (actual <= expected + EPSILON)):
            msg = "Found incorret school distance: \n"
            msg += f"\tExpected: {expected}\n\tActual:   {actual}\n"
            self.fail(msg) 

    @number("2.8")
    @weight(2)
    def test_2_8(self):
        """ Testing CPS attribute """

        actual_cps = CPS("schools.csv")

        # number of schools
        expected = 661
        actual = len(actual_cps.schools)
        if expected != actual:
            msg = "Found incorret number of schools: \n"
            msg += f"\tExpected: {expected}\n\tActual:   {actual}\n"
            self.fail(msg) 

        # type of school
        expected = "<class 'problem2.School'>"
        actual = str(type(actual_cps.schools[0]))
        if expected != actual:
            msg = "Found incorret type in schools: \n"
            msg += f"\tExpected: {expected}\n\tActual:   {actual}\n"
            self.fail(msg) 

    @number("2.9")
    @weight(2)
    def test_2_9(self):
        """ Testing CPS nearby_schools """

        actual_cps = CPS("schools.csv")
        coordinate = Coordinate(0.73, -1.52)

        expected = []
        actual = actual_cps.nearby_schools(coordinate)
        if expected != actual:
            msg = "Found incorret nearby schools: \n"
            msg += f"\tExpected: {expected}\n\tActual:   {actual}\n"
            self.fail(msg) 

    @number("2.10")
    @weight(2)
    def test_2_10(self):
        """ Testing CPS nearby_schools """

        actual_cps = CPS("schools.csv")
        coordinate = Coordinate(0.730991014625029, -1.5294843834001908)

        expected_list = ['CHICAGO VIRTUAL', 'NOBLE - MUCHIN HS', 'YCCS - INNOVATIONS', 'JONES HS']
        actual_list = actual_cps.nearby_schools(coordinate)
        for i in range(len(actual_list)):
            actual = actual_list[i].name
            if actual not in expected_list:
                msg = "Found incorret nearby schools: \n"
                msg += f"\tExpected: {expected_list}\n\Found:   {actual}\n"
                self.fail(msg) 

    @number("2.11")
    @weight(2)
    def test_2_11(self):
        """ Testing CPS nearby_schools """

        actual_cps = CPS("schools.csv")
        coordinate = Coordinate(0.730991014625029, -1.5294843834001908)

        expected_list = ['NOBLE - MUCHIN HS', 'YCCS - INNOVATIONS']
        actual_list = actual_cps.nearby_schools(coordinate, radius=0.5)
        for i in range(len(actual_list)):
            actual = actual_list[i].name
            if actual not in expected_list:
                msg = "Found incorret nearby schools: \n"
                msg += f"\tExpected: {expected_list}\n\Found:   {actual}\n"
                self.fail(msg) 

    @number("2.12")
    @weight(2)
    def test_2_12(self):
        """ Testing CPS get_schools_by_grade """

        actual_cps = CPS("schools.csv")

        expected_list = ['FARRAGUT HS']
        actual_list = actual_cps.get_schools_by_grade("PK", "12")
        for i in range(len(actual_list)):
            actual = actual_list[i].name
            if actual not in expected_list:
                msg = "Found incorret nearby schools: \n"
                msg += f"\tExpected: {expected_list}\n\Found:   {actual}\n"
                self.fail(msg) 

    @number("2.13")
    @weight(2)
    def test_2_13(self):
        """ Testing CPS get_schools_by_grade """

        actual_cps = CPS("schools.csv")

        expected = []
        actual = actual_cps.get_schools_by_grade("PK", "8", "12")
        if expected != actual:
            msg = "Found incorret nearby schools: \n"
            msg += f"\tExpected: {expected}\n\tActual:   {actual}\n"
            self.fail(msg) 

    @number("2.14")
    @weight(2)
    def test_2_14(self):
        """ Testing CPS get_schools_by_network """

        actual_cps = CPS("schools.csv")

        expected = []
        actual = actual_cps.get_schools_by_network("Hello")
        if expected != actual:
            msg = "Found incorret schools by network: \n"
            msg += f"\tExpected: {expected}\n\tActual:   {actual}\n"
            self.fail(msg) 

    @number("2.15")
    @weight(2)
    def test_2_15(self):
        """ Testing CPS get_schools_by_network """

        actual_cps = CPS("schools.csv")

        expected_list = ['CHIARTS HS', 'HOPE INSTITUTE', 'PLATO', 'CHICAGO TECH HS']
        actual_list = actual_cps.get_schools_by_network("Contract")
        for i in range(len(actual_list)):
            actual = actual_list[i].name
            if actual not in expected_list:
                msg = "Found incorret schools by network: \n"
                msg += f"\tExpected: {expected_list}\n\Found:   {actual}\n"
                self.fail(msg) 

if __name__ == '__main__':
    suite = unittest.defaultTestLoader.loadTestsFromNames(
        ['__main__.TestProblem1', '__main__.TestProblem2'])

    # For students
    unittest.TextTestRunner(verbosity=2).run(suite)

    # # For Gradescope
    # from gradescope_utils.autograder_utils.json_test_runner import JSONTestRunner

    # with open('/autograder/results/results.json', 'w') as f:
    #     JSONTestRunner(visibility='visible', stream=f).run(suite)
