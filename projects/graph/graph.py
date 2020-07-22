"""
Simple graph implementation
"""
from util import Stack, Queue  # These may come in handy

class Graph:

    """Represent a graph as a dictionary of vertices mapping labels to edges."""
    def __init__(self):
        self.vertices = {}

    def add_vertex(self, vertex_id):
        """
        Add a vertex to the graph.
        """
        # unique id to identify each vertex 
        self.vertices[vertex_id] = set()

    def add_edge(self, v1, v2):
        """
        Add a directed edge to the graph.
        """
        # check if there is an between two vertices 
        if v1 in self.vertices and v2 in self.vertices:
            # instantiate edge
            self.vertices[v1].add(v2)
        else:
            raise IndexError("Nonexistent vertex, please try again")


    def get_neighbors(self, vertex_id):
        """
        Get all neighbors (edges) of a vertex.
        """
        return self.vertices[vertex_id]

    def bft(self, starting_vertex_id):
        """
        Print each vertex in breadth-first order
        beginning from starting_vertex.
        """
        # instantiate queue for bft 
        q = Queue() 

        # enqueue the staring node with the 
        # starting vertex 
        q.enqueue(starting_vertex_id)
        # store visited nodes in a set 
        visited = set()

        while q.size() > 0:
            v = q.dequeue()
            if v not in visited:
                # mark as visited 
                visited.add(v)
                # print the node
                print(v)
                # add all the neighbors to the queue 
                for next_vertice in self.get_neighbors(v):
                    q.enqueue(next_vertice)

    def dft(self, starting_vertex):
        """
        Print each vertex in depth-first order
        beginning from starting_vertex.
        """
        s = Stack()

        visited = set()

        s.push(starting_vertex)

        while s.size() > 0:
            v = s.pop()

            if v not in visited:
                visited.add(v)
                print(v)
                for next_vertice in self.get_neighbors(v):
                    s.push(next_vertice)
             

    def dft_recursive(self, starting_vertex):
        """
        Print each vertex in depth-first order
        beginning from starting_vertex.

        This should be done using recursion.
        """
        s = Stack()
        visited = set()

        if not starting_vertex:
            return starting_vertex
        else:
            s.push(starting_vertex)
            v = s.pop
            if v not in visited:
                visited.add(v)
                print(v)
                for next_vertice in self.get_neighbors(v):
                    s.push(next_vertice)
        return dft_recursive(starting_vertex)

    def bfs(self, starting_vertex, destination_vertex):
        """
        Return a list containing the shortest path from
        starting_vertex to destination_vertex in
        breath-first order.
        """
        q = Queue()
        q.enqueue([starting_vertex])
        # Create a Set to store visited vertices
        visited = set()
        # While the queue is not empty...
        while q.size() > 0:
            # Dequeue the first PATH
            path = q.dequeue()
            # Grab the last vertex from the PATH
            v = path[-1]
            # If that vertex has not been visited...
            if v not in visited:
                # CHECK IF IT'S THE TARGET
                  # IF SO, RETURN PATH
                if v == destination_vertex:
                    return path
                # Mark it as visited...
                visited.add(v)
                # Then add A PATH TO its neighbors to the back of the queue
                  # COPY THE PATH
                  # APPEND THE NEIGHOR TO THE BACK
                for next_vert in self.get_neighbors(v):
                    new_path = list(path)  # Copy the list
                    new_path.append(next_vert)
                    q.enqueue(new_path)
        # If we got here, we didn't find it
        return None

    def dfs(self, starting_vertex, destination_vertex):
        """
        Return a list containing a path from
        starting_vertex to destination_vertex in
        depth-first order.
        """
        s = Stack()
        s.push([starting_vertex])
        # Create a Set to store visited vertices
        visited = set()
        # While the queue is not empty...
        while s.size() > 0:
            # Dequeue the first PATH
            path = s.pop()
            # Grab the last vertex from the PATH
            s = path[-1]
            # If that vertex has not been visited...
            if s not in visited:
                # CHECK IF IT'S THE TARGET
                  # IF SO, RETURN PATH
                if s == destination_vertex:
                    return path

                # Mark it as visited...
                visited.add(s)

                # Then add A PATH TO its neighbors to the back of the queue
                  # COPY THE PATH
                  # APPEND THE NEIGHOR TO THE BACK

                for next_vert in self.get_neighbors(s):
                    new_path = list(path)  # Copy the list
                    new_path.append(next_vert)
                    s.push(new_path)
        # If we got here, we didn't find it
        return None

    def dfs_recursive(self, starting_vertex, destination_vertex):
        """
        Return a list containing a path from
        starting_vertex to destination_vertex in
        depth-first order.

        This should be done using recursion.
        """
        s = Stack()
        s.push([starting_vertex])
        # Create a Set to store visited vertices
        visited = set()
        # While the queue is not empty...
        if not starting_vertex:
            return starting_vertex
        if s.size() < 0:
            return 
        else:
            # Dequeue the first PATH
            path = s.pop()
            # Grab the last vertex from the PATH
            s = path[-1]
            # If that vertex has not been visited...
            if s not in visited:
                # CHECK IF IT'S THE TARGET
                  # IF SO, RETURN PATH
                if s == destination_vertex:
                    return path

                # Mark it as visited...
                visited.add(s)

                # Then add A PATH TO its neighbors to the back of the queue
                  # COPY THE PATH
                  # APPEND THE NEIGHOR TO THE BACK

                for next_vert in self.get_neighbors(s):
                    new_path = list(path)  # Copy the list
                    new_path.append(next_vert)
                    s.push(new_path)
        return dfs_recursive(starting_vertex,destination_vertex)
       

