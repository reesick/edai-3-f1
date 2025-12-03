"""
Binary Tree Traversals - Enhanced with 15+ production-grade frames
"""
from typing import List, Dict, Any
from .tree_utils import build_tree_from_array, serialize_tree, create_empty_frame, TreeNode

METADATA = {
    "name": "Binary Tree Traversals",
    "description": "Visualize Inorder, Preorder, and Postorder tree traversals",
    "time_complexity": "O(n) - visits each node once",
    "space_complexity": "O(h) for recursion stack",
    "default_input": {
        "tree_values": [50, 30, 70, 20, 40, 60, 80],
        "traversal_type": "inorder"
    }
}

def traverse_inorder(node, serialized, result, frames, frame_id_list):
    if not node:
        return
    
    traverse_inorder(node.left, serialized, result, frames, frame_id_list)
    
    # Visit node
    node_id = next((n["id"] for n in serialized if n["value"] == node.value), None)
    result.append(node.value)
    
    frame = create_empty_frame(frame_id_list[0], f"📍 Visit: {node.value} | Inorder: LEFT → ROOT → RIGHT | Result so far: {result}")
    frame["trees"] = [{"name": "Binary Search Tree", "nodes": serialized,
                      "highlights": {"node_ids": [node_id], "colors": ["#2ecc71"], "labels": ["VISITING"]}}]
    frame["variables"] = [{"name": "current_node", "value": str(node.value), "type": "int"},
                          {"name": "result", "value": str(result), "type": "array"}]
    frames.append(frame)
    frame_id_list[0] += 1
    
    traverse_inorder(node.right, serialized, result, frames, frame_id_list)

def traverse_preorder(node, serialized, result, frames, frame_id_list):
    if not node:
        return
    
    # Visit node first
    node_id = next((n["id"] for n in serialized if n["value"] == node.value), None)
    result.append(node.value)
    
    frame = create_empty_frame(frame_id_list[0], f"📍 Visit: {node.value} | Preorder: ROOT → LEFT → RIGHT | Result so far: {result}")
    frame["trees"] = [{"name": "Binary Search Tree", "nodes": serialized,
                      "highlights": {"node_ids": [node_id], "colors": ["#3498db"], "labels": ["VISITING"]}}]
    frame["variables"] = [{"name": "current_node", "value": str(node.value), "type": "int"},
                          {"name": "result", "value": str(result), "type": "array"}]
    frames.append(frame)
    frame_id_list[0] += 1
    
    traverse_preorder(node.left, serialized, result, frames, frame_id_list)
    traverse_preorder(node.right, serialized, result, frames, frame_id_list)

def traverse_postorder(node, serialized, result, frames, frame_id_list):
    if not node:
        return
    
    traverse_postorder(node.left, serialized, result, frames, frame_id_list)
    traverse_postorder(node.right, serialized, result, frames, frame_id_list)
    
    # Visit node last
    node_id = next((n["id"] for n in serialized if n["value"] == node.value), None)
    result.append(node.value)
    
    frame = create_empty_frame(frame_id_list[0], f"📍 Visit: {node.value} | Postorder: LEFT → RIGHT → ROOT | Result so far: {result}")
    frame["trees"] = [{"name": "Binary Search Tree", "nodes": serialized,
                      "highlights": {"node_ids": [node_id], "colors": ["#9b59b6"], "labels": ["VISITING"]}}]
    frame["variables"] = [{"name": "current_node", "value": str(node.value), "type": "int"},
                          {"name": "result", "value": str(result), "type": "array"}]
    frames.append(frame)
    frame_id_list[0] += 1

def execute(params: dict) -> List[Dict[str, Any]]:
    frames, frame_id = [], 0
    tree_values = params.get('tree_values', [])
    traversal_type = params.get('traversal_type', 'inorder').lower()
    
    root = build_tree_from_array(tree_values)
    
    # Frame 0: Intro
    frame = create_empty_frame(frame_id, "🌳 Binary Tree Traversals: Systematic ways to visit every node exactly once")
    if root:
        frame["trees"] = [{"name": "Binary Search Tree", "nodes": serialize_tree(root)}]
    frame["variables"] = [{"name": "traversal_type", "value": traversal_type.upper(), "type": "string"}]
    frames.append(frame)
    frame_id += 1
    
    # Frame 1: Three types explained
    frame = create_empty_frame(frame_id, "📚 Three Types: (1) INORDER: Left→Root→Right (2) PREORDER: Root→Left→Right (3) POSTORDER: Left→Right→Root")
    if root:
        frame["trees"] = [{"name": "Binary Search Tree", "nodes": serialize_tree(root)}]
    frames.append(frame)
    frame_id += 1
    
    # Frame 2: Selected type
    type_desc = {
        'inorder': "INORDER: Visit left subtree, then root, then right subtree (gives sorted order for BST!)",
        'preorder': "PREORDER: Visit root first, then left subtree, then right subtree (good for copying tree)",
        'postorder': "POSTORDER: Visit left subtree, then right subtree, then root last (good for deleting tree)"
    }
    
    frame = create_empty_frame(frame_id, f"🎯 Selected: {traversal_type.upper()} | {type_desc.get(traversal_type, '')}")
    if root:
        frame["trees"] = [{"name": "Binary Search Tree", "nodes": serialize_tree(root)}]
    frames.append(frame)
    frame_id += 1
    
    # Frame 3: Recursion concept
    frame = create_empty_frame(frame_id, "🔄 How it works: Uses RECURSION - function calls itself on left/right children until reaching NULL")
    frames.append(frame)
    frame_id += 1
    
    if not root:
        frame = create_empty_frame(frame_id, "Empty tree - nothing to traverse!")
        frames.append(frame)
        return frames
    
    # Perform traversal
    serialized = serialize_tree(root)
    result = []
    frame_id_list = [frame_id]
    
    if traversal_type == 'inorder':
        traverse_inorder(root, serialized, result, frames, frame_id_list)
    elif traversal_type == 'preorder':
        traverse_preorder(root, serialized, result, frames, frame_id_list)
    else:  # postorder
        traverse_postorder(root, serialized, result, frames, frame_id_list)
    
    frame_id = frame_id_list[0]
    
    # Final summary
    frame = create_empty_frame(frame_id, f"✅ {traversal_type.upper()} Traversal Complete! Visited {len(result)} nodes")
    if root:
        frame["trees"] = [{"name": "Binary Search Tree", "nodes": serialized}]
    frame["variables"] = [{"name": "traversal_order", "value": str(result), "type": "array"},
                          {"name": "nodes_visited", "value": str(len(result)), "type": "int"}]
    frames.append(frame)
    frame_id += 1
    
    # Usage explanation
    usage = {
        'inorder': "BST traversal gives SORTED values",
        'preorder': "Used for tree CLONING/COPYING",
        'postorder': "Used for tree DELETION"
    }
    
    frame = create_empty_frame(frame_id, f"💡 Use Case: {usage.get(traversal_type, '')} | Time: O(n), Space: O(h)")
    frame["variables"] = [{"name": "result", "value": str(result), "type": "array"}]
    frames.append(frame)
    
    return frames
