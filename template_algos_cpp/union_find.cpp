#include <vector>

// Initialize the DSU with 'n' elements
class DSU {
private:
    std::vector<int> parents;
    std::vector<int> rank;

public:
    // Constructor to initialize the DSU
    DSU(int n) {
        parents.resize(n);
        rank.resize(n, 1); // Initialize rank (size) to 1 for all elements
        for (int i = 0; i < n; ++i) {
            parents[i] = i; // Each element is its own parent initially
        }
    }

    // Find function with path compression
    int find(int x) {
        if (parents[x] != x) {
            parents[x] = find(parents[x]); // Path compression
        }
        return parents[x];
    }

    // Union function with union by rank
    void unite(int x, int y) {
        int px = find(x);
        int py = find(y);
        if (px != py) {
            // Union by rank
            if (rank[px] > rank[py]) {
                std::swap(px, py);
            }
            parents[px] = py;
            rank[py] += rank[px];
            rank[px] = 0;
        }
    }

    // Optional: Function to get the size of the set containing element x
    int getRank(int x) {
        int px = find(x);
        return rank[px];
    }
};

#include <iostream>

int main() {
    int n = 10; // Number of elements
    DSU dsu(n);

    // Perform some unions
    dsu.unite(2, 3);
    dsu.unite(3, 4);
    dsu.unite(5, 6);

    // Check if two elements are in the same set
    if (dsu.find(2) == dsu.find(4)) {
        std::cout << "2 and 4 are in the same set." << std::endl;
    } else {
        std::cout << "2 and 4 are in different sets." << std::endl;
    }

    // Get the size of the set containing element 3
    std::cout << "Size of the set containing 3: " << dsu.getRank(3) << std::endl;

    return 0;
}