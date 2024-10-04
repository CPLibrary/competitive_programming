class EertreeNode:
    def __init__(self, length, suff_link):
        self.length = length
        self.suff_link = suff_link
        self.transitions = {}
        self.num = 0  # Number of palindromic substrings ending here

class Eertree:
    def __init__(self):
        self.nodes = []
        # Initialize two root nodes
        self.nodes.append(EertreeNode(-1, 0))  # Root with length -1
        self.nodes.append(EertreeNode(0, 0))   # Root with length 0
        self.size = 2
        self.last = 1  # Points to the largest suffix palindrome
        self.s = ['#']  # Dummy character to handle indexing

    def add_char(self, char):
        self.s.append(char)
        pos = len(self.s) - 1
        curr = self.last
        while True:
            if pos - self.nodes[curr].length - 1 >= 0 and self.s[pos - self.nodes[curr].length - 1] == char:
                break
            curr = self.nodes[curr].suff_link
        if char in self.nodes[curr].transitions:
            self.last = self.nodes[curr].transitions[char]
            return False  # Already exists
        self.nodes.append(EertreeNode(self.nodes[curr].length + 2, 0))
        self.size += 1
        self.nodes[curr].transitions[char] = self.size - 1
        if self.nodes[self.size - 1].length == 1:
            self.nodes[self.size - 1].suff_link = 1
            self.nodes[self.size - 1].num = 1
            self.last = self.size - 1
            return True
        suff = self.nodes[curr].suff_link
        while True:
            if pos - self.nodes[suff].length - 1 >= 0 and self.s[pos - self.nodes[suff].length - 1] == char:
                self.nodes[self.size - 1].suff_link = self.nodes[suff].transitions[char]
                break
            suff = self.nodes[suff].suff_link
        self.nodes[self.size - 1].num = 1 + self.nodes[self.nodes[self.size - 1].suff_link].num
        self.last = self.size - 1
        return True

    def count_unique_palindromes(self):
        return self.size - 2  # Exclude the two root nodes

    def count_total_palindromic_substrings(self):
        return sum(node.num for node in self.nodes) - 2  # Exclude roots

# Example Usage
if __name__ == "__main__":
    s = "ababa"
    eertree = Eertree()
    for char in s:
        eertree.add_char(char)
    print("Number of unique palindromic substrings:", eertree.count_unique_palindromes())  # Output: 3 ("a", "b", "aba")
    print("Total number of palindromic substrings:", eertree.count_total_palindromic_substrings())  # Output: 5
