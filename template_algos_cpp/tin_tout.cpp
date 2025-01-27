

int timer = 0;

void recur_fn(int node, int parent,  vector<vector<int>>& graph, vector<int>& arr, vector<int>& tin, vector<int>& tout, vector<int>& new_arr) {
    tin[node] = timer;
    timer += 1;
    new_arr.push_back(arr[node]);
    for (int child : graph[node]) {
        if (child == parent) continue;
        recur_fn(child,node,graph,arr,tin,tout,new_arr);
    }

    tout[node] = timer-1;
}

int solve(int N, vector<int>& arr, vector<vector<int>>& graph) {
    timer = 0;
    vector<int> tin(N);
    vector<int> tout(N);
    vector<int> new_arr;


    recur_fn(0,-1,graph,arr, tin,tout,new_arr);

    vector<int> pre(N+1);

    for (int i = 0; i < new_arr.size(); ++i) {
        pre[i+1] = max(pre[i],new_arr[i]);
    }
    vector<int> suff(N+1);
    for (int i = new_arr.size()-1; i >= 0; i--) {
        suff[i] = max(suff[i+1],new_arr[i]);
    }

    int ans = 0;
    int max_weight = 0;
    for (int i = 0; i < arr.size(); ++i) {
        if (max(pre[tin[i]],suff[tout[i]+1]) > arr[i]) {
            if (arr[i] > max_weight) {
                max_weight = arr[i];
                ans = i+1;
            }
        }
    }

    return ans;

}