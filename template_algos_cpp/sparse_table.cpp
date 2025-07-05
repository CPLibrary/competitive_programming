



#include <bits/stdc++.h>
using namespace std;

vector<int> build_logs(int n) {
    vector<int> log2(n+1);
    log2[1] = 0;
    for (int i = 2; i <= n; ++i)
        log2[i] = log2[i/2] + 1;
    return log2;
}

vector<vector<int>> build_sparse_table(const vector<int>& arr, vector<int>& log2) {
    int n = arr.size();
    log2 = build_logs(n);
    int K = log2[n] + 1;

    vector<vector<int>> st(K, vector<int>(n));
    for (int i = 0; i < n; ++i)
        st[0][i] = arr[i];

    for (int k = 1; k < K; ++k) {
        int len = 1 << (k-1);
        for (int i = 0; i + (1<<k) <= n; ++i) {
            st[k][i] = gcd(st[k-1][i], st[k-1][i + len]);
        }
    }
    return st;
}

int query_table(const vector<vector<int>>& st, const vector<int>& log2, int L, int R) {
    int len = R - L + 1;
    int k = log2[len];
    return gcd(st[k][L], st[k][R - (1<<k) + 1]);
}

int main(){
    ios::sync_with_stdio(false);
    cin.tie(nullptr);

    vector<int> arr = {12, 15, 18, 6, 9, 3, 21};
    vector<int> log2;
    auto st = build_sparse_table(arr, log2);

    cout << query_table(st, log2, 1, 4) << "\n";

    cout << query_table(st, log2, 2, 6) << "\n";

    return 0;
}