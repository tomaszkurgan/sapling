from collections import deque


class traverse_method():
    dfs = 'depth-first search'
    bfs = 'breadth-first search'


class Node(object):
    _PATH_SEP = '/'

    def __init__(self, name, data=None):
        self.name = name
        self.data = data if data else name

        self.parent = None
        self.children = []

    def set_parent(self, other, force=False):
        if other is None:
            self.unparent()
        else:
            if other is self:
                raise ValueError('cannot parent node to itself')
            if other in self.children:
                if force:
                    self.children.remove(other)
                else:
                    raise ValueError('cannot parent node to one of it\'s children')
            self.parent = other
            other.children.append(self)

    def unparent(self):
        self.parent.children.remove(self)
        self.parent = None

    def __cmp__(self, other):
        return cmp(self.data, other.data)

    def traverse(self, method=traverse_method.dfs):
        yield self

        queue = deque()
        queue.extend(self.children)

        while queue:
            n = queue.popleft()
            yield n
            if method == traverse_method.bfs:  # Breadth-first search
                queue.extend(n.children)
            else:  # Depth-first search
                queue.extendleft(reversed(n.children))

    @property
    def root(self):
        parent = self

        while parent.parent:
            parent = parent.parent

        return parent

    @property
    def path(self):
        path_elements = [self]
        parent = self.parent
        while parent:
            path_elements.append(parent)
            parent = parent.parent

        path = self.root._PATH_SEP.join(reversed([i.name for i in path_elements]))
        return path

    @property
    def siblings(self):
        parent = self.parent
        if parent is None:
            return []

        children = parent.children
        siblings = []
        for child in children:
            if child != self:
                siblings.append(child)
        return siblings

    @property
    def leaves(self):
        leaves = []
        for node in self.traverse():
            if not node.children:
                leaves.append(node)
        return leaves

    def __str__(self):
        return '<{} {}>'.format(type(self).__name__, self.name)


if __name__ == '__main__':
    pass
