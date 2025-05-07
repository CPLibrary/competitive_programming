


set<pair<int,int>> cur;

long long ans;

int mag(pii x) {
    return x.second-x.first+1;
}

void rem(int a, int b) {
    while (1) {
        auto it = cur.lower_bound({a,-MOD});
        if (it == cur.end() || it->first > b) break;
        int B = it->second;
        ans -= mag(*it); cur.erase(it);
        if (B > b) {
            cur.insert({b+1,B});
            ans += B-b;
        }
    }

    auto it = cur.lower_bound({a,-MOD});
    if (it == cur.begin()) return;
    it = prev(it);
    if (it->second < a) return;
    else if (it->second > b) {
        int A = it->first, B = it->second;
        ans -= mag(*it);
        cur.erase(it);
        cur.insert({A,a-1});
        cur.insert({b+1,B});
        ans += a-A;
        ans += B-b;
    } else {
        int A = it->first;
        ans -= mag(*it);
        cur.erase(it);
        cur.insert({A,a-1});
        ans += a-A;
    }
}

void upd(int a, int b, int c) {
    rem(a,b);
    if (c == 2) {
        ans += b-a+1;
        cur.insert({a,b});
    }
}

void solve(int Q, int N, vector<vector<int>> mat_q) {
    ans = 0;
    upd(1,N,2);


    //cout << "ans" << ans << endl;
    for (vector<int>& zeb : mat_q) {
        upd(zeb[1],zeb[2],zeb[0]);
        cout << ans << endl;
    }

    return;
}