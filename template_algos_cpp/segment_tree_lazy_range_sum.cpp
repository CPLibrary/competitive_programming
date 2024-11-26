#include <iostream>
#include <vector>

using namespace std;

class LazySegmentTree {
private:
    vector<long long> tree, lazy;
    int n;

    void build(vector<long long>& arr, int node, int start, int end) {
        if (start == end) {
            tree[node] = arr[start];
        } else {
            int mid = (start + end) / 2;
            build(arr, 2 * node, start, mid);
            build(arr, 2 * node + 1, mid + 1, end);
            tree[node] = tree[2 * node] + tree[2 * node + 1];
        }
    }

    void propagate(int node, int start, int end) {
        if (lazy[node] != 0) {
            tree[node] += lazy[node] * (end - start + 1);
            if (start != end) {
                lazy[2 * node] += lazy[node];
                lazy[2 * node + 1] += lazy[node];
            }
            lazy[node] = 0;
        }
    }

    void updateRange(int node, int start, int end, int l, int r, long long val) {
        propagate(node, start, end);
        if (start > end || start > r || end < l) return;

        if (start >= l && end <= r) {
            lazy[node] += val;
            propagate(node, start, end);
            return;
        }

        int mid = (start + end) / 2;
        updateRange(2 * node, start, mid, l, r, val);
        updateRange(2 * node + 1, mid + 1, end, l, r, val);
        tree[node] = tree[2 * node] + tree[2 * node + 1];
    }

    long long queryRange(int node, int start, int end, int l, int r) {
        propagate(node, start, end);
        if (start > end || start > r || end < l) return 0;

        if (start >= l && end <= r) return tree[node];

        int mid = (start + end) / 2;
        long long leftSum = queryRange(2 * node, start, mid, l, r);
        long long rightSum = queryRange(2 * node + 1, mid + 1, end, l, r);
        return leftSum + rightSum;
    }

public:
    LazySegmentTree(vector<long long>& arr) {
        n = arr.size();
        tree.resize(4 * n, 0LL);
        lazy.resize(4 * n, 0LL);
        build(arr, 1, 0, n - 1);
    }

    void update(int l, int r, long long val) {
        updateRange(1, 0, n - 1, l, r, val);
    }

    long long query(int l, int r) {
        return queryRange(1, 0, n - 1, l, r);
    }
};

int main() {
    int N;
    int M;
    cin >> N;
    cin >> M;
    vector<long long> arr = {1LL, 2LL, 3LL, 4LL, 5LL};
    LazySegmentTree segtree(arr);

    cout << "Initial sum (0 to 4): " << segtree.query(0, 4) << endl; // 15

    segtree.update(0, 2, 3LL); // Add 3 to elements 0, 1, 2
    cout << "Sum after range update (0 to 4): " << segtree.query(0, 4) << endl; // 24

    cout << "Sum of range (1 to 3): " << segtree.query(1, 3) << endl; // 18

    segtree.update(2, 4, 2LL); // Add 2 to elements 2, 3, 4
    cout << "Sum after another update (0 to 4): " << segtree.query(0, 4) << endl; // 30

    return 0;
}

