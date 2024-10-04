### 

class SparseMaxTreeNode:
    def __init__(self, low, high):
        self._low = low
        self._high = high
        self._max_val = 0
        self._left = None
        self._right = None

    def _extend(self):
        if self._left is None and self._low < self._high:
            mid = (self._low + self._high) // 2
            self._left = SparseMaxTreeNode(self._low, mid)
            if mid + 1 <= self._high:
                self._right = SparseMaxTreeNode(mid + 1, self._high)

    def add(self, key, val):
        self._extend()
        self._max_val = max(self._max_val, val)
        if self._left is not None:
            if key <= self._left._high:
                self._left.add(key, val)
            else:
                self._right.add(key, val)

    def get_max(self, low, high):
        if low <= self._low and self._high <= high:
            return self._max_val
        if max(self._low, low) > min(self._high, high):
            return 0
        self._extend()
        return max(self._left.get_max(low, high), self._right.get_max(low, high))

### LAZY
class SparseMaxTreeNode:
    def __init__(self, low, high, val):
        self.low = low
        self.high = high
        self.val = val
        self.lazy = 0
        self.left = None
        self.right = None

    def _extend(self):
        if self.low < self.high:
            if self.left is None:
                mid = (self.low + self.high) // 2
                self.left = SparseMaxTreeNode(self.low, mid, self.val)
                if mid + 1 <= self.high:
                    self.right = SparseMaxTreeNode(mid + 1, self.high, self.val)
            elif self.lazy != 0:
                self.left.val += self.lazy
                self.left.lazy += self.lazy
                self.right.val += self.lazy
                self.right.lazy += self.lazy
        self.lazy = 0

    def update(self, low, high, delta):
        if low > high or self.high < low or high < self.low:
            return
        if low <= self.low and self.high <= high:
            self.val += delta
            self.lazy += delta
            return
        self._extend()
        self.left.update(low, high, delta)
        self.right.update(low, high, delta)
        self.val = max(self.left.val, self.right.val)

    def query(self, low, high):
        if low > high or self.high < low or high < self.low:
            return 0
        if low <= self.low and self.high <= high:
            return self.val
        self._extend()
        return max(self.left.query(low, high), self.right.query(low, high))

segtree = SparseMaxTreeNode(0,N+1,0)
## add 1 to [l,r]
segtree.update(l,r,1)
## get max [l,r]
segtree.query(l,r)






































# limit for array size
N = 100000;

# Max size of tree
tree = [0] * (2 * N);

# function to build the tree
def build(arr) :

    # insert leaf nodes in tree
    for i in range(n) :
        tree[n + i] = arr[i];

    # build the tree by calculating parents
    for i in range(n - 1, 0, -1) :
        tree[i] = tree[i << 1] + tree[i << 1 | 1];

# function to update a tree node
def updateTreeNode(p, value) :

    # set value at position p
    tree[p + n] = value;
    p = p + n;

    # move upward and update parents
    i = p;

    while i > 1 :

        tree[i >> 1] = tree[i] + tree[i ^ 1];
        i >>= 1;

# function to get sum on interval [l, r)
def query(l, r) :

    res = 0;

    # loop to find the sum in the range
    l += n;
    r += n;

    while l < r :

        if (l & 1) :
            res += tree[l];
            l += 1

        if (r & 1) :
            r -= 1;
            res += tree[r];

        l >>= 1;
        r >>= 1

    return res;
