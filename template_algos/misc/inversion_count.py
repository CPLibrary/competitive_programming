def count_inversions(arr):
    # Step 1: Coordinate Compression (Normalize array values to 1-based indices)
    sorted_arr = sorted(set(arr))
    rank = {value: i + 1 for i, value in enumerate(sorted_arr)}

    # Map array to normalized values
    normalized_arr = [rank[value] for value in arr]

    # Step 2: Fenwick Tree for inversion counting
    max_value = len(sorted_arr)
    fenwick_tree = [0] * (max_value + 1)

    def fenwick_update(index, delta):
        while index <= max_value:
            fenwick_tree[index] += delta
            index += index & -index

    def fenwick_query(index):
        sum_val = 0
        while index > 0:
            sum_val += fenwick_tree[index]
            index -= index & -index
        return sum_val

    # Count inversions
    inversion_count = 0
    for i in reversed(normalized_arr):
        # Count elements smaller than the current element
        inversion_count += fenwick_query(i - 1)
        # Add current element to the Fenwick Tree
        fenwick_update(i, 1)

    return inversion_count
