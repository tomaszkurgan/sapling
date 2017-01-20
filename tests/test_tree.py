import unittest

from sapling import Tree, traverse_method


class Test_TreeBase(unittest.TestCase):
    def test_create_from_dict(self):
        t_lst = {'a': {'b': ['c', 'd', {'h': ['i', 'j', {'1': ['a', 'b']}]}], 'e': ['i', 'g']}}
        t = Tree.create_from_dict(t_lst)
        self.assertEqual(t.name, 'a')
        self.assertSequenceEqual([c.name for c in t.children], ['b', 'e'])


if __name__ == '__main__':
    unittest.main()
