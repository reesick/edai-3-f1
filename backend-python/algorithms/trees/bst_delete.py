"""
BST Delete - Enhanced with 15+ production-grade frames
"""
from typing import List, Dict, Any
from .tree_utils import build_tree_from_array, serialize_tree, create_empty_frame, TreeNode

METADATA = {
    "name": "BST Delete",
    "description": "Delete a node from Binary Search Tree maintaining BST property",
    "time_complexity": "O(log n) average, O(n) worst case",
    "space_complexity": "O(h) for recursion stack",
    "default_input": {"tree_values": [50, 30, 70, 20, 40, 60, 80], "delete_value": 30}
}

def find_min(node):
    while node and node.left:
        node = node.left
    return node

def delete_node_recursive(root, value, frames, frame_id_list):
    if not root:
        return root
    
    if value < root.value:
        root.left = delete_node_recursive(root.left, value, frames, frame_id_list)
    elif value > root.value:
        root.right = delete_node_recursive(root.right, value, frames, frame_id_list)
    else:
        # Node found - delete it
        if not root.left and not root.right:
            return None
        elif not root.left:
            return root.right
        elif not root.right:
            return root.left
        else:
            # Two children - use inorder successor
            successor = find_min(root.right)
            root.value = successor.value
            root.right = delete_node_recursive(root.right, successor.value, frames, frame_id_list)
    
    return root

