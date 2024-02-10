# https://arxiv.org/abs/2203.00671

def preflow_push(graph):
    V = len(graph)
    source = 0
    sink = V - 1

    ver = [0] * V
    e_flow = [0] * V 
    edge = []

    def add_edge(u, v, capacity):
        edge.append([0, capacity, u, v])

    for u in range(V):
        for v in range(V):
            if graph[u][v] > 0:
                add_edge(u, v, graph[u][v])

    ver[source] = V
    for i in range(len(edge)):
        if edge[i][2] == source:
            edge[i][0] = edge[i][1]
            e_flow[edge[i][3]] += edge[i][0]
            edge.append([-edge[i][0], 0, edge[i][3], source])

    def overflow_vertex():
        for i in range(1, V - 1):
            if e_flow[i] > 0:
                return i
        return -1

    def update_reverse_edge_flow(i, flow):
        u, v = edge[i][3], edge[i][2]
        for j in range(len(edge)):
            if edge[j][3] == v and edge[j][2] == u:
                edge[j][0] -= flow
                return
        edge.append([0, flow, u, v])

    def push(u):
        for i in range(len(edge)):
            if edge[i][2] == u:
                if edge[i][0] == edge[i][1]:
                    continue
                if ver[u] > ver[edge[i][3]]:
                    flow = min(edge[i][1] - edge[i][0], e_flow[u])
                    e_flow[u] -= flow
                    e_flow[edge[i][3]] += flow
                    edge[i][0] += flow
                    update_reverse_edge_flow(i, flow)
                    return True
        return False

    def relabel(u):
        mh = float('inf')
        for i in range(len(edge)):
            if edge[i][2] == u:
                if edge[i][0] == edge[i][1]:
                    continue
                if ver[edge[i][3]] < mh:
                    mh = ver[edge[i][3]]
                    ver[u] = mh + 1

    while overflow_vertex() != -1:
        u = overflow_vertex()
        if not push(u):
            relabel(u)

    return e_flow[sink]


# normalizing a graph to have only one S and only one T
# boundary edge (S, S^i) has infinite capacity
def normalize_path(entrances, exits, path):
    path_length = len(path)
    residual_graph_length = path_length + 2
    residual_graph = [[0] * (residual_graph_length) for _ in range(residual_graph_length)]

    # path
    for i in range(path_length): 
        residual_graph[i + 1][1:path_length + 1] = path[i]

    # global S
    for i in entrances: 
        residual_graph[0][i + 1] = float('inf')

    # global T
    for i in exits: 
        residual_graph[i + 1][-1] = float('inf')

    return residual_graph

    """
    [0, inf, inf, 0, 0, 0, 0, 0]
    [0, 0, 0, 4, 6, 0, 0, 0]
    [0, 0, 0, 5, 2, 0, 0, 0]
    [0, 0, 0, 0, 0, 4, 4, 0]
    [0, 0, 0, 0, 0, 6, 6, 0]
    [0, 0, 0, 0, 0, 0, 0, inf]
    [0, 0, 0, 0, 0, 0, 0, inf]
    [0, 0, 0, 0, 0, 0, 0, 0]
"""

# implementation uses preflow_push, because
# for given constraints such as V=50 E=2500 F=2000000
# and complexity O(V^2*E) seems to be satysfying result
# if the input gets wider, we can consider using this
# algorithm, which has complexity close to linear:
# https://arxiv.org/abs/2203.00671
def solution(entrances, exits, path):
    path = normalize_path(entrances, exits, path)
    return preflow_push(path)

res = solution(
    [0, 1], 
    [4, 5], 
    [
        [0, 0, 4, 6, 0, 0], 
        [0, 0, 5, 2, 0, 0], 
        [0, 0, 0, 0, 4, 4], 
        [0, 0, 0, 0, 6, 6], 
        [0, 0, 0, 0, 0, 0], 
        [0, 0, 0, 0, 0, 0]
    ]
)

print(res)
