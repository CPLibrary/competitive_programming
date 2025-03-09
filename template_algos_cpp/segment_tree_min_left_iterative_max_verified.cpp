template <typename T>
    class SegTree {
    public:
        int n;         // original number of elements (logical size)
        int z;         // number of leaves (power of 2)
        std::vector<T> tree;
        T default_val; // identity element (for maximum, typically a very small value)

        SegTree(int n, T default_val) : n(n), default_val(default_val) {
            z = 1;
            while (z < n) {
                z *= 2;
            }
            tree = std::vector<T>(z * 2, default_val);
        }

        // Combine function: here, maximum.
        T _combine(T a, T b) const {
            return std::max(a, b);
        }

        // Query in the half-open interval [l, r)
        T query(int l, int r) const {
            l += z;
            r += z;
            T ans = default_val;
            while (l < r) {
                if (l & 1) {
                    ans = std::max(ans, tree[l]);
                    l++;
                }
                if (r & 1) {
                    r--;
                    ans = std::max(ans, tree[r]);
                }
                l /= 2;
                r /= 2;
            }
            return ans;
        }

        // Point update: update index i to value x.
        void update(int i, T x) {
            i += z;
            tree[i] = x;
            while (i > 1) {
                i /= 2;
                tree[i] = _combine(tree[2 * i], tree[2 * i + 1]);
            }
        }

        // Returns the smallest index i such that the element at i is at least 'value'
        // (returns -1 if no such index exists).
        int smallest_index(T value) const {
            if (tree[1] < value) {
                return -1;
            }
            int curr = 1;
            while (curr < z) {
                if (tree[2 * curr] >= value)
                    curr = 2 * curr;
                else
                    curr = 2 * curr + 1;
            }
            return curr - z;
        }

        // max_right(l, f):
        // Finds the maximum index r (with l <= r <= n) such that
        //     f( _combine(a[l], a[l+1], ... , a[r-1]) ) is true.
        // The predicate f must be monotonic (if f(x) is true then f(op(x, y)) is also true)
        // and must satisfy f(default_val) == true.
        template <typename F>
        int max_right(int l, F f) const {
            if (l < 0 || l > n) throw std::out_of_range("max_right: l out of range");
            T sm = default_val;  // identity element
            l += z;
            // Invariant: f(sm) is true.
            do {
                // While l is a right child, move up.
                while ((l % 2) == 0) l /= 2;
                // If combining the current accumulator with tree[l] violates f...
                if (!f(_combine(sm, tree[l]))) {
                    // Descend into the subtree to find the exact boundary.
                    while (l < z) {
                        l = 2 * l;
                        if (f(_combine(sm, tree[l]))) {
                            sm = _combine(sm, tree[l]);
                            l++;
                        }
                    }
                    return l - z;
                }
                sm = _combine(sm, tree[l]);
                l++;
            } while ((l & -l) != l);
            return n;
        }

        // min_left(r, f):
        // Finds the minimum index l (with 0 <= l <= r) such that
        //     f( _combine(a[l], a[l+1], ... , a[r-1]) ) is true.
        // The predicate f must be monotonic (if f(x) is true then f(op(y, x)) is also true)
        // and must satisfy f(default_val) == true.
        template <typename F>
        int min_left(int r, F f) const {
            if (r < 0 || r > n) throw std::out_of_range("min_left: r out of range");
            if (r == 0) return 0;
            T sm = default_val;
            r += z;
            do {
                r--;
                while (r > 1 && (r & 1)) r /= 2;
                if (!f(_combine(tree[r], sm))) {
                    // Descend into the subtree to find the exact boundary.
                    while (r < z) {
                        r = 2 * r + 1;
                        if (f(_combine(tree[r], sm))) {
                            sm = _combine(tree[r], sm);
                            r--;
                        }
                    }
                    return r + 1 - z;
                }
                sm = _combine(tree[r], sm);
            } while ((r & -r) != r);
            return 0;
            }
        };



SegTree seg_tree(baskets.size(),0);

auto f = [&curr](int x) { return x < curr; };
int index = seg_tree.max_right(l, f); // returns index where it fails or end of array 




