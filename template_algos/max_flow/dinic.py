

from collections import deque

class Edge:
    def __init__(self, to, rev, cap):
        self.to = to
        self.rev = rev
        self.cap = cap

class MaxFlow:
    def __init__(self, N):
        self.size = N
        self.graph = [[] for _ in range(N)]

    def add_edge(self, fr, to, cap):
        forward = Edge(to, len(self.graph[to]), cap)
        backward = Edge(fr, len(self.graph[fr]), 0)
        self.graph[fr].append(forward)
        self.graph[to].append(backward)

    def bfs_level(self, s, t, level):
        """Build levels using BFS."""
        queue = deque()
        level[:] = [-1] * self.size
        level[s] = 0
        queue.append(s)
        while queue:
            v = queue.popleft()
            for e in self.graph[v]:
                if e.cap > 0 and level[e.to] == -1:
                    level[e.to] = level[v] + 1
                    queue.append(e.to)
                    if e.to == t:
                        return
        return

    def dfs_flow(self, v, t, upTo, iter_, level):
        """Find augmenting paths using DFS."""
        if v == t:
            return upTo
        for i in range(iter_[v], len(self.graph[v])):
            e = self.graph[v][i]
            if e.cap > 0 and level[v] < level[e.to]:
                d = self.dfs_flow(e.to, t, min(upTo, e.cap), iter_, level)
                if d > 0:
                    e.cap -= d
                    self.graph[e.to][e.rev].cap += d
                    return d
            iter_[v] += 1
        return 0

    def max_flow(self, s, t):
        """Compute the maximum flow from s to t."""
        flow = 0
        level = [-1] * self.size
        while True:
            self.bfs_level(s, t, level)
            if level[t] == -1:
                break
            iter_ = [0] * self.size
            while True:
                f = self.dfs_flow(s, t, float('inf'), iter_, level)
                if f == 0:
                    break
                flow += f
        return flow
        
