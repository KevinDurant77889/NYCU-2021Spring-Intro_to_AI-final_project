from utils import getEdgeData

class PriorityQueue:
    def __init__(self):
        self.items = []

    def isEmpty(self):
        return self.items == []

    def push(self, item):
        # item: 2-tuple (node ID, total cost)
        self.items.insert(0, item)
    
    def pop(self):
        # Always return the node with minimum cost
        min_node = 0
        for i in range(len(self.items)):
            if self.items[i][1] < self.items[min_node][1]:
                min_node = i
        return self.items.pop(min_node)

def ucs(start, end):
    '''To be output'''
    path = []
    dist = 0.0

    '''1. Initialize the search model'''
    neighbor_data = getEdgeData()
    frontier = PriorityQueue()
    explored = set()
    prev = {}

    '''2. From the start node search for the end node'''
    frontier.push((start, 0.0))
    while not frontier.isEmpty():
        '''(1) Pop out a node from the frontier'''
        curr_node, cost = frontier.pop()
        if curr_node in explored:
            continue
        explored.add(curr_node)
        if curr_node == end:
            break

        '''(2) Expand all the neighbor nodes of the current node'''
        if curr_node not in neighbor_data:
            continue
        for neighbor in neighbor_data[curr_node]:
            if not (neighbor in explored):
                delta = neighbor_data[curr_node][neighbor][0]
                frontier.push((neighbor, cost+delta))
                prev[neighbor] = curr_node

    '''3. Reconstruct the solution by the mapping of expansion'''
    curr_node = end
    path.insert(0, end)
    while curr_node != start:
        dist += (neighbor_data[ prev[curr_node] ][ curr_node ][0])
        curr_node = prev[curr_node]
        path.insert(0, curr_node)

    return path, dist

def getDist(p1, p2):
    path, dist = ucs(p1, p2)
    return dist

def getPath(p1, p2):
    path, dist = ucs(p1, p2)
    return path
