import typing

def _ceil_pow2(n: int) -> int:
    """Small helper to compute ceil(log2(n))"""
    x = 0
    while (1 << x) < n:
        x += 1
    return x

class LazySegTree:
    def __init__(
            self,
            op: typing.Callable[[typing.Any, typing.Any], typing.Any],
            e: typing.Any,
            mapping: typing.Callable[[typing.Any, typing.Any], typing.Any],
            composition: typing.Callable[[typing.Any, typing.Any], typing.Any],
            id_: typing.Any,
            v: typing.Union[int, typing.List[typing.Any]]
    ) -> None:
        self._op = op           # e.g. lambda a, b: a + b
        self._e = e            # e.g. 0
        self._mapping = mapping # e.g. lambda f, x: x + f
        self._composition = composition # e.g. lambda f, g: f + g
        self._id = id_         # e.g. 0

        if isinstance(v, int):
            v = [e] * v

        self._n = len(v)
        self._log = _ceil_pow2(self._n)
        self._size = 1 << self._log
        self._d = [e] * (2 * self._size)
        self._lz = [self._id] * self._size

        # Build initial tree
        for i in range(self._n):
            self._d[self._size + i] = v[i]
        for i in range(self._size - 1, 0, -1):
            self._update(i)

    def _update(self, k: int) -> None:
        """Updates node k by recalculating its value from children."""
        self._d[k] = self._op(self._d[2 * k], self._d[2 * k + 1])

    def _all_apply(self, k: int, f: typing.Any) -> None:
        """Applies the lazy value f to node k."""
        self._d[k] = self._mapping(f, self._d[k])
        if k < self._size:
            self._lz[k] = self._composition(f, self._lz[k])

    def _push(self, k: int) -> None:
        """Push down lazy value from node k to its children."""
        self._all_apply(2 * k, self._lz[k])
        self._all_apply(2 * k + 1, self._lz[k])
        self._lz[k] = self._id

    def set(self, p: int, x: typing.Any) -> None:
        """Set the element at index p to x."""
        assert 0 <= p < self._n
        p += self._size
        # Push lazy values on the path from root to p
        for i in range(self._log, 0, -1):
            self._push(p >> i)
        # Update leaf
        self._d[p] = x
        # Rebuild the tree upwards
        for i in range(1, self._log + 1):
            self._update(p >> i)

    def get(self, p: int) -> typing.Any:
        """Return the element at index p."""
        assert 0 <= p < self._n
        p += self._size
        # Push lazy values on the path from root to p
        for i in range(self._log, 0, -1):
            self._push(p >> i)
        return self._d[p]

    def prod(self, left: int, right: int) -> typing.Any:
        """
        Range query on the interval [left, right).
        In this sum example: sum of elements from index left to right-1.
        """
        assert 0 <= left <= right <= self._n
        if left == right:
            return self._e

        left += self._size
        right += self._size

        # Push lazy propagation down for partial blocks
        for i in range(self._log, 0, -1):
            if ((left >> i) << i) != left:
                self._push(left >> i)
            if ((right >> i) << i) != right:
                self._push((right - 1) >> i)

        sml = self._e
        smr = self._e
        # Merge over segments
        while left < right:
            if left & 1:
                sml = self._op(sml, self._d[left])
                left += 1
            if right & 1:
                right -= 1
                smr = self._op(self._d[right], smr)
            left >>= 1
            right >>= 1
        return self._op(sml, smr)

    def all_prod(self) -> typing.Any:
        """Returns the result of the operation over the entire array."""
        return self._d[1]

    def apply(self, left: int, right: typing.Optional[int] = None,
              f: typing.Optional[typing.Any] = None) -> None:
        """
        If right is None: apply f to element at index left.
        Otherwise, apply f to all elements in the interval [left, right).
        """
        assert f is not None

        if right is None:
            p = left
            assert 0 <= p < self._n
            p += self._size
            # Push lazy values down to p
            for i in range(self._log, 0, -1):
                self._push(p >> i)
            # Apply f
            self._d[p] = self._mapping(f, self._d[p])
            # Update parents
            for i in range(1, self._log + 1):
                self._update(p >> i)
        else:
            assert 0 <= left <= right <= self._n
            if left == right:
                return

            left += self._size
            right += self._size

            # Push lazy values for partial blocks
            for i in range(self._log, 0, -1):
                if ((left >> i) << i) != left:
                    self._push(left >> i)
                if ((right >> i) << i) != right:
                    self._push((right - 1) >> i)

            l2 = left
            r2 = right
            # Apply f in the range
            while left < right:
                if left & 1:
                    self._all_apply(left, f)
                    left += 1
                if right & 1:
                    right -= 1
                    self._all_apply(right, f)
                left >>= 1
                right >>= 1

            # Rebuild parents
            left = l2
            right = r2
            for i in range(1, self._log + 1):
                if ((left >> i) << i) != left:
                    self._update(left >> i)
                if ((right >> i) << i) != right:
                    self._update((right - 1) >> i)

    # For completeness, examples of max_right and min_left are in the original code
    # but we won't focus on them in this example.

def main():
    # Define the operations for range-sum queries + range-add updates.
    def op(a, b):
        return a + b

    e = 0  # Identity for sum is 0

    def mapping(lazy_val, seg_val):
        # 'lazy_val' is the increment to add
        # 'seg_val' is the node's current value
        return seg_val + lazy_val

    def composition(f, g):
        # Combine two lazy values (just sum them)
        return f + g

    id_ = 0  # Identity for the lazy operation is 0 (adding 0 changes nothing)

    # Example array
    v = [1, 2, 3, 4, 5]

    # Initialize segment tree
    seg = LazySegTree(op, e, mapping, composition, id_, v)

    print("Initial array:", v)
    print("Initial all_prod (sum of all):", seg.all_prod())

    # Range-sum query on [0, 5)
    print("prod(0, 5):", seg.prod(0, 5))  # should be 1+2+3+4+5 = 15

    # Apply +10 to the range [1, 4) => affects indices 1, 2, 3
    seg.apply(1, 4, 10)
    # Now array is effectively [1, (2+10), (3+10), (4+10), 5] = [1, 12, 13, 14, 5]
    print("After applying +10 to [1,4): prod(0,5) =", seg.prod(0, 5))  # 1+12+13+14+5 = 45

    # Get the value at index 3
    print("get(3):", seg.get(3))  # should be 14

    # Set index 2 to 100
    seg.set(2, 100)
    # Now array is effectively [1, 12, 100, 14, 5]
    print("After set(2, 100): prod(0,5) =", seg.prod(0, 5))  # 1+12+100+14+5 = 132

if __name__ == "__main__":
    main()
