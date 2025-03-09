fmax = lambda x, y: x if x > y else y

class SEG:
    def __init__(self, n):
        # Build the tree with a power-of-two number of leaves.
        z = 1
        while z < n:
            z *= 2
        self.tree = [0] * (2 * z)
        self.n = z

    def op(self, a, b):
        # Operation used in the segment tree (here: maximum)
        return fmax(a, b)

    def e(self):
        # Identity element for the operation (for maximum, use -1 if all values are nonnegative)
        return -1

    def update(self, i, x):
        i += self.n
        self.tree[i] = x
        while i > 1:
            i //= 2
            self.tree[i] = self.op(self.tree[2 * i], self.tree[2 * i + 1])

    def query(self, l, r):
        # Returns the maximum value in the interval [l, r)
        ans = -1
        l += self.n
        r += self.n
        while l < r:
            if l & 1:
                ans = fmax(ans, self.tree[l])
                l += 1
            if r & 1:
                r -= 1
                ans = fmax(ans, self.tree[r])
            l //= 2
            r //= 2
        return ans

    def smallest_index(self, value):
        # Returns the smallest index where the value is at least 'value'
        if self.tree[1] < value:
            return -1
        i = 1
        while i < self.n:
            if self.tree[2 * i] >= value:
                i = 2 * i
            else:
                i = 2 * i + 1
        return i - self.n

    def max_right(self, l, f):
        """
        Finds the maximum index r (l <= r <= n) such that
            f( op(a[l], a[l+1], ... , a[r-1]) ) is True.
        f must be a monotonic predicate with f(e()) = True.
        Returns r when the predicate first fails.
        """
        if l < 0 or l > self.n:
            raise ValueError("l is out of bounds")
        if l == self.n:
            return self.n
        sm = self.e()
        l += self.n
        while True:
            while l % 2 == 0:
                l //= 2
            if not f(self.op(sm, self.tree[l])):
                # Descend into the subtree to find the exact boundary.
                while l < self.n:
                    l = 2 * l
                    if f(self.op(sm, self.tree[l])):
                        sm = self.op(sm, self.tree[l])
                        l += 1
                return l - self.n
            sm = self.op(sm, self.tree[l])
            l += 1
            # When l is a power of two, we've finished processing
            if (l & -l) == l:
                break
        return self.n

    def min_left(self, r, f):
        """
        Finds the minimum index l (0 <= l <= r) such that
            f( op(a[l], a[l+1], ... , a[r-1]) ) is True.
        f must be a monotonic predicate with f(e()) = True.
        Returns l when the predicate first fails from the left.
        """
        if r < 0 or r > self.n:
            raise ValueError("r is out of bounds")
        if r == 0:
            return 0
        sm = self.e()
        r += self.n
        while True:
            r -= 1
            while r > 1 and (r & 1):
                r //= 2
            if not f(self.op(self.tree[r], sm)):
                # Descend to find the exact boundary.
                while r < self.n:
                    r = 2 * r + 1
                    if f(self.op(self.tree[r], sm)):
                        sm = self.op(self.tree[r], sm)
                        r -= 1
                return r + 1 - self.n
            sm = self.op(self.tree[r], sm)
            if (r & -r) == r:
                break
        return 0
