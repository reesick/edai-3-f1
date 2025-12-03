"""
BST Insert Algorithm - PRODUCTION GRADE with 15-20 frames
Enhanced with educational content and detailed step-by-step visualization
"""

from typing import List, Dict, Any
from .tree_utils import (
    build_tree_from_array,
    serialize_tree,
    create_empty_frame,
    TreeNode
)


METADATA = {
    "name": "BST Insert",
    "description": "Insert a value into Binary Search Tree maintaining BST property",
    "time_complexity": "O(log n) average, O(n) worst case",
    "space_complexity": "O(h) for recursion stack",
    "default_input": {
        "tree_values": [50, 30, 70, 20, 40, 60, 80],
        "insert_value": 45
    }
}


def execute(params: dict) -> List[Dict[str, Any]]:
    """Execute BST insert with detailed 15-20 frame visualization"""
    frames = []
    
    tree_values = params.get('tree_values', [])
    insert_value = params.get('insert_value')
    
    if insert_value is None:
        frame = create_empty_frame(0, "Error: No value provided to insert")
        frames.append(frame)
        return frames
    
    if insert_value in [v for v in tree_values if v is not None]:
        frame = create_empty_frame(0, f"Error: Value {insert_value} already exists in BST. Duplicates not allowed.")
        frames.append(frame)
        return frames
    
    root = build_tree_from_array(tree_values)
    frame_id = 0
    
    # FRAME 0: Introduction - What is BST Insert?
    frame = create_empty_frame(frame_id, "📚 BST Insert: Maintaining the Binary Search Tree Property")
    if root:
        frame["trees"] = [{"name": "Initial Binary Search Tree", "nodes": serialize_tree(root)}]
    frame["variables"] = [
        {"name": "insert_value", "value": str(insert_value), "type": "int"},
        {"name": "rule", "value": "Left < Parent < Right", "type": "string"}
    ]
    frames.append(frame)
    frame_id += 1
    
    # FRAME 1: Show the value to insert with explanation
    frame = create_empty_frame(frame_id, f"🎯 Goal: Insert value {insert_value} while maintaining BST property (all left children < parent < all right children)")
    if root:
        frame["trees"] = [{"name": "Binary Search Tree", "nodes": serialize_tree(root)}]
    frame["variables"] = [
        {"name": "insert_value", "value": str(insert_value), "type": "int"},
        {"name": "strategy", "value": "Compare & Navigate", "type": "string"},
        {"name": "total_nodes", "value": str(len(tree_values)), "type": "int"}
    ]
    frames.append(frame)
    frame_id += 1
    
    # FRAME 2: Strategy explanation
    frame = create_empty_frame(frame_id, "🧭 Strategy: Start at root, compare values, go left if smaller, right if larger, until we find an empty spot")
    if root:
        serialized = serialize_tree(root)
        frame["trees"] = [{
            "name": "Binary Search Tree",
            "nodes": serialized,
            "highlights": {
                "node_ids": [0],  # Highlight root
                "colors": ["#9b59b6"],
                "labels": ["START HERE"]
            }
        }]
    frame["variables"] = [
        {"name": "insert_value", "value": str(insert_value), "type": "int"},
        {"name": "current_position", "value": "ROOT (50)", "type": "string"}
    ]
    frames.append(frame)
    frame_id += 1
    
    if not root:
        # Empty tree case
        root = TreeNode(insert_value)
        frame = create_empty_frame(frame_id, f"🌱 Tree is empty! {insert_value} becomes the root node (first node in the tree)")
        frame["trees"] = [{
            "name": "Binary Search Tree",
            "nodes": serialize_tree(root),
            "highlights": {
                "node_ids": [0],
                "colors": ["#2ecc71"],
                "labels": ["NEW ROOT"]
            }
        }]
        frames.append(frame)
        return frames
    
    # Traverse and insert
    current = root
    path_values = []
    comparisons = 0
    
    while current:
        comparisons += 1
        serialized = serialize_tree(root)
        
        # Find IDs for all nodes in path
        current_node_id = None
        path_node_ids = []
        for node in serialized:
            if node["value"] == current.value:
                current_node_id = node["id"]
            if node["value"] in path_values:
                path_node_ids.append(node["id"])
        
        path_values.append(current.value)
        
        # Comparison decision frame
        if insert_value < current.value:
            # FRAME: Show comparison - going left
            frame = create_empty_frame(frame_id, f"🔍 Compare: {insert_value} < {current.value}? YES! → BST rule says go LEFT")
            frame["trees"] = [{
                "name": "Binary Search Tree",
                "nodes": serialized,
                "highlights": {
                    "node_ids": path_node_ids + [current_node_id],
                    "colors": ["#95a5a6"] * len(path_node_ids) + ["#f39c12"],
                    "labels": ["VISITED"] * len(path_node_ids) + ["COMPARING"]
                }
            }]
            frame["variables"] = [
                {"name": "insert_value", "value": str(insert_value), "type": "int"},
                {"name": "current_node", "value": str(current.value), "type": "int"},
                {"name": "comparison", "value": f"{insert_value} < {current.value}", "type": "string"},
                {"name": "decision", "value": "GO LEFT ←", "type": "string"},
                {"name": "comparisons_made", "value": str(comparisons), "type": "int"},
                {"name": "path", "value": " → ".join(map(str, path_values)), "type": "string"}
            ]
            frames.append(frame)
            frame_id += 1
            
            # FRAME: Explain WHY we go left
            frame = create_empty_frame(frame_id, f"💡 WHY go left? Because in BST, ALL values in left subtree must be smaller than {current.value}")
            frame["trees"] = [{
                "name": "Binary Search Tree", 
                "nodes": serialized,
                "highlights": {
                    "node_ids": [current_node_id],
                    "colors": ["#3498db"],
                    "labels": ["PARENT"]
                }
            }]
            frame["variables"] = [
                {"name": "rule", "value": f"Left < {current.value} < Right", "type": "string"},
                {"name": "our_value", "value": str(insert_value), "type": "int"}
            ]
            frames.append(frame)
            frame_id += 1
            
            if current.left is None:
                # Found insertion point!
                current.left = TreeNode(insert_value)
                serialized = serialize_tree(root)
                
                new_node_id = None
                for node in serialized:
                    if node["value"] == insert_value:
                        new_node_id = node["id"]
                        break
                
                # FRAME: Found NULL spot frame = create_empty_frame(frame_id, f"🎯 Found NULL spot! Left child of {current.value} is empty - perfect place for {insert_value}!")
                frame["trees"] = [{
                    "name": "Binary Search Tree",
                    "nodes": serialized,
                    "highlights": {
                        "node_ids": [current_node_id],
                        "colors": ["#e67e22"],
                        "labels": ["INSERTION PARENT"]
                    }
                }]
                frames.append(frame)
                frame_id += 1
                
                # FRAME: Actually insert
                frame = create_empty_frame(frame_id, f"✨ INSERT! Creating new node with value {insert_value} as LEFT CHILD of {current.value}")
                frame["trees"] = [{
                    "name": "Binary Search Tree",
                    "nodes": serialized,
                    "highlights": {
                        "node_ids": [new_node_id, current_node_id],
                        "colors": ["#2ecc71", "#3498db"],
                        "labels": ["INSERTED!", "PARENT"]
                    }
                }]
                frame["variables"] = [
                    {"name": "inserted_value", "value": str(insert_value), "type": "int"},
                    {"name": "parent_node", "value": str(current.value), "type": "int"},
                    {"name": "position", "value": "LEFT CHILD", "type": "string"},
                    {"name": "total_comparisons", "value": str(comparisons), "type": "int"}
                ]
                frames.append(frame)
                frame_id += 1
                
                # FRAME: Verify BST property maintained
                frame = create_empty_frame(frame_id, f"✅ Verify: {insert_value} < {current.value}? YES! BST property maintained")
                frame["trees"] = [{
                    "name": "Binary Search Tree",
                    "nodes": serialized,
                    "highlights": {
                        "node_ids": [new_node_id],
                        "colors": ["#2ecc71"],
                        "labels": ["VALID POSITION"]
                    }
                }]
                frames.append(frame)
                frame_id += 1
                break
            else:
                # FRAME: Moving to left child
                frame = create_empty_frame(frame_id, f"➡️ Moving to left child... Next node to check: {current.left.value}")
                frame["trees"] = [{
                    "name": "Binary Search Tree",
                    "nodes": serialized
                }]
                frames.append(frame)
                frame_id += 1
                current = current.left
                
        else:  # insert_value >= current.value
            # FRAME: Show comparison - going right
            frame = create_empty_frame(frame_id, f"🔍 Compare: {insert_value} > {current.value}? YES! → BST rule says go RIGHT")
            frame["trees"] = [{
                "name": "Binary Search Tree",
                "nodes": serialized,
                "highlights": {
                    "node_ids": path_node_ids + [current_node_id],
                    "colors": ["#95a5a6"] * len(path_node_ids) + ["#f39c12"],
                    "labels": ["VISITED"] * len(path_node_ids) + ["COMPARING"]
                }
            }]
            frame["variables"] = [
                {"name": "insert_value", "value": str(insert_value), "type": "int"},
                {"name": "current_node", "value": str(current.value), "type": "int"},
                {"name": "comparison", "value": f"{insert_value} > {current.value}", "type": "string"},
                {"name": "decision", "value": "GO RIGHT →", "type": "string"},
                {"name": "comparisons_made", "value": str(comparisons), "type": "int"},
                {"name": "path", "value": " → ".join(map(str, path_values)), "type": "string"}
            ]
            frames.append(frame)
            frame_id += 1
            
            # FRAME: Explain WHY we go right
            frame = create_empty_frame(frame_id, f"💡 WHY go right? Because in BST, ALL values in right subtree must be greater than {current.value}")
            frame["trees"] = [{
                "name": "Binary Search Tree",
                "nodes": serialized,
                "highlights": {
                    "node_ids": [current_node_id],
                    "colors": ["#3498db"],
                    "labels": ["PARENT"]
                }
            }]
            frame["variables"] = [
                {"name": "rule", "value": f"Left < {current.value} < Right", "type": "string"},
                {"name": "our_value", "value": str(insert_value), "type": "int"}
            ]
            frames.append(frame)
            frame_id += 1
            
            if current.right is None:
                # Found insertion point!
                current.right = TreeNode(insert_value)
                serialized = serialize_tree(root)
                
                new_node_id = None
                for node in serialized:
                    if node["value"] == insert_value:
                        new_node_id = node["id"]
                        break
                
                # FRAME: Found NULL spot
                frame = create_empty_frame(frame_id, f"🎯 Found NULL spot! Right child of {current.value} is empty - perfect place for {insert_value}!")
                frame["trees"] = [{
                    "name": "Binary Search Tree",
                    "nodes": serialized,
                    "highlights": {
                        "node_ids": [current_node_id],
                        "colors": ["#e67e22"],
                        "labels": ["INSERTION PARENT"]
                    }
                }]
                frames.append(frame)
                frame_id += 1
                
                # FRAME: Actually insert
                frame = create_empty_frame(frame_id, f"✨ INSERT! Creating new node with value {insert_value} as RIGHT CHILD of {current.value}")
                frame["trees"] = [{
                    "name": "Binary Search Tree",
                    "nodes": serialized,
                    "highlights": {
                        "node_ids": [new_node_id, current_node_id],
                        "colors": ["#2ecc71", "#3498db"],
                        "labels": ["INSERTED!", "PARENT"]
                    }
                }]
                frame["variables"] = [
                    {"name": "inserted_value", "value": str(insert_value), "type": "int"},
                    {"name": "parent_node", "value": str(current.value), "type": "int"},
                    {"name": "position", "value": "RIGHT CHILD", "type": "string"},
                    {"name": "total_comparisons", "value": str(comparisons), "type": "int"}
                ]
                frames.append(frame)
                frame_id += 1
                
                # FRAME: Verify BST property maintained
                frame = create_empty_frame(frame_id, f"✅ Verify: {insert_value} > {current.value}? YES! BST property maintained")
                frame["trees"] = [{
                    "name": "Binary Search Tree",
                    "nodes": serialized,
                    "highlights": {
                        "node_ids": [new_node_id],
                        "colors": ["#2ecc71"],
                        "labels": ["VALID POSITION"]
                    }
                }]
                frames.append(frame)
                frame_id += 1
                break
            else:
                # FRAME: Moving to right child
                frame = create_empty_frame(frame_id, f"➡️ Moving to right child... Next node to check: {current.right.value}")
                frame["trees"] = [{
                    "name": "Binary Search Tree",
                    "nodes": serialized
                }]
                frames.append(frame)
                frame_id += 1
                current = current.right
    
    # FINAL FRAME: Complete tree with stats
    frame = create_empty_frame(frame_id, f"🎉 Insertion Complete! Tree now has {len(tree_values) + 1} nodes. Path taken: {' → '.join(map(str, path_values))}")
    frame["trees"] = [{
        "name": "Final Binary Search Tree",
        "nodes": serialize_tree(root)
    }]
    frame["variables"] = [
        {"name": "total_nodes", "value": str(len(tree_values) + 1), "type": "int"},
        {"name": "comparisons_made", "value": str(comparisons), "type": "int"},
        {"name": "path_length", "value": str(len(path_values)), "type": "int"},
        {"name": "status", "value": "SUCCESS ✅", "type": "string"}
    ]
    frames.append(frame)
    frame_id += 1
    
    # BONUS FRAME: Time complexity explanation
    frame = create_empty_frame(frame_id, f"⏱️ Time Complexity: O(h) where h = height of tree. In this case, we made {comparisons} comparisons (height = {len(path_values)})")
    frame["trees"] = [{
        "name": "Binary Search Tree",
        "nodes": serialize_tree(root)
    }]
    frame["variables"] = [
        {"name": "best_case", "value": "O(log n) - balanced tree", "type": "string"},
        {"name": "worst_case", "value": "O(n) - skewed tree", "type": "string"},
        {"name": "this_case", "value": f"O({len(path_values)})", "type": "string"}
    ]
    frames.append(frame)
    
    return frames
