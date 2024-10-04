class SegmentTree:
    def __init__(self, data, func, default):
        self.n = len(data)
        self.size = 1
        while self.size < self.n:
            self.size <<= 1
        self.tree = [default] * (2 * self.size)
        self.lazy = [0] * (2 * self.size)
        self.func = func
        self.default = default
        # Initialize the leaves
        for i in range(self.n):
            self.tree[self.size + i] = data[i]
        # Build the tree
        for i in range(self.size - 1, 0, -1):
            self.tree[i] = self.func(self.tree[2 * i], self.tree[2 * i + 1])

    def _push(self, pos):
        """Push the updates to the children."""
        for s in range(int.bit_length(self.size)):
            i = pos >> s
            if self.lazy[i]:
                self._apply(2 * i, self.lazy[i])
                self._apply(2 * i + 1, self.lazy[i])
                self.lazy[i] = 0

    def _apply(self, pos, value):
        """Apply the update to the node."""
        self.tree[pos] += value
        if pos < self.size:
            self.lazy[pos] += value

    def update_range(self, l, r, value):
        """Range update: add `value` to all elements in [l, r)."""
        l += self.size
        r += self.size
        l0, r0 = l, r
        while l < r:
            if l & 1:
                self._apply(l, value)
                l += 1
            if r & 1:
                r -= 1
                self._apply(r, value)
            l >>= 1
            r >>= 1
        self._push(l0)
        self._push(r0 - 1)

    def query_range(self, l, r):
        """Range query: compute the function over [l, r)."""
        self._push(l + self.size)
        self._push(r - 1 + self.size)
        res = self.default
        l += self.size
        r += self.size
        while l < r:
            if l & 1:
                res = self.func(res, self.tree[l])
                l += 1
            if r & 1:
                r -= 1
                res = self.func(res, self.tree[r])
            l >>= 1
            r >>= 1
        return res
