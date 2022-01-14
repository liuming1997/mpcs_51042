import unittest
import math
from itertools import zip_longest

try:
    import problem1
except ImportError:
    pass

try:
    import problem2
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
    longMessage = False

    def setUp(self):
        self.dice = {
            'Boo': (0, 0, 5, 5, 7, 7),
            'Bowser': (0, 0, 1, 8, 9, 10),
            'BowserJr': (1, 1, 1, 4, 4, 9),
            'Daisy': (3, 3, 3, 3, 4, 4),
            'DiddyKong': (0, 0, 0, 7, 7, 7),
            'DonkeyKong': (0, 0, 0, 0, 10, 10),
            'DryBones': (1, 1, 1, 6, 6, 6),
            'Goomba': (0, 0, 3, 4, 5, 6),
            'HammerBro': (0, 1, 1, 5, 5, 5),
            'Koopa': (1, 1, 2, 3, 3, 10),
            'Luigi': (1, 1, 1, 5, 6, 7),
            'Mario': (1, 3, 3, 3, 5, 6),
            'MontyMole': (0, 2, 3, 4, 5, 6),
            'Peach': (0, 2, 4, 4, 4, 6),
            'PomPom': (0, 3, 3, 3, 3, 8),
            'Rosalina': (0, 0, 2, 3, 4, 8),
            'ShyGuy': (0, 4, 4, 4, 4, 4),
            'Standard': (1, 2, 3, 4, 5, 6),
            'Waluigi': (0, 1, 3, 5, 5, 7),
            'Wario': (6, 6, 6, 6, 0, 0),
            'Yoshi': (0, 1, 3, 3, 5, 7)
        }

    @number("1.1")
    @weight(4)
    def test_1_1(self):
        """ Test mean_stddev_stdlib """
        expected = {'Boo': [4, 2.943920288775949],
                    'Bowser': [4.666666666666667, 4.384315479321969],
                    'BowserJr': [3.3333333333333335, 2.8674417556808756],
                    'Daisy': [3.3333333333333335, 0.4714045207910317],
                    'DiddyKong': [3.5, 3.5],
                    'DonkeyKong': [3.3333333333333335, 4.714045207910317],
                    'DryBones': [3.5, 2.5],
                    'Goomba': [3, 2.309401076758503],
                    'HammerBro': [2.8333333333333335, 2.1921577396609844],
                    'Koopa': [3.3333333333333335, 3.0912061651652345],
                    'Luigi': [3.5, 2.565800719723442],
                    'Mario': [3.5, 1.6072751268321592],
                    'MontyMole': [3.3333333333333335, 1.9720265943665387],
                    'Peach': [3.3333333333333335, 1.8856180831641267],
                    'PomPom': [3.3333333333333335, 2.357022603955158],
                    'Rosalina': [2.8333333333333335, 2.733536577809454],
                    'ShyGuy': [3.3333333333333335, 1.4907119849998598],
                    'Standard': [3.5, 1.707825127659933],
                    'Waluigi': [3.5, 2.4324199198877374],
                    'Wario': [4, 2.8284271247461903],
                    'Yoshi': [3.1666666666666665, 2.3392781412697]}

        actual = problem1.mean_stddev_stdlib(self.dice)

        failures = []
        for player in expected:
            if not all(map(math.isclose, expected[player], actual[player])):
                failures.append(player)

        if failures:
            msg = "Results for these players are wrong: \n"
            for f in failures:
                msg += f"\t{f}\n\t\tExpected: {expected[f]}\n\t\tActual:   {actual[f]}\n"
            self.fail(msg)

    @number("1.2")
    @weight(4)
    def test_1_2(self):
        """ Test mean_stddev_nostdlib """
        expected = {'Boo': [4, 2.943920288775949],
                    'Bowser': [4.666666666666667, 4.384315479321969],
                    'BowserJr': [3.3333333333333335, 2.8674417556808756],
                    'Daisy': [3.3333333333333335, 0.4714045207910317],
                    'DiddyKong': [3.5, 3.5],
                    'DonkeyKong': [3.3333333333333335, 4.714045207910317],
                    'DryBones': [3.5, 2.5],
                    'Goomba': [3, 2.309401076758503],
                    'HammerBro': [2.8333333333333335, 2.1921577396609844],
                    'Koopa': [3.3333333333333335, 3.0912061651652345],
                    'Luigi': [3.5, 2.565800719723442],
                    'Mario': [3.5, 1.6072751268321592],
                    'MontyMole': [3.3333333333333335, 1.9720265943665387],
                    'Peach': [3.3333333333333335, 1.8856180831641267],
                    'PomPom': [3.3333333333333335, 2.357022603955158],
                    'Rosalina': [2.8333333333333335, 2.733536577809454],
                    'ShyGuy': [3.3333333333333335, 1.4907119849998598],
                    'Standard': [3.5, 1.707825127659933],
                    'Waluigi': [3.5, 2.4324199198877374],
                    'Wario': [4, 2.8284271247461903],
                    'Yoshi': [3.1666666666666665, 2.3392781412697]}

        actual = problem1.mean_stddev_no_stdlib(self.dice)

        failures = []
        for player in expected:
            if not all(map(math.isclose, expected[player], actual[player])):
                failures.append(player)

        if failures:
            msg = "Results for these players are wrong: \n"
            for f in failures:
                msg += f"\t{f}\n\t\tExpected: {expected[f]}\n\t\tActual:   {actual[f]}\n"
            self.fail(msg)

    @number("1.3")
    @weight(4)
    def test_1_3(self):
        """ Test mean_stddev_sorted """
        expected = [('HammerBro', [2.8333333333333335, 2.1921577396609844]),
                    ('Rosalina', [2.8333333333333335, 2.733536577809454]),
                    ('Goomba', [3, 2.309401076758503]),
                    ('Yoshi', [3.1666666666666665, 2.3392781412697]),
                    ('Daisy', [3.3333333333333335, 0.4714045207910317]),
                    ('ShyGuy', [3.3333333333333335, 1.4907119849998598]),
                    ('Peach', [3.3333333333333335, 1.8856180831641267]),
                    ('MontyMole', [3.3333333333333335, 1.9720265943665387]),
                    ('PomPom', [3.3333333333333335, 2.357022603955158]),
                    ('BowserJr', [3.3333333333333335, 2.8674417556808756]),
                    ('Koopa', [3.3333333333333335, 3.0912061651652345]),
                    ('DonkeyKong', [3.3333333333333335, 4.714045207910317]),
                    ('Mario', [3.5, 1.6072751268321592]),
                    ('Standard', [3.5, 1.707825127659933]),
                    ('Waluigi', [3.5, 2.4324199198877374]),
                    ('DryBones', [3.5, 2.5]),
                    ('Luigi', [3.5, 2.565800719723442]),
                    ('DiddyKong', [3.5, 3.5]),
                    ('Wario', [4, 2.8284271247461903]),
                    ('Boo', [4, 2.943920288775949]),
                    ('Bowser', [4.666666666666667, 4.384315479321969])]

        actual = problem1.mean_stddev_sorted(self.dice)

        failures = dict()
        for e, a in zip_longest(expected, actual):
            if e[0] != a[0]:
                e_order = [x[0] for x in expected]
                a_order = [x[0] for x in actual]
                msg = f"Results are not ordered correctly: \n\tExpected order: {e_order}\n\tActual order:   {a_order}"
                self.fail(msg)
            if not all(map(math.isclose, e[1], a[1])):
                failures[a[0]] = {'expected': e[1], 'actual': a[1]}

        if failures:
            msg = "Results for these players are wrong: \n"
            for k, v in failures.items():
                msg += f"\t{k}\n\t\tExpected: {v['expected']}\n\t\tActual:   {v['actual']}\n"
            self.fail(msg)

    @number("1.4")
    @weight(4)
    def test_1_4(self):
        """ Test mean_stddev_filtered """
        expected = [['Mario', [3.5, 1.6072751268321592]],
                    ['Standard', [3.5, 1.707825127659933]],
                    ['Waluigi', [3.5, 2.4324199198877374]],
                    ['DryBones', [3.5, 2.5]],
                    ['Luigi', [3.5, 2.565800719723442]],
                    ['DiddyKong', [3.5, 3.5]],
                    ['Wario', [4, 2.8284271247461903]],
                    ['Boo', [4, 2.943920288775949]],
                    ['Bowser', [4.666666666666667, 4.384315479321969]]]

        actual = problem1.mean_stddev_filtered(self.dice)

        failures = dict()
        for e, a in zip_longest(expected, actual):
            if e[0] != a[0]:
                e_order = [x[0] for x in expected]
                a_order = [x[0] for x in actual]
                msg = f"Results are not ordered or filtered correctly: \n\tExpected order: {e_order}\n\tActual order:   {a_order}"
                self.fail(msg)
            if not all(map(math.isclose, e[1], a[1])):
                failures[a[0]] = {'expected': e[1], 'actual': a[1]}

        if failures:
            msg = "Results for these players are wrong: \n"
            for k, v in failures.items():
                msg += f"\t{k}\n\t\tExpected: {v['expected']}\n\t\tActual:   {v['actual']}\n"
            self.fail(msg)


