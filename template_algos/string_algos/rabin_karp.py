import sys

class RabinKarp:
    def __init__(self, pattern, base=256, mod=10**9 + 7):
        self.pattern = pattern
        self.m = len(pattern)
        self.base = base
        self.mod = mod
        self.pattern_hash = self._compute_hash(pattern)
        self.highest_power = pow(self.base, self.m-1, self.mod)  # base^(m-1) % mod

    def _compute_hash(self, s):
        h = 0
        for char in s:
            h = (h * self.base + ord(char)) % self.mod
        return h

    def search(self, text):
        n = len(text)
        m = self.m
        if m > n:
            return []

        text_hash = self._compute_hash(text[:m])
        occurrences = []
        if text_hash == self.pattern_hash and text[:m] == self.pattern:
            occurrences.append(0)

        for i in range(1, n - m + 1):
            leading_char = ord(text[i - 1])
            trailing_char = ord(text[i + m - 1])
            # Remove leading char, add trailing char
            text_hash = (text_hash - leading_char * self.highest_power) % self.mod
            text_hash = (text_hash * self.base + trailing_char) % self.mod
            if text_hash == self.pattern_hash:
                if text[i:i + m] == self.pattern:
                    occurrences.append(i)
        return occurrences

def main():
    # Read input from standard input
    import sys
    input = sys.stdin.read
    data = input().split()
    if len(data) < 2:
        print("Please provide both text and pattern.")
        return
    text = data[0]
    pattern = data[1]
    rk = RabinKarp(pattern)
    occurrences = rk.search(text)
    print(len(occurrences))
    if occurrences:
        print(' '.join(map(str, occurrences)))

### single pattern

pattern = "abc"
text = "abcabcabc"
rk = RabinKarp(pattern, text)
occurrences = rk.search()
print(f"Pattern '{pattern}' found at positions: {occurrences}")  # Output: [0, 3, 6]


### multiple pattern
patterns = ["abc", "bc", "a"]
text = "abcabcabc"
result = multiple_rabin_karp(patterns, text)
for pat in patterns:
    print(f"Pattern '{pat}' found at positions: {result[pat]}")



### double rabin karp

class DoubleRabinKarp:
    def __init__(self, pattern, base1=256, mod1=10**9 + 7, base2=257, mod2=10**9 + 9):
        self.pattern = pattern
        self.m = len(pattern)
        self.base1 = base1
        self.mod1 = mod1
        self.base2 = base2
        self.mod2 = mod2
        self.pattern_hash1 = self._compute_hash(pattern, self.base1, self.mod1)
        self.pattern_hash2 = self._compute_hash(pattern, self.base2, self.mod2)
        self.highest_power1 = pow(self.base1, self.m-1, self.mod1)
        self.highest_power2 = pow(self.base2, self.m-1, self.mod2)

    def _compute_hash(self, s, base, mod):
        h = 0
        for char in s:
            h = (h * base + ord(char)) % mod
        return h

    def search(self, text):
        n = len(text)
        m = self.m
        if m > n:
            return []

        hash1 = self._compute_hash(text[:m], self.base1, self.mod1)
        hash2 = self._compute_hash(text[:m], self.base2, self.mod2)
        occurrences = []
        if hash1 == self.pattern_hash1 and hash2 == self.pattern_hash2 and text[:m] == self.pattern:
            occurrences.append(0)

        for i in range(1, n - m + 1):
            leading_char = ord(text[i - 1])
            trailing_char = ord(text[i + m - 1])
            # Update hash1
            hash1 = (hash1 - leading_char * self.highest_power1) % self.mod1
            hash1 = (hash1 * self.base1 + trailing_char) % self.mod1
            # Update hash2
            hash2 = (hash2 - leading_char * self.highest_power2) % self.mod2
            hash2 = (hash2 * self.base2 + trailing_char) % self.mod2
            # Check for match
            if hash1 == self.pattern_hash1 and hash2 == self.pattern_hash2:
                if text[i:i + m] == self.pattern:
                    occurrences.append(i)
        return occurrences
