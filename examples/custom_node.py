import uuid

import sapling


# create your own node by inheritance from sapling.Node
class MyNode(sapling.Node):
    def __init__(self, name, data=None, id=None):
        self.id = id or uuid.uuid4()
        super(MyNode, self).__init__(name, data=data)


# There are two ways to force the sapling.Tree to use your node's class:
# 1. create new tree class using sapling.Tree and your node class as bases
#    Because sapling.Tree inherits from sapling.Node class, using dependency injection by inheritance
#    gives your the possibility to override much of sapling.Tree features simultaneously with
#    sapling.Node features, without any additional effort of overriding function directly in
#    tree class.
#    All nodes in tree, including tree-node itself, will get all features form your new
#    node class.
# 2. pass your node class as parameter while constructing Tree
#    Option 2. is monkey patch which create new class inherited from Tree class
#    and new node class in runtime.
#    Because of that, first solution is the prefered one.
class MyTree(sapling.Tree, MyNode):
    pass


if __name__ == '__main__':
    t = MyTree('a')
    t.insert('a/b/c/d/e', force=True)
    t.insert('a/b/f/g', force=True)
    t.insert('a/b/h/i/j', force=True)
    t.insert('a/b/h/i/k', force=True)
    t.insert('a/b/h/i/l', force=True)
    t.insert('a/z', force=True)
    t.insert('a/zz/e/f/g', force=True)
    t.insert('a/zz/z/f/g', force=True)

    print t.printout()

    # all nodes in the tree are instances of MyNode
    for node in t:
        print node, type(node), node.id

    print '\n\n'

    # if you don't want to create new Tree class
    # use optional parameter while creating Tree instance
    # But remember - it's monkey patching
    t2 = sapling.Tree('a', node_cls=MyNode)
    t2.insert('a/b/c/d/e', force=True)
    t2.insert('a/b/f/g', force=True)
    t2.insert('a/b/h/i/j', force=True)
    t2.insert('a/b/h/i/k', force=True)
    t2.insert('a/b/h/i/l', force=True)

    print t2.printout()
    for node in t2:
        print node, type(node), node.id

    print '\n\n'

    t3 = sapling.Tree('a', node_cls=MyNode)
    print type(t3)

    t4 = sapling.Tree('a', node_cls=MyNode)
    print type(t4)
    print type(t2) is type(t4)

    t5 = MyTree('a')
    print type(t5)
    print type(t) is type(t5)