class TestProblem2(unittest.TestCase):
    longMessage = False

    def compare_sets(self, commands, actual, expected):
        if actual != expected:
            msg = "Result failed for: \n"
            for c in commands:
                msg += f"\t{c}\n"
            msg += f"Expected:\n\t{expected}\n"
            msg += f"Actual:\n\t{actual}\n"
            self.fail(msg)

    def setUp(self):
        self.c_dict = problem2.fill_completions('articles.txt')

    @number("2.1")
    @weight(4)
    def test_2_1(self):
        """ Test if fill_completions parsed '_eat' words from articles.txt """
        expected = {'beaten', 'heat', 'weathered', 'deaths', 'meat', 'seattle', 'featuring',
                    'feature', 'deaton', 'death', 'heather', 'heath', 'feathers', 'heaton',
                    'weathermen', 'features', 'neat', 'featured', 'seat', 'weather', 'feather'}
        actual = self.c_dict[(1, 'e')] & self.c_dict[(2, 'a')] & self.c_dict[(3, 't')]
        self.compare_sets(
            commands=["c_dict = fill_completions('articles.txt')",
                      "c_dict[(1, 'e')] & c_dict[(2, 'a')] & c_dict[(3, 't')]"],
            expected=expected,
            actual=actual
        )

    @number("2.2")
    @weight(4)
    def test_2_2(self):
        """ Test if fill_completions parsed 'ea_t' words from articles.txt"""
        expected = {'earth', 'east', 'easter', 'eastern', 'easton'}
        actual = self.c_dict[(0, 'e')] & self.c_dict[(1, 'a')] & self.c_dict[(3, 't')]
        self.compare_sets(
            commands=["c_dict = fill_completions('articles.txt')",
                      "c_dict[(0, 'e')] & c_dict[(1, 'a')] & c_dict[(3, 't')]"],
            expected=expected,
            actual=actual
        )

    @number("2.3")
    @weight(4)
    def test_2_3(self):
        """ Test if fill_completions parsed 'm_tt_r' words from articles.txt"""
        expected = {'matter', 'mattered', 'matters', 'muttered', 'muttering'}
        actual = self.c_dict[(0, 'm')] & self.c_dict[(2, 't')] & self.c_dict[(3, 't')] & \
                 self.c_dict[(5, 'r')]
        self.compare_sets(
            commands=["c_dict = fill_completions('articles.txt')",
                      "c_dict[(0, 'm')] & c_dict[(2, 't')] & c_dict[(3, 't')] & c_dict[(5, 'r')]"],
            expected=expected,
            actual=actual
        )

    @number("2.4")
    @weight(4)
    def test_2_4(self):
        """ Test if words that begin with 'e' and words that begin with 'a' are disjoint """
        expected = set()
        actual = self.c_dict[(0, 'a')] & self.c_dict[(0, 'b')]
        self.compare_sets(
            commands=["c_dict = fill_completions('articles.txt')",
                      "c_dict[(0, 'a')] & c_dict[(0, 'b')]"],
            expected=expected,
            actual=actual
        )

    @number("2.5")
    @weight(4)
    def test_2_5(self):
        """ Test if fill_completions found no 'a_q' words """
        expected = set()
        actual = self.c_dict[(0, 'a')] & self.c_dict[(3, 'q')]
        self.compare_sets(
            commands=["c_dict = fill_completions('articles.txt')",
                      "c_dict[(0, 'a')] & c_dict[(3, 'q')]"],
            expected=expected,
            actual=actual
        )

    @number("2.6")
    @weight(2)
    def test_2_6(self):
        """ Test if fill_completions found no words with 'x' in position 10 """
        with self.assertRaises(LookupError):
            actual = self.c_dict[(10, 'x')]

    @number("2.7")
    @weight(4)
    def test_2_7(self):
        """ Test find_completions('geo') """
        expected = {'geoffrey', 'geographical', 'george', 'georgia'}
        actual = problem2.find_completions('geo', self.c_dict)
        self.compare_sets(
            commands=["c_dict = fill_completions('articles.txt')",
                      "find_completions('geo', c_dict)"],
            expected=expected,
            actual=actual
        )

    @number("2.8")
    @weight(4)
    def test_2_8(self):
        """ Test find_completions('geor') """
        expected = {'george', 'georgia'}
        actual = problem2.find_completions('geor', self.c_dict)
        self.compare_sets(
            commands=["c_dict = fill_completions('articles.txt')",
                      "find_completions('geor', c_dict)"],
            expected=expected,
            actual=actual
        )

    @number("2.9")
    @weight(4)
    def test_2_9(self):
        """ Test find_completions('george') """
        expected = {'george'}
        actual = problem2.find_completions('george', self.c_dict)
        self.compare_sets(
            commands=["c_dict = fill_completions('articles.txt')",
                      "find_completions('george', c_dict)"],
            expected=expected,
            actual=actual
        )

    @number("2.10")
    @weight(4)
    def test_2_10(self):
        """ Test find_completions('georges') """
        expected = set()
        actual = problem2.find_completions('georges', self.c_dict)
        self.compare_sets(
            commands=["c_dict = fill_completions('articles.txt')",
                      "find_completions('georges', c_dict)"],
            expected=expected,
            actual=actual
        )

    @number("2.11")
    @weight(4)
    def test_2_11(self):
        """ Test find_completions('can') """
        expected = {'can', 'canadian', 'cancer', 'cancers', 'candidate', 'candidates', 'cane',
                    'cannot', 'cans', 'canterbury'}
        actual = problem2.find_completions('can', self.c_dict)
        self.compare_sets(
            commands=["c_dict = fill_completions('articles.txt')",
                      "find_completions('can', c_dict)"],
            expected=expected,
            actual=actual
        )

    @number("2.12")
    @weight(4)
    def test_2_12(self):
        """ Test find_completions('candidate') """
        expected = {'candidate', 'candidates'}
        actual = problem2.find_completions('candidate', self.c_dict)
        self.compare_sets(
            commands=["c_dict = fill_completions('articles.txt')",
                      "find_completions('candidate', c_dict)"],
            expected=expected,
            actual=actual
        )

    @number("2.13")
    @weight(4)
    def test_2_13(self):
        """ Test find_completions('candidates') """
        expected = {'candidates'}
        actual = problem2.find_completions('candidates', self.c_dict)
        self.compare_sets(
            commands=["c_dict = fill_completions('articles.txt')",
                      "find_completions('candidates', c_dict)"],
            expected=expected,
            actual=actual
        )

    @number("2.14")
    @weight(4)
    def test_2_14(self):
        """ Test find_completions('candidatesx') """
        expected = set()
        actual = problem2.find_completions('candidatesx', self.c_dict)
        self.compare_sets(
            commands=["c_dict = fill_completions('articles.txt')",
                      "find_completions('candidatesx', c_dict)"],
            expected=expected,
            actual=actual
        )


if __name__ == '__main__':
    suite = unittest.defaultTestLoader.loadTestsFromNames(
        ['__main__.TestProblem1', '__main__.TestProblem2'])

    # For students
    unittest.TextTestRunner(verbosity=2).run(suite)

    # For Gradescope
    # from gradescope_utils.autograder_utils.json_test_runner import JSONTestRunner
    # with open('/autograder/results/results.json', 'w') as f:
    #         JSONTestRunner(visibility='visible', stream=f).run(suite)
