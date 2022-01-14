"""
MPCS 51042 Assignment 4

Ming Liu

Problem 2

I did browse some of the posts on edstem, but did not otherwise talk to anyone.
"""

import collections
import typing

def lru_cache(func, maxsize=128):
    class LRUCache:
        """
        The LRUCache class exists just to help out with the LRU cache.

        Parameters:
        cache : OrderedDict
            The cache itself; powers the main operation. Stores things as {input, function(input)} pairs.
        storage : int
            Integer representing the maximum size.
        """
        def __init__(self, storage=128):
            """
            Constructor. Takes an optional argument for the maximum size, but is 128 if not specified.
            """
            self.cache = collections.OrderedDict()
            self.storage = storage 

        def find(self, key):
            """
            Find a specific thing in the LRU cache; returns False if what you're looking for isn't there, and the value otherwise.
            """
            if key not in self.cache:
                return False
            else:
                # move your key to the end because it was most recently searched
                self.cache.move_to_end(key)
                return self.cache[key]

        def append(self, key, value):
            """
            Adds a pair to the cache dictionary. Note that inputs are generally in {input, function(input)} pairs.
            More importantly, if the cache is too big, pops off the oldest value.
            """
            self.cache[key] = value
            # most importantly, moves it to the end so that it is the most recently accessed
            self.cache.move_to_end(key)
            # remove oldest
            if len(self.cache) > self.storage:
                self.cache.popitem(last = False)

    class CacheInfo(typing.NamedTuple):
        """
        NamedTuple with four internals, all of type int.
        """
        hits: int
        misses: int
        maxsize: int
        currsize: int

    # initialize values for the CacheInfo variables.
    CacheInfo.maxsize = maxsize
    CacheInfo.hits = 0
    CacheInfo.misses = 0
    CacheInfo.currsize = 0
    
    cache = LRUCache(maxsize)

    def inner(first, *args):
        """
        The inner function. Takes arguments and passes them to the function that was submitted earlier. Returns what it finds in the cache, if anything.
        """
        # first will always be a positional argument, but there are many optional arguments afterwards
        if cache.find(first):
            # if something was found
            # increment hits
            CacheInfo.hits += 1
            return cache.find(first)
        else: 
            # if nothing found (the search returned FALSE)
            # increment misses, and append the value, AND its function value.
            CacheInfo.misses += 1
            cache.append(first, func(first, *args))
            # increment the current size, because you only expand it if you have to.
            CacheInfo.currsize += 1
            return func(first, *args)
        
    # update the current size
    CacheInfo.currsize = len(cache.cache.keys())     

    def cacheInfo():
        """
        Returns a large string of the cache info.
        Probably unnecessary in hindsight, but useful for keeping all the code on the screen.
        """
        return "CacheInfo(hits=" + str(CacheInfo.hits) + ", misses=" + str(CacheInfo.misses) + ", maxsize=" + str(CacheInfo.maxsize) + ", currsize=" + str(CacheInfo.currsize) + ")"
    
    inner.cache_info = cacheInfo
    return inner
