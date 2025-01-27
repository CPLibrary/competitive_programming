
def solve(N ,arr ,graph):

    timer = 0
    new_arr = []
    tin = [0 ] *N
    tout = [0 ] *N

    stack = [(0, -1, False)]

    while stack:
        node, par, visited = stack.pop()

        if not visited:
            tin[node] = timer
            timer += 1
            new_arr.append(arr[node])

            stack.append((node, par, True))

            for child in reversed(graph[node]):
                if child != par:
                    stack.append((child, node, False))
        else:
            tout[node] = timer - 1

    pre = [0 ] *( N +1)
    suf = [0 ] *( N +1)

    for i in range(len(new_arr)):
        pre[ i +1] = max(pre[i] ,new_arr[i])
    for i in range(len(new_arr ) -1 ,-1 ,-1):
        suf[i] = max(suf[ i +1] ,new_arr[i])


    max_weight = 0
    ans = 0

    for i in range(len(arr)):
        if max(pre[tin[i]] ,suf[tout[i ] +1]) > arr[i]:
            if arr[i] > max_weight:
                ans = i+ 1
                max_weight = arr[i]
    return ans