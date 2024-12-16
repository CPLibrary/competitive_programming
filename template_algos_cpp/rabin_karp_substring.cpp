#include <iostream>
#include <vector>
#include <string>

using namespace std;

// Constants
const int mod = 1e9 + 7;
const int d = 111;
const int mod1 = 1e9 + 9;
const int d1 = 113;
const int N = 1e5 + 10;

// Function to compute prefix powers of d modulo prime
vector<long long> compute_prefix(int N, int prime, int d) {
    vector<long long> prefix(N + 2);
    prefix[0] = 1;
    for (int i = 0; i <= N; ++i) {
        prefix[i + 1] = (prefix[i] * d) % prime;
    }
    return prefix;
}

// Function to compute prefix hashes of the target string
vector<long long> compute_hash(const string& target, int prime, int d) {
    vector<long long> arr(target.size() + 1);
    arr[0] = 0; // Initialize with 0 for an empty string
    long long hash_value = 0;
    for (size_t i = 0; i < target.size(); ++i) {
        hash_value = (hash_value * d + target[i]) % prime;
        arr[i + 1] = hash_value;
    }
    return arr;
}

// Function to compute the hash of a substring target[l:r]
// Note: This computes the hash for target[l] to target[r - 1]
long long compute_substring_hash(int l, int r, const vector<long long>& arr, const vector<long long>& prefix, int prime) {
    long long hash_value = (arr[r] - arr[l] * prefix[r - l]) % prime;
    if (hash_value < 0)
        hash_value += prime;
    return hash_value;
}

int main() {
    // Example usage
    // Initialize the target string
    string target = "this is an example string for hashing";

    // Precompute prefix powers
    vector<long long> prefix = compute_prefix(N,mod, d);
    vector<long long> prefix1 = compute_prefix(N,mod1, d1);

    // Compute the prefix hashes for the target string
    vector<long long> arr = compute_hash(target, mod, d);
    vector<long long> arr1 = compute_hash(target, mod1, d1);

    // Indices of the substring you want to hash (inclusive l, exclusive r)
    int l = 5;  // Starting index (inclusive)
    int r = 15; // Ending index (exclusive)

    // Compute the substring hash for both hash functions
    long long hash_value = compute_substring_hash(l, r, arr, prefix, mod);
    long long hash_value1 = compute_substring_hash(l, r, arr1, prefix1, mod1);

    // Output the results
    cout << "Hash of substring '" << target.substr(l, r - l) << "' modulo " << mod << ": " << hash_value << endl;
    cout << "Hash of substring '" << target.substr(l, r - l) << "' modulo " << mod1 << ": " << hash_value1 << endl;

    return 0;
}