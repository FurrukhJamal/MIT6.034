# Fall 2012 6.034 Lab 2: Search
#
# Your answers for the true and false questions will be in the following form.  
# Your answers will look like one of the two below:
#ANSWER1 = True
#ANSWER1 = False

# 1: True or false - Hill Climbing search is guaranteed to find a solution
#    if there is a solution
ANSWER1 = False

# 2: True or false - Best-first search will give an optimal search result
#    (shortest path length).
#    (If you don't know what we mean by best-first search, refer to
#     http://courses.csail.mit.edu/6.034f/ai3/ch4.pdf (page 13 of the pdf).)
ANSWER2 = False

# 3: True or false - Best-first search and hill climbing make use of
#    heuristic values of nodes.
ANSWER3 = True

# 4: True or false - A* uses an extended-nodes set.
ANSWER4 = True

# 5: True or false - Breadth first search is guaranteed to return a path
#    with the shortest number of nodes.
ANSWER5 = True 

# 6: True or false - The regular branch and bound uses heuristic values
#    to speed up the search for an optimal path.
ANSWER6 = False 

# Import the Graph data structure from 'search.py'
# Refer to search.py for documentation
from search import Graph

## Optional Warm-up: BFS and DFS
# If you implement these, the offline tester will test them.
# If you don't, it won't.
# The online tester will not test them.

from copy import deepcopy

class Node(object):
    def __init__(self, name, parent = None):
        self.name = name
        self.parent = parent
    
    def __eq__(self,other):
        return self.name == other.name 

    
    
    def __hash__(self):
        return hash(self.name)
    
    def __repr__(self):
        return "Node : " + self.name
    


class Path():
    def __init__(self, node):
        if type(node) == list:
            self.path = node 
        else:
            self.path = [node]
        self.length = 0
    def addNode(self, node, length):
        self.path.append(node)
        self.length += length
    def getPath(self):
        return self.path
    def getLastNode(self):
        return self.path[-1]
    def getPathLength(self):
        return self.length
    def __eq__(self, other):
        return self.length == other.length
    def __lt__(self, other):
        return self.length < other.length
    def __gt__(self,other):
        return self.length > other.length
    def __repr__(self):
        return f"path : {self.path} len : {self.length}"

class APath(Path):
    def __init__(self, node, heuristic):
        super().__init__(node)
        self.heuristicEstimate = self.length + heuristic

    def addNode(self, node, length, heuristic):
        self.path.append(node)
        self.length += length
        self.heuristicEstimate = self.length + heuristic 
        
    
    def __eq__(self, other):
        return self.heuristicEstimate == other.heuristicEstimate
    def __lt__(self, other):
        return self.heuristicEstimate < other.heuristicEstimate
    def __gt__(self,other):
        return self.heuristicEstimate > other.heuristicEstimate
    def __repr__(self):
        return f"path : {self.path} heuristicestimate : {self.heuristicEstimate}" 

class BeamPath(Path):
    def __init__(self, node, heuristic):
        if type(node) == list:
            self.path = node 
        else:
            self.path = [node]
        self.length = heuristic

    def addNode(self, node, heuristic):
        self.path.append(node)
        self.length = heuristic 





def bfs(graph, start, goal):
    # raise NotImplementedError
    # print(f"nodes : {graph.nodes}")
    # print(f"start : {start}")
    if start == goal:
        return[start]

    agenda = []
    # agenda.append(start)
    neighbors = graph.get_connected_nodes(start)
    start = Node(start)
    
    for neighbor in neighbors:
        agenda.insert(0, Node(neighbor, start))
    # print(f"agenda : {agenda}")
    
    explored = set()
    explored.add(start)
    targetNode = None
    
    while len(agenda) != 0:
        u = agenda.pop()
        
        if u.name == goal:
            # print(f"found the goal")
            # targetNode = Node(goal, start)
            targetNode = u
            break 
        for neighbor in graph.get_connected_nodes(u.name):
            if Node(neighbor, u) not in explored:
                
                agenda.insert(0, Node(neighbor, u))
        explored.add(u)
        start = u

    result = []
    result.append(targetNode.name)
    parent = targetNode.parent
    # print(f"parent : {parent}")
    while parent:
        # print(f"parent at start of while : {parent}")
        result.append(parent.name)
        parent = parent.parent
        # print(f"parent at end of while : {parent}")
    result.reverse()
    print(f"result : {result}")
    return result 

