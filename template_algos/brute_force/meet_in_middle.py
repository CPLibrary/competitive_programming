
from itertools import combinations

def meet_in_middle(arr, target):
    """Count the number of subsets that sum to target using Meet in the Middle."""
    n = len(arr)
    left = arr[:n//2]
    right = arr[n//2:]
    sum_left = [sum(comb) for r in range(len(left)+1) for comb in combinations(left, r)]
    sum_right = [sum(comb) for r in range(len(right)+1) for comb in combinations(right, r)]
    sum_right.sort()
    count = 0
    for s in sum_left:
        count += bisect.bisect_right(sum_right, target - s) - bisect.bisect_left(sum_right, target - s)
    return count
