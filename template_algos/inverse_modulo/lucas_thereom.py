def lucas_thereom(n,m,p):
    def n_choose_k(N,K):
        if K > N:
            return 0
        return (fac[N]*ifac[N-K]*ifac[K])%MOD
    n_arr = []
    m_arr = []

    while n > 0:
        n_arr.append(n%p)
        n = n//p
    while m > 0:
        m_arr.append(m%p)
        m = m //p

    m_arr = m_arr + [0]*max(0,len(n_arr)-len(m_arr))
    n_arr = n_arr + [0]*max(0,len(m_arr)-len(n_arr))

    ans = 1
    for ni,mi in zip(n_arr,m_arr):
        ans *= n_choose_k(ni,mi)
        ans %= p
    return ans 
