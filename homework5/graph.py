"""
MPCS 51042 Homework 5: Graphs

Ming Liu

For your consideration:
Node: a string object denoting the name of a node
Edge: a list of two nodes (that the edge connects)

Graph: a dictionary object with keys corresponding to nodes, and values corresponding to their neighborhood
"""

class Graph:
    """
    The main Graph class, handles everything. Originally there was supposed to be a Node class with parameters for the name of the node and its personal adjacency list,
    but time considerations made me cut that short.
    """
    def __init__(self, edges: list = None):
        """
        Constructs the Graph object. It may take in a list of edges, or it may not. If no list is given, creates an empty graph.
        If a list is given, for each pair of nodes in the list of edges, appends the node(s) if not already present.
        This is the only time that an edge operation can add a node (see add_edge() for details about the latter).

        Parameters:
        edges: list of edges (list of lists, with each sublist having two elements)
        """
        # create a dictionary with node: neighbors
        self.graph = dict()
        if edges == None:
            pass
        else:
            for pair in edges:
                first = pair[0]
                second = pair[1]
                if first not in self.graph.keys():
                    Graph.add_node(self, first)
                if second not in self.graph.keys():
                    Graph.add_node(self, second)
                Graph.add_edge(self, pair)

    def add_node(self, node: str):
        """
        Adds a new node to the graph.
        Note: DOES NOT automatically connect nodes. Use add_edge() for that.

        Parameters:
        node: string input with the name of a new node

        Returns:
        True if the node was successfully added.
        False if the node is already existing, and thus pointless to add.
        """
        # set node to a string, if it isn't already
        node = str(node)
        if node not in self.graph.keys():
            self.graph[node] = set()
            return True
        else:
            return False

    def add_edge(self, edge: list):
        """
        Adds an edge to the graph. Only returns False if unsuccessful.
        Note: add_edge() will NOT add an edge if the node(s) do not exist already; add them with add_node().

        Parameters:
        edge: list of two nodes, which may or may not be in the graph

        Returns:
        True if both nodes in edge are in the graph
        """
        first = edge[0]
        second = edge[1]
        if first in self.graph.keys() and second in self.graph.keys():
            # since these are sets, adding them if they already exist just does a whole lot of nothing in particular
            self.graph[first].add(second)
            self.graph[second].add(first)
            return True
        else:
            return False

    def bfs(self, node: str):
        """
        Breadth-first search, taking in a node and returning a collection of other nodes and the distances to those nodes.

        Parameters:
        A string name of a node that you'd like to find the distances to.

        Returns:
        a dictionary, with keys equal to the other nodes and values equal to the distances from the input node, or None, if you entered an invalid node.
        """
        if node not in self.graph.keys():
            return None
        else:
            distances = {}
            queue = []
            queue.append(node)
            search = list(self.graph.keys())
            search.remove(node)
            for query in search:
                distances[query] = Graph.distance(self, node, query)
            return distances

    def distance(self, start: str, end: str):
        """
        I had some trouble getting looping in BFS to work correctly, and I blame the lack of coffee for this. So instead BFS calls this repeatedly instead of something
        far more elegant.

        Parameters:
        start: the starting node you'd like to use
        end: the ending node you'd like to see the path for

        Returns:
        an integer distance between the two nodes, or None if there is not a node with that name
        """
        if start not in self.graph.keys() or end not in self.graph.keys():
            return None
        else:
            queue = []
            # push the first path into the queue
            queue.append([start])
            while queue:
                # get the first path
                path = queue.pop(0)
                # get the last node
                node = path[-1]
                # if path found
                if node == end:
                    # subtract 1 because path includes the node of origin
                    return len(path) - 1
                # otherwise find all adjacent nodes, and try again
                for adjacent in self.graph.get(node, []):
                    path2 = list(path)
                    path2.append(adjacent)
                    queue.append(path2)

    def __iter__(self):
        """
        Function that returns out the list of all nodes, as a list.

        Returns:
        a list of all the nodes in the graph
        """
        return iter(self.graph.keys())

    def __getitem__(self, node: str):
        """
        Function that searches the Graph object (or its internal dictionary) for a node. If nonexistent, returns None. Otherwise, returns the adjacency list of the node.
        """
        return self.graph.get(node, None)

    def __contains__(self, node: str):
        """
        Function that returns whether or not a given node name is in the graph.

        Parameters:

        """
        search = self.graph.get(node, False)
        if search:
            return True
        else:
            return False
