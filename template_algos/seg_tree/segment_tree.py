class SEG:
    def __init__(self, n):
        self.n = n
        self.tree = [0] * 2 * self.n

    def query(self, l, r): ## interval [l,r)
        l += self.n
        r += self.n
        ans = 0
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

    def update(self, i, val):
        i += self.n
        self.tree[i] = val
        while i > 1:
            i >>= 1
            self.tree[i] = max(self.tree[i * 2], self.tree[i * 2 + 1])



class SEGmin:
    def __init__(self, n):
        self.n = n
        self.tree = [float('inf')] * 2 * self.n

    def query(self, l, r): ## interval [l,r)
        l += self.n
        r += self.n
        ans = float('inf')
        while l < r:
            if l & 1:
                ans = min(ans, self.tree[l])
                l += 1
            if r & 1:
                r -= 1
                ans = min(ans, self.tree[r])
            l >>= 1
            r >>= 1
        return ans

    def update(self, i, val):
        i += self.n
        self.tree[i] = val
        while i > 1:
            i >>= 1
            self.tree[i] = min(self.tree[i * 2], self.tree[i * 2 + 1])


class SEG:
    def __init__(self, n):
        self.n = n
        self.tree = [0] * 2 * self.n

    def query(self, l, r): ## interval [l,r)
        l += self.n
        r += self.n
        ans = 0
        while l < r:
            if l & 1:
                ans = sum(ans, self.tree[l])
                l += 1
            if r & 1:
                r -= 1
                ans = sum(ans, self.tree[r])
            l >>= 1
            r >>= 1
        return ans

    def update(self, i, val):
        i += self.n
        self.tree[i] = val
        while i > 1:
            i >>= 1
            self.tree[i] = sum(self.tree[i * 2], self.tree[i * 2 + 1])
