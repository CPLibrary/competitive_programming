

def matrix_mult(a, b, mod):
    """Multiply two matrices a and b under modulo `mod`."""
    n, m, p = len(a), len(a[0]), len(b[0])
    result = [[0] * p for _ in range(n)]
    for i in range(n):
        for j in range(p):
            for k in range(m):
                result[i][j] = (result[i][j] + a[i][k] * b[k][j]) % mod
    return result

def matrix_pow(mat, power, mod):
    """Raise matrix `mat` to the power `power` under modulo `mod`."""
    result = [[int(i == j) for j in range(len(mat))] for i in range(len(mat))]
    while power > 0:
        if power & 1:
            result = matrix_mult(result, mat, mod)
        mat = matrix_mult(mat, mat, mod)
        power >>= 1
    return result
