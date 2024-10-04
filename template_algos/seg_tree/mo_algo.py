import sys
import math
from collections import defaultdict

# Fast input reading
def input():
    return sys.stdin.readline()

# Define a Query class to store query information
class Query:
    def __init__(self, l, r, idx):
        self.l = l  # Left index of the query (0-based)
        self.r = r  # Right index of the query (exclusive, 0-based)
        self.idx = idx  # Original index of the query

    # Comparison method for sorting queries
    def __lt__(self, other):
        if self.block != other.block:
            return self.block < other.block
        # If in the same block, sort by R value
        # For optimization, sort every alternate block in reverse order
        if self.block % 2 == 0:
            return self.r < other.r
        else:
            return self.r > other.r

# Mo's Algorithm Implementation
def mos_algorithm(n, q, arr, queries):
    """
    :param n: Size of the array
    :param q: Number of queries
    :param arr: The input array
    :param queries: List of Query objects
    :return: List of answers corresponding to each query
    """
    block_size = int(math.sqrt(n)) + 1
    for query in queries:
        query.block = query.l // block_size

    # Sort the queries using Mo's ordering
    queries.sort()

    # Initialize current pointers and answer variables
    current_L = 0
    current_R = 0
    answer = 0
    freq = defaultdict(int)  # Frequency map for elements
    answers = [0] * q  # To store answers for each query

    # Define the add and remove functions based on the problem
    def add(x):
        nonlocal answer
        freq[arr[x]] += 1
        # Example: Count distinct elements
        if freq[arr[x]] == 1:
            answer += 1

    def remove(x):
        nonlocal answer
        freq[arr[x]] -= 1
        # Example: Count distinct elements
        if freq[arr[x]] == 0:
            answer -= 1

    # Process each query
    for query in queries:
        L, R = query.l, query.r

        # Expand to the left
        while current_L > L:
            current_L -= 1
            add(current_L)

        # Expand to the right
        while current_R < R:
            add(current_R)
            current_R += 1

        # Shrink from the left
        while current_L < L:
            remove(current_L)
            current_L += 1

        # Shrink from the right
        while current_R > R:
            current_R -= 1
            remove(current_R)

        # Store the answer for this query
        answers[query.idx] = answer

    return answers

# Example Problem: Number of Distinct Elements in Each Query Range
def main():
    import sys
    sys.setrecursionlimit(1 << 25)
    n, q = map(int, input().split())
    arr = list(map(int, input().split()))
    queries = []
    for i in range(q):
        l, r = map(int, input().split())
        # Assuming the input queries are 1-based and inclusive
        queries.append(Query(l - 1, r, i))

    # Run Mo's algorithm
    results = mos_algorithm(n, q, arr, queries)

    # Output the results
    for res in results:
        print(res)

if __name__ == "__main__":
    main()
