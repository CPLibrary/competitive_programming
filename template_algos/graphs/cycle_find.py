


def cycle_finding(x0,arr_a): ### arr_a is next array, x0 is start index
    # main phase: search successive powers of two
    power = lam = 1
    tortoise = x0
    hare = arr_a[x0]  # f(x0) is the element/node next to x0.
    while tortoise != hare:
        if power == lam:  # time to start a new power of two?
            tortoise = hare
            power *= 2
            lam = 0
        hare = arr_a[hare]
        lam += 1

    # Find the position of the first repetition of length lam
    mu = 0
    tortoise = hare = x0
    for _ in range(lam):
        hare = arr_a[hare]
    # The distance between the hare and tortoise is now lam.

    # Next, the hare and tortoise move at same speed until they agree
    while tortoise != hare:
        tortoise = arr_a[tortoise]
        hare = arr_a[hare]
        mu += 1
    ### lam is length of cycle, mu is how many indices from start point need to go to get to first cycle, arr_a is next array
    return lam, mu






def has_cycle_undirected(adj):
    visited = set()
    def dfs(u, parent):
        visited.add(u)
        for v in adj[u]:
            if v not in visited:
                if dfs(v, u):
                    return True
            elif v != parent:
                return True
        return False

    for u in adj:
        if u not in visited:
            if dfs(u, None):
                return True
    return False



def has_cycle_directed(adj):
    WHITE, GRAY, BLACK = 0, 1, 2
    color = {u: WHITE for u in adj}

    def dfs(u):
        color[u] = GRAY
        for v in adj[u]:
            if color[v] == GRAY:
                return True   # back‐edge ⇒ cycle
            if color[v] == WHITE and dfs(v):
                return True
        color[u] = BLACK
        return False

    for u in adj:
        if color[u] == WHITE and dfs(u):
            return True
    return False
