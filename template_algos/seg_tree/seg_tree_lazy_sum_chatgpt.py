

class LazySegTreeSum:
    """Range add, range sum. 0-indexed on the external interface: [l, r)."""

    def __init__(self, arr):
        self.n = len(arr)
        self.size = 1 << (self.n - 1).bit_length()
        self.h = self.size.bit_length() - 1  # height

        # 1-indexed tree arrays; index 0 unused
        self.data = [0] * (2 * self.size)
        self.lazy = [0] * (2 * self.size)

        # build leaves
        self.data[self.size:self.size + self.n] = arr
        # build internal nodes
        for i in range(self.size - 1, 0, -1):
            self.data[i] = self.data[2 * i] + self.data[2 * i + 1]

    def _seg_len(self, idx: int) -> int:
        # node at depth d covers size / 2^d elements, where d = bit_length(idx)-1
        return self.size >> (idx.bit_length() - 1)

    def _apply(self, idx: int, add: int, seg_len: int):
        self.data[idx] += add * seg_len
        self.lazy[idx] += add

    def _push(self, idx: int):
        add = self.lazy[idx]
        if add == 0:
            return
        self.lazy[idx] = 0
        half = self._seg_len(idx) // 2
        self._apply(2 * idx, add, half)
        self._apply(2 * idx + 1, add, half)

    def _push_path(self, idx: int):
        for s in range(self.h, 0, -1):
            self._push(idx >> s)

    def _pull(self, idx: int):
        while idx > 1:
            idx >>= 1
            seg_len = self._seg_len(idx)
            # children already include their own lazy effects; add this node's pending lazy too
            self.data[idx] = self.data[2 * idx] + self.data[2 * idx + 1] + self.lazy[idx] * seg_len

    def add(self, l: int, r: int, x: int):
        if l >= r:
            return
        l0 = l + self.size
        r0 = r + self.size

        # make boundary paths "clean" so pulls are correct
        self._push_path(l0)
        self._push_path(r0 - 1)

        L, R = l0, r0
        seg_len = 1  # at leaf level

        while L < R:
            if L & 1:
                self._apply(L, x, seg_len)
                L += 1
            if R & 1:
                R -= 1
                self._apply(R, x, seg_len)
            L >>= 1
            R >>= 1
            seg_len <<= 1

        self._pull(l0)
        self._pull(r0 - 1)

    def query(self, l: int, r: int) -> int:
        if l >= r:
            return 0
        l += self.size
        r += self.size

        self._push_path(l)
        self._push_path(r - 1)

        res = 0
        while l < r:
            if l & 1:
                res += self.data[l]
                l += 1
            if r & 1:
                r -= 1
                res += self.data[r]
            l >>= 1
            r >>= 1
        return res