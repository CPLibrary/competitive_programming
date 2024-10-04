class State:
    def __init__(self):
        self.length = 0         # Length of the longest substring ending at this state
        self.link = -1          # Suffix link
        self.next = {}          # Transitions (edges) to other states
        self.count = 0          # Number of times this state is visited (endpos)

class SuffixAutomaton:
    def __init__(self):
        self.states = [State()]  # Initialize with the initial state
        self.size = 1            # Current size of the automaton (number of states)
        self.last = 0            # The index of the state representing the entire string

    def extend(self, char):
        """
        Extend the automaton with a new character and update occurrence counts.

        :param char: The character to add to the automaton.
        """
        p = self.last
        curr = self.size
        self.states.append(State())
        self.states[curr].length = self.states[p].length + 1
        self.states[curr].count = 1  # Each new state corresponds to a new end position
        self.size += 1

        # Update the transitions for state p
        while p != -1 and char not in self.states[p].next:
            self.states[p].next[char] = curr
            p = self.states[p].link

        if p == -1:
            self.states[curr].link = 0  # Link to the initial state
        else:
            q = self.states[p].next[char]
            if self.states[p].length + 1 == self.states[q].length:
                self.states[curr].link = q
            else:
                clone = self.size
                self.states.append(State())
                self.states[clone].length = self.states[p].length + 1
                self.states[clone].next = self.states[q].next.copy()
                self.states[clone].link = self.states[q].link
                self.states[clone].count = 0  # Clone state does not correspond to a new end position
                self.size += 1

                while p != -1 and self.states[p].next[char] == q:
                    self.states[p].next[char] = clone
                    p = self.states[p].link

                self.states[q].link = clone
                self.states[curr].link = clone

        self.last = curr

    def build_automaton(self, s):
        """
        Build the suffix automaton for the given string.

        :param s: The input string to build the automaton from.
        """
        for char in s:
            self.extend(char)

    def count_occurrences(self):
        """
        Count the number of occurrences for each state using suffix links.
        This should be called after building the automaton.
        """
        # Sort states in order of decreasing length
        order = sorted(range(self.size), key=lambda x: self.states[x].length, reverse=True)
        for state in order:
            if self.states[state].link != -1:
                self.states[self.states[state].link].count += self.states[state].count

    def number_of_occurrences(self, s):
        """
        Count the number of occurrences of a substring s in the original string.

        :param s: The substring to count occurrences of.
        :return: The number of times s appears in the original string.
        """
        current = 0
        for char in s:
            if char in self.states[current].next:
                current = self.states[current].next[char]
            else:
                return 0  # Substring not found
        return self.states[current].count

    def count_distinct_substrings(self):
        """
        Count the number of distinct substrings in the original string.

        :return: The total number of distinct substrings.
        """
        count = 0
        for state in self.states[1:]:  # Exclude the initial state
            count += state.length - self.states[state.link].length
        return count

    def is_substring(self, s):
        """
        Check if a string s is a substring of the original string.

        :param s: The string to check.
        :return: True if s is a substring, False otherwise.
        """
        current = 0
        for char in s:
            if char in self.states[current].next:
                current = self.states[current].next[char]
            else:
                return False
        return True

    def get_all_substrings(self):
        """
        Retrieve all distinct substrings of the original string.

        :return: A list of all distinct substrings.
        """
        substrings = []
        stack = [(0, "")]
        while stack:
            state, path = stack.pop()
            for char, next_state in self.states[state].next.items():
                new_path = path + char
                substrings.append(new_path)
                stack.append((next_state, new_path))
        return substrings

    def __str__(self):
        """
        String representation of the automaton for debugging purposes.

        :return: A string describing the automaton's states and transitions.
        """
        output = []
        for idx, state in enumerate(self.states):
            output.append(f"State {idx}: len={state.length}, link={state.link}, next={state.next}, count={state.count}")
        return "\n".join(output)


# Example Usage
if __name__ == "__main__":
    # Input string
    s = "ababa"

    # Initialize and build the suffix automaton
    sa = SuffixAutomaton()
    sa.build_automaton(s)

    # Count occurrences by propagating counts via suffix links
    sa.count_occurrences()

    # Print the automaton (for debugging)
    print("Suffix Automaton States:")
    print(sa)

    # Count distinct substrings
    print("\nNumber of distinct substrings:", sa.count_distinct_substrings())

    # Check if a substring exists
    substring = "aba"
    print(f"\nIs '{substring}' a substring of '{s}'?", sa.is_substring(substring))

    # Count occurrences of a substring
    print(f"Number of occurrences of '{substring}':", sa.number_of_occurrences(substring))

    # List all distinct substrings
    print("\nAll distinct substrings:")
    for substr in sa.get_all_substrings():
        print(substr)

s = "ababa"
sa = SuffixAutomaton()
sa.build_automaton(s)
sa.count_occurrences()
print("Number of distinct substrings:", sa.count_distinct_substrings())  # Output: 9


substring = "aba"
print(f"Is '{substring}' a substring of '{s}'?", sa.is_substring(substring))  # Output: True
print(f"Number of occurrences of '{substring}':", sa.number_of_occurrences(substring))  # Output: 2
