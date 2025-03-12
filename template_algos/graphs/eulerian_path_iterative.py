def eulerian_path(graph):
    """
    Finds an Eulerian path in a directed graph (if one exists) using Hierholzer's algorithm.
    
    Parameters:
        graph (dict): A dictionary where each key is a vertex and the value is a list 
                      of vertices that can be reached by an edge from that vertex.
    
    Returns:
        list: A list of vertices representing the Eulerian path.
              The returned path uses each edge exactly once.
    """
    # Make a copy of the graph to avoid modifying the original.
    graph_copy = {u: neighbors[:] for u, neighbors in graph.items()}
    
    # Compute in-degree and out-degree for each vertex.
    out_deg = {u: len(neighbors) for u, neighbors in graph_copy.items()}
    in_deg = {u: 0 for u in graph_copy}
    for u in graph_copy:
        for v in graph_copy[u]:
            in_deg[v] = in_deg.get(v, 0) + 1
            if v not in out_deg:
                out_deg[v] = 0  # Ensure every vertex appears in out_deg.
    
    # Find a valid starting vertex:
    # For Eulerian path in a directed graph, if there is a vertex with outdegree - indegree == 1, use it.
    start = None
    for u in graph_copy:
        if out_deg[u] - in_deg.get(u, 0) == 1:
            start = u
            break
    
    # If not, choose any vertex with an outgoing edge.
    if start is None:
        for u in graph_copy:
            if out_deg[u] > 0:
                start = u
                break
                
    if start is None:
        return []  # The graph has no edges.
    
    # Use a stack to simulate the traversal.
    stack = [start]
    path = []
    
    while stack:
        u = stack[-1]
        if graph_copy.get(u) and graph_copy[u]:
            # If there are outgoing edges, take one and push the vertex.
            v = graph_copy[u].pop()
            stack.append(v)
        else:
            # No more outgoing edges; add vertex to path.
            path.append(stack.pop())
    
    # The path is built in reverse order.
    return path[::-1]

# Example usage:
if __name__ == "__main__":
    # Directed graph with an Eulerian path.
    # For example, consider the graph:
    # 0 -> 1, 0 -> 2, 1 -> 2, 2 -> 0, 2 -> 1.
    # One Eulerian path is: 0 -> 2 -> 0 -> 1 -> 2 -> 1
    graph = {
        0: [1, 2],
        1: [2],
        2: [0, 1]
    }
    
    path = eulerian_path(graph)
    print("Eulerian Path:", path)
