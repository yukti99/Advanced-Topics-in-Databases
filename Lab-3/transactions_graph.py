from collections import defaultdict

class Graph():
    def __init__(self, vertices):
        self.graph = defaultdict(list)
        self.V = vertices

    # creating a directed graph
    def addEdge(self, u, v):
        self.graph[u].append(v)

    def isEdge(self, u, v):
        for i in self.graph[u]:
            if (i==v):
                return True
        return False
    def getVertices(self):
        return self.V

    def isCyclicUtil(self, v, visited, stack):
        visited[v] = True
        stack[v] = True
        # we recur for all the neighbours of v, if any one of them,
        # is visited and in stack, then graph has a cycle
        for neighbour in self.graph[v]:
            if (not visited[neighbour]):
                if self.isCyclicUtil(neighbour, visited, stack):
                    return True
            elif stack[neighbour] == True:
                return True
        # current node is removed/popped from the recursion stack
        stack[v] = False
        return False
    # to detect cycles in directed graph
    def isCyclic(self):
        visited = [False for i in range(self.V)]
        stack = [False for i in range(self.V)]
        for node in range(self.V):
            if not visited[node]:
                if self.isCyclicUtil(node, visited, stack):
                    return True
        return False

    def topologicalSortUtil(self, v, visited, stack):
        # marking the vertex as visited
        visited[v] = True
        # recur for all the vertices adjacent to this vertex
        for i in self.graph[v]:
            if not visited[i]:
                self.topologicalSortUtil(i,visited, stack)
        stack.append(v)

    def topologicalSort(self):
        # marking all the vertices as not visited
        visited = [False for i in range(self.V)]
        stack = []
        # Call the recursive helper function
        # to store Topological sort starting all vertices one by one
        for i in range(self.V):
            if not visited[i]:
                self.topologicalSortUtil(i, visited, stack)

        # print the stack in reverse order for topological sort
        return(stack[::-1])

    def printGraph(self):
        for i in range(self.V):
            print("Vertex " + str(i) + ":", end="")
            temp = self.graph[i]
            for i in range(len(temp)):
                print(" -> {}".format(temp[i]), end="")
            print()