def execute(params: dict) -> List[Dict[str, Any]]:
    frames, frame_id = [], 0
    tree_values, delete_value = params.get('tree_values', []), params.get('delete_value')
    
    if delete_value is None:
        frames.append(create_empty_frame(0, "Error: No value provided to delete"))
        return frames
    
    root = build_tree_from_array(tree_values)
    
    # Frame 0: Intro
    frame = create_empty_frame(frame_id, "🗑️ BST Delete: Removing a node while maintaining the Binary Search Tree property")
    if root:
        frame["trees"] = [{"name": "Binary Search Tree", "nodes": serialize_tree(root)}]
    frame["variables"] = [{"name": "delete_value", "value": str(delete_value), "type": "int"}]
    frames.append(frame)
    frame_id += 1
    
    # Frame 1: Three cases explained
    frame = create_empty_frame(frame_id, f"🎯 Goal: Delete {delete_value}. Three cases exist: (1) Leaf node (2) One child (3) Two children")
    if root:
        frame["trees"] = [{"name": "Binary Search Tree", "nodes": serialize_tree(root)}]
    frames.append(frame)
    frame_id += 1
    
    # Frame 2: Strategy
    frame = create_empty_frame(frame_id, "🧭 Strategy: First find the node, identify its case, then apply appropriate deletion method")
    if root:
        frame["trees"] = [{"name": "Binary Search Tree", "nodes": serialize_tree(root)}]
    frames.append(frame)
    frame_id += 1
    
    # Search for node
    current, parent = root, None
    found, comparisons = False, 0
    path = []
    
    while current:
        comparisons += 1
        path.append(current.value)
        
        serialized = serialize_tree(root)
        node_id = next((n["id"] for n in serialized if n["value"] == current.value), None)
        
        if current.value == delete_value:
            found = True
            frame = create_empty_frame(frame_id, f"✓ Found node {delete_value} after {comparisons} comparisons!")
            frame["trees"] = [{"name": "Binary Search Tree", "nodes": serialized,
                              "highlights": {"node_ids": [node_id], "colors": ["#e74c3c"], "labels": ["FOUND"]}}]
            frames.append(frame)
            frame_id += 1
            break
        
        frame = create_empty_frame(frame_id, f"🔍 Searching... {delete_value} {'<' if delete_value < current.value else '>'} {current.value}, go {'LEFT' if delete_value < current.value else 'RIGHT'}")
        frame["trees"] = [{"name": "Binary Search Tree", "nodes": serialized,
                          "highlights": {"node_ids": [node_id], "colors": ["#f39c12"], "labels": ["CHECKING"]}}]
        frames.append(frame)
        frame_id += 1
        
        parent = current
        current = current.left if delete_value < current.value else current.right
    
    if not found:
        frame = create_empty_frame(frame_id, f"❌ Node {delete_value} not found in tree")
        frames.append(frame)
        return frames
    
    # Determine case
    serialized = serialize_tree(root)
    node_id = next((n["id"] for n in serialized if n["value"] == delete_value), None)
    
    if not current.left and not current.right:
        # CASE 1: Leaf
        frame = create_empty_frame(frame_id, f"📋 CASE 1 DETECTED: Leaf Node (no children)")
        frame["trees"] = [{"name": "Binary Search Tree", "nodes": serialized,
                          "highlights": {"node_ids": [node_id], "colors": ["#e67e22"], "labels": ["LEAF"]}}]
        frames.append(frame)
        frame_id += 1
        
        frame = create_empty_frame(frame_id, f"✂️ Simply remove the leaf node {delete_value}")
        frames.append(frame)
        frame_id += 1
        
        if parent is None:
            root = None
        elif parent.left == current:
            parent.left = None
        else:
            parent.right = None
            
    elif not current.left or not current.right:
        # CASE 2: One child
        child = current.left or current.right
        child_side = "LEFT" if current.left else "RIGHT"
        
        frame = create_empty_frame(frame_id, f"📋 CASE 2 DETECTED: One Child (has {child_side} child: {child.value})")
        frame["trees"] = [{"name": "Binary Search Tree", "nodes": serialized,
                          "highlights": {"node_ids": [node_id], "colors": ["#e67e22"], "labels": ["ONE CHILD"]}}]
        frames.append(frame)
        frame_id += 1
        
        frame = create_empty_frame(frame_id, f"🔄 Replace node {delete_value} with its child {child.value}")
        frames.append(frame)
        frame_id += 1
        
        if parent is None:
            root = child
        elif parent.left == current:
            parent.left = child
        else:
            parent.right = child
            
    else:
        # CASE 3: Two children
        frame = create_empty_frame(frame_id, f"📋 CASE 3 DETECTED: Two Children (most complex case)")
        frame["trees"] = [{"name": "Binary Search Tree", "nodes": serialized,
                          "highlights": {"node_ids": [node_id], "colors": ["#e67e22"], "labels": ["TWO CHILDREN"]}}]
        frames.append(frame)
        frame_id += 1
        
        frame = create_empty_frame(frame_id, "🔍 Finding inorder successor (minimum value in right subtree)...")
        frames.append(frame)
        frame_id += 1
        
        successor = find_min(current.right)
        serialized = serialize_tree(root)
        succ_id = next((n["id"] for n in serialized if n["value"] == successor.value), None)
        
        frame = create_empty_frame(frame_id, f"✓ Found inorder successor: {successor.value}")
        frame["trees"] = [{"name": "Binary Search Tree", "nodes": serialized,
                          "highlights": {"node_ids": [succ_id, node_id], "colors": ["#2ecc71", "#e74c3c"], 
                                       "labels": ["SUCCESSOR", "TO DELETE"]}}]
        frames.append(frame)
        frame_id += 1
        
        successor_value = successor.value
        current.value = successor_value
        
        frame = create_empty_frame(frame_id, f"📝 Replace {delete_value} with successor value {successor_value}")
        serialized = serialize_tree(root)
        frame["trees"] = [{"name": "Binary Search Tree", "nodes": serialized}]
        frames.append(frame)
        frame_id += 1
        
        # Delete successor (which is now duplicate)
        frame = create_empty_frame(frame_id, f"🗑️ Remove the duplicate successor node from right subtree")
        frames.append(frame)
        frame_id += 1
        
        frame_id_list = [frame_id]
        root = delete_node_recursive(root, successor_value, frames, frame_id_list)
        frame_id = frame_id_list[0]
    
    # Final frames
    frame = create_empty_frame(frame_id, f"✅ Deletion Complete! BST property maintained. Tree now has {len(tree_values)-1} nodes")
    if root:
        frame["trees"] = [{"name": "Final Binary Search Tree", "nodes": serialize_tree(root)}]
    frame["variables"] = [{"name": "deleted_value", "value": str(delete_value), "type": "int"},
                          {"name": "comparisons", "value": str(comparisons), "type": "int"}]
    frames.append(frame)
    frame_id += 1
    
    frame = create_empty_frame(frame_id, "⏱️ Time Complexity: O(h) to find + O(h) to delete = O(h) where h is height")
    if root:
        frame["trees"] = [{"name": "Binary Search Tree", "nodes": serialize_tree(root)}]
    frames.append(frame)
    
    return frames
