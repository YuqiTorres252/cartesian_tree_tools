# cartesian_tree_tools

Builds a min-heap-ordered binary tree over the indices of a numeric sequence, with
linear-time construction and iterative traversals.

```python
from cartesian_tree_tools import build, inorder, preorder, postorder

tree = build([3.0, 1.0, 4.0, 2.0, 5.0])
print(tree.root)          # 1
print(tree.left(1))       # 0
print(tree.right(1))      # 3
print(list(inorder(tree)))   # [0, 1, 2, 3, 4]
print(list(preorder(tree)))  # [1, 0, 3, 2, 4]
print(list(postorder(tree))) # [0, 2, 4, 3, 1]
```

The exported names are `CartesianTree`, `build`, `inorder`, `preorder`, and `postorder`.
`build` returns a `CartesianTree`; traversals are generators that yield integer indices
into the original sequence.

## Why this exists

The Cartesian tree of a sequence is the unique binary tree that is heap-ordered by the
sequence values and in-order by index. It is the structure behind several range-query
techniques and is a useful intermediate representation when you need to reason about
local minima without mutating the input.

This library makes one deliberate trade-off: ties in the input values are broken by
index, so the earliest index wins the heap comparison. That makes the tree canonical
for sequences with duplicates, which is what you want if you are comparing trees or
deriving results that must be reproducible. The cost is that the tree is not symmetric
under value ties; if you need a different tie-break you should pre-process the values.

## Edge cases

- An empty input produces a tree with `len(tree) == 0` and `tree.root is None`.
- All traversals are iterative, so deeply skewed inputs (monotone sequences) do not
  hit Python's recursion limit.
- `tree[i]` returns `(value, left_child, right_child)` where missing children are
  `None`.
