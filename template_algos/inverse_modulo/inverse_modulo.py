

MOD = 10 ** 9 + 7
MX = 10 ** 5 + 1

fac = [1] * MX
for i in range(1, MX):
    fac[i] = fac[i-1] * i % MOD
ifac = [pow(fac[MX - 1], MOD-2, MOD)] * MX
for i in range(MX - 1, 0, -1):
    ifac[i-1] = ifac[i] * i % MOD



def n_choose_k(N,K):
    return (fac[N]*ifac[N-K]*ifac[K])%MOD


def mod_inverse(x, mod):
    return power(x, mod - 2, mod)
