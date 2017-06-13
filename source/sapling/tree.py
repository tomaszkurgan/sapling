from sapling.node import Node, traverse_method

# cache for all dynamically created tree classes
_dynamic_tree_classes = {}


def printTree(start_node,
              vbar='|',
              level_hbar='|--',
              level_last_hbar='`--',
              level_offset=0):
    def _print(node, level_indent='', next_level_indent='', last_child=False):
        s = ''

        indent_temp = level_indent + (level_last_hbar if last_child else level_hbar)
        s += indent_temp + ' ' + str(node) if next_level_indent else str(node)

        level_indent += next_level_indent + ' ' * level_offset
        level_pointer_length = len(level_hbar)
        next_level_indent = vbar + ' ' * level_pointer_length

        for i, child in reversed(list(enumerate(reversed(node.children)))):
            if not i:
                next_level_indent = ' ' * (level_pointer_length + 1)

            s += '\n' + _print(child,
                               level_indent=level_indent,
                               next_level_indent=next_level_indent,
                               last_child=not bool(i))
        return s

    return _print(start_node)


class TreeBase(Node):
    _node_cls = Node

    @classmethod
    def create_from_dict(cls, dct):
        def parent(parent_node, child_node_name, child_children=None):
            if isinstance(child_node_name, dict):
                for node_name, children in child_node_name.iteritems():
                    parent(parent_node, node_name, children)
            else:
                node = cls._node_cls(child_node_name)
                node.set_parent(parent_node)
                if isinstance(child_children, list):
                    for child in child_children:
                        parent(node, child)

        if len(dct.keys()) > 1:
            raise ValueError('Multiple roots are forbidden')

        dct_root = dct.keys()[0]
        tree = cls(dct_root)
        parent(tree, dct[dct_root])

        return tree

    @classmethod
    def create_from_path(cls, path):
        nodes = path.split(TreeBase._PATH_SEP)

        tree = cls(nodes[0])

        current_node = tree.root
        for node in nodes[1:]:
            n = cls._node_cls(node)
            n.set_parent(current_node)
            current_node = n

        return tree

    def __new__(cls, name, data=None, printer=None, node_cls=None):
        if node_cls:
            if node_cls not in _dynamic_tree_classes:
                _dynamic_tree_classes[node_cls] = type('Tree', (cls, node_cls), dict(cls.__dict__))
            new_cls = _dynamic_tree_classes[node_cls]

            instance = new_cls.__new__(new_cls, name)
            instance._node_cls = node_cls
            return instance
        else:
            return super(TreeBase, cls).__new__(cls, name, data)

    def __init__(self, name, data=None, printer=printTree, node_cls=None):
        super(TreeBase, self).__init__(name, data=data)

        self.printer = printer

    @property
    def root(self):
        return self

    def insert(self, path, node=None, force=False):
        sep = TreeBase._PATH_SEP
        node_names = path.rstrip(sep).split(sep)
        if self.root.name != node_names[0]:
            return False

        current_node = self.root
        for i, node_name in enumerate(node_names[1:]):
            for child in current_node.children:
                if child.name == node_name:
                    current_node = child
                    break
            else:
                n = self._node_cls(node_name)
                if force:
                    n.set_parent(current_node)
                    current_node = n
                else:
                    return False
        if node:
            node.set_parent(current_node)
        return True

    # iterator protocol
    @property
    def depth_iter(self):
        return self.traverse(method=traverse_method.dfs)

    @property
    def breadth_iter(self):
        return self.traverse(method=traverse_method.bfs)

    def __iter__(self):
        return self.traverse()

    # indexing
    def get_all(self, node, start_node=None):
        start_node = start_node or self.root

        find_by_name = not isinstance(node, self._node_cls)
        for n in start_node.traverse():
            if find_by_name:
                if n.name == node:
                    yield n
            elif n == node:
                yield n

    def get(self, node, start_node=None):
        for n in self.get_all(node, start_node=start_node):
            return n
        return None

    def get_by_path(self, path):
        sep = TreeBase._PATH_SEP
        nodes = path.strip(sep).split(sep)
        if self.root.name != nodes[0]:
            return None

        current_node = self.root
        for node in nodes[1:]:
            for child in current_node.children:
                if child.name == node:
                    current_node = child
                    break
            else:
                return None
        return current_node

    def __contains__(self, node):
        if isinstance(node, basestring):
            if node.find(TreeBase._PATH_SEP):
                return self.get_by_path(node) or False

        return self.get(node) or False

    def __getitem__(self, index):
        item = self.get_by_path(index) or self.get(index)
        if item is None:
            raise IndexError('cannot get the node \'{}\' inside the tree'.format(index))
        return item

    def printout(self, start_node=None, printer=None):
        start_node = start_node or self.root
        printer = printer or self.printer

        return printer(start_node)


class TreeMeta(type):
    """

    """

    def __new__(mcs, name, bases, dct):
        cls = super(TreeMeta, mcs).__new__(mcs, name, bases, dct)
        for c in cls.mro():
            if issubclass(c, Node) and not issubclass(c, TreeBase):
                cls._node_cls = c
                break

        return cls


class Tree(TreeBase):
    """External interface for tree-based classes.
    """
    __metaclass__ = TreeMeta


if __name__ == '__main__':
    pass