## Once you have completed the breadth-first search,
## this part should be very simple to complete.
def dfs(graph, start, goal):
    if start == goal:
        return [start]
    
    agenda = []

    neighbors = graph.get_connected_nodes(start)
    start = Node(start)
    
    for neighbor in neighbors:
        agenda.append(Node(neighbor, start))
    # print(f"agenda : {agenda}")
    
    explored = set()
    explored.add(start)
    targetNode = None
    
    while len(agenda) != 0:
        u = agenda.pop()
        
        if u.name == goal:
            # print(f"found the goal")
            # targetNode = Node(goal, start)
            targetNode = u
            break 
        for neighbor in graph.get_connected_nodes(u.name):
            if Node(neighbor, u) not in explored:
                
                agenda.append(Node(neighbor, u))
        explored.add(u)
        start = u

    result = []
    result.append(targetNode.name)
    parent = targetNode.parent
    # print(f"parent : {parent}")
    while parent:
        # print(f"parent at start of while : {parent}")
        result.append(parent.name)
        parent = parent.parent
        # print(f"parent at end of while : {parent}")
    result.reverse()
    # print(f"result : {result}")
    # print(f"is_valid_path(self, path) : {graph.is_valid_path(result)}")
    return result
    


## Now we're going to add some heuristics into the search.  
## Remember that hill-climbing is a modified version of depth-first search.
## Search direction should be towards lower heuristic values to the goal.
def hill_climbing(graph, start, goal):
    if start == goal:
        return [start]
    
    agenda = []

    neighbors = graph.get_connected_nodes(start)
    start = Node(start)
    
    for neighbor in neighbors:
        agenda.append(Node(neighbor, start))
    # print(f"agenda : {agenda}")
    
    #sorting acording to heuristics
    heuristics = {}
    for node in agenda:
        heuristics[node] = graph.get_heuristic(node.name, goal)
    agenda = sorted(heuristics, key = heuristics.get, reverse = True)
    

    explored = set()
    explored.add(start)
    # targetNode = Node(None)
    targetNode = None
    
    while len(agenda) != 0:
        u = agenda.pop()
        # print(f"u at start of while : {u}")
        # print(f"its parent : {u.parent}")
        # print(f"explored at the start of while : {explored}")
        # # print(f"agenda at the start : {agenda}")
        if u.name == goal:
            # print(f"found the goal")
            # targetNode = Node(goal, start)
            targetNode = u
            # print(f"targetNode : {targetNode}")
            # print(f"targetNode.parent: {targetNode.parent}")
            break 
        # print(f"{u}'s children {graph.get_connected_nodes(u.name)}")
        adjacentNeighbors = []
        for neighbor in graph.get_connected_nodes(u.name):
            
            if Node(neighbor, u) not in explored:
                print(f"creating node for : {neighbor}")
                adjacentNeighbors.append(Node(neighbor, u))
        # print(f"adjacentNeighbors : {adjacentNeighbors}")   
        #sorting acording to heuristics
        
        heuristics = {}
        for node in adjacentNeighbors:
            heuristics[node] = graph.get_heuristic(node.name, goal)
        # print(f"heuristics : {heuristics}")
        adjacentNeighbors = sorted(heuristics, key = heuristics.get, reverse = True)
        agenda += adjacentNeighbors
        
        # print(f"agenda in while loop : {agenda}\n")

        explored.add(u)
        start = u
    
    
    
    result = []
    # try :
    #     result.append(targetNode.name)
    #     parent = targetNode.parent
    #     while parent:
    #         result.append(parent.name)
    #         parent = parent.parent
    #     result.reverse()
    #     return result
    # except AttributeError :
    #     return result
    result.append(targetNode.name)
    parent = targetNode.parent
    # print(f"parent : {parent}")
    while parent:
        # print(f"parent at start of while : {parent}")
        result.append(parent.name)
        parent = parent.parent
        # print(f"parent at end of while : {parent}")
    result.reverse()
    # print(f"result : {result}")
    # print(f"is_valid_path(self, path) : {graph.is_valid_path(result)}")
    return result
    

