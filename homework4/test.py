from functools import lru_cache

# @lru_cache(maxsize=None)
def vectorize(func):
    """
    Takes in a function and allows it to return output for each item that the function may have to deal with.
    Copied from Homework 3.
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
    return func2

inputs = ["a", "b", "c", "d", "a", "e", "d", "f", "g", "d", "h"]
thing = vectorize(str.upper)
print(thing([x for x in inputs]))