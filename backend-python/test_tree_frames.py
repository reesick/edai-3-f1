"""Test script to check frame counts for all tree algorithms"""

import sys
sys.path.append('.')

from algorithms.trees.bst_insert import execute as bst_insert_exec
from algorithms.trees.bst_search import execute as bst_search_exec
from algorithms.trees.bst_delete import execute as bst_delete_exec
from algorithms.trees.binary_tree_traversals import execute as traversals_exec
from algorithms.trees.lca_in_bst import execute as lca_exec

# Test BST Insert
print("=" * 60)
print("BST INSERT - Frame Analysis")
print("=" * 60)
frames = bst_insert_exec({'tree_values': [50,30,70,20,40,60,80], 'insert_value': 45})
print(f"Total frames: {len(frames)}\n")
for i, frame in enumerate(frames):
    print(f"Frame {i}: {frame['description']}")

# Test BST Search
print("\n" + "=" * 60)
print("BST SEARCH - Frame Analysis")
print("=" * 60)
frames = bst_search_exec({'tree_values': [50,30,70,20,40,60,80], 'search_value': 40})
print(f"Total frames: {len(frames)}\n")
for i, frame in enumerate(frames):
    print(f"Frame {i}: {frame['description']}")

# Test BST Delete
print("\n" + "=" * 60)
print("BST DELETE - Frame Analysis")
print("=" * 60)
frames = bst_delete_exec({'tree_values': [50,30,70,20,40,60,80], 'delete_value': 30})
print(f"Total frames: {len(frames)}\n")
for i, frame in enumerate(frames):
    print(f"Frame {i}: {frame['description']}")

# Test Traversals
print("\n" + "=" * 60)
print("BINARY TREE TRAVERSALS - Frame Analysis")
print("=" * 60)
frames = traversals_exec({'tree_values': [50,30,70,20,40,60,80], 'traversal_type': 'inorder'})
print(f"Total frames: {len(frames)}\n")
for i, frame in enumerate(frames):
    desc = frame['description'][:80] + "..." if len(frame['description']) > 80 else frame['description']
    print(f"Frame {i}: {desc}")

# Test LCA
print("\n" + "=" * 60)
print("LCA IN BST - Frame Analysis")
print("=" * 60)
frames = lca_exec({'tree_values': [50,30,70,20,40,60,80], 'node1': 20, 'node2': 60})
print(f"Total frames: {len(frames)}\n")
for i, frame in enumerate(frames):
    print(f"Frame {i}: {frame['description']}")

print("\n" + "=" * 60)
print("SUMMARY")
print("=" * 60)
print("Current frame counts are GOOD but can be enhanced with:")
print("1. More intermediate explanation frames")
print("2. Visual path history showing traversal")
print("3. Educational 'WHY' explanations")
print("4. Comparison with alternative scenarios")
