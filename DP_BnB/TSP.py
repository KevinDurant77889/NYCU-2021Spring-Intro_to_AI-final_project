import pandas as pd
from queue import PriorityQueue
import random

cnt1=0 #counts for number of state_space_tree node explored by Brach and Bound
cnt2=0 #counts for number of state_space_tree node explored by DP


def generate(n):
    matrix=[]
    for i in range(n):
        row=[]
        for j in range(n):
            if i==j: row.append(float('inf'))
            elif i<j: row.append(random.uniform(0, 20))
            else: row.append(matrix[j][i])
        matrix.append(row)
    return matrix



# Branch and Bound approach

class Node(object):
    def __init__(self, level=None, path=None, bound=None):
        self.level = level
        self.path = path
        self.bound = bound

    def __lt__(self, other):
        return self.bound < other.bound

    def __eq__(self, other):
        if(other == None):
            return False
        if(not isinstance(other, Node)):
            return False
        return self.bound == other.dound



def BranchAndBound_TSP(adj_mat, src=0):
    global cnt1
    optimal_tour = []
    n = len(adj_mat)
    u = Node()
    PQ = PriorityQueue()
    v = Node(level=0, path=[0], bound=0)
    min_length = float('inf')
    # Compute initial lower bound
    for i in range(n):    
        v.bound+=huristic(adj_mat,i)
    cnt1+=1
    PQ.put(v)
    while not PQ.empty():
        cnt1+=1
        v = PQ.get()
        if v.bound < min_length:
            u.level = v.level + 1
            last = v.path[-1]
            for i in filter(lambda x: x not in v.path, range(1, n)):
                u.path = v.path[:]
                u.path.append(i)

                if u.level == n - 2:
                    l = set(range(1, n)) - set(u.path)
                    u.path.append(list(l)[0])
                    # putting the depot at last
                    u.path.append(0)
                    _len = get_cost(adj_mat, u)
                    if _len < min_length:
                        min_length = _len
                        optimal_tour = u.path[:]

                else:
                    #compute lower bound of successor node u and add it into PQ if it's decent
                    u.bound = v.bound - huristic(adj_mat,last) + adj_mat[last][i]
                    if u.bound < min_length:
                        PQ.put(u)

                u = Node(level=u.level)

    return optimal_tour, min_length


def get_cost(adj_mat, node):
    tour = node.path
    return sum([adj_mat[tour[i]][tour[i + 1]] for i in range(len(tour) - 1)])


def huristic(adj_mat, i):
    first = second = float('inf')
    n = len(adj_mat)
    for j in range(n):
        if adj_mat[i][j] < first:
            second = first
            first = adj_mat[i][j]          
        elif(adj_mat[i][j] < second):
            second = adj_mat[i][j]
    return (first+second)/2



#------------------------------------------------------------------------------



# DP approach

def DP_TSP(adj_mat):
    global cnt2
    n = len(adj_mat)
    all_points_set = set(range(n))

    # dp keys: tuple(visted_set, last_point_in_path)
    # dp values: tuple(cost, predecessor)
    dp = {(tuple([0,i]), i): tuple([adj_mat[0][i], 0]) for i in range(1,n)}
    dp[tuple([0]),0]=(0,None)
    queue = [(tuple([0,i]), i) for i in range(1,n)]
    cnt2+=n

    while queue:
        cnt2+=1
        visited, last_node = queue.pop(0)
        prev_dist, predecessor = dp[(visited, last_node)]
        to_visit = all_points_set.difference(set(visited))

        if len(to_visit)==0:
            #back to depot (predecessor no change for retrace)
            dp[(visited,last_node)] = (prev_dist+adj_mat[last_node][0], predecessor)
            continue

        for successor in to_visit:
            new_visited = tuple(sorted(list(visited) + [successor]))
            new_dist = (prev_dist + adj_mat[last_node][successor])

            if (new_visited, successor) not in dp:
                dp[(new_visited, successor)] = (new_dist, last_node)
                queue += [(new_visited, successor)]
            else:
                if new_dist < dp[(new_visited, successor)][0]:
                    dp[(new_visited, successor)] = (new_dist, last_node)

    optimal_path, optimal_cost = get_rel(dp, n)
    return optimal_path, optimal_cost


def get_rel(dp,n):
    points_to_retrace = tuple(range(n))

    leaf_node_path = dict((k, v) for k, v in dp.items() 
                          if k[0] == points_to_retrace)
    path= min(leaf_node_path.keys(), key=lambda x: leaf_node_path[x][0])

    optimal_cost, predecessor = dp[path]
    optimal_path = [path[1]]
    points_to_retrace = tuple(sorted(set(points_to_retrace).difference({path[1]})))

    while predecessor is not None:
        last_point = predecessor
        path_key = (points_to_retrace, last_point)
        _, predecessor = dp[path_key]
        points_to_retrace = tuple(sorted(set(points_to_retrace).difference({last_point})))
        optimal_path = [last_point] + optimal_path

    optimal_path = optimal_path + [0]  # putting the depot at last
    return optimal_path, optimal_cost




if __name__ == '__main__':
    #load map example
    df=pd.read_csv('adjMatrix.csv')
    points = list(df.columns.values)
    adj_matrix = [[float(y) for y in x] for x in df.values.T.tolist()]

    # generate N*N symmetirc adj_matrix (for testing)
    matrix = generate(15)
    print('DP: ',DP_TSP(matrix),'node explored: ',cnt2)
    print('branch_and_bound: ',BranchAndBound_TSP(matrix),'node explored: ',cnt1)


    cnt1=0
    cnt2=0

    #test on map example
    '''
    optimal_path, optimal_cost = DP_TSP(adj_matrix)
    print('DP: ',optimal_cost,'node explored: ', cnt2)
    for i in optimal_path:
        print(points[i])

    optimal_path, optimal_cost = BranchAndBound_TSP(adj_matrix)
    print('DP: ',optimal_cost,'node explored: ', cnt1)
    for i in optimal_path:
        print(points[i])
    '''