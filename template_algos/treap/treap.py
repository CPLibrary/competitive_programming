import random
from typing import Optional, Tuple, List

class TreapNode:
    def __init__(self, key: int):
        self.key: int = key
        self.priority: int = random.randint(1, 1 << 30)
        self.left: Optional['TreapNode'] = None
        self.right: Optional['TreapNode'] = None
        self.size: int = 1
        self.lazy: int = 0  # For range updates

    def update_size(self):
        self.size = 1
        if self.left:
            self.size += self.left.size
        if self.right:
            self.size += self.right.size

class Treap:
    def __init__(self):
        self.root: Optional[TreapNode] = None

    def push(self, node: Optional[TreapNode]):
        if node and node.lazy != 0:
            node.key += node.lazy  # Apply the lazy update to the current node
            if node.left:
                node.left.lazy += node.lazy
            if node.right:
                node.right.lazy += node.lazy
            node.lazy = 0

    def update(self, node: Optional[TreapNode]):
        if node:
            node.update_size()

    def rotate_right(self, p: TreapNode) -> TreapNode:
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
        self.root = self.treap_insert(self.root, key)

    def split_by_index(self, node: Optional[TreapNode], index: int) -> Tuple[Optional[TreapNode], Optional[TreapNode]]:
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

    def treap_range_decrement(self, node: Optional[TreapNode], r: int) -> Optional[TreapNode]:
        if not node or r <= 0:
            return node
        left, right = self.split_by_index(node, r)
        if left:
            left.lazy -= 1  # Decrement the first r elements
        node = self.merge(left, right)
        return node

    def range_decrement(self, r: int):
        self.root = self.treap_range_decrement(self.root, r)

    def bisect_right(self, x: int) -> int:
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
            return True

    def inorder_traversal(self) -> List[int]:
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