if __name__ == '__main__':
    graph = Graph()  # Instantiate your graph
    # https://github.com/LambdaSchool/Graphs/blob/master/objectives/breadth-first-search/img/bfs-visit-order.png
    graph.add_vertex(1)
    graph.add_vertex(2)
    graph.add_vertex(3)
    graph.add_vertex(4)
    graph.add_vertex(5)
    graph.add_vertex(6)
    graph.add_vertex(7)
    graph.add_edge(5, 3)
    graph.add_edge(6, 3)
    graph.add_edge(7, 1)
    graph.add_edge(4, 7)
    graph.add_edge(1, 2)
    graph.add_edge(7, 6)
    graph.add_edge(2, 4)
    graph.add_edge(3, 5)
    graph.add_edge(2, 3)
    graph.add_edge(4, 6)

    '''
    Should print:
        {1: {2}, 2: {3, 4}, 3: {5}, 4: {6, 7}, 5: {3}, 6: {3}, 7: {1, 6}}
    '''
    print(graph.vertices)

    # '''
    # Valid BFT paths:
    #     1, 2, 3, 4, 5, 6, 7
    #     1, 2, 3, 4, 5, 7, 6
    #     1, 2, 3, 4, 6, 7, 5
    #     1, 2, 3, 4, 6, 5, 7
    #     1, 2, 3, 4, 7, 6, 5
    #     1, 2, 3, 4, 7, 5, 6
    #     1, 2, 4, 3, 5, 6, 7
    #     1, 2, 4, 3, 5, 7, 6
    #     1, 2, 4, 3, 6, 7, 5
    #     1, 2, 4, 3, 6, 5, 7
    #     1, 2, 4, 3, 7, 6, 5
    #     1, 2, 4, 3, 7, 5, 6
    # '''
    # graph.bft(1)

    # '''
    # Valid DFT paths:
    #     1, 2, 3, 5, 4, 6, 7
    #     1, 2, 3, 5, 4, 7, 6
    #     1, 2, 4, 7, 6, 3, 5
    #     1, 2, 4, 6, 3, 5, 7
    # '''
    # graph.dft(1)
    # graph.dft_recursive(1)

    # '''
    # Valid BFS path:
    #     [1, 2, 4, 6]
    # '''
    # print(graph.bfs(1, 6))

    # '''
    # Valid DFS paths:
    #     [1, 2, 4, 6]
    #     [1, 2, 4, 7, 6]
    # '''
    # print(graph.dfs(1, 6))
    # print(graph.dfs_recursive(1, 6))
