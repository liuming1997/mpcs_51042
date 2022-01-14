"""
MPCS 51042 Assignment 1
Problem 1
Ming Liu
"""

def isect(s1, s2):
    """
    Function that takes in two string inputs, s1 and s2, assuming they are comma-separated integers.
    This function then finds the unique integers that appear in BOTH s1 and s2, and contains the digit 2 in them, WITHOUT duplicates.
    It then returns a sorted list of integers.
    """
    # here we construct two lists that hold the splits of s1 and s2
    # normally I would have some input checking code, but it has been stated that such code to validate input is NOT needed
    list1 = s1.split(",")
    list2 = s2.split(",")
    # find out which ones have the digit '2' in them AND appear in the OTHER list
    # then convert them to integers and place them in new lists
    filtered1 = []
    filtered2 = []
    for i in list1:
        if "2" in i and i in list2:
            filtered1.append(int(i))
    for j in list2:
        if "2" in j and i in list1:
            filtered2.append(int(j))
    # not strictly necessary but good for memory
    del list1, list2
    # remove repeats
    # you can iterate through a list, or you can go from list to dictionary since dictionaries can't have duplicate keys
    # and then convert it back to a list
    # reference: https://docs.python.org/3/library/stdtypes.html#dict.fromkeys and https://docs.python.org/3/tutorial/datastructures.html
    # specifically when they talk about performing list() on a dictionary
    # as the reference document implies, doing what I did on dict.fromkeys() is almost certainly not intended behavior, but it works
    filtered1 = list(dict.fromkeys(filtered1))
    filtered2 = list(dict.fromkeys(filtered2))
    # construct one more list, the common list
    # find out which ones appear in both lists
    commonList = []
    for a in filtered1:
        if a in filtered2:
            commonList.append(a)
    commonList.sort()
    return commonList

"""
Test code below
"""

# def main():
#     print(isect("3,123,201,10,12,20", "20,3,201,124,0,12"))
#     print(isect("3,123,201,12,20", "20,3,201,124,0,12"))
#     print(isect("3,123,201,10,12,20", "20,201,124,0,12"))
#     print(isect("3,10,12,20,-4,20", "20,3,12,0,12"))
#     print(isect("3,10,12", "20,3,0"))
#     print(isect("20,12,20,201", "201,20,20,12"))

# if __name__ == "__main__":
#     main()