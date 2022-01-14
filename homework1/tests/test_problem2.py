import unittest
from problem2 import expand

try:
    from gradescope_utils.autograder_utils.decorators import number, weight
except ImportError:
    from gradescope_utils_dummy import number, weight

class TestProblem2(unittest.TestCase):

    # display input and output for failed tests
    def helper(self, rng, expected):
        actual = expand(rng)
    
        msg = "\n\nTest failed: expand(\"{}\")\n".format(rng)
        msg += "  Actual: {}\n".format(actual)
        msg += "  Expected: {}\n".format(expected)

        self.assertListEqual(actual, expected, msg)

    @number("2.1")
    @weight(2)
    def test1(self):
        rng = "1"
        expected = [1]
        self.helper(rng, expected)

    @number("2.2")
    @weight(2)
    def test2(self):
        rng = "2-5"
        expected = [2, 3, 4]
        self.helper(rng, expected)

    @number("2.3")
    @weight(2)
    def test3(self):
        rng = "1,2-5"
        expected = [1, 2, 3, 4]
        self.helper(rng, expected)

    @number("2.4")
    @weight(2)
    def test4(self):
        rng = "1,2-5,5"
        expected = [1, 2, 3, 4, 5]
        self.helper(rng, expected)

    @number("2.5")
    @weight(2)
    def test5(self):
        rng = "1,2-5,5,6-10"
        expected = [1, 2, 3, 4, 5, 6, 7, 8, 9]
        self.helper(rng, expected)

    @number("2.6")
    @weight(2)
    def test6(self):
        rng = "6-10,1,2-5,5"
        expected = [1, 2, 3, 4, 5, 6, 7, 8, 9]
        self.helper(rng, expected)

    @number("2.7")
    @weight(2)
    def test7(self):
        rng = "1,2-6,5,6-10"
        expected = [1, 2, 3, 4, 5, 6, 7, 8, 9]
        self.helper(rng, expected)

    @number("2.8")
    @weight(2)
    def test8(self):
        rng = "1,2-6,8-12"
        expected = [1, 2, 3, 4, 5, 8, 9, 10, 11]
        self.helper(rng, expected)

    @number("2.9")
    @weight(2)
    def test9(self):
        rng = "1,2-6,8-12,14"
        expected = [1, 2, 3, 4, 5, 8, 9, 10, 11, 14]
        self.helper(rng, expected)

    @number("2.10")
    @weight(2)
    def test10(self):
        rng = "1,2-6,14,8-12"
        expected = [1, 2, 3, 4, 5, 8, 9, 10, 11, 14]
        self.helper(rng, expected)