import math

class LCA:
    def __init__(self, n, adj, root=0):
        self.n = n
        self.LOG = math.ceil(math.log2(n)) + 1
        self.parent = [[-1] * n for _ in range(self.LOG)]
        self.depth = [0] * n
        self._dfs(adj, root, -1)
        self._build()

    def _dfs(self, adj, node, par):
        """DFS to set the first ancestor and depth."""
        self.parent[0][node] = par
        for neighbor in adj[node]:
            if neighbor != par:
                self.depth[neighbor] = self.depth[node] + 1
                self._dfs(adj, neighbor, node)

    def _build(self):
        """Build the ancestor table."""
        for k in range(1, self.LOG):
            for v in range(self.n):
                if self.parent[k-1][v] != -1:
                    self.parent[k][v] = self.parent[k-1][self.parent[k-1][v]]

    def get_lca(self, u, v):
        """Compute the LCA of nodes u and v."""
        if self.depth[u] < self.depth[v]:
            u, v = v, u
        # Lift u up to the depth of v
        for k in range(self.LOG - 1, -1, -1):
            if self.depth[u] - (1 << k) >= self.depth[v]:
                u = self.parent[k][u]
        if u == v:
            return u
        # Lift both u and v until their parents match
        for k in range(self.LOG - 1, -1, -1):
            if self.parent[k][u] != self.parent[k][v]:
                u = self.parent[k][u]
                v = self.parent[k][v]
        return self.parent[0][u]
