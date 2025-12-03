"""
Utility functions for tree algorithms
Handles tree construction, serialization, and position calculation
"""

from typing import List, Dict, Any, Optional
import math


class TreeNode:
    """Binary tree node"""
    def __init__(self, value):
        self.value = value
        self.left = None
        self.right = None


def build_tree_from_array(values: List[Optional[int]]) -> Optional[TreeNode]:
    """
    Build binary tree from level-order array representation.
    None values indicate missing nodes.
    
    Example: [50, 30, 70, 20, 40, None, 80] creates:
            50
           /  \
         30    70
        /  \     \
       20  40    80
    """
    if not values or values[0] is None:
        return None
    
    root = TreeNode(values[0])
    queue = [root]
    i = 1
    
    while queue and i < len(values):
        node = queue.pop(0)
        
        # Left child
        if i < len(values) and values[i] is not None:
            node.left = TreeNode(values[i])
            queue.append(node.left)
        i += 1
        
        # Right child
        if i < len(values) and values[i] is not None:
            node.right = TreeNode(values[i])
            queue.append(node.right)
        i += 1
    
    return root


def serialize_tree(root: Optional[TreeNode]) -> List[Dict[str, Any]]:
    """
    Convert tree to array of nodes for visualization.
    
    Returns list of node dicts with:
    - id: unique identifier
    - value: node value
    - left_child_id: reference to left child
    - right_child_id: reference to right child
    - x, y: position coordinates
    """
    if not root:
        return []
    
    nodes = []
    node_id_map = {}
    
    def assign_ids(node: TreeNode, current_id: int = 0) -> int:
        """Recursively assign IDs to all nodes"""
        if not node:
            return current_id
        
        node_id_map[id(node)] = current_id
        nodes.append({
            "id": current_id,
            "value": node.value,
            "left_child_id": None,
            "right_child_id": None,
            "x": 0,
            "y": 0
        })
        
        next_id = current_id + 1
        
        if node.left:
            nodes[current_id]["left_child_id"] = next_id
            next_id = assign_ids(node.left, next_id)
        
        if node.right:
            nodes[current_id]["right_child_id"] = next_id
            next_id = assign_ids(node.right, next_id)
        
        return next_id
    
    assign_ids(root)
    calculate_positions(nodes)
    
    return nodes


def calculate_positions(nodes: List[Dict[str, Any]]):
    """
    Calculate x, y coordinates for tree visualization.
    Uses a layout algorithm that prevents node overlap.
    """
    if not nodes:
        return
    
    # Calculate tree height
    def get_height(node_id: int) -> int:
        if node_id >= len(nodes):
            return 0
        node = nodes[node_id]
        left_height = get_height(node["left_child_id"]) if node["left_child_id"] is not None else 0
        right_height = get_height(node["right_child_id"]) if node["right_child_id"] is not None else 0
        return 1 + max(left_height, right_height)
    
    height = get_height(0)
    total_width = 2 ** height * 40  # Width increases with tree height
    
    def assign_positions(node_id: int, x: int, y: int, width: int):
        """Recursively assign positions"""
        if node_id is None or node_id >= len(nodes):
            return
        
        nodes[node_id]["x"] = x
        nodes[node_id]["y"] = y
        
        # Calculate positions for children
        if nodes[node_id]["left_child_id"] is not None:
            assign_positions(
                nodes[node_id]["left_child_id"],
                x - width // 4,
                y + 80,
                width // 2
            )
        
        if nodes[node_id]["right_child_id"] is not None:
            assign_positions(
                nodes[node_id]["right_child_id"],
                x + width // 4,
                y + 80,
                width // 2
            )
    
    # Start from root at top center
    assign_positions(0, total_width // 2, 50, total_width)


def find_node(root: Optional[TreeNode], value: int) -> Optional[TreeNode]:
    """Find node with given value in BST"""
    if not root or root.value == value:
        return root
    
    if value < root.value:
        return find_node(root.left, value)
    else:
        return find_node(root.right, value)


def find_parent(root: Optional[TreeNode], target: TreeNode) -> Optional[TreeNode]:
    """Find parent of target node"""
    if not root or root == target:
        return None
    
    if root.left == target or root.right == target:
        return root
    
    if target.value < root.value:
        return find_parent(root.left, target)
    else:
        return find_parent(root.right, target)


def get_node_id(nodes: List[Dict], value: int) -> Optional[int]:
    """Get node ID by value"""
    for node in nodes:
        if node["value"] == value:
            return node["id"]
    return None


def tree_to_array(root: Optional[TreeNode]) -> List[Optional[int]]:
    """Convert tree back to level-order array"""
    if not root:
        return []
    
    result = []
    queue = [root]
    
    while queue:
        node = queue.pop(0)
        if node:
            result.append(node.value)
            queue.append(node.left)
            queue.append(node.right)
        else:
            result.append(None)
    
    # Remove trailing None values
    while result and result[-1] is None:
        result.pop()
    
    return result


def create_empty_frame(frame_id: int, description: str) -> Dict[str, Any]:
    """Create an empty frame structure"""
    return {
        "frame_id": frame_id,
        "timestamp_ms": frame_id * 1000,
        "description": description,
        "trees": [],
        "arrays": [],
        "variables": [],
        "stacks": [],
        "queues": [],
        "graphs": [],
        "linked_lists": [],
        "pointers": []
    }
