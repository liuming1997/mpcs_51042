"""
MPCS 51042 Homework 5: Graphs

Ming Liu

For your consideration:
Node: a string object denoting the name of a node
Edge: a list of two nodes (that the edge connects)

Graph: a dictionary object with keys corresponding to nodes, and values corresponding to their neighborhood
"""

import unittest
from graph import Graph

"""
The Graph constructor has been called in three different ways, so all tests are in triplicate. Any test with a "2" or a "3" behind its name does the same thing as "test1", 
but just for a different Graph object.
"""

# first one: fiddle with the Graph object's internal dictionary
test1 = Graph()
test1.graph = {
    "1": set(["2", "5"]),
    "2": set(["1", "3", "5"]),
    "3": set(["2", "4"]),
    "4": set(["3", "5", "6"]),
    "5": set(["1", "2", "4"]),
    "6": set(["4"])
}

# should be the same thing, but by calling a list of the edges in a constructor
test2 = Graph([["1", "2"], ["1", "5"], ["2", "5"], ["2", "3"], ["3", "4"], ["4", "5"], ["4", "6"]])

# another check, calling all of the add functions
test3 = Graph()
test3.add_node("1")
test3.add_node("2")
test3.add_node("3")
test3.add_node("4")
test3.add_node("5")
test3.add_node("6")
test3.add_edge(["1", "2"])
test3.add_edge(["1", "5"])
test3.add_edge(["2", "5"])
test3.add_edge(["2", "3"])
test3.add_edge(["3", "4"])
test3.add_edge(["4", "5"])
test3.add_edge(["4", "6"])

class Test(unittest.TestCase):
    global test1
    global test2
    global test3

    # "7" is a node that does not exist.

    def test_sanityCheck1(self):
        """
        A very, very basic sanity check just to make sure that the in operator works properly.
        """
        assert("7" not in test1.graph)
        assert("1" in test1.graph)
    def test_sanityCheck2(self):
        assert("7" not in test2.graph)
        assert("1" in test2.graph)
    def test_sanityCheck3(self):
        assert("7" not in test3.graph)
        assert("1" in test3.graph)
    
    def test_getitem1(self):
        """
        Tests __getitem__ to make sure subscripting works, and that if the item does not actually exist, returns None instead.
        """
        assert(test1["1"] == set(["2", "5"]))
        assert(test1["7"] == None)
    def test_getitem2(self):
        assert(test2["3"] == set(["2", "4"]))
        assert(test2["8"] == None)
    def test_getitem3(self):
        assert(test3["6"] == set(["4"]))
        assert(test3["4"] == set(["3", "5", "6"]))
        assert(test3["9"] == None)
    
    def test_iter1(self):
        """
        Tests that iterables work. Fairly straightforwards.
        """
        test1_dummy = []
        for a in test1:
            test1_dummy.append(a)
        assert(sorted(test1_dummy) == ["1", "2", "3", "4", "5", "6"])
    def test_iter2(self):
        test2_dummy = []
        for b in test2:
            test2_dummy.append(str(int(b)-1))
        assert(sorted(test2_dummy) == ["0", "1", "2", "3", "4", "5"])
    def test_iter3(self):
        test3_dummy = []
        for c in test3:
            test3_dummy.append(int(c))
        assert(sorted(test3_dummy) == [1, 2, 3, 4, 5, 6])

    def test_distance1(self):
        """
        Tests that the distance function correctly returns the distance between two points, and that None is returned if one of the two points does not exist.
        """
        assert(test1.distance("1", "4") == 2)
        assert(test1.distance("1", "7") == None)
    def test_distance2(self):
        assert(test2.distance("1", "6") == 3)
        assert(test2.distance("9", "8") == None)
    def test_distance3(self):
        assert(test3.distance("3", "4") == 1)
        assert(test3.distance("5", "9") == None)

    def test_addnode1(self):
        """
        Tests whether or not adding nodes works. If the node already exists, return False; if it does not, return True.
        """
        assert(test1.add_node("1") == False)
        # add a node
        assert(test1.add_node("foo") == True)
        # remove it
        test1.graph.pop("foo")
    def test_addnode2(self):
        assert(test2.add_node("3") == False)
    def test_addnode3(self):
        assert(test3.add_node("4") == False)

    def test_addedge1(self):
        """
        Tests:
        adding an existing edge just fails silently since it's not needed
        adding a new edge returns True
        adding an edge with nodes that do not exist returns False
        """
        assert(test1.add_edge(["1", "2"]) == True)
    def test_addedge2(self):
        # add the node back
        assert(test2.add_node("foo") == True)
        assert(test2.add_edge(["1", "foo"]) == True)
        assert(test2.distance("1", "foo") == 1)
        test2.graph.pop("foo")
    def test_addedge3(self):
        assert(test3.add_edge(["foo", "bar"]) == False)

    def test_bfs1(self):
        """
        Tests that the breadth-first search correctly gives a dictionary of nodes other than the starting node and their shortest distances,
        and that None is returned if the starting node does not actually exist.
        """
        assert(test1.bfs("1") == {'2': 1, '3': 2, '4': 2, '5': 1, '6': 3})
    def test_bfs2(self):
        assert(test2.bfs("7") == None)
    def test_bfs(self):
        assert(test3.bfs("4") == {'1': 2, '2': 2, '3': 1, '5': 1, '6': 1})
    

if __name__ == '__main__':
    unittest.main()