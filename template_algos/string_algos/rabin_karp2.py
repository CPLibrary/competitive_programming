

mod = 10**9 + 7
d = 111
mod1 = 10**9 + 9
d1 = 113
N = 10**5 + 10

def compute_prefix(prime,d):
    prefix = [1]
    for i in range(N+1):
        prefix.append((prefix[-1]*d)%prime)
    return prefix

prefix = compute_prefix(mod,d)
prefix1 = compute_prefix(mod1,d1)

def compute_hash(target,prime,d):
    arr = [0]
    hash_value = 0
    for char in target:
        hash_value = ((hash_value*d)%prime + ord(char) )%prime
        arr.append(hash_value)
    return arr

### use r+1 if you want to include r
def compute_substring_hash(l, r, arr, prefix, prime):
    hash_value = (arr[r] - arr[l] * prefix[r - l]) % prime
    if hash_value < 0:
        hash_value += prime
    return hash_value

def compute(patterns,prime, d):
    seen = set()
    for word in patterns:
        hash_value = 0
        for char in word:
            hash_value = ((hash_value*d)%prime + ord(char) )%prime
            seen.add(hash_value)
    return seen