## Now we're going to implement beam search, a variation on BFS
## that caps the amount of memory used to store paths.  Remember,
## we maintain only k candidate paths of length n in our agenda at any time.
## The k top candidates are to be determined using the 
## graph get_heuristic function, with lower values being better values.
def beam_search(graph, start, goal, beam_width):
    # print(f"start : {start}, goal : {goal}")
    # print(f"beam width : {beam_width}")
    if start == goal :
        return [start]
    path = BeamPath(start, graph.get_heuristic(start, goal))
    q = []
    q.insert(0, [path])
    explored = set()
    counter = 0
    while len(q) != 0:
        paths = q.pop()
        # print(f"paths : {paths}")
        if len(paths) == 0:
            break
        nextLevelPaths = []
        for path in paths:
            lastNode = path.getLastNode()
            if lastNode == goal:
                return path.getPath()
            neighbors = graph.get_connected_nodes(lastNode)
            neighborsOfSingleNode = []
            for neighbor in neighbors:
                if neighbor not in explored:
                    h = graph.get_heuristic(neighbor, goal)
                    newPath = deepcopy(path)
                    newPath.addNode(neighbor, h)
                    neighborsOfSingleNode.append(newPath)
            explored.add(lastNode)
            for val in neighborsOfSingleNode:
                nextLevelPaths.append(val)
        nextLevelPaths = sorted(nextLevelPaths)
        nextLevelPaths = nextLevelPaths[: beam_width]
        q.append(nextLevelPaths)
        counter += 1
        # if counter == 5:
        #     break
    return []
        
        




    

## Now we're going to try optimal search.  The previous searches haven't
## used edge distances in the calculation.

## This function takes in a graph and a list of node names, and returns
## the sum of edge lengths along the path -- the total distance in the path.
def path_length(graph, node_names):
    length = 0
    if len(node_names) == 1:
        return length
    
    for nodeIndex in range(len(node_names) - 1):
        edge = graph.get_edge(node_names[nodeIndex], node_names[nodeIndex + 1])
        length += edge.length
    return length 



def branch_and_bound(graph, start, goal):
    path = Path(start)
    q = []
    q.append(path)
    explored = set()
    counter = 0
    while len(q) != 0:
        u = q.pop()
        # print(f"u : {u}")
        lastNode = u.getLastNode()
        # print(f"lastNode : {lastNode}")
        if lastNode == goal:
            return u.getPath()
        
        neighbors = graph.get_connected_nodes(lastNode)
        # print(f"neighbors : {neighbors}")
        # print(f"explored : {explored}")
        for neighbor in neighbors:
            if neighbor not in explored:
                edgeWeight = graph.get_edge(lastNode, neighbor).length
                path = deepcopy(u)
                path.addNode(neighbor, edgeWeight)
                # print(f"path added : {path}")
                q.append(path)
        explored.add(lastNode)
        q = sorted(q, reverse = True)
        # print(f"q at the end: {q}\n")
        # counter += 1
        # if counter == 5:
        #     break
    return []



def a_star(graph, start, goal):
    # print(f"start : {start} goal : {goal}")
    # print(f"graph : {graph}")
    path = APath(start, graph.get_heuristic(start, goal))
    q = []
    q.append(path)
    explored = set()
    counter = 0
    while len(q) != 0:
        u = q.pop()
        # print(f"u : {u}")
        lastNode = u.getLastNode()
        # print(f"lastNode : {lastNode}")
        if lastNode == goal:
            return u.getPath()
        
        neighbors = graph.get_connected_nodes(lastNode)
        # print(f"neighbors : {neighbors}")
        # print(f"explored : {explored}")
        for neighbor in neighbors:
            if neighbor not in explored:
                edgeWeight = graph.get_edge(lastNode, neighbor).length
                path = deepcopy(u)
                path.addNode(neighbor, edgeWeight, graph.get_heuristic(neighbor, goal))
                # print(f"path added : {path}")
                q.append(path)
        explored.add(lastNode)
        q = sorted(q, reverse = True)
        # print(f"q at the end: {q}\n")
        
    return [""]

    # raise NotImplementedError


