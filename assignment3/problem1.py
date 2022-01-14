"""
MPCS 51042 Assignment 3
Ming Liu

These programs were written without discussing them with anyone.
"""

# Problem 1

def vectorize(func):
    """
    Takes in a function and allows it to return output for each item that the function may have to deal with.
    """
    def func2(*args):
        # take args and put into list
        # source: https://www.geeksforgeeks.org/args-kwargs-python/
        trueInput = list(args)
        # loop over list as usual
        output = []
        for i in trueInput:
            output.append(func(i))
        return output
        # this was supposed to go somewhere, and was left here for the grader to suggest how it might work, because it doesnt't
        # return [lambda i: func(i) for i in trueInput]
    return func2
