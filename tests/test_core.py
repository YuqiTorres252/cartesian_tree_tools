import unittest

from cartesian_tree_tools import (
    CartesianTree,
    build,
    inorder,
    preorder,
    postorder,
)


class TestBuild(unittest.TestCase):
    def test_empty(self):
        t = build([])
        self.assertEqual(len(t), 0)
        self.assertIsNone(t.root)
        self.assertEqual(list(inorder(t)), [])

    def test_single(self):
        t = build([42.0])
        self.assertEqual(len(t), 1)
        self.assertEqual(t.root, 0)
        self.assertEqual(t.value(0), 42.0)
        self.assertIsNone(t.left(0))
        self.assertIsNone(t.right(0))

    def test_increasing(self):
        t = build([1.0, 2.0, 3.0, 4.0])
        self.assertEqual(t.root, 0)
        self.assertEqual(t.right(0), 1)
        self.assertEqual(t.right(1), 2)
        self.assertEqual(t.right(2), 3)
        self.assertIsNone(t.left(0))

    def test_decreasing(self):
        t = build([4.0, 3.0, 2.0, 1.0])
        self.assertEqual(t.root, 3)
        self.assertEqual(t.left(3), 2)
        self.assertEqual(t.left(2), 1)
        self.assertEqual(t.left(1), 0)
        self.assertIsNone(t.right(3))

    def test_mixed(self):
        t = build([3.0, 1.0, 4.0, 2.0, 5.0])
        self.assertEqual(t.root, 1)
        self.assertEqual(t.left(1), 0)
        self.assertEqual(t.right(1), 3)
        self.assertEqual(t.right(3), 4)
        self.assertEqual(t.left(3), 2)

    def test_ties_stable(self):
        t = build([2.0, 2.0, 2.0])
        self.assertEqual(t.root, 0)
        self.assertEqual(t.right(0), 1)
        self.assertEqual(t.right(1), 2)

    def test_heap_property(self):
        vals = [5.0, 3.0, 8.0, 1.0, 4.0, 7.0, 2.0]
        t = build(vals)
        for i in range(len(vals)):
            l = t.left(i)
            r = t.right(i)
            if l is not None:
                self.assertLessEqual(t.value(i), t.value(l))
            if r is not None:
                self.assertLessEqual(t.value(i), t.value(r))

    def test_getitem(self):
        t = build([3.0, 1.0, 2.0])
        self.assertEqual(t[1], (1.0, 0, 2))
        self.assertEqual(t[0], (3.0, None, None))

    def test_equality(self):
        a = build([1.0, 2.0, 3.0])
        b = build([1.0, 2.0, 3.0])
        c = build([1.0, 2.0, 4.0])
        self.assertEqual(a, b)
        self.assertNotEqual(a, c)
        self.assertNotEqual(a, "not a tree")


class TestTraversals(unittest.TestCase):
    def test_inorder_sorted(self):
        t = build([3.0, 1.0, 4.0, 2.0, 5.0])
        self.assertEqual(list(inorder(t)), [0, 1, 2, 3, 4])

    def test_preorder(self):
        t = build([3.0, 1.0, 4.0, 2.0, 5.0])
        self.assertEqual(list(preorder(t)), [1, 0, 3, 2, 4])

    def test_postorder(self):
        t = build([3.0, 1.0, 4.0, 2.0, 5.0])
        self.assertEqual(list(postorder(t)), [0, 2, 4, 3, 1])

    def test_traversals_empty(self):
        t = build([])
        self.assertEqual(list(inorder(t)), [])
        self.assertEqual(list(preorder(t)), [])
        self.assertEqual(list(postorder(t)), [])

    def test_traversals_single(self):
        t = build([7.0])
        self.assertEqual(list(inorder(t)), [0])
        self.assertEqual(list(preorder(t)), [0])
        self.assertEqual(list(postorder(t)), [0])


if __name__ == "__main__":
    unittest.main()
