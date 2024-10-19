const int MAXN = 1000005; // Maximum number of nodes
const int LOG = 22;      // Because 2^20 > 10^6

struct LCA {
    int n; // Number of nodes
    int LOG_LEVEL; // Number of levels in binary lifting
    vector<vector<int>> adj; // Adjacency list
    vector<int> depth; // Depth of each node
    vector<vector<int>> up; // Ancestor table

    // Constructor
    LCA(int nodes, const vector<vector<int>> &adj_list, int root = 0) {
        n = nodes;
        adj.assign(n, vector<int>());
        for(int i = 0; i < n; ++i){
            adj[i] = adj_list[i];
        }

        LOG_LEVEL = ceil(log2(n)) + 1;
        depth.assign(n, 0);
        up.assign(LOG_LEVEL, vector<int>(n, -1));

        // Initialize ancestor table
        compute_depth_and_ancestors(root);
    }

    // Function to compute depth and fill the first ancestor (2^0)
    void compute_depth_and_ancestors(int root) {
        // Iterative DFS using stack
        stack<pair<int, int>> s; // Pair of (node, parent)
        s.push({root, -1});
        depth[root] = 0;
        up[0][root] = -1; // Root has no parent

        while(!s.empty()){
            pair<int, int> current = s.top();
            s.pop();
            int node = current.first;
            int parent = current.second;

            // Iterate over all children
            for(auto &child : adj[node]){
                if(child == parent) continue;
                depth[child] = depth[node] + 1;
                up[0][child] = node;
                s.push({child, node});
            }
        }

        // Fill the ancestor table
        for(int k = 1; k < LOG_LEVEL; ++k){
            for(int v = 0; v < n; ++v){
                if(up[k-1][v] != -1){
                    up[k][v] = up[k-1][up[k-1][v]];
                }
                else{
                    up[k][v] = -1;
                }
            }
        }
    }

    // Function to find LCA of two nodes
    int get_lca(int u, int v) const {
        if(depth[u] < depth[v]) swap(u, v);

        // Bring u to the same depth as v
        for(int k = LOG_LEVEL -1; k >=0; --k){
            if(up[k][u] != -1 && depth[up[k][u]] >= depth[v]){
                u = up[k][u];
            }
        }

        if(u == v) return u;

        // Lift both u and v up until their ancestors diverge
        for(int k = LOG_LEVEL -1; k >=0; --k){
            if(up[k][u] != -1 && up[k][u] != up[k][v]){
                u = up[k][u];
                v = up[k][v];
            }
        }

        // Now u and v are children of LCA
        return up[0][u];
    }

    // Function to compute distance between two nodes
    int distance_between(int u, int v) const {
        int lca = get_lca(u, v);
        return depth[u] + depth[v] - 2 * depth[lca];
    }
};

LCA lca_struct(N,mat,0); 
