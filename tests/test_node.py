import unittest

from sapling import Node, traverse_method


class Test_Node(unittest.TestCase):
    @staticmethod
    def create_network():
        a = Node('a')
        b = Node('b')
        c = Node('c')
        d = Node('d')
        e = Node('e')
        f = Node('f')

        b.set_parent(a)
        c.set_parent(a)
        d.set_parent(b)
        e.set_parent(c)
        f.set_parent(c)

        return a, b, c, d, e, f

    def test_set_parent(self):
        a = Node('a')
        with self.assertRaises(ValueError):
            a.set_parent(a)

        b = Node('b')
        b.set_parent(a)
        self.assertIs(b.parent, a)
        self.assertIn(b, a.children)

        b.set_parent(None)
        self.assertIs(b.parent, None)
        self.assertNotIn(b, a.children)

        with self.assertRaises(ValueError):
            b.set_parent(a)
            a.set_parent(b)

        a.set_parent(b, force=True)
        self.assertIs(b, a.parent)
        self.assertIn(a, b.children)

    def test_unparent(self):
        a = Node('a')
        b = Node('b')
        b.set_parent(a)
        self.assertIs(b.parent, a)
        b.unparent()
        self.assertIs(b.parent, None)
        b.set_parent(a)
        self.assertIs(b.parent, a)
        b.set_parent(None)
        self.assertIs(b.parent, None)

    def test_cmp(self):
        a1 = Node('a')
        a2 = Node('a')
        self.assertEqual(a1, a2)
        a2.data = 'b'
        self.assertNotEqual(a1, a2)
        a1.data = 'b'
        self.assertEqual(a1, a2)

    def test_traverse(self):
        a, b, c, d, e, f = self.create_network()

        self.assertSequenceEqual(list(a.traverse()), [a, b, d, c, e, f])
        self.assertSequenceEqual(list(a.traverse(method=traverse_method.bfs)), [a, b, c, d, e, f])

    def test_root(self):
        a, b, c, d, e, f = self.create_network()

        self.assertEqual(a.root, a)
        self.assertEqual(b.root, a)
        self.assertEqual(c.root, a)
        self.assertEqual(d.root, a)
        self.assertEqual(e.root, a)
        self.assertEqual(f.root, a)

    def test_path(self):
        a, b, c, d, e, f = self.create_network()

        self.assertEqual(a.path, 'a')
        self.assertEqual(b.path, 'a/b')
        self.assertEqual(c.path, 'a/c')
        self.assertEqual(d.path, 'a/b/d')
        self.assertEqual(e.path, 'a/c/e')
        self.assertEqual(f.path, 'a/c/f')

    def test_siblings(self):
        a, b, c, d, e, f = self.create_network()

        self.assertSequenceEqual(a.siblings, [])
        self.assertSequenceEqual(b.siblings, [c])
        self.assertSequenceEqual(d.siblings, [])
        self.assertSequenceEqual(e.siblings, [f])
        self.assertSequenceEqual(f.siblings, [e])

    def test_leaves(self):
        a, b, c, d, e, f = self.create_network()

        self.assertSequenceEqual(a.leaves, [d, e, f])
        self.assertSequenceEqual(b.leaves, [d])
        self.assertSequenceEqual(d.leaves, [d])
        self.assertSequenceEqual(c.leaves, [e, f])

    def test_str(self):
        a = Node('a')
        self.assertEqual(a.__str__(), '<Node a>')


if __name__ == '__main__':
    unittest.main()
