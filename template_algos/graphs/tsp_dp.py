def tsp_dp(n, graph, start=0):
    """Solve the TSP using DP with bitmasking."""
    dp = [[float('inf')] * n for _ in range(1 << n)]
    dp[1 << start][start] = 0
    for mask in range(1 << n):
        for u in range(n):
            if not (mask & (1 << u)):
                continue
            for v in range(n):
                if mask & (1 << v):
                    continue
                next_mask = mask | (1 << v)
                dp[next_mask][v] = min(dp[next_mask][v], dp[mask][u] + graph[u][v])
    # Return the minimum cost to return to the start
    return min(dp[(1 << n) - 1][u] + graph[u][start] for u in range(n))
