import math

class SEG:
    def __init__(self, n):
        self.n = n
        self.tree = [-math.inf] * (2 * self.n)  # Initialize with a very low value
        self.lazy_add = [0] * (2 * self.n)  # Lazy array for addition
        self.lazy_set = [None] * (2 * self.n)  # Lazy array for setting values

    def _apply_set(self, i, val):
        """Apply set operation to a node."""
        self.tree[i] = val
        if i < self.n:
            self.lazy_set[i] = val  # Set value for lazy propagation
            self.lazy_add[i] = 0  # Clear any pending additions

    def _apply_add(self, i, val):
        """Apply add operation to a node."""
        if self.lazy_set[i] is not None:
            # If a set value is pending, apply it first
            self.tree[i] = self.lazy_set[i] + val
        else:
            self.tree[i] += val

        if i < self.n:
            if self.lazy_set[i] is not None:
                self.lazy_set[i] += val
            else:
                self.lazy_add[i] += val

    def _push(self, i):
        """Push updates from node i down to its children."""
        if self.lazy_set[i] is not None:
            # If there's a set operation pending, apply it to children
            self._apply_set(i * 2, self.lazy_set[i])
            self._apply_set(i * 2 + 1, self.lazy_set[i])
            self.lazy_set[i] = None
        if self.lazy_add[i] != 0:
            # Apply any add operations
            self._apply_add(i * 2, self.lazy_add[i])
            self._apply_add(i * 2 + 1, self.lazy_add[i])
            self.lazy_add[i] = 0

    def _build(self, i):
        """Rebuild tree upwards from node i."""
        while i > 1:
            i >>= 1
            if self.lazy_set[i] is None:  # Rebuild only if no set operation is pending
                self.tree[i] = max(self.tree[i * 2], self.tree[i * 2 + 1]) + self.lazy_add[i]
            else:
                self.tree[i] = self.lazy_set[i]

    def _pull(self, l, r):
        """Push all updates from the root to the node range [l, r)."""
        h = 1
        while (l >> h) > 0:
            if self.lazy_set[l >> h] is not None or self.lazy_add[l >> h] != 0:
                self._push(l >> h)
            h += 1
        h = 1
        while (r >> h) > 0:
            if self.lazy_set[(r - 1) >> h] is not None or self.lazy_add[(r - 1) >> h] != 0:
                self._push((r - 1) >> h)
            h += 1

    def query(self, l, r):
        """Query the maximum value in the interval [l, r)."""
        l += self.n
        r += self.n
        self._pull(l, r)  # Make sure all updates are applied
        ans = -math.inf
        while l < r:
            if l & 1:
                ans = max(ans, self.tree[l])
                l += 1
            if r & 1:
                r -= 1
                ans = max(ans, self.tree[r])
            l >>= 1
            r >>= 1
        return ans

    def update_add(self, l, r, val):
        """Range add: add `val` to all elements in the interval [l, r)."""
        l0, r0 = l + self.n, r + self.n
        while l0 < r0:
            if l0 & 1:
                self._apply_add(l0, val)
                l0 += 1
            if r0 & 1:
                r0 -= 1
                self._apply_add(r0, val)
            l0 >>= 1
            r0 >>= 1
        # Rebuild affected nodes to reflect the changes
        self._build(l + self.n)
        self._build(r - 1 + self.n)

    def update_set(self, l, r, val):
        """Range set: set all elements in the interval [l, r) to `val`."""
        l0, r0 = l + self.n, r + self.n
        while l0 < r0:
            if l0 & 1:
                self._apply_set(l0, val)
                l0 += 1
            if r0 & 1:
                r0 -= 1
                self._apply_set(r0, val)
            l0 >>= 1
            r0 >>= 1
        # Rebuild affected nodes to reflect the changes
        self._build(l + self.n)
        self._build(r - 1 + self.n)


    def update(self, i, val):
        """Point update: set the value at index `i` to `val`."""
        i += self.n
        # Push any pending lazy updates to the node
        self._pull(i, i + 1)
        # Set the value at the specific index
        self.tree[i] = val
        self.lazy_add[i] = 0
        self.lazy_set[i] = None
        # Rebuild the tree upwards to reflect the new value
        self._build(i)
