# Segment tree for range maximum subarray sum queries

# Global segment tree storage (size will be 4 * N)
t = []

# Global input array
a = []

# Neutral value for empty segments
NEG_INF = -10**5

class Data1:
    __slots__ = ('sum', 'pref', 'suff', 'ans')
    def __init__(self, val):
        # For make_data1: initialize all fields to val
        self.sum  = val
        self.pref = val
        self.suff = val
        self.ans  = val

def combine(l, r):
    """
    Combines two child nodes l and r into a parent node.
    """
    res = Data1(0)
    # total sum
    res.sum = l.sum + r.sum
    # best prefix in [l..r]
    res.pref = max(l.pref, l.sum + r.pref)
    # best suffix in [l..r]
    res.suff = max(r.suff, r.sum + l.suff)
    # best subarray anywhere: either in l, in r, or crossing the middle
    res.ans = max(max(l.ans, r.ans), l.suff + r.pref)
    return res

def make_data1(val):
    """
    Creates a leaf node. If val is very negative (NEG_INF),
    this acts as a neutral element for queries that fall outside the range.
    """
    if val == NEG_INF:
        # sum should be very negative so it doesn't affect combine
        leaf = Data1(NEG_INF)
        leaf.sum = NEG_INF
        leaf.pref = NEG_INF
        leaf.suff = NEG_INF
        leaf.ans = NEG_INF
        return leaf
    else:
        return Data1(val)

def build(arr, v, tl, tr):
    """
    Builds the segment tree t over the input array arr.
    v: current tree index
    tl..tr: segment of the array covered by node v
    """
    if tl == tr:
        t[v] = make_data1(arr[tl])
    else:
        tm = (tl + tr) // 2
        build(arr, v*2,     tl,   tm)
        build(arr, v*2 + 1, tm+1, tr)
        t[v] = combine(t[v*2], t[v*2+1])

def update(v, tl, tr, pos, new_val):
    """
    Point update: set a[pos] = new_val and update the tree.
    """
    if tl == tr:
        t[v] = make_data1(new_val)
    else:
        tm = (tl + tr) // 2
        if pos <= tm:
            update(v*2,     tl,   tm,   pos, new_val)
        else:
            update(v*2 + 1, tm+1, tr, pos, new_val)
        t[v] = combine(t[v*2], t[v*2+1])

def query(v, tl, tr, l, r):
    """
    Range query on [l..r]. Returns a Data1 summarizing that segment.
    """
    if l > r:
        return make_data1(NEG_INF)
    if l == tl and r == tr:
        return t[v]
    tm = (tl + tr) // 2
    left  = query(v*2,     tl,   tm,   l,         min(r, tm))
    right = query(v*2 + 1, tm+1, tr,   max(l, tm+1), r)
    return combine(left, right)

def solve(N, M, mat_q):
    """
    N: size of array a
    M: number of queries
    mat_q: list of queries, each is [type, x, y]
      type == 0 → update: set a[x-1] = y
      type == 1 → query: print max subarray sum on [x-1 .. y-1]
    """
    global t, a
    # Initialize global array 'a' with size N
    # (should be populated before calling solve)
    # Here we assume 'a' is already filled.
    # Build segment tree of size 4*N
    t = [None] * (4 * N)
    build(a, 1, 0, N-1)

    for q in mat_q:
        typ, x, y = q
        if typ == 0:
            # update
            pos = x - 1
            update(1, 0, N-1, pos, y)
        else:
            # range query
            l = x - 1
            r = y - 1
            res = query(1, 0, N-1, l, r)
            print(res.ans)