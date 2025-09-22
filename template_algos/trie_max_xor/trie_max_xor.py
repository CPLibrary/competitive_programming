
class TrieNode:
    __slots__ = ("children", "count", "is_end")
    def __init__(self):
        self.children = [None, None]
        self.count = 0
        self.is_end = False

def getNode():
    return TrieNode()

def insert(root: TrieNode, key: int) -> None:
    p = root
    for j in range(30, -1, -1):
        bit = (key >> j) & 1
        if p.children[bit] is None:
            p.children[bit] = getNode()
        p = p.children[bit]
        p.count += 1
    p.is_end = True

def remove(root: TrieNode, key: int) -> None:
    p = root
    for j in range(30, -1, -1):
        bit = (key >> j) & 1
        p = p.children[bit]
        p.count -= 1
    p.is_end = True

def get_max_xor(root: TrieNode, key: int) -> int:
    """
    Returns key XOR best_partner, i.e., the maximum XOR value achievable
    against some number currently present in the trie (with count > 0).
    This mirrors the C++ logic exactly (tracking 'ans' starting from key
    and flipping bits in the same situations).
    """
    p = root
    ans = key
    for j in range(30, -1, -1):
        bit = (key >> j) & 1
        opp = bit ^ 1
        if p.children[opp] is not None and p.children[opp].count > 0:
            p = p.children[opp]
            if bit == 0:
                ans ^= (1 << j)
        else:
            p = p.children[bit]
            if bit == 1:
                ans ^= (1 << j)
    return ans