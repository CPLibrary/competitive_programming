
// this does range update and computes maximum

template <typename T>
class LazySegTree {
    public:
    int n;
    vector<T> tree;
    vector<T> lazy;
    T default_val;

    LazySegTree(int n, T default_val) : n(n), default_val(default_val) {
        tree = vector<T>(n * 4, default_val);
        lazy = vector<T>(n * 4, default_val);
        //second_tree = vector<T>(n * 4, default_val);
    }

    T _combine(T a, T b) {
        return a + b;
    }

    T _combine2(T a, T b) {
        return min(a,b);
    }

    void _push(int node) {
        tree[node * 2] = _combine(tree[node * 2], lazy[node]);
        lazy[node * 2] = _combine(lazy[node * 2], lazy[node]);
        tree[node * 2 + 1] = _combine(tree[node * 2 + 1], lazy[node]);
        lazy[node * 2 + 1] = _combine(lazy[node * 2 + 1], lazy[node]);
        lazy[node] = default_val;
    }

    T query(int pos) {
        return _query(1, 0, n - 1, pos, pos);
    }

    T query(int low, int high) { // [l,r] inclusive
        return _query(1, 0, n - 1, low, high);
    }

    T _query(int node, int node_low, int node_high, int low, int high) {
        if (low > high) return 1000000009;
        if (low <= node_low && node_high <= high) return tree[node];
        _push(node);
        int node_mid = (node_low + node_high) / 2;
        return _combine2(_query(node * 2, node_low, node_mid, low, min(high, node_mid)),
                        _query(node * 2 + 1, node_mid + 1, node_high, max(low, node_mid + 1), high));
    }

    void update(int pos, T delta) {
        _update(1, 0, n - 1, pos, pos, delta);
    }

    void update(int low, int high, T delta) {
        _update(1, 0, n - 1, low, high, delta);
    }

    void _update(int node, int node_low, int node_high, int low, int high, T delta) {
        if (low > high) return;
        if (low == node_low && node_high == high) {
            tree[node] = _combine(tree[node], delta);
            lazy[node] = _combine(lazy[node], delta);
        } else {
            _push(node);
            int node_mid = (node_low + node_high) / 2;
            _update(node * 2, node_low, node_mid, low, min(high, node_mid), delta);
            _update(node * 2 + 1, node_mid + 1, node_high, max(low, node_mid + 1), high, delta);
            tree[node] = _combine2(tree[node * 2], tree[node * 2 + 1]);
        }
    }
};

struct item {
    int max_val;
    int max_count;

    item(int max_val = 0, int max_count = 0) : max_val(max_val), max_count(max_count) {
    }

    item operator+(const item& other) const {
        if (other.max_val < max_val) return *this;
        if (other.max_val > max_val) return other;
        return {max_val, max_count + other.max_count};
    }
};

LazySegTree<int>* seg_tree = new LazySegTree<int>((int)nums.size()+1, 1000000009);


for (int i = 0; i < nums.size(); ++i) {
    if (nums[i] == 0) {
        seg_tree->update(i,-1e6);
    } else {
        seg_tree->update(i,nums[i]);
    }

}

std::sort(queries.begin(), queries.end(),
      [](const std::vector<int>& a, const std::vector<int>& b) {
  return a[0] > b[0] || ((a[0] == b[0]) && a[1] < b[1]);
});

for (vector<int>& zeb : queries) {
    int l = zeb[0];
    int r = zeb[1];
    seg_tree->update(l,r,-1);
}