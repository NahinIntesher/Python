import numpy as np # type: ignore
from queue import PriorityQueue

# Taking input from file
# ---------------------------------------------------------
adjList = {}
coOrdinates = {}
Edges = {}
# with open('input.txt', 'r') as file:
with open('D:/Visual Studio Code WorkShop/Python/Artificial Intelligence Lab/Assignment 2/input.txt', 'r') as file:
    noOfVarteices = int(file.readline())
    for i in range(noOfVarteices):
        node, x, y = file.readline().split()
        coOrdinates[node] = (int(x), int(y))
        adjList[node] = []
    
    noOfEdges = int(file.readline())
    for i in range(noOfEdges):
        u, v, cost = file.readline().split()
        Edges[(u,v)] = int(cost) # Making a Edges
        adjList[u].append((v, int(cost)))  # only for directed graph
        # adjList[v].append(u) # for undirected graph
    
    startNode = file.readline().rstrip()
    goalNode = file.readline().rstrip()
# ---------------------------------------------------------



# Debugging: Print the structures
# ---------------------------------------------------------
# print("Coordinates:", coOrdinates)
# print("Adjacency List:", adjList)
# print("Edges:", Edges)
# print("Start Node:", startNode)
# print("Goal Node:", goalNode)
# ---------------------------------------------------------




# Demo input for testing purpose only
# ---------------------------------------------------------
# coOrdinates = {
#     'S': (6, 0),
#     'A': (6, 0),
#     'B': (1, 0),
#     'C': (2, 0),
#     'D': (1, 0),
#     'G': (0, 0),
# }
# adjList = {
#     'S': [('A', 1), ('C', 2), ('D', 4)],
#     'A': [('B', 2)],
#     'B': [('A', 2), ('G', 1)],  
#     'C': [('S', 2), ('G', 4)],
#     'D': [('G', 4)],
#     'G': []
# }
# Edges = {
#     ('S', 'A'): 1,
#     ('S', 'C'): 2,
#     ('S', 'D'): 4,
#     ('A', 'B'): 2,
#     ('B', 'A'): 2,
#     ('B', 'G'): 1,
#     ('C', 'S'): 2,
#     ('C', 'G'): 4,
#     ('D', 'G'): 4
# }
# startNode = 'S'
# goalNode = 'G'
# ---------------------------------------------------------





# Euclidean function
# ---------------------------------------------------------
def euclidean(node1, node2):
    x1, y1 = coOrdinates[node1]
    x2, y2 = coOrdinates[node2]
    # return (np.sqrt((x1-x2)**2 + (y1-y2)**2))
    point1 = np.array((x1, y1))
    point2 = np.array((x2, y2))
    dist = np.linalg.norm(point1 - point2)
    # print(dist)
    return float(dist)
    # print(euclidean('A', 'D'))
# ---------------------------------------------------------


# Heuristic function
# ---------------------------------------------------------
def makeHeuristic(adjList):
    heuristic = {}
    n = len(adjList)
    for i in range(n):
        node = list(adjList.keys())[i]
        # print(node)
        m = len(adjList[node])
        for j in range(m):
            adjNode, cost = adjList[node][j]
            # print(node, adjNode)
            heuristic[node, adjNode] = euclidean(node, adjNode)
    # print(heuristic)  
    return heuristic
# ---------------------------------------------------------


# Calculate heuristic
heuristic = makeHeuristic(adjList)






# A* Search Algorithm
# --------------------------------------------------------------------------------------------------------------------
def AStarSearch(adjList, heuristic, startNode, goalNode):
    # Priority queue for the open set
    mainPQ = PriorityQueue()
    mainPQ.put((0, startNode))  # (finalCost, currentNode)
    
    visited = set() # To track visited nodes in O(1) time {list is O(n)}
    cameFrom = {} # To reconstruct the path

    # Cost from start to each node
    backwordCost = {startNode: 0}
    finalCost = {startNode: heuristic.get((startNode, goalNode), float('inf'))}
    
    while not mainPQ.empty():
        current_cost, currentNode = mainPQ.get()
        
        # Check if the goal is reached
        if currentNode == goalNode:
            # print(f"Goal Reached: {goalNode}")
            break
        
        # Check if the node is already visited
        if currentNode in visited:
            continue

        # Mark the node as visited
        visited.add(currentNode)
        
        # Explore neighbors
        for adjNode, edgeCost in adjList[currentNode]:
            if adjNode in visited:
                continue
            
            # Calculate tentative backwordCost and total cost
            tentativeBackwordCost = backwordCost[currentNode] + edgeCost
            
            # Only update if this path is better
            if tentativeBackwordCost < backwordCost.get(adjNode, float('inf')):
                cameFrom[adjNode] = currentNode
                backwordCost[adjNode] = tentativeBackwordCost
                
                # Calculate finalCost using heuristic from current node to goal
                heuristicCost = heuristic.get((adjNode, goalNode), float('inf'))
                finalCost[adjNode] = tentativeBackwordCost + heuristicCost
                
                mainPQ.put((finalCost[adjNode], adjNode))

    
    # Reconstruct the path
    path = []
    current = goalNode
    while current in cameFrom:
        path.append(current)
        current = cameFrom[current]
    path.append(startNode)
    path.reverse()
    
    return path, backwordCost[goalNode] if goalNode in backwordCost else float('inf')
# --------------------------------------------------------------------------------------------------------------------





# Main execution
# ---------------------------------------------------------
path, solutionCost = AStarSearch(adjList, heuristic, startNode, goalNode)
    
print("Solution Path:", " - ".join(path))
print("Solution Cost:", solutionCost)
# ---------------------------------------------------------