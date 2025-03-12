def manacher(s):
    """Find all palindromic substrings in linear time using Manacher's algorithm."""
    A = '@#' + '#'.join(s) + '#$'
    Z = [0] * len(A)
    center = right = 0
    for i in range(1, len(A) - 1):
        if i < right:
            Z[i] = min(right - i, Z[2 * center - i])
        while A[i + Z[i] + 1] == A[i - Z[i] - 1]:
            Z[i] += 1
        if i + Z[i] > right:
            center, right = i, i + Z[i]
    return Z



def longest_palindrome_from_manacher(s):
    # Compute the manacher array for s
    Z = manacher(s)
    max_len = 0
    center_index = 0
    for i, radius in enumerate(Z):
        if radius > max_len:
            max_len = radius
            center_index = i
    # Map the center in the modified string back to the original string.
    start = (center_index - max_len) // 2
    return s[start:start + max_len]
