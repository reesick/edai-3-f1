"""
BST Search Algorithm - PRODUCTION GRADE with 15-20 frames
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
    "name": "BST Search",
    "description": "Search for a value in Binary Search Tree",
    "time_complexity": "O(log n) average, O(n) worst case",
    "space_complexity": "O(h) for recursion stack",
    "default_input": {
        "tree_values": [50, 30, 70, 20, 40, 60, 80],
        "search_value": 40
    }
}


def execute(params: dict) -> List[Dict[str, Any]]:
    """Execute BST search with detailed 15-20 frame visualization"""
    frames = []
    frame_id = 0
    
    tree_values = params.get('tree_values', [])
    search_value = params.get('search_value')
    
    if search_value is None:
        frame = create_empty_frame(0, "Error: No search value provided")
        frames.append(frame)
        return frames
    
    root = build_tree_from_array(tree_values)
    
    # FRAME 0: Introduction
    frame = create_empty_frame(frame_id, "🔍 BST Search: Finding a value efficiently using Binary Search Tree properties")
    if root:
        frame["trees"] = [{"name": "Binary Search Tree", "nodes": serialize_tree(root)}]
    frame["variables"] = [
        {"name": "search_value", "value": str(search_value), "type": "int"},
        {"name": "rule", "value": "Left < Parent < Right", "type": "string"}
    ]
    frames.append(frame)
    frame_id += 1
    
    # FRAME 1: Goal explanation
    frame = create_empty_frame(frame_id, f"🎯 Goal: Find if value {search_value} exists in the BST. If found, return TRUE; otherwise FALSE")
    if root:
        frame["trees"] = [{"name": "Binary Search Tree", "nodes": serialize_tree(root)}]
    frame["variables"] = [
        {"name": "search_value", "value": str(search_value), "type": "int"},
        {"name": "total_nodes", "value": str(len(tree_values)), "type": "int"}
    ]
    frames.append(frame)
    frame_id += 1
    
    # FRAME 2: Strategy
    frame = create_empty_frame(frame_id, "🧭 Strategy: Start at root. If value < current, go LEFT. If value > current, go RIGHT. Until found or NULL")
    if root:
        serialized = serialize_tree(root)
        frame["trees"] = [{
            "name": "Binary Search Tree",
            "nodes": serialized,
            "highlights": {
                "node_ids": [0],
                "colors": ["#9b59b6"],
                "labels": ["START"]
            }
        }]
    frames.append(frame)
    frame_id += 1
    
    if not root:
        frame = create_empty_frame(frame_id, "Tree is empty! Search failed.")
        frames.append(frame)
        return frames
    
    # Perform search
    current = root
    found = False
    comparisons = 0
    path_values = []
    
    while current:
        comparisons += 1
        serialized = serialize_tree(root)
        
        # Find IDs
        current_node_id = None
        path_node_ids = []
        for node in serialized:
            if node["value"] == current.value:
                current_node_id = node["id"]
            if node["value"] in path_values:
                path_node_ids.append(node["id"])
        
        path_values.append(current.value)
        
        # Check if found
        if current.value == search_value:
            # FRAME: Found match!
            frame = create_empty_frame(frame_id, f"✅ MATCH! Current node {current.value} == {search_value}. Value FOUND!")
            frame["trees"] = [{
                "name": "Binary Search Tree",
                "nodes": serialized,
                "highlights": {
                    "node_ids": [current_node_id],
                    "colors": ["#2ecc71"],
                    "labels": ["FOUND!"]
                }
            }]
            frame["variables"] = [
                {"name": "search_value", "value": str(search_value), "type": "int"},
                {"name": "current_node", "value": str(current.value), "type": "int"},
                {"name": "status", "value": "FOUND ✅", "type": "string"},
                {"name": "comparisons", "value": str(comparisons), "type": "int"}
            ]
            frames.append(frame)
            frame_id += 1
            
            # FRAME: Success confirmation
            frame = create_empty_frame(frame_id, f"🎉 Success! Found {search_value} in the BST after {comparisons} comparisons")
            frame["trees"] = [{
                "name": "Binary Search Tree",
                "nodes": serialized,
                "highlights": {
                    "node_ids": path_node_ids + [current_node_id],
                    "colors": ["#95a5a6"] * len(path_node_ids) + ["#2ecc71"],
                    "labels": ["VISITED"] * len(path_node_ids) + ["TARGET"]
                }
            }]
            frame["variables"] = [
                {"name": "result", "value": "TRUE", "type": "boolean"},
                {"name": "path_taken", "value": " → ".join(map(str, path_values)), "type": "string"}
            ]
            frames.append(frame)
            found = True
            break
        
        # Comparison frames
        elif search_value < current.value:
            # FRAME: Comparison - go left
            frame = create_empty_frame(frame_id, f"🔍 Compare: {search_value} < {current.value}? YES! Search in LEFT subtree")
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
                {"name": "search_value", "value": str(search_value), "type": "int"},
                {"name": "current_node", "value": str(current.value), "type": "int"},
                {"name": "comparison", "value": f"{search_value} < {current.value}", "type": "string"},
                {"name": "decision", "value": "GO LEFT ←", "type": "string"},
                {"name": "comparisons", "value": str(comparisons), "type": "int"}
            ]
            frames.append(frame)
            frame_id += 1
            
            # FRAME: Why go left
            frame = create_empty_frame(frame_id, f"💡 WHY left? BST property: All left values < {current.value}. Since {search_value} < {current.value}, it MUST be in left subtree (if it exists)")
            frame["trees"] = [{
                "name": "Binary Search Tree",
                "nodes": serialized,
                "highlights": {
                    "node_ids": [current_node_id],
                    "colors": ["#3498db"],
                    "labels": ["PARENT"]
                }
            }]
            frames.append(frame)
            frame_id += 1
            
            if current.left is None:
                # FRAME: Reached NULL
                frame = create_empty_frame(frame_id, f"🚫 Reached NULL! Left child of {current.value} doesn't exist. {search_value} NOT FOUND in tree")
                frame["trees"] = [{
                    "name": "Binary Search Tree",
                    "nodes": serialized,
                    "highlights": {
                        "node_ids": path_node_ids + [current_node_id],
                        "colors": ["#e74c3c"] * (len(path_node_ids) + 1),
                        "labels": ["FAILED PATH"] * (len(path_node_ids) + 1)
                    }
                }]
                frame["variables"] = [
                    {"name": "result", "value": "FALSE", "type": "boolean"},
                    {"name": "comparisons", "value": str(comparisons), "type": "int"}
                ]
                frames.append(frame)
                break
            
            # FRAME: Moving left
            frame = create_empty_frame(frame_id, f"➡️ Moving to left child: {current.left.value}")
            frame["trees"] = [{"name": "Binary Search Tree", "nodes": serialized}]
            frames.append(frame)
            frame_id += 1
            current = current.left
            
        else:  # search_value > current.value
            # FRAME: Comparison - go right
            frame = create_empty_frame(frame_id, f"🔍 Compare: {search_value} > {current.value}? YES! Search in RIGHT subtree")
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
                {"name": "search_value", "value": str(search_value), "type": "int"},
                {"name": "current_node", "value": str(current.value), "type": "int"},
                {"name": "comparison", "value": f"{search_value} > {current.value}", "type": "string"},
                {"name": "decision", "value": "GO RIGHT →", "type": "string"},
                {"name": "comparisons", "value": str(comparisons), "type": "int"}
            ]
            frames.append(frame)
            frame_id += 1
            
            # FRAME: Why go right
            frame = create_empty_frame(frame_id, f"💡 WHY right? BST property: All right values > {current.value}. Since {search_value} > {current.value}, it MUST be in right subtree (if it exists)")
            frame["trees"] = [{
                "name": "Binary Search Tree",
                "nodes": serialized,
                "highlights": {
                    "node_ids": [current_node_id],
                    "colors": ["#3498db"],
                    "labels": ["PARENT"]
                }
            }]
            frames.append(frame)
            frame_id += 1
            
            if current.right is None:
                # FRAME: Reached NULL
                frame = create_empty_frame(frame_id, f"🚫 Reached NULL! Right child of {current.value} doesn't exist. {search_value} NOT FOUND in tree")
                frame["trees"] = [{
                    "name": "Binary Search Tree",
                    "nodes": serialized,
                    "highlights": {
                        "node_ids": path_node_ids + [current_node_id],
                        "colors": ["#e74c3c"] * (len(path_node_ids) + 1),
                        "labels": ["FAILED PATH"] * (len(path_node_ids) + 1)
                    }
                }]
                frame["variables"] = [
                    {"name": "result", "value": "FALSE", "type": "boolean"},
                    {"name": "comparisons", "value": str(comparisons), "type": "int"}
                ]
                frames.append(frame)
                break
            
            # FRAME: Moving right
            frame = create_empty_frame(frame_id, f"➡️ Moving to right child: {current.right.value}")
            frame["trees"] = [{"name": "Binary Search Tree", "nodes": serialized}]
            frames.append(frame)
            frame_id += 1
            current = current.right
    
    # FINAL FRAME: Summary
    result_text = "FOUND ✅" if found else "NOT FOUND ❌"
    frame = create_empty_frame(frame_id, f"🏁 Search Complete! Result: {search_value} was {result_text}. Path: {' → '.join(map(str, path_values))}")
    frame["trees"] = [{"name": "Binary Search Tree", "nodes": serialize_tree(root)}]
    frame["variables"] = [
        {"name": "search_value", "value": str(search_value), "type": "int"},
        {"name": "result", "value": "TRUE" if found else "FALSE", "type": "boolean"},
        {"name": "total_comparisons", "value": str(comparisons), "type": "int"},
        {"name": "path_length", "value": str(len(path_values)), "type": "int"}
    ]
    frames.append(frame)
    frame_id += 1
    
    # BONUS FRAME: Complexity
    frame = create_empty_frame(frame_id, f"⏱️ Time Complexity: O(h) = O({len(path_values)}). Best: O(log n) balanced, Worst: O(n) skewed")
    frame["trees"] = [{"name": "Binary Search Tree", "nodes": serialize_tree(root)}]
    frame["variables"] = [
        {"name": "comparisons_made", "value": str(comparisons), "type": "int"},
        {"name": "efficiency", "value": f"Checked {comparisons}/{len(tree_values)} nodes", "type": "string"}
    ]
    frames.append(frame)
    
    return frames
