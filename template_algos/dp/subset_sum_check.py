

def subset_sum(arr, target):
    """Check if any subset sums up to the target using Bitmask DP."""
    dp = 1
    for num in arr:
        dp |= dp << num
    return (dp >> target) & 1
    
