import itertools

list1 = [10]
list2 = [1, 11]

list3 = []
if len(list1) == 1:
    for i in list2:
        list3.append(list1[0] + i)
else:
    for thing in itertools.permutations(list1, len(list2)):
        zipped = zip(thing, list2)
        list3.append(list(zipped))
# filter out list to only unique elements


print(list3)

list1 = [7, 17]
list2 = [1, 11]

list3 = []

if len(list1) == 1:
    for i in list2:
        list3.append(list1[0] + i)
else:
    for thing in itertools.permutations(list1, len(list2)):
        zipped = zip(thing, list2)
        list3.append(list(zipped))
# filter out list to only unique elements

print(list3)