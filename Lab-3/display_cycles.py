from collections import defaultdict

def simple_cycles(G):
    # Yield every elementary cycle in python G exactly once
    def unblock(thisnode, blocked, B):
        # to get unique values
        stack = set([thisnode])
        #  while stack is not empty
        while stack:
            # get top element of stack
            node = stack.pop()
            if node in blocked:
                blocked.remove(node)
                stack.update(B[node])
                B[node].clear()

    # A duplicate copy of the graph
    # nbrs = neighbours
    G = {v: set(nbrs) for (v,nbrs) in G.items()}
    # using function to get all strongly connected components of the graph
    sccs = strongly_connected_components(G)
    #print("sccs = ",sccs)
    # using strongly connected components in the graph to find all unique cycles
    while sccs:
        # get the group of strongly connected  vertices
        scc = sccs.pop()
        #print(scc)
        startnode = scc.pop()
        #print(startnode)
        path = [startnode]
        # declaring blocked and closed sets
        blocked = set()
        closed = set()
        blocked.add(startnode)
        # declaring B as a default dictionary
        B = defaultdict(set)
        # creating a stack containing start node and all its neighbours
        stack = [(startnode,list(G[startnode])) ]
        #print("stack = ",stack)
        while stack:
            #print("start node = ",startnode)
            #print("stack_start = ", stack)
            thisnode, nbrs = stack[-1]
            #print(thisnode, nbrs)
            # if the current start node has neighbours
            if nbrs:
                # going to neighbour node
                nextnode = nbrs.pop()
                #print("popped = ",nextnode)
                # if the next node is start node itself, we found a cycle
                if nextnode == startnode:
                    #print("cycle found = ",path[:])
                    # get the whole path of cycle traversed
                    yield path[:]
                    # closed will contain all the cycle paths already discovered
                    closed.update(path)
                elif nextnode not in blocked:
                    # add next node to path
                    path.append(nextnode)
                    #print("path = ",path)
                    # now update stack with this next node and its neighbours
                    stack.append( (nextnode,list(G[nextnode])) )
                    #print("stack-2 = ",stack)
                    # remove nextnode from closed nodes list
                    #print("next node = ", nextnode)
                    closed.discard(nextnode)
                    #print("closed = ",closed)
                    # add it to blocked nodes list
                    blocked.add(nextnode)
                    #print("blocked = ",blocked)
                    continue
            # if the node has no neighbours
            if not nbrs:
                # if the nodes is closed, then unblock it
                if thisnode in closed:
                    unblock(thisnode,blocked,B)
                else:
                    for nbr in G[thisnode]:
                        if thisnode not in B[nbr]:
                            B[nbr].add(thisnode)
                stack.pop()
                path.pop()

        remove_node(G, startnode)
        H = subgraph(G, set(scc))
        sccs.extend(strongly_connected_components(H))


# Tarjan's Method for SCC
def strongly_connected_components(graph):
    index_counter, stack, lowlink, index, result = [0], [], {}, {}, []

    # Nested functions
    def strong_connect(node):
        index[node] = index_counter[0]
        lowlink[node] = index_counter[0]
        index_counter[0] += 1
        stack.append(node)
        successors = graph[node]
        for successor in successors:
            if successor not in index:
                strong_connect(successor)
                lowlink[node] = min(lowlink[node], lowlink[successor])
            elif successor in stack:
                lowlink[node] = min(lowlink[node], index[successor])
        if lowlink[node] == index[node]:
            connected_component = []
            while True:
                successor = stack.pop()
                connected_component.append(successor)
                if successor == node: break
            result.append(connected_component[:])

    for node in graph:
        if node not in index:
            strong_connect(node)
    return result


# Both below two fns expect values of G to be sets
def remove_node(graph, target):
        del graph[target]
        for i in graph.values():
            i.discard(target)


# Get the subgraph of G induced by set vertices
def subgraph(graph, vertices):
    return {v: graph[v] & vertices for v in vertices}

def print_cycles_in_graph(graph):
    print(graph)
    no_cycles = 0
    s = ""
    cycles = simple_cycles(graph)
    for c in cycles:
        for i in c:
            s+= "T"+str(i+1)+" "
        print("Conflict - {}".format(no_cycles+1)+" : "+s)
        no_cycles+=1
        # reset string
        s = ""
