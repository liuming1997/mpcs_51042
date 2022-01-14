"""
MPCS 51042 Assignment 2
Ming Liu
"""

# Problem 1

import statistics as stats

def mean_stddev_stdlib(inDict):
    """
    Takes an input dictionary (inDict) with key (str) and value (tuple) pairs, and for each key, returns the mean and standard deviation of the matching tuple set.
    """
    outDict = {}
    for key in inDict:
        # get the values for each key
        sample = inDict.get(key)
        mean = stats.mean(sample)
        stdev = stats.pstdev(sample)
        values = (mean, stdev)
        outDict[key] = values
    return outDict

def mean_stddev_no_stdlib(inDict):
    """
    Takes an input dictionary (inDict) with key (str) and value (tuple) pairs, and for each key, returns the mean and standard deviation of the matching tuple set.
    This implementation does not use the standard library functions for mean and stdev.
    """
    outDict = {}
    for key in inDict:
        # get the values for each key
        sample = inDict.get(key)
        # find mean
        mean = sum(sample)/len(sample)
        # dummy stdev numbers
        stdev = 0
        deviations = 0
        # rate limiting step makes this O(n^2)
        for num in sample:
            diff = abs(num - mean)**2
            deviations += diff
        # you could do math.sqrt, or just realize this
        stdev = (deviations/len(sample))**(1/2)
        values = (mean, stdev)
        outDict[key] = values
    return outDict

def mean_stddev_sorted(inDict):
    """
    Takes an input dictionary (inDict) with key (str) and value (tuple) pairs, and for each key, returns the mean and standard deviation of the matching tuple set.
    This implementation does not use the standard library functions for mean and stdev, and sorts the output by mean, then standard deviation, in increasing value.
    """
    outDict = {}
    for key in inDict:
        # get the values for each key
        sample = inDict.get(key)
        # find mean
        mean = sum(sample)/len(sample)
        # dummy stdev numbers
        stdev = 0
        deviations = 0
        # rate limiting step makes this O(n^2)
        for num in sample:
            diff = abs(num - mean)**2
            deviations += diff
        # you could do math.sqrt, or just realize this
        stdev = (deviations/len(sample))**(1/2)
        values = (mean, stdev)
        outDict[key] = values
    # sort the dictionary using lambda; the lambda does it first by mean, then by stdev
    sortedDict = sorted(outDict.items(), key=lambda item:(item[1][0], item[1][1]))
    return sortedDict

def mean_stddev_filtered(inDict):
    """
    Takes an input dictionary (inDict) with key (str) and value (tuple) pairs, and for each key, returns the mean and standard deviation of the matching tuple set.
    This implementation does not use the standard library functions for mean and stdev, and only returns the ones for which mean >= 3.5.
    """
    outDict = {}
    for key in inDict:
        # get the values for each key
        sample = inDict.get(key)
        # find mean
        mean = sum(sample)/len(sample)
        # skip all of the code below if the mean isn't what we want
        if mean < 3.5:
            continue
        else:
            # dummy stdev numbers
            stdev = 0
            deviations = 0
            # rate limiting step makes this O(n^2)
            for num in sample:
                diff = abs(num - mean)**2
                deviations += diff
            # you could do math.sqrt, or just realize this
            stdev = (deviations/len(sample))**(1/2)
            values = (mean, stdev)
            outDict[key] = values
    # sort the dictionary using lambda; the lambda does it first by mean, then by stdev
    sortedDict = sorted(outDict.items(), key=lambda item:(item[1][0], item[1][1]))
    return sortedDict

"""
Why would you want to play a game with rigged dice that causes you to lose all your friends?
If you wanted to do the latter you could always play Diplomacy instead, it'll tell you who is trustworthy and who isn't.
"""