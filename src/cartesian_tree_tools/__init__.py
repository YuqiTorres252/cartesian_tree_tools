"""Cartesian tree construction and traversal helpers.

Exports:
    CartesianTree: immutable heap-ordered binary tree with array indices.
    build: construct a CartesianTree from a sequence.
    inorder: yield indices in left-root-right order.
    preorder: yield indices in root-left-right order.
    postorder: yield indices in left-right-root order.
"""

from .core import CartesianTree, build, inorder, preorder, postorder

__all__ = [
    "CartesianTree",
    "build",
    "inorder",
    "preorder",
    "postorder",
]
