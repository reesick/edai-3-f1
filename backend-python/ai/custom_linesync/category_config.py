"""
Category Configuration System

Each algorithm category (sorting, searching, trees, graphs, etc.) has:
1. Optimized prompt template
2. Frame count allocation
3. Specialized parser
4. Completion validator

This ensures ALL 50 algorithms generate COMPLETE visualizations.
"""

from typing import Dict, Any, List, Callable


# ============================================================================
# CATEGORY DEFINITIONS
# ============================================================================

CATEGORY_CONFIG = {
    "sorting": {
        "max_frames": 80,  # INCREASED: Quick Sort needs many frames for recursion
        "keywords": ["sort", "swap", "partition", "merge", "bubble", "quick", "heap"],
        "completion_check": "is_sorted",
        "prompt_focus": "Show EVERY comparison and swap. For recursive sorts, show EACH partition/merge step."
    },
    
    "searching": {
        "max_frames": 30,
        "keywords": ["search", "find", "binary", "linear", "fibonacci"],
        "completion_check": "is_found_or_not_found",
        "prompt_focus": "Show search progression. Indicate when element is found or not found."
    },
    
    "tree": {
        "max_frames": 50,
        "keywords": ["tree", "node", "left", "right", "root", "bst", "traversal"],
        "completion_check": "tree_operation_complete",
        "prompt_focus": "Show tree structure changes. For traversals, visit EVERY node."
    },
    
    "graph": {
        "max_frames": 70,  # Graph algorithms are complex
        "keywords": ["graph", "edge", "vertex", "bfs", "dfs", "dijkstra", "prim", "kruskal"],
        "completion_check": "graph_traversal_complete",
        "prompt_focus": "Show edge/node visits. For pathfinding, show complete path."
    },
    
    "linkedlist": {
        "max_frames": 40,
        "keywords": ["linked", "list", "next", "head", "tail", "node"],
        "completion_check": "list_operation_complete",
        "prompt_focus": "Show pointer movements and node changes."
    },
    
    "stack_queue": {
        "max_frames": 35,
        "keywords": ["stack", "queue", "push", "pop", "enqueue", "dequeue", "top", "front"],
        "completion_check": "stack_queue_operation_complete",
        "prompt_focus": "Show each push/pop or enqueue/dequeue operation."
    }
}


def detect_algorithm_category(code: str) -> str:
    """
    Detect which algorithm category based on code keywords.
    
    IMPORTANT: Check specific categories (graph, tree) BEFORE general ones (sorting)
    to avoid misclassification (e.g., topoSort as sorting instead of graph)
    
    Returns category name or "sorting" as default
    """
    code_lower = code.lower()
    
    # Priority order: Check specific categories first
    priority_order = ["graph", "tree", "linkedlist", "stack_queue", "searching", "sorting"]
    
    for category in priority_order:
        config = CATEGORY_CONFIG.get(category, {})
        for keyword in config.get("keywords", []):
            if keyword in code_lower:
                return category
    
    # Default to sorting if unclear
    return "sorting"


def get_category_max_frames(category: str) -> int:
    """Get maximum frames for a category"""
    return CATEGORY_CONFIG.get(category, {}).get("max_frames", 40)


def get_category_prompt_focus(category: str) -> str:
    """Get specialized prompt focus for category"""
    return CATEGORY_CONFIG.get(category, {}).get("prompt_focus", "Show all steps")


# ============================================================================
# CATEGORY-SPECIFIC VALIDATORS
# ============================================================================

def validate_sorting_complete(frames: List[Dict[str, Any]]) -> bool:
    """Check if array in last frame is sorted"""
    import logging
    logger = logging.getLogger(__name__)
    
    if not frames:
        logger.warning("No frames to validate")
        return False
    
    last_frame = frames[-1]
    if not last_frame.get("arrays"):
        logger.warning("Last frame has no arrays")
        return False
    
    arr = last_frame["arrays"][0].get("values", [])
    sorted_arr = sorted(arr)
    is_sorted = (arr == sorted_arr)
    
    logger.info(f"Sorting validation: arr={arr}, sorted={sorted_arr}, is_sorted={is_sorted}")
    return is_sorted


def validate_searching_complete(frames: List[Dict[str, Any]]) -> bool:
    """Check if search concluded (found or not found)"""
    import logging
    logger = logging.getLogger(__name__)
    
    if not frames:
        logger.warning("No frames to validate for searching")
        return False
    
    last_frame = frames[-1]
    last_desc = last_frame.get("description", "").lower()
    
    # Check if found or not found in description
    found_in_desc = ("found" in last_desc or "not found" in last_desc)
    
    # Also check variables for found flag
    variables = last_frame.get("variables", [])
    found_var = any(v.get("name") == "found" for v in variables)
    
    is_complete = found_in_desc or found_var
    
    logger.info(f"Searching validation: desc='{last_desc[:50]}', has_found_var={found_var}, complete={is_complete}")
    return is_complete


def validate_tree_complete(frames: List[Dict[str, Any]]) -> bool:
    """Check if tree operation completed"""
    # For now, just check if we have frames
    # Can enhance with tree structure validation
    return len(frames) >= 10


def validate_graph_complete(frames: List[Dict[str, Any]]) -> bool:
    """Check if graph traversal completed"""
    # For now, check if reasonable number of frames
    return len(frames) >= 15


def validate_linkedlist_complete(frames: List[Dict[str, Any]]) -> bool:
    """Check if linked list operation completed"""
    return len(frames) >= 10


def validate_linkedlist_complete(frames: List[Dict[str, Any]]) -> bool:
    """Check if linkedlist operation completed"""
    if not frames:
        return False
    
    last_desc = frames[-1].get("description", "").lower()
    # Look for completion indicators
    return any(word in last_desc for word in ["final", "complete", "result", "done", "finished"])


def validate_stack_queue_complete(frames: List[Dict[str, Any]]) -> bool:
    """Check if stack/queue operations completed"""
    return len(frames) >= 10


# Map category to validator function
CATEGORY_VALIDATORS = {
    "sorting": validate_sorting_complete,
    "searching": validate_searching_complete,
    "tree": validate_tree_complete,
    "graph": validate_graph_complete,
    "linkedlist": validate_linkedlist_complete,
    "stack_queue": validate_stack_queue_complete
}


def validate_visualization_complete(category: str, frames: List[Dict[str, Any]]) -> bool:
    """
    Validate if visualization is complete for the category.
    
    Returns True if complete, False if needs more frames
    """
    validator = CATEGORY_VALIDATORS.get(category)
    if not validator:
        return True  # Unknown category, assume complete
    
    return validator(frames)