def getshortestPathLength(graph, start, goal):
    # print(f"start : {start} goal : {goal}")
    # print(f"graph : {graph}")
    path = APath(start, graph.get_heuristic(start, goal))
    q = []
    q.append(path)
    explored = set()
    counter = 0
    while len(q) != 0:
        u = q.pop()
        # print(f"u : {u}")
        lastNode = u.getLastNode()
        # print(f"lastNode : {lastNode}")
        if lastNode == goal:
            return u.getPathLength()
        
        neighbors = graph.get_connected_nodes(lastNode)
        # print(f"neighbors : {neighbors}")
        # print(f"explored : {explored}")
        for neighbor in neighbors:
            if neighbor not in explored:
                edgeWeight = graph.get_edge(lastNode, neighbor).length
                path = deepcopy(u)
                path.addNode(neighbor, edgeWeight, graph.get_heuristic(neighbor, goal))
                # print(f"path added : {path}")
                q.append(path)
        explored.add(lastNode)
        q = sorted(q, reverse = True)
        # print(f"q at the end: {q}\n")
        # counter += 1
        # if counter == 5:
        #     break
    return []



## It's useful to determine if a graph has a consistent and admissible
## heuristic.  You've seen graphs with heuristics that are
## admissible, but not consistent.  Have you seen any graphs that are
## consistent, but not admissible?

def is_admissible(graph, goal):
    
    for node in graph.nodes:
        sLength = getshortestPathLength(graph, node, goal)
        if graph.get_heuristic(node, goal) > sLength:
            return False
    return True

def is_consistent(graph, goal):
    for node1 in graph.nodes:
        for node2 in graph.nodes:
            edge = graph.get_edge(node1, node2)
            if  edge != None:
                heuristicDiff = abs(graph.get_heuristic(node1, goal) - graph.get_heuristic(node2, goal))
                if edge.length < heuristicDiff:
                    return False
    return True 

HOW_MANY_HOURS_THIS_PSET_TOOK = 'more than 5 days'
WHAT_I_FOUND_INTERESTING = 'the inner workings of all the searches'
WHAT_I_FOUND_BORING = 'the debugging'

 


