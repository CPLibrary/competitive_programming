#include <bits/stdc++.h>
using namespace std;

class LazySegmentTreeMin {
private:
    vector<long long> mn, mx, lazy;
    int n;

    void build(const vector<long long>& arr, int node, int start, int end) {
        if (start == end) {
            mn[node] = mx[node] = arr[start];
        } else {
            int mid = (start + end) / 2;
            build(arr, node << 1, start, mid);
            build(arr, node << 1 | 1, mid + 1, end);
            pull(node);
        }
    }

    inline void apply(int node, long long addv) {
        mn[node] += addv;
        mx[node] += addv;
        lazy[node] += addv;
    }

    void propagate(int node) {
        long long z = lazy[node];
        if (z != 0) {
            apply(node << 1, z);
            apply(node << 1 | 1, z);
            lazy[node] = 0;
        }
    }

    inline void pull(int node) {
        mn[node] = min(mn[node << 1], mn[node << 1 | 1]);
        mx[node] = max(mx[node << 1], mx[node << 1 | 1]);
    }

    void updateRange(int node, int start, int end, int l, int r, long long val) {
        if (r < start || end < l) return;
        if (l <= start && end <= r) { apply(node, val); return; }
        int mid = (start + end) / 2;
        propagate(node);
        updateRange(node << 1, start, mid, l, r, val);
        updateRange(node << 1 | 1, mid + 1, end, l, r, val);
        pull(node);
    }

    long long queryMin(int node, int start, int end, int l, int r) {
        if (r < start || end < l) return (long long)4e18;
        if (l <= start && end <= r) return mn[node];
        int mid = (start + end) / 2;
        propagate(node);
        return min(queryMin(node << 1, start, mid, l, r),
                   queryMin(node << 1 | 1, mid + 1, end, l, r));
    }

    // Find first index in [l,r] where value == x. Returns -1 if none.
    int findFirstEq(int node, int start, int end, int l, int r, long long x) {
        if (r < start || end < l) return -1;
        // If x is not achievable in this segment, prune.
        if (x < mn[node] || x > mx[node]) return -1;

        if (start == end) {
            // Here mn==mx==value; since x in [mn,mx], it must equal.
            return start;
        }
        int mid = (start + end) / 2;
        propagate(node);

        int leftAns = findFirstEq(node << 1, start, mid, l, r, x);
        if (leftAns != -1) return leftAns;
        return findFirstEq(node << 1 | 1, mid + 1, end, l, r, x);
    }

public:
    LazySegmentTreeMin(const vector<long long>& arr) {
        n = (int)arr.size();
        mn.assign(4 * n + 5, 0);
        mx.assign(4 * n + 5, 0);
        lazy.assign(4 * n + 5, 0);
        if (n) build(arr, 1, 0, n - 1);
    }

    void add(int l, int r, long long val) {
        if (l > r) return;
        updateRange(1, 0, n - 1, l, r, val);
    }

    long long query(int l, int r) {
        if (l > r) return (long long)4e18;
        return queryMin(1, 0, n - 1, l, r);
    }

    // Convenience: whole array
    int find_first_equal(long long x) {
        if (n == 0) return -1;
        return findFirstEq(1, 0, n - 1, 0, n - 1, x);
    }

    // Range-restricted version
    int find_first_equal(int l, int r, long long x) {
        if (n == 0 || l > r) return -1;
        l = max(l, 0); r = min(r, n - 1);
        return findFirstEq(1, 0, n - 1, l, r, x);
    }
};