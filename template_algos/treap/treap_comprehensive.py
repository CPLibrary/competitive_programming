## this is slow but has a lot of fuctionality

import random
from typing import Optional, Tuple, List

class TreapNode:
    def __init__(self, key: int):
        self.key: int = key
        self.priority: int = random.randint(1, 1 << 30)
        self.left: Optional['TreapNode'] = None
        self.right: Optional['TreapNode'] = None
        self.size: int = 1
        self.sum: int = key
        self.min: int = key
        self.max: int = key
        self.lazy: int = 0       # For range increments/decrements
        self.set_lazy: Optional[int] = None  # For range setting

    def update_size(self):
        """
        Updates the size, sum, min, and max of the subtree rooted at this node.
        """
        self.size = 1
        self.sum = self.key
        self.min = self.key
        self.max = self.key

        if self.left:
            self.size += self.left.size
            self.sum += self.left.sum
            self.min = min(self.min, self.left.min)
            self.max = max(self.max, self.left.max)

        if self.right:
            self.size += self.right.size
            self.sum += self.right.sum
            self.min = min(self.min, self.right.min)
            self.max = max(self.max, self.right.max)


class Treap:
    def __init__(self):
        self.root: Optional[TreapNode] = None

    def push(self, node: Optional[TreapNode]):
        """
        Propagates the lazy updates (both additive and set) to the children and updates the current node's key, sum, min, and max.
        """
        if node is None:
            return

        if node.set_lazy is not None:
            # Apply the set_lazy operation
            node.key = node.set_lazy
            node.sum = node.set_lazy * node.size
            node.min = node.set_lazy
            node.max = node.set_lazy

            # Propagate to children
            if node.left:
                node.left.set_lazy = node.set_lazy
                node.left.lazy = 0  # Reset additive lazy
            if node.right:
                node.right.set_lazy = node.set_lazy
                node.right.lazy = 0  # Reset additive lazy

            node.set_lazy = None  # Reset after propagation

        if node.lazy != 0:
            # Apply the additive lazy operation
            node.key += node.lazy
            node.sum += node.lazy * node.size
            node.min += node.lazy
            node.max += node.lazy

            # Propagate to children
            if node.left:
                if node.left.set_lazy is not None:
                    node.left.set_lazy += node.lazy
                else:
                    node.left.lazy += node.lazy
            if node.right:
                if node.right.set_lazy is not None:
                    node.right.set_lazy += node.lazy
                else:
                    node.right.lazy += node.lazy

            node.lazy = 0  # Reset after propagation

    def update(self, node: Optional[TreapNode]):
        """
        Updates the size, sum, min, and max of the node based on its children.
        """
        if node:
            node.update_size()

    def rotate_right(self, p: TreapNode) -> TreapNode:
        """
        Performs a right rotation around node p.
        """
        self.push(p)
        q = p.left
        if not q:
            return p
        self.push(q)
        p.left = q.right
        q.right = p
        self.update(p)
        self.update(q)
        return q

    def rotate_left(self, p: TreapNode) -> TreapNode:
        """
        Performs a left rotation around node p.
        """
        self.push(p)
        q = p.right
        if not q:
            return p
        self.push(q)
        p.right = q.left
        q.left = p
        self.update(p)
        self.update(q)
        return q

    def treap_insert(self, node: Optional[TreapNode], key: int) -> TreapNode:
        """
        Recursively inserts a key into the treap rooted at node.
        """
        if not node:
            return TreapNode(key)
        self.push(node)
        if key < node.key:
            node.left = self.treap_insert(node.left, key)
            self.update(node)
            if node.left and node.left.priority > node.priority:
                node = self.rotate_right(node)
        else:
            node.right = self.treap_insert(node.right, key)
            self.update(node)
            if node.right and node.right.priority > node.priority:
                node = self.rotate_left(node)
        return node

    def insert(self, key: int):
        """
        Inserts a key into the treap.
        """
        self.root = self.treap_insert(self.root, key)

    def split_by_index(self, node: Optional[TreapNode], index: int) -> Tuple[Optional[TreapNode], Optional[TreapNode]]:
        """
        Splits the treap into two treaps:
        - Left treap contains the first 'index' elements.
        - Right treap contains the remaining elements.
        Zero-based indexing.
        """
        if not node:
            return (None, None)
        self.push(node)
        left_size = node.left.size if node.left else 0
        if index <= left_size:
            left, right = self.split_by_index(node.left, index)
            node.left = right
            self.update(node)
            return (left, node)
        else:
            left, right = self.split_by_index(node.right, index - left_size - 1)
            node.right = left
            self.update(node)
            return (node, right)

    def merge(self, left: Optional[TreapNode], right: Optional[TreapNode]) -> Optional[TreapNode]:
        """
        Merges two treaps into one and returns the new root.
        """
        self.push(left)
        self.push(right)
        if not left or not right:
            return left or right
        if left.priority > right.priority:
            left.right = self.merge(left.right, right)
            self.update(left)
            return left
        else:
            right.left = self.merge(left, right.left)
            self.update(right)
            return right

    def treap_range_decrement(self, node: Optional[TreapNode], l: int, r: int, value: int = 1) -> Optional[TreapNode]:
        """
        Decrements (or increments if value is positive) elements from index l to r (inclusive) by 'value'.
        Zero-based indexing.
        """
        if not node or l > r:
            return node
        # Split into three parts: left (< l), middle [l, r], right (> r)
        left, middle_right = self.split_by_index(node, l)
        middle, right = self.split_by_index(middle_right, r - l + 1)
        if middle:
            middle.lazy -= value  # Decrement by 'value'
        # Merge back the three parts
        node = self.merge(left, self.merge(middle, right))
        return node

    def range_decrement(self, l: int, r: int, value: int = 1):
        """
        Public method to decrement (or increment if value is positive) elements from index l to r (inclusive) by 'value'.
        Zero-based indexing.
        """
        self.root = self.treap_range_decrement(self.root, l, r, value)




    def treap_range_query_sum(self, node: Optional[TreapNode], l: int, r: int) -> int:
        """
        Returns the sum of elements from index l to r (inclusive).
        Zero-based indexing.
        """
        if not node or l > r:
            return 0
        left, middle_right = self.split_by_index(node, l)
        middle, right = self.split_by_index(middle_right, r - l + 1)
        total = middle.sum if middle else 0
        # Merge back
        node = self.merge(left, self.merge(middle, right))
        self.root = node
        return total

    def range_sum(self, l: int, r: int) -> int:
        """
        Public method to get the sum of elements from index l to r (inclusive).
        Zero-based indexing.
        """
        return self.treap_range_query_sum(self.root, l, r)

    def treap_range_query_min(self, node: Optional[TreapNode], l: int, r: int) -> Optional[int]:
        """
        Returns the minimum value of elements from index l to r (inclusive).
        Zero-based indexing.
        """
        if not node or l > r:
            return None
        left, middle_right = self.split_by_index(node, l)
        middle, right = self.split_by_index(middle_right, r - l + 1)
        minimum = middle.min if middle else None
        # Merge back
        node = self.merge(left, self.merge(middle, right))
        self.root = node
        return minimum

    def range_min(self, l: int, r: int) -> Optional[int]:
        """
        Public method to get the minimum of elements from index l to r (inclusive).
        Zero-based indexing.
        """
        return self.treap_range_query_min(self.root, l, r)

    def treap_range_query_max(self, node: Optional[TreapNode], l: int, r: int) -> Optional[int]:
        """
        Returns the maximum value of elements from index l to r (inclusive).
        Zero-based indexing.
        """
        if not node or l > r:
            return None
        left, middle_right = self.split_by_index(node, l)
        middle, right = self.split_by_index(middle_right, r - l + 1)
        maximum = middle.max if middle else None
        # Merge back
        node = self.merge(left, self.merge(middle, right))
        self.root = node
        return maximum

    def range_max(self, l: int, r: int) -> Optional[int]:
        """
        Public method to get the maximum of elements from index l to r (inclusive).
        Zero-based indexing.
        """
        return self.treap_range_query_max(self.root, l, r)

    def treap_range_set(self, node: Optional[TreapNode], l: int, r: int, value: int) -> Optional[TreapNode]:
        """
        Sets elements from index l to r (inclusive) to 'value'.
        Zero-based indexing.
        """
        if not node or l > r:
            return node
        # Split into three parts: left (< l), middle [l, r], right (> r)
        left, middle_right = self.split_by_index(node, l)
        middle, right = self.split_by_index(middle_right, r - l + 1)
        if middle:
            middle.set_lazy = value  # Set elements in [l, r] to 'value'
            middle.lazy = 0         # Reset any pending additive operations
            self.push(middle)       # Apply the set_lazy immediately
            self.update(middle)
        # Merge back the three parts
        node = self.merge(left, self.merge(middle, right))
        return node

    def range_set(self, l: int, r: int, value: int):
        """
        Public method to set elements from index l to r (inclusive) to 'value'.
        Zero-based indexing.
        """
        self.root = self.treap_range_set(self.root, l, r, value)

    def bisect_right(self, x: int) -> int:
        """
        Returns the number of elements in the treap that are <= x.
        Equivalent to bisect_right in a sorted list.
        """
        return self._bisect_right(self.root, x)

    def _bisect_right(self, node: Optional[TreapNode], x: int) -> int:
        if not node:
            return 0
        self.push(node)
        if x < node.key:
            return self._bisect_right(node.left, x)
        else:
            left_size = node.left.size if node.left else 0
            return left_size + 1 + self._bisect_right(node.right, x)

    def contains(self, x: int) -> bool:
        """
        Checks whether the value x is present in the treap.
        Returns True if present, False otherwise.
        """
        return self._contains(self.root, x)

    def _contains(self, node: Optional[TreapNode], x: int) -> bool:
        if not node:
            return False
        self.push(node)
        if x < node.key:
            return self._contains(node.left, x)
        elif x > node.key:
            return self._contains(node.right, x)
        else:
            return True  # Found the value

    def treap_remove_at(self, node: Optional[TreapNode], index: int) -> Optional[TreapNode]:
        """
        Removes the element at the given zero-based index.
        """
        if not node:
            return None
        self.push(node)
        left_size = node.left.size if node.left else 0
        if index < left_size:
            node.left = self.treap_remove_at(node.left, index)
            self.update(node)
        elif index > left_size:
            node.right = self.treap_remove_at(node.right, index - left_size - 1)
            self.update(node)
        else:
            # Node to be removed found
            node = self.merge(node.left, node.right)
        return node

    def remove_at(self, index: int):
        """
        Removes the element at the given zero-based index.
        """
        if index < 0 or (self.root and index >= self.root.size) or not self.root:
            print(f"Index {index} is out of bounds. No removal performed.")
            return
        self.root = self.treap_remove_at(self.root, index)

    def treap_remove_key(self, node: Optional[TreapNode], key: int) -> Optional[TreapNode]:
        """
        Removes one occurrence of the key from the treap.
        If duplicates exist, only one is removed.
        """
        if not node:
            return None
        self.push(node)
        if key < node.key:
            node.left = self.treap_remove_key(node.left, key)
            self.update(node)
        elif key > node.key:
            node.right = self.treap_remove_key(node.right, key)
            self.update(node)
        else:
            # Node to be deleted found
            node = self.merge(node.left, node.right)
        return node

    def remove_key(self, key: int):
        """
        Removes one occurrence of the specified key from the treap.
        If duplicates exist, only one instance is removed.
        """
        self.root = self.treap_remove_key(self.root, key)

    def inorder_traversal(self) -> List[int]:
        """
        Returns the sorted list of elements in the treap.
        """
        result: List[int] = []
        self._inorder_traversal(self.root, result)
        return result

    def _inorder_traversal(self, node: Optional[TreapNode], result: List[int]):
        if not node:
            return
        self.push(node)
        self._inorder_traversal(node.left, result)
        result.append(node.key)
        self._inorder_traversal(node.right, result)


    def get_at(self, index: int) -> Optional[int]:
        """
        Retrieves the value at the specified zero-based index.
        Returns the key if the index is valid, otherwise returns None.
        """
        if index < 0 or not self.root or index >= self.root.size:
            print(f"Index {index} is out of bounds.")
            return None
        return self._get_at(self.root, index)

    def _get_at(self, node: TreapNode, index: int) -> int:
        """
        Helper method to recursively find the key at the given index.
        """
        self.push(node)  # Ensure all lazy updates are applied
        left_size = node.left.size if node.left else 0

        if index < left_size:
            return self._get_at(node.left, index)
        elif index == left_size:
            return node.key
        else:
            return self._get_at(node.right, index - left_size - 1)



def insert(value,treap,N):
    index = 0
    l = value
    r = N+value
    best_ans = N+value
    while l <= r:
        mid = l +(r-l)//2
        index = treap.bisect_right(mid)
        if index + value <= mid:
            best_ans = mid
            r = mid-1
        else:
            l = mid+1
    treap.range_decrement(0,treap.bisect_right(best_ans)-1,1)
    treap.insert(best_ans)
    #print(treap.inorder_traversal())


def solve(N,G,arr):

    treap = Treap()

    for i,x in enumerate(arr):
        insert(x,treap,i+10)

    zeb = list(treap.inorder_traversal())
    indices = list(range(len(arr)))[::-1]

    best_dist = math.inf
    best_index = None
    for index,value in zip(indices,zeb):
        if abs(G-value) < best_dist:
            best_dist = abs(G-value)
            best_index = index+1
        elif abs(G-value) == best_dist:
            best_index = min(best_index,index+1)
    return [best_index,best_dist]
