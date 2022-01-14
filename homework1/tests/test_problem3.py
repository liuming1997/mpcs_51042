import unittest
from problem3 import newton

try:
    from gradescope_utils.autograder_utils.decorators import number, weight
except ImportError:
    from gradescope_utils_dummy import number, weight

# functions to test with Newton
def f1(x):
    return (x-1)**2

def f1_pr(x):
    return 2*(x-1)

def f2(x):
    return (x**2)-4

def f2_pr(x):
    return 2*x

class TestProblem3(unittest.TestCase):

    # display input and output for failed tests
    def helper(self, f, f_str, f_pr, f_pr_str, x_0, tol, max_iters, expected):
        actual = newton(f, f_pr, x_0, tol, max_iters)
    
        msg = "\n\nTest failed: newton(f, f_pr, {}, {}, {})\n".format(x_0, tol, max_iters)
        msg += "  f(x) = {}\n".format(f_str)
        msg += "  f_pr(x) = {}\n\n".format(f_pr_str)
        msg += "  Actual: {}\n".format(actual)
        msg += "  Expected: {}\n".format(expected)

        self.assertAlmostEqual(actual, expected, places=4, msg=msg)

    @number("3.1")
    @weight(2)
    def test1(self):
        self.helper(f1, "(x-1)**2", f1_pr, "2*(x-1)", 0, 1e-16, 1, 0.5)

    @number("3.2")
    @weight(2)
    def test2(self):
        self.helper(f1, "(x-1)**2", f1_pr, "2*(x-1)", 0, 1e-16, 2, 0.75)

    @number("3.3")
    @weight(2)
    def test3(self):
        self.helper(f1, "(x-1)**2", f1_pr, "2*(x-1)", 0, 1e-16, 4, 0.9375)

    @number("3.4")
    @weight(2)
    def test4(self):
        self.helper(f1, "(x-1)**2", f1_pr, "2*(x-1)", 0, 1e-16, 5, 0.96875)

    @number("3.5")
    @weight(2)
    def test5(self):
        self.helper(f2, "(x**2)-4", f2_pr, "2*x", -1, 1e-16, 2, -2.05)

    @number("3.6")
    @weight(2)
    def test6(self):
        self.helper(f2, "(x**2)-4", f2_pr, "2*x", -1, 1e-16, 1000, -2.0)

    @number("3.7")
    @weight(2)
    def test7(self):
        self.helper(f2, "(x**2)-4", f2_pr, "2*x", 1, 1e-16, 2, 2.05)

    @number("3.8")
    @weight(2)
    def test8(self):
        self.helper(f2, "(x**2)-4", f2_pr, "2*x", 1, 1e-16, 1000, 2.0)

    @number("3.9")
    @weight(2)
    def test9(self):
        self.helper(f2, "(x**2)-4", f2_pr, "2*x", 3, 1e-16, 1, 2.16666666666)

    @number("3.10")
    @weight(2)
    def test10(self):
        self.helper(f2, "(x**2)-4", f2_pr, "2*x", 3, 1e-16, 1000, 2.0)
    