

class DSU:
    """
    Disjoint Set Union with parity tracking to test bipartiteness.
    - root[i] == -1 means i is a root.
    - rank[i] stores size of the component rooted at i.
    - col[i] is the parity (0/1) from node i to its parent/root.
    """
    def __init__(self, n: int):
        self.n = n
        self.comp = n
        self.root = [-1] * n
        self.rank = [1] * n
        self.col = [0] * n
        self.is_bipartite = True

    def find(self, x: int) -> int:
        if self.root[x] == -1:
            return x
        p = self.find(self.root[x])
        # Accumulate parity to the (new) root during path compression
        self.col[x] ^= self.col[self.root[x]]
        self.root[x] = p
        return p

    def merge(self, a: int, b: int) -> bool:
        u = self.find(a)
        v = self.find(b)
        if u == v:
            # Same component: edge (a,b) must connect opposite colors
            if self.col[a] == self.col[b]:
                self.is_bipartite = False
            return False

        # Union by size (rank)
        if self.rank[u] < self.rank[v]:
            u, v = v, u
            a, b = b, a

        self.comp -= 1
        self.root[v] = u
        self.rank[u] += self.rank[v]

        # Set parity of v so that a and b end up with opposite colors
        if self.col[a] == self.col[b]:
            self.col[v] ^= 1

        return True

    def same(self, u: int, v: int) -> bool:
        return self.find(u) == self.find(v)

    def get_rank(self, x: int) -> int:
        return self.rank[self.find(x)]

    def get_group(self):
        """Return list of components (each a list of members), largest first."""
        ans = [[] for _ in range(self.n)]
        for i in range(self.n):
            ans[self.find(i)].append(i)
        ans = [g for g in ans if g]
        ans.sort(key=len, reverse=True)
        return ans