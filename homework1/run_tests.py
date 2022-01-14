import unittest

if __name__ == '__main__':
    suite = unittest.defaultTestLoader.discover('tests')
    try:
        from gradescope_utils.autograder_utils.json_test_runner import JSONTestRunner

        with open('/autograder/results/results.json', 'w') as f:
            JSONTestRunner(visibility='visible', stream=f).run(suite)
    except ImportError:
        unittest.TextTestRunner().run(suite)