if __name__ == "__main__":
    from search import Graph, Edge
    testGraph = Graph(["A", "B", "C", "D", "E", "F" , "G", "S"])
    testGraph.add_edge("S", "A", 3)
    testGraph.add_edge("S", "D", 4)
    testGraph.add_edge("A", "B", 4)
    testGraph.add_edge("A", "D", 5)
    # testGraph.add_edge("D", "A", 5)
    testGraph.add_edge("D", "E", 2)
    testGraph.add_edge("E", "B", 5)
    testGraph.add_edge("E", "F", 4)
    testGraph.add_edge("B", "C", 4)
    # testGraph.add_edge("B", "E", 5)
    # testGraph.add_edge("D", "E", 2)
    testGraph.add_edge("F", "G", 3)

    pathA = Path("S")
    pathB = Path("S")
    pathA.addNode("A", 4)
    pathB.addNode("B", 6)

    test = [pathA, pathB]
    test = sorted(test, reverse= True)
    print(test)

    branch_and_bound(testGraph, "S", "G")
    print(f" path length : {getshortestPathLength(testGraph, 'S', 'G')}")
    print(f"nodes : {testGraph.nodes}")
    print(f"testing edge : {testGraph.get_edge('S', 'A')}")
    print(f"testing edge : {testGraph.get_edge('S', 'S')}")

    print(f"debugging Astar...\n")
    NEWGRAPH4 = Graph(nodes=["S","A", "B", "C", "D", "E", "F", "H", "J", "K",
            "L", "T" ],
                 edgesdict = [{ 'NAME': 'eSA', 'LENGTH': 2, 'NODE1': 'S', 'NODE2': 'A' },
              { 'NAME': 'eSB', 'LENGTH': 10, 'NODE1': 'S', 'NODE2':'B' },
              { 'NAME': 'eBC', 'LENGTH': 5, 'NODE1': 'B', 'NODE2':'C' },
              { 'NAME': 'eBF', 'LENGTH': 2, 'NODE1': 'B', 'NODE2':'F' },
              { 'NAME': 'eCE', 'LENGTH': 5, 'NODE1': 'C', 'NODE2':'E' },
              { 'NAME': 'eCJ', 'LENGTH': 12, 'NODE1': 'C', 'NODE2':'J' },
              { 'NAME': 'eFH', 'LENGTH': 8, 'NODE1': 'F', 'NODE2':'H' },
              { 'NAME': 'eHD', 'LENGTH': 3, 'NODE1': 'H', 'NODE2':'D' },
              { 'NAME': 'eHK', 'LENGTH': 5, 'NODE1': 'H', 'NODE2':'K' },
              { 'NAME': 'eKJ', 'LENGTH': 1, 'NODE1': 'K', 'NODE2':'J' },
              { 'NAME': 'eJL', 'LENGTH': 4, 'NODE1': 'J', 'NODE2':'L' },
              { 'NAME': 'eKT', 'LENGTH': 7, 'NODE1': 'K', 'NODE2':'T' },
              { 'NAME': 'eLT', 'LENGTH': 5, 'NODE1': 'L', 'NODE2':'T' },
              ],
                 heuristic={"T":{'S': 10,
                                 'A': 6,
                                 'B': 5,
                                 'C': 2,
                                 'D': 5,
                                 'E': 1,
                                 'F': 100,
                                 'H': 2,
                                 'J': 3,
                                 'K': 100,
                                 'L': 4,
                                 'T': 0,}})
    print(f"test result : {a_star(NEWGRAPH4, 'S', 'T')}")
    print(f"should be : {list('SBCJLT')}")

    NEWGRAPH1 = Graph(edgesdict=[ 
        { 'NAME': 'e1',  'LENGTH':  6, 'NODE1': 'S', 'NODE2': 'A' },
        { 'NAME': 'e2',  'LENGTH':  4, 'NODE1': 'A', 'NODE2': 'B' },
        { 'NAME': 'e3',  'LENGTH':  7, 'NODE1': 'B', 'NODE2': 'F' },
        { 'NAME': 'e4',  'LENGTH':  6, 'NODE1': 'C', 'NODE2': 'D' },
        { 'NAME': 'e5',  'LENGTH':  3, 'NODE1': 'C', 'NODE2': 'A' },
        { 'NAME': 'e6',  'LENGTH':  7, 'NODE1': 'E', 'NODE2': 'D' },
        { 'NAME': 'e7',  'LENGTH':  6, 'NODE1': 'D', 'NODE2': 'H' },
        { 'NAME': 'e8',  'LENGTH':  2, 'NODE1': 'S', 'NODE2': 'C' },
        { 'NAME': 'e9',  'LENGTH':  2, 'NODE1': 'B', 'NODE2': 'D' },
        { 'NAME': 'e10', 'LENGTH': 25, 'NODE1': 'E', 'NODE2': 'G' },
        { 'NAME': 'e11', 'LENGTH':  5, 'NODE1': 'E', 'NODE2': 'C' } ],
                  heuristic={"G":{'S': 11,
                                  'A': 9,
                                  'B': 6,
                                  'C': 12,
                                  'D': 8,
                                  'E': 15,
                                  'F': 1,
                                  'H': 2},
                             "H":{'S': 11,
                                  'A': 9,
                                  'B': 6,
                                  'D': 12,
                                  'E': 8,
                                  'F': 15,
                                  'G': 14},
                             'A':{'S':5, # admissible
                                  "B":1, # h(d) > h(b)+c(d->b) ...  6 > 1 + 2
                                  "C":3,
                                  "D":6,
                                  "E":8,
                                  "F":11,
                                  "G":33,
                                  "H":12},
                             'C':{"S":2, # consistent
                                  "A":3,
                                  "B":7,
                                  "D":6,
                                  "E":5,
                                  "F":14,
                                  "G":30,
                                  "H":12},
                             "D":{"D":3}, # dumb
                             "E":{} # empty
                             })

    
    
    print(f"Debugging beam search\n")
    print(f"test result : {beam_search(NEWGRAPH1, 'F', 'G', 2)}")
    print(f"should have been : {list('FBASCEG')}")

    # print(f"test result : {beam_search(NEWGRAPH1, 'S', 'G', 2)}")
    # print(f"should be : []")    