

class DSU {
public:
    int n, comp;
    vi root, rank, col;
    bool is_bipartite;
    DSU(int n) {
        this->n = n;
        comp = n;
        root.rsz(n, -1), rank.rsz(n, 1), col.rsz(n, 0);
        is_bipartite = true;
    }
    
    int find(int x) {
        if(root[x] == -1) return x;
        int p = find(root[x]);
        col[x] ^= col[root[x]];
        return root[x] = p;
    }

    bool merge(int a, int b) {
        int u = find(a);
        int v = find(b);
        if (u == v) {
            if(col[a] == col[b]) {
                is_bipartite = false;
            }
            return 0;
        }
        if(rank[u] < rank[v]) {
            swap(u, v);
            swap(a, b);
        }
        comp--;
        root[v] = u;
        rank[u] += rank[v];
        if(col[a] == col[b])
            col[v] ^= 1;
        return 1;
    }

    bool same(int u, int v) {
        return find(u) == find(v);
    }

    int get_rank(int x) {
        return rank[find(x)];
    }

    vvi get_group() {
        vvi ans(n);
        for(int i = 0; i < n; i++) {
            ans[find(i)].pb(i);
        }
        sort(all(ans), [](const vi& a, const vi& b) {return a.size() > b.size();});
        while(!ans.empty() && ans.back().empty()) ans.pop_back();
        return ans;
    }
};
