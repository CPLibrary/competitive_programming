import math

class SEG:
    def __init__(self, n):
        """
        Initialize the segment tree with size n.
        """
        self.n = 1
        while self.n < n:
            self.n <<= 1  # Ensure n is a power of 2
        self.size = self.n * 2
        self.tree = [-math.inf] * self.size  # Initialize with very low values
        self.lazy_add = [0] * self.size      # Lazy array for range addition
        self.lazy_set = [None] * self.size   # Lazy array for range setting

    def _apply_set(self, i, val, l, r):
        """
        Apply a range set operation to node i covering range [l, r).
        """
        self.tree[i] = val
        if i < self.n:
            self.lazy_set[i] = val
            self.lazy_add[i] = 0  # Clear any pending additions

    def _apply_add(self, i, val, l, r):
        """
        Apply a range add operation to node i covering range [l, r).
        """
        if self.lazy_set[i] is not None:
            # If a set operation is pending, update it instead of adding
            self.lazy_set[i] += val
            self.tree[i] += val
        else:
            self.lazy_add[i] += val
            self.tree[i] += val

    def _push(self, i, l, r):
        """
        Push the lazy updates from node i down to its children.
        """
        if self.lazy_set[i] is not None:
            mid = (l + r) // 2
            self._apply_set(i*2, self.lazy_set[i], l, mid)
            self._apply_set(i*2+1, self.lazy_set[i], mid, r)
            self.lazy_set[i] = None  # Clear after pushing

        if self.lazy_add[i] != 0:
            mid = (l + r) // 2
            self._apply_add(i*2, self.lazy_add[i], l, mid)
            self._apply_add(i*2+1, self.lazy_add[i], mid, r)
            self.lazy_add[i] = 0  # Clear after pushing

    def _build(self, i):
        """
        Rebuild the tree upwards from node i to ensure accurate aggregate values.
        """
        while i > 1:
            i >>= 1
            left = self.tree[i*2]
            right = self.tree[i*2+1]
            self.tree[i] = max(left, right)
            if self.lazy_set[i] is not None:
                self.tree[i] = self.lazy_set[i] + self.lazy_add[i]
            else:
                self.tree[i] += self.lazy_add[i]

    def _pull(self, l, r):
        """
        Push all updates from the root to the node range [l, r).
        """
        h = self.n.bit_length()
        for d in range(h, 0, -1):
            node = (l >> d)
            if node > 0 and (self.lazy_set[node] is not None or self.lazy_add[node] != 0):
                self._push(node, 0, self.n)
        for d in range(h, 0, -1):
            node = ((r -1) >> d)
            if node > 0 and (self.lazy_set[node] is not None or self.lazy_add[node] != 0):
                self._push(node, 0, self.n)

    def query(self, ql, qr):
        """
        Query the maximum value in the interval [ql, qr).
        """
        res = -math.inf
        l = ql + self.n
        r = qr + self.n
        # Push all pending updates for the query range
        self._pull(l, r)
        while l < r:
            if l & 1:
                res = max(res, self.tree[l])
                l +=1
            if r &1:
                r -=1
                res = max(res, self.tree[r])
            l >>=1
            r >>=1
        return res

    def update_add(self, ul, ur, val):
        """
        Range add: add `val` to all elements in the interval [ul, ur).
        """
        l = ul + self.n
        r = ur + self.n
        orig_l, orig_r = l, r
        while l < r:
            if l &1:
                self._apply_add(l, val, 0, self.n)
                l +=1
            if r &1:
                r -=1
                self._apply_add(r, val, 0, self.n)
            l >>=1
            r >>=1
        # Rebuild affected nodes to maintain accurate aggregate values
        self._build(orig_l)
        self._build(orig_r -1)

    def update_set(self, ul, ur, val):
        """
        Range set: set all elements in the interval [ul, ur) to `val`.
        """
        l = ul + self.n
        r = ur + self.n
        orig_l, orig_r = l, r
        while l < r:
            if l &1:
                self._apply_set(l, val, 0, self.n)
                l +=1
            if r &1:
                r -=1
                self._apply_set(r, val, 0, self.n)
            l >>=1
            r >>=1
        # Rebuild affected nodes to maintain accurate aggregate values
        self._build(orig_l)
        self._build(orig_r -1)

    def update(self, pos, val):
        """
        Point update: set the value at index `pos` to `val`.
        """
        pos += self.n
        # Push all pending updates along the path to the leaf
        self._pull(pos, pos +1)
        self.tree[pos] = val
        self.lazy_add[pos] = 0
        self.lazy_set[pos] = None
        # Rebuild the tree upwards to maintain accurate aggregate values
        self._build(pos)
