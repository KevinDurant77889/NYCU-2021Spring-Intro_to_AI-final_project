import math
import csv


def getEdgeData():
    # Read edge data to build a graph topology
    # Format: { node A: { neighbor 1: (distance 1, speed limit 1), neighbor 2: (distance 2, speed limit 2), ... }, node B: {...}, ... }
    data = {}
    with open("edges.csv", newline='') as csvfile:
        rows = csv.DictReader(csvfile)
        for row in rows:
            if int(row['start']) not in data:
                data[ int(row['start']) ] = {}
            d = ( float(row['distance']), float(row['speed limit'])*1000/3600 )
            data[ int(row['start']) ][ int(row['end']) ] = d
    return data


def possibleNextNodes (graph, visited):
    g = len(graph)
    v = len(visited)
    if v == g:
        return [graph[0]]
    if v > g:
        return []
    if v < g:
        return list (set(graph) - set(visited))


def pathCost(path, dists):
    totalCost = 0
    for i in range(len(path) - 1):
        totalCost += dists[path[i]][path[i+1]]
    return totalCost


def powerset(seq):
    if len(seq) <= 1:
        yield seq
        yield []
    else:
        for item in powerset(seq[1:]):
            yield [seq[0]]+item
            yield item

def indexS(graph, state):
    ps = sorted([sorted(x) for x in powerset(graph)])
    stateSet = sorted(state)
    l = list(graph)
    l.append(graph[0])
    if stateSet == sorted(l):
        return len(graph) 
    else:
        return ps.index(stateSet)

def indexA(graph, action):
    return graph.index(action)
