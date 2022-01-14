"""
MPCS 51042 Assignment 2
Ming Liu
"""

# Problem 2

from os import sep


def fill_completions(fileName):
    """
    Takes in an article and attempts to populate a dictionary of completions.
    """
    completions = {}
    with open(fileName, 'r', encoding='utf-8') as file:
        rawFile = file.read()
    # split off the words
    rawList = rawFile.split()
    wordList = []
    for i in rawList:
        # convert words to lowercase and check for alphanumeric only
        i = i.lower()
        if i.isalpha():
            wordList.append(i)
    for j in wordList:
        index = 0
        for k in j:
            try:
                completions[(index, k)].add(j)
                index += 1
            except:
                completions[(index, k)] = set()
                completions[(index, k)].add(j)
                index += 1
    return completions

def find_completions(prefix, c_dict):
    """
    Take in a prefix and the completion dictionary and returns the set of all possible words.
    """
    # list of all possible matches
    matches = []
    index = 0
    for i in prefix:
        if index == 0:
            search = c_dict.get((index, i))
            # set of all possible matches
            filterSet = set(search)
            for j in filterSet:
                matches.append(j)
            index += 1
        else:
            # now we take the nth letter in the word
            search = c_dict.get((index,i))
            # tempList is a list of all the words in matches that are also in the new search term
            tempList = []
            # edge cases for if you index out of bounds
            if search == None:
                matches = []
            else:
                filterSet = set(search)
                for j in matches:
                    if j in search:
                        tempList.append(j)
                    # we set matches to tempList now to filter it down
                    matches = tempList
            index += 1
    return set(matches)

def main():
    mainDict = fill_completions("articles.txt")
    keepRunning = True
    while keepRunning:
        query = input("Prefix: ")
        # I feel like this is not a great implementation. What if the user wants to search for 'quit'?
        if query.lower() == "quit":
            break
        else:
            possibleCompletions =  find_completions(query.lower(), mainDict)
            if len(possibleCompletions) == 0:
                print("No completions are possible.")
            else:
                possibleCompletions = sorted(possibleCompletions)
                for i in possibleCompletions:
                    print(i)

if __name__ == '__main__':
    main()
