# sapling/tree.py
from sapling.node import Node, traverse_method


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
            raise ValueError('multiple roots are forbidden')

        dct_root = dct.keys()[0]
        tree = cls(dct_root)
        parent(tree, dct[dct_root])

        return tree

    def __init__(self, name, data=None, printer=None):
        super(TreeBase, self).__init__(name, data=data)

        self.printer = printer

    @property
    def root(self):
        return self

    def insert(self, path, node=None, force=False):
        sep = TreeBase.path_sep
        node_names = path.strip(sep).split(sep)
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
            node.parent(current_node)
        return True

    # iterator protocol
    @property
    def depth(self):
        return self.traverse()

    @property
    def breadth(self):
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
        sep = TreeBase.path_sep
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
            if node.find(TreeBase.path_sep):
                return self.get_by_path(node) or False

        return self.get(node) or False

    def __getitem__(self, index):
        item = self.get_by_path(index) or self.get(index)
        if item is None:
            raise IndexError('cannot get the node \'{}\' inside the tree'.format(index))
        return item

    def printout(self, start_node=None, printer=None):
        start_node = start_node or self.root
        printer = printer or self.printer or TreePrinter()

        return printer.printout(start_node)


class TreePrinter(object):
    def __init__(self, data_repr=None, level_pointer_text='--', level_offset=0):
        self.data_repr = data_repr
        self.level_pointer_text = level_pointer_text
        self.level_offset = level_offset

    def printout(self, start_node=None,
                 _root=True, _indent='', _next_level_indent='   ', _level_end=False):
        level_pointer_length = len(self.level_pointer_text)

        s = ''

        node_print_template = '{repr}\n' if _root else '{indent} {repr}\n'

        indent = _indent + ('`' if _level_end else '|') + self.level_pointer_text
        representation = self.data_repr(start_node) if self.data_repr else str(start_node)

        s += node_print_template.format(**{'indent': indent,
                                           'repr': representation})

        child_count = len(start_node.children)
        _indent += '' if _root else _next_level_indent + ' ' * (self.level_offset + 1)
        _next_level_indent = '|' + ' ' * level_pointer_length if child_count > 1 else ' ' * (level_pointer_length + 1)

        for i, child in enumerate(start_node.children):
            if i == child_count - 1:
                _next_level_indent = ' ' * (level_pointer_length + 1)
            s += self.printout(child,
                               _root=False,
                               _indent=_indent,
                               _next_level_indent=_next_level_indent,
                               _level_end=(i == child_count - 1))
        return str(s)


class TreeMeta(type):
    def __new__(mcs, name, bases, dct):
        cls = super(TreeMeta, mcs).__new__(mcs, name, bases, dct)
        for c in cls.mro():
            if issubclass(c, Node) and not issubclass(c, TreeBase):
                cls._node_cls = c
                break

        return cls


class Tree(TreeBase):
    """
    External interface for tree-based classes.
    """
    __metaclass__ = TreeMeta


if __name__ == '__main__':
    t_lst = {'a': {'b': ['c', 'd', {'h': ['i', 'j', {'1': ['a', 'b']}]}], 'e': ['i', 'g']}}

    t = Tree.create_from_dict(t_lst)
    t.traverse_method = traverse_method.dfs
    t.printer = TreePrinter(data_repr=lambda x: x, level_pointer_text='-->', level_offset=4)

    print t.printout()

    # print [str(i) for i in t.get_all('i')]
    # for i in t.get_all('i'):
    #     print i.path
    # print '\n'
    #
    # z = t.get('i')
    # print z.path
    print t['i'].path


    # print i.root
    # print t.root
    # print [str(a) for a in i.siblings]
    # print [str(a) for a in i.leaves]
    # i._graph = t
    # print i, i.path()




    # class T(object):
    #     def __init__(self, value):
    #         self.a = value
    #         self.b = 2 * value
    #
    #     def __setattr__(self, key, value):
    #         print '>>', key, value
    #         print self.__dict__
    #
    #         super(T, self).__setattr__(key, value)
    #
    # f = T(2)
    # print '@>', f.a
