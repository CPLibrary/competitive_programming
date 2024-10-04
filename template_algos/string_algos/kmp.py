def compute_lps(pattern):
    """Compute the longest prefix suffix (LPS) array for KMP."""
    lps = [0] * len(pattern)
    length = 0
    for i in range(1, len(pattern)):
        while length > 0 and pattern[i] != pattern[length]:
            length = lps[length - 1]
        if pattern[i] == pattern[length]:
            length += 1
            lps[i] = length
    return lps

def kmp_search(text, pattern):
    """Perform KMP search of `pattern` in `text`."""
    lps = compute_lps(pattern)
    i = j = 0
    occurrences = []
    while i < len(text):
        if text[i] == pattern[j]:
            i += 1
            j += 1
            if j == len(pattern):
                occurrences.append(i - j)
                j = lps[j - 1]
        else:
            if j != 0:
                j = lps[j - 1]
            else:
                i += 1
    return occurrences
