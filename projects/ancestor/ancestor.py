
class Stack():
    def __init__(self):
        self.stack = []
    def push(self, value):
        self.stack.append(value)
    def pop(self):
        if self.size() > 0:
            return self.stack.pop()
        else:
            return None
    def size(self):
        return len(self.stack)

class Queue():
    def __init__(self):
        self.queue = []
    def enqueue(self, value):
        self.queue.append(value)
    def dequeue(self):
        if self.size() > 0:
            return self.queue.pop(0)
        else:
            return None
    def size(self):
        return len(self.queue)


def earliest_ancestor(ancestors,starting_node):
    
    s = Stack()

    s.push([starting_node])

    visited = set()
    earliest_ancestor = []

    while s.size() > 0:
        path = s.pop()
        s = path[-1]

        if s not in visited:
            visited.add(s)
            if len(path) > 1:
                earliest_ancestor.append(path[0])
                if earliest_ancestor > 1:
                    return min(earliest_ancestor)
            else:
                return -1

            for next_node in self.get_neighbors(s):
                new_path = list(path)
                new_path.append(next_node)
                s.push(new_path)


def get_neighbors(child,ancestors):
    parents = set()
    for ancestor in ancestors:
        this_child = ancestor[1]
        if this_child == child:
            parents.add(ancestor[0])
    return parents





# Write a function that, given the dataset and the ID of an individual in the dataset, returns their earliest known ancestor – 
# the one at the farthest distance from the input individual. 
# If there is more than one ancestor tied for "earliest", 
# return the one with the lowest numeric ID. 
# If the input individual has no parents, the function should return -1.


# Clarifications:
# * The input will not be empty.
# * There are no cycles in the input.
# * There are no "repeated" ancestors – if two individuals are connected, it is by exactly one path.
# * IDs will always be positive integers.
# * A parent may have any number of children.

