class FenwickTree:
    def __init__(self, size):
        self.size = size
        self.tree = [0] * (size + 1)

    def update(self, idx, delta):
        """Add `delta` to index `idx`."""
        while idx <= self.size:
            self.tree[idx] += delta
            idx += idx & -idx

    def query(self, idx):
        """Compute prefix sum up to index `idx`."""
        res = 0
        while idx > 0:
            res += self.tree[idx]
            idx -= idx & -idx
        return res

    def range_query(self, l, r):
        """Compute the sum in range [l, r]."""
        return self.query(r) - self.query(l - 1)
