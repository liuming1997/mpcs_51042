"""
MPCS 51042 Assignment 4

Ming Liu

Problem 1
"""

def prime_generator():
    """
    Prime number generator with caching.

    Parameters:
    No parameters.

    Return value:
    Doesn't return anything per se, but does have yield to start the iteration from the next value.
    """
    primes = []
    # the first prime
    primes.append(2)
    yield 2
    # all subsequent primes
    number = 3
    while True:
        # infinite loop to keep going as long as you don't stop it
        # test prime divisors only
        # drawback: you really only need to test to sqrt(n), but we don't stop until n in this implementation
        # it's not the greatest in efficiency but I don't have time to test a more efficient solution
        # maybe something to the tune of:
        # if number % test == 0:
        #   break
        # elif test > n ** (1/2):
        #   primes.append(number)
        for test in primes:
            if number % test == 0:
                break
        else:
            primes.append(number)
            yield number
        number += 1
