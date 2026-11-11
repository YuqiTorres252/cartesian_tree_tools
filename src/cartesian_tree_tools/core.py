from __future__ import annotations

from typing import Iterable, Iterator, List, Optional, Sequence, Tuple


class CartesianTree:
    """A min-heap-ordered binary tree over the indices of a sequence.

    Each node stores an index into the original sequence. The tree satisfies
    the min-heap property on the sequence values: a parent's value is less
    than or equal to both children's values. Ties are broken by the index,
    so the structure is deterministic for equal values.

    The tree is immutable after construction. ``left`` and ``right`` are
    tuples of child indices (empty when absent).
    """

    __slots__ = ("_values", "_left", "_right", "_root")

    def __init__(
        self,
        values: Sequence[float],
        left: Sequence[Optional[int]],
        right: Sequence[Optional[int]],
        root: Optional[int],
    ) -> None:
        self._values = tuple(values)
        self._left = tuple(left)
        self._right = tuple(right)
        self._root = root

    @property
    def values(self) -> Tuple[float, ...]:
        """The original sequence values, in index order."""
        return self._values

    @property
    def root(self) -> Optional[int]:
        """Index of the root, or None for an empty tree."""
        return self._root

    def left(self, index: int) -> Optional[int]:
        """Index of the left child of ``index``, or None."""
        return self._left[index]

    def right(self, index: int) -> Optional[int]:
        """Index of the right child of ``index``, or None."""
        return self._right[index]

    def value(self, index: int) -> float:
        """Value stored at ``index``."""
        return self._values[index]

    def __len__(self) -> int:
        return len(self._values)

    def __getitem__(self, index: int) -> Tuple[float, Optional[int], Optional[int]]:
        """Return ``(value, left_child, right_child)`` for ``index``."""
        return (self._values[index], self._left[index], self._right[index])

    def __repr__(self) -> str:  # pragma: no cover - trivial
        return f"CartesianTree(root={self._root!r}, size={len(self)})]".replace("]", ")")

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, CartesianTree):
            return NotImplemented
        return (
            self._values == other._values
            and self._left == other._left
            and self._right == other._right
            and self._root == other._root
        )

    def __hash__(self) -> int:
        return hash((self._values, self._left, self._right, self._root))


def build(values: Iterable[float]) -> CartesianTree:
    """Build a Cartesian tree from ``values``.

    The algorithm is the standard linear-time stack method. We keep a stack
    of indices whose values are increasing from bottom to top. For each new
    index we pop larger values; the last popped becomes the left child of the
    new node, and the new node becomes the right child of the stack top.
    Ties are resolved in favour of the earlier index (stable), which makes
    the result a canonical form for equal values.
    """
    vals: List[float] = list(values)
    n = len(vals)
    left: List[Optional[int]] = [None] * n
    right: List[Optional[int]] = [None] * n
    stack: List[int] = []

    for i in range(n):
        last = None
        while stack and vals[stack[-1]] > vals[i]:
            last = stack.pop()
        if last is not None:
            left[i] = last
        if stack:
            right[stack[-1]] = i
        stack.append(i)

    root = stack[0] if stack else None
    return CartesianTree(vals, left, right, root)


def inorder(tree: CartesianTree) -> Iterator[int]:
    """Yield indices in left-root-right order."""
    if tree.root is None:
        return
    stack: List[Tuple[int, bool]] = [(tree.root, False)]
    while stack:
        node, visited = stack.pop()
        if visited:
            yield node
            continue
        r = tree.right(node)
        if r is not None:
            stack.append((r, False))
        stack.append((node, True))
        l = tree.left(node)
        if l is not None:
            stack.append((l, False))


def preorder(tree: CartesianTree) -> Iterator[int]:
    """Yield indices in root-left-right order."""
    if tree.root is None:
        return
    stack: List[int] = [tree.root]
    while stack:
        node = stack.pop()
        yield node
        r = tree.right(node)
        if r is not None:
            stack.append(r)
        l = tree.left(node)
        if l is not None:
            stack.append(l)


def postorder(tree: CartesianTree) -> Iterator[int]:
    """Yield indices in left-right-root order."""
    if tree.root is None:
        return
    stack: List[Tuple[int, bool]] = [(tree.root, False)]
    while stack:
        node, visited = stack.pop()
        if visited:
            yield node
            continue
        stack.append((node, True))
        r = tree.right(node)
        if r is not None:
            stack.append((r, False))
        l = tree.left(node)
        if l is not None:
            stack.append((l, False))
