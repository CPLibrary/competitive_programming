


def extended_gcd(a, b):
    """returns gcd(a, b), s, r s.t. a * s + b * r == gcd(a, b)"""
    s, old_s = 0, 1
    r, old_r = b, a
    while r:
        q = old_r // r
        old_r, r = r, old_r - q * r
        old_s, s = s, old_s - q * s
    return old_r, old_s, (old_r - old_s * a) // b if b else 0



g, s, t = extended_gcd(15, 25)
# For the equation to have a solution, 5 must be divisible by gcd(15, 25)
if 5 % g == 0:
    # Multiply the coefficients by 5/g to get a particular solution
    factor = 5 // g
    x = s * factor
    y = t * factor
    print("A solution to 15x + 25y = 5 is: x =", x, ", y =", y)
else:
    print("No solution exists for 15x + 25y = 5")


def equation_solving(x_coef, y_coef, ans):
    ### solves AX + BY = C for X and Y
    def extended_gcd(a, b):
        """returns gcd(a, b), s, r s.t. a * s + b * r == gcd(a, b)"""
        s, old_s = 0, 1
        r, old_r = b, a
        while r:
            q = old_r // r
            old_r, r = r, old_r - q * r
            old_s, s = s, old_s - q * s
        return old_r, old_s, (old_r - old_s * a) // b if b else 0

    g, s, t = extended_gcd(15, 25)
    # For the equation to have a solution, 5 must be divisible by gcd(15, 25)
    if ans % g == 0:
        # Multiply the coefficients by 5/g to get a particular solution
        factor = ans // g
        x = s * factor
        y = t * factor
        print("A solution to {}x + {}y = {} is: x =".format(x_coef, y_coef, ans), x, ", y =", y)
        return s, t
    else:
        print("No solution exists for 15x + 25y = 5")
        return math.inf, math.inf