import math

# Function to calculate Euclidean distance for heuristics
def euclidean_distance(coord1, coord2):
    return math.sqrt((coord1[0] - coord2[0])**2 + (coord1[1] - coord2[1])**2)

# Reading input from file
adjList = {}
coOrdinates = {}
Edges = {}
heuristic = {}

with open('/Artificial Intelligence Lab/Assignment 2/input.txt', 'r') as file:
    # Number of vertices
    noOfVertices = int(file.readline().strip())
    
    # Reading coordinates
    for _ in range(noOfVertices):
        node, x, y = file.readline().split()
        coOrdinates[node] = (int(x), int(y))
        adjList[node] = []

    # Number of edges
    noOfEdges = int(file.readline().strip())
    
    # Reading edges
    for _ in range(noOfEdges):
        u, v, cost = file.readline().split()
        cost = int(cost)
        Edges[(u, v)] = cost  # Directed graph
        adjList[u].append((v, cost))

        # Uncomment below for undirected graph
        # Edges[(v, u)] = cost
        # adjList[v].append((u, cost))

    # Start and goal nodes
    startNode = file.readline().strip()
    goalNode = file.readline().strip()

# Calculating heuristic based on Euclidean distance
for u in coOrdinates:
    for v in coOrdinates:
        if u != v:  # Avoid self-loops
            heuristic[(u, v)] = euclidean_distance(coOrdinates[u], coOrdinates[v])

# Debugging: Print the structures
print("Coordinates:", coOrdinates)
print("Adjacency List:", adjList)
print("Edges:", Edges)
print("Heuristic:", heuristic)
print("Start Node:", startNode)
print("Goal Node:", goalNode)