"""
LCA in BST - Enhanced with 15+ production-grade frames
"""
from typing import List, Dict, Any
from .tree_utils import build_tree_from_array, serialize_tree, create_empty_frame, TreeNode

METADATA = {
    "name": "LCA in BST",
    "description": "Find Lowest Common Ancestor of two nodes in Binary Search Tree",
    "time_complexity": "O(log n) average, O(n) worst case",
    "space_complexity": "O(h) for recursion stack",
    "default_input": {
        "tree_values": [50, 30, 70, 20, 40, 60, 80],
        "node1": 20,
        "node2": 60
    }
}

def execute(params: dict) -> List[Dict[str, Any]]:
    frames, frame_id = [], 0
    tree_values = params.get('tree_values', [])
    node1, node2 = params.get('node1'), params.get('node2')
    
    if node1 is None or node2 is None:
        frames.append(create_empty_frame(0, "Error: Two node values required for LCA"))
        return frames
    
    root = build_tree_from_array(tree_values)
    
    # Frame 0: Intro
    frame = create_empty_frame(frame_id, "🔍 Lowest Common Ancestor (LCA): Find the deepest node that is ancestor of BOTH given nodes")
    if root:
        frame["trees"] = [{"name": "Binary Search Tree", "nodes": serialize_tree(root)}]
    frame["variables"] = [{"name": "node1", "value": str(node1), "type": "int"},
                          {"name": "node2", "value": str(node2), "type": "int"}]
    frames.append(frame)
    frame_id += 1
    
    # Frame 1: What is an ancestor?
    frame = create_empty_frame(frame_id, "📚 Ancestor: A node is ancestor of another if it lies on the path from root to that node")
    if root:
        frame["trees"] = [{"name": "Binary Search Tree", "nodes": serialize_tree(root)}]
    frames.append(frame)
    frame_id += 1
    
    # Frame 2: Goal
    frame = create_empty_frame(frame_id, f"🎯 Find LCA of {node1} and {node2}: The split point where paths to both nodes diverge")
    if root:
        serialized = serialize_tree(root)
        # Highlight both target nodes
        ids = [n["id"] for n in serialized if n["value"] in [node1, node2]]
        if len(ids) == 2:
            frame["trees"] = [{
                "name": "Binary Search Tree",
                "nodes": serialized,
                "highlights": {"node_ids": ids, "colors": ["#f39c12", "#9b59b6"], "labels": ["TARGET 1", "TARGET 2"]}
            }]
    frames.append(frame)
    frame_id += 1
    
    # Frame 3: Strategy
    frame = create_empty_frame(frame_id, "🧭 BST Strategy: If both nodes < current, LCA in LEFT. If both > current, LCA in RIGHT. Else, current IS LCA!")
    if root:
        frame["trees"] = [{"name": "Binary Search Tree", "nodes": serialize_tree(root)}]
    frames.append(frame)
    frame_id += 1
    
    if not root:
        frame = create_empty_frame(frame_id, "Empty tree - no LCA")
        frames.append(frame)
        return frames
    
    # Verify nodes exist
    def find_node(node, value):
        if not node:
            return False
        if node.value == value:
            return True
        return find_node(node.left, value) or find_node(node.right, value)
    
    if not find_node(root, node1) or not find_node(root, node2):
        frame = create_empty_frame(frame_id, f"❌ One or both nodes not found in tree")
        frames.append(frame)
        return frames
    
    # Find LCA
    current = root
    path = []
    
    while current:
        path.append(current.value)
        serialized = serialize_tree(root)
        node_id = next((n["id"] for n in serialized if n["value"] == current.value), None)
        
        # Frame: Current position
        frame = create_empty_frame(frame_id, f"📍 At node {current.value}: Checking where {node1} and {node2} are relative to this node")
        frame["trees"] = [{"name": "Binary Search Tree", "nodes": serialized,
                          "highlights": {"node_ids": [node_id], "colors": ["#3498db"], "labels": ["CURRENT"]}}]
        frame["variables"] = [{"name": "node1", "value": str(node1), "type": "int"},
                              {"name": "node2", "value": str(node2), "type": "int"},
                              {"name": "current", "value": str(current.value), "type": "int"}]
        frames.append(frame)
        frame_id += 1
        
        if node1 < current.value and node2 < current.value:
            # Both in left subtree
            frame = create_empty_frame(frame_id, f"⬅️ Both {node1} and {node2} < {current.value} → Both are in LEFT subtree, move left")
            frame["trees"] = [{"name": "Binary Search Tree", "nodes": serialized,
                              "highlights": {"node_ids": [node_id], "colors": ["#f39c12"], "labels": ["GO LEFT"]}}]
            frames.append(frame)
            frame_id += 1
            current = current.left
            
        elif node1 > current.value and node2 > current.value:
            # Both in right subtree
            frame = create_empty_frame(frame_id, f"➡️ Both {node1} and {node2} > {current.value} → Both are in RIGHT subtree, move right")
            frame["trees"] = [{"name": "Binary Search Tree", "nodes": serialized,
                              "highlights": {"node_ids": [node_id], "colors": ["#f39c12"], "labels": ["GO RIGHT"]}}]
            frames.append(frame)
            frame_id += 1
            current = current.right
            
        else:
            # Split point - this is LCA!
            frame = create_empty_frame(frame_id, f"⭐ SPLIT POINT! {node1} and {node2} are on OPPOSITE sides (or one equals current)")
            serialized = serialize_tree(root)
            lca_id = next((n["id"] for n in serialized if n["value"] == current.value), None)
            target_ids = [n["id"] for n in serialized if n["value"] in [node1, node2]]
            
            frame["trees"] = [{
                "name": "Binary Search Tree",
                "nodes": serialized,
                "highlights": {
                    "node_ids": [lca_id] + target_ids,
                    "colors": ["#f1c40f"] + ["#e74c3c"] * len(target_ids),
                    "labels": ["LCA ⭐"] + ["TARGET"] * len(target_ids)
                }
            }]
            frames.append(frame)
            frame_id += 1
            
            # Explanation why
            frame = create_empty_frame(frame_id, f"💡 WHY is {current.value} the LCA? It's the deepest node where paths to {node1} and {node2} split")
            frame["trees"] = [{
                "name": "Binary Search Tree",
                "nodes": serialized,
                "highlights": {"node_ids": [lca_id], "colors": ["#f1c40f"], "labels": ["LCA"]}
            }]
            frames.append(frame)
            frame_id += 1
            break
    
    # Final summary
    frame = create_empty_frame(frame_id, f"✅ LCA Found! The Lowest Common Ancestor of {node1} and {node2} is {current.value}")
    serialized = serialize_tree(root)
    lca_id = next((n["id"] for n in serialized if n["value"] == current.value), None)
    frame["trees"] = [{
        "name": "Binary Search Tree",
        "nodes": serialized,
        "highlights": {"node_ids": [lca_id], "colors": ["#2ecc71"], "labels": ["LCA ✓"]}
    }]
    frame["variables"] = [
        {"name": "lca", "value": str(current.value), "type": "int"},
        {"name": "path_taken", "value": " → ".join(map(str, path)), "type": "string"}
    ]
    frames.append(frame)
    frame_id += 1
    
    # Complexity
    frame = create_empty_frame(frame_id, f"⏱️ Time Complexity: O(h) where h={len(path)} (height of tree). Visited {len(path)} nodes")
    frame["variables"] = [
        {"name": "comparisons", "value": str(len(path)), "type": "int"},
        {"name": "efficiency", "value": f"{len(path)}/{len(tree_values)} nodes checked", "type": "string"}
    ]
    frames.append(frame)
    
    return frames
