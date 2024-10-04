
def coordinate_compression(arr):
    """Compress coordinates to a smaller range."""
    sorted_unique = sorted(set(arr))
    mapping = {val: idx for idx, val in enumerate(sorted_unique)}
    return [mapping[x] for x in arr]
