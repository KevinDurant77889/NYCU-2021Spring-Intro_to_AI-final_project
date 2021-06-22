import math, random, itertools
import utils

class TSPsolver:
    def __init__(self, graph, dists):
        self.graph = graph  # represented by a list of nodes
        self.edges = dists  # costs of edges
        self.visited = [graph[0]]   # A "state" is represented by a list of visited nodes
        self.epsilon = 1    # the probability of "exploration" rather than "exploitation"
        self.alpha = 0.9    # the learning rate
        self.gamma = 0.9    # the discount factor
        self.q_values = [[0 for i in range(len(graph) + 1)] for j in range(2 ** (len(graph)) + 1)]

    def getQvalue(self, state, action):
        idx_s = utils.indexS(self.graph, state)
        idx_a = utils.indexA(self.graph, action)
        return self.q_values[idx_s][idx_a]

    def setQvalue(self, state, action, val):
        idx_s = utils.indexS(self.graph, state)
        idx_a = utils.indexA(self.graph, action)
        self.q_values[idx_s][idx_a] = val

    def getNextState(self, action):
        '''Append the next node to the list of visited nodes'''
        l = self.visited
        l.append(action)
        return l

    def getValue(self, state):
        '''Output the value of the current state'''
        actions = utils.possibleNextNodes(self.graph, state)
        if actions == []:
            return 0
        else:
            maxVal = float('-inf')
            for action in actions:
                curr = self.getQvalue(state, action)
                if curr > maxVal:
                    maxVal = curr
                    bestAction = action
            return maxVal

    def getPolicy(self, state):
        '''Output the best action (the best node to go to next) according to the current state'''
        actions = utils.possibleNextNodes(self.graph, state)
        if actions == []:
            return []
        else:
            maxVal = float('-inf')
            bestAction = actions[0]
            for action in actions:
                curr = self.getQvalue(state, action)
                if curr > maxVal:
                    maxVal = curr
                    bestAction = action
            return bestAction

    def getAction(self):
        '''Choose a possible next node'''
        rand = random.random()
        possibilities = utils.possibleNextNodes(self.graph, self.visited)
        if possibilities == []:
            # No possible new nodes
            return []
        else:
            if (rand > self.epsilon):
                # Taking best policy (exploitation)
                return self.getPolicy(self.visited)
            else:
                # Taking random (exploration)
                return random.choice(possibilities)

    def update(self, action):
        '''Optimizing Q-table'''
        alpha = self.alpha
        nextState = self.getNextState(action)
        reward = 0 - self.edges[self.visited[-1]][action]
        target_Q = reward + self.gamma * self.getValue(nextState)
        model_Q = self.getQvalue(self.visited, action)
        new_Q = model_Q + alpha * (target_Q - model_Q)
        self.setQvalue(self.visited, action, new_Q)
        self.visited = nextState


def genRandomGraph(numPoints):
    matrix=[]
    for i in range(numPoints):
        row=[]
        for j in range(numPoints):
            if i==j: row.append(float('-inf'))
            elif i<j: row.append(random.uniform(0, 20))
            else: row.append(matrix[j][i])
        matrix.append(row)
    return matrix


if __name__ == '__main__':
    dists = genRandomGraph(15)
    testGraph = list(range(len(dists)))
    print("Starting Graph:", testGraph)

    bestSolution = []
    shortest = float('inf')
    myAgent = TSPsolver(testGraph, dists)
    num_trials = 50
    for i in range(num_trials):
        nextAction = True
        myAgent.visited = [testGraph[0]]
        myAgent.epsilon = 1 / math.sqrt(i + 1)
        while(nextAction != []):
            nextAction = myAgent.getAction()
            if(nextAction != []):
                myAgent.update(nextAction)
        
        newCost = utils.pathCost(myAgent.visited, myAgent.edges)
        if newCost < shortest:
            shortest = newCost
            bestSolution = myAgent.visited
            bestTrial = i + 1

        if (i+1) % (num_trials / 10) == 0:
            print("After", i+1, "trials:", myAgent.visited, newCost)

    print("Best solution at trial", bestTrial, ":", bestSolution, shortest)