import unittest
from problem1 import isect

try:
    from gradescope_utils.autograder_utils.decorators import number, weight
except ImportError:
    from gradescope_utils_dummy import number, weight

class TestProblem1(unittest.TestCase):

    # display input and output for failed tests
    def helper(self, s1, s2, expected):
        actual = isect(s1, s2)
    
        msg = "\n\nTest failed: isect(\"{}\", \"{}\")\n".format(s1, s2)
        msg += "  Actual: {}\n".format(actual)
        msg += "  Expected: {}\n".format(expected)

        self.assertListEqual(actual, expected, msg)

    @number("1.1")
    @weight(2)
    def test1(self):
        s1 = "3"
        s2 = "3"
        expected = []
        self.helper(s1, s2, expected)

    @number("1.2")
    @weight(2)
    def test2(self):
        s1 = "12"
        s2 = "12"
        expected = [12]
        self.helper(s1, s2, expected)

    @number("1.3")
    @weight(2)
    def test3(self):
        s1 = "3"
        s2 = "12"
        expected = []
        self.helper(s1, s2, expected)

    @number("1.4")
    @weight(2)
    def test4(self):
        s1 = "3,10,12"
        s2 = "20,3,0"
        expected = []
        self.helper(s1, s2, expected)

    @number("1.5")
    @weight(2)
    def test5(self):
        s1 = "3,12,20"
        s2 = "20,3,12"
        expected = [12, 20]
        self.helper(s1, s2, expected)

    @number("1.6")
    @weight(2)
    def test6(self):
        s1 = "3,123,201,10,12,20"
        s2 = "20,3,201,124,0,12"
        expected = [12, 20, 201]
        self.helper(s1, s2, expected)

    @number("1.7")
    @weight(2)
    def test7(self):
        s1 = "3,123,201,12,20"
        s2 = "20,3,201,124,0,12"
        expected = [12, 20, 201]
        self.helper(s1, s2, expected)

    @number("1.8")
    @weight(2)
    def test8(self):
        s1 = "3,10,12,-4,20"
        s2 = "20,3,12,0,12"
        expected = [12, 20]
        self.helper(s1, s2, expected)

    @number("1.9")
    @weight(2)
    def test9(self):
        s1 = "3,10,12,20,-4,20"
        s2 = "20,3,12,0,12"
        expected = [12, 20]
        self.helper(s1, s2, expected)

    @number("1.10")
    @weight(2)
    def test10(self):
        s1 = "20,12,20,201"
        s2 = "201,20,20,12"
        expected = [12, 20, 201]
        self.helper(s1, s2, expected)