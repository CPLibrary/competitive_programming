


from math import log2
from math import gcd

def build_logs(n):
    log = [0] * (n + 1)
    for i in range(2, n + 1):
        log[i] = log[i // 2] + 1
    return log

def build_sparse_table(arr,fn):
    n = len(arr)
    log = build_logs(n)
    K = log[n] + 1

    st = [[0] * n for _ in range(K)]
    for i in range(n):
        st[0][i] = arr[i]

    for k in range(1, K):
        length = 1 << (k - 1)
        for i in range(n - (1 << k) + 1):
            st[k][i] = fn(st[k - 1][i], st[k - 1][i + length])

    return st, log

def query_table(st, log, L, R, fn):
    length = R - L + 1
    k = log[length]
    return fn(st[k][L], st[k][R - (1 << k) + 1])


st,log = build_gcd_sparse_table(nums,gcd)
query_table(st,log,j,i,gcd)