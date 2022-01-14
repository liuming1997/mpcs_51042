"""
MPCS 51042 Assignment 1
Problem 2
Ming Liu
"""

def expand(rng):
    """
    Takes a string, separated by commas, of values and ranges. Expands the ranges to [a,b), keeps the values, returns a sorted list without duplicates.
    """
    # basic typechecking
    if type(rng) != str:
        print("Invalid input. You did not enter a string.")
        return None
    else:
        values = rng.split(",")
        # construct master list
        completeList = []
        for i in values:
            if "-" not in i:
                # add to the master list if i is not a range
                completeList.append(int(i))
            else:
                # create the range and add i to the master list if it is a range
                # give an error and stop execution if it doesn't work for whatever reason
                try:
                    temp = i.split("-")
                    for j in range(int(temp[0]), int(temp[1])):
                        completeList.append(j)
                except:
                    print("Syntax error: ", i, " is not a valid range.")
                    break
        # calling sorted() instead of list() automatically returns a sorted list
        # doing the same convert-to-dictionary-and-back approach to removing duplicates from a list
        completeList = sorted(dict.fromkeys(completeList))
        return completeList

"""
Test code
"""

# def main():
#     print(expand("1,2-5,5,6-10"))
#     print(expand("6-10,1,2-5,5"))
#     print(expand("1,2-6,5,6-10"))
#     print(expand("1,2-6,5-10"))

# if __name__ == "__main__":
#     main()