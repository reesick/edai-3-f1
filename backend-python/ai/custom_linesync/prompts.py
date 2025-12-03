"""
Prompt Templates for Gemini 2.0 Flash

Carefully crafted prompts with strict schema enforcement,
few-shot examples, and validation rules to ensure high-quality output.
"""

import json
from typing import Dict, Any, List


# ============================================================================
# DATA STRUCTURE DETECTION SYSTEM
# ============================================================================

DATA_STRUCTURE_HINTS = {
    "array": [
        "arr[", "vector<", "int arr", "int a[", "float arr",
        "array<", "double arr", "char arr"
    ],
    "tree": [
        "Node*", "TreeNode", "left", "right", "root",
        "struct Node", "class Node", "parent", "child"
    ],
    "graph": [
        "adjacency", "edges", "vertices", "graph",
        "adj[", "visited", "distance", "neighbor"
    ],
    "linked_list": [
        "ListNode", "next", "head", "tail", "->next",
        "struct Node", "prev", "doubly", "singly"
    ],
    "stack": [
        "push", "pop", "top", "stack<", "LIFO",
        ".push(", ".pop(", ".top()"
    ],
    "queue": [
        "enqueue", "dequeue", "front", "rear", "queue<",
        "FIFO", ".push(", ".front(", "circular"
    ]
}


def detect_data_structures(code: str) -> List[str]:
    """
    Auto-detect which data structures are present in the code.
    
    Args:
        code: C++ source code
    
    Returns:
        List of detected data structure types
    """
    detected = []
    code_lower = code.lower()
    
    for ds_type, hints in DATA_STRUCTURE_HINTS.items():
        for hint in hints:
            if hint.lower() in code_lower:
                if ds_type not in detected:
                    detected.append(ds_type)
                break
    
    # Default to array if nothing detected
    if not detected:
        detected.append("array")
    
    return detected


def analyze_code_complexity(code: str) -> dict:
    """
    Analyze code complexity to determine appropriate frame count.
    
    Args:
        code: C++ source code
    
    Returns:
        Dict with complexity metrics
    """
    import re
    
    # Count nested loops
    loop_depth = 0
    max_loop_depth = 0
    
    lines = code.split('\n')
    for line in lines:
        # Count opening braces for for/while loops
        if re.search(r'\b(for|while)\s*\(', line):
            loop_depth += 1
            max_loop_depth = max(max_loop_depth, loop_depth)
        # Count closing braces
        if '}' in line:
            loop_depth = max(0, loop_depth - 1)
    
    # Detect recursion
    has_recursion = False
    function_names = re.findall(r'\b\w+\s*\(', code)
    if function_names:
        # Simple heuristic: function calls itself
        for match in re.finditer(r'(\w+)\s*\([^)]*\)\s*{', code):
            func_name = match.group(1)
            # Look for calls to same function name in body
            if re.search(rf'\b{func_name}\s*\(', code[match.end():]):
                has_recursion = True
                break
    
    # Count total lines of actual code (not comments/empty)
    code_lines = [l.strip() for l in lines if l.strip() and not l.strip().startswith('//')]
    loc = len(code_lines)
    
    return {
        'max_loop_depth': max_loop_depth,
        'has_recursion': has_recursion,
        'lines_of_code': loc
    }


def calculate_recommended_frames(complexity: dict) -> int:
    """
    Calculate recommended frame count based on complexity.
    
    Args:
        complexity: Dict from analyze_code_complexity
    
    Returns:
        Recommended number of frames (max 25 for chunked system)
    """
    loop_depth = complexity['max_loop_depth']
    has_recursion = complexity['has_recursion']
    
    # Frame count for chunked system (5 frames per chunk)
    if loop_depth >= 3 or has_recursion:
        # Complex: Quick Sort, Dijkstra - 25 frames (5 chunks)
        return 25
    elif loop_depth == 2:
        # Medium: Bubble Sort, BFS - 20 frames (4 chunks)
        return 20
    else:
        # Simple: Linear Search - 15 frames (3 chunks)
        return 15


# ============================================================================
# STRUCTURE-SPECIFIC PROMPT GUIDES
# ============================================================================

LINKED_LIST_GUIDE = """
LINKED LIST VISUALIZATION REQUIREMENTS:
- Use "linked_lists" field in frames (NOT arrays)
- Each node must have: id, value, next_id (and prev_id for doubly)
- Set head_id and tail_id appropriately
- Show pointer changes when inserting/deleting
- Use highlights to show current, previous nodes
- Example:
  "linked_lists": [{
    "name": "list",
    "type": "singly",
    "nodes": [
      {"id": 0, "value": 10, "next_id": 1, "highlighted": true},
      {"id": 1, "value": 20, "next_id": 2},
      {"id": 2, "value": 30, "next_id": null}
    ],
    "head_id": 0,
    "tail_id": 2
  }]
"""

STACK_QUEUE_GUIDE = """
STACK/QUEUE VISUALIZATION REQUIREMENTS:
- Use "stacks" or "queues" field in frames
- For stacks: show vertical layout with top element highlighted
- For queues: show horizontal layout with front/rear indices
- Update indices as elements are added/removed
- Stack example:
  "stacks": [{
    "name": "s",
    "values": [5, 10, 15, 20],
    "highlights": {"indices": [3], "colors": ["yellow"], "labels": ["top"]}
  }]
- Queue example:
  "queues": [{
    "name": "q",
    "values": [5, 10, 15],
    "front_index": 0,
    "rear_index": 2
  }]
"""

GRAPH_GUIDE = """
GRAPH VISUALIZATION REQUIREMENTS:
- Use "graphs" field in frames
- Each node needs: id, label, x, y coordinates
- Each edge needs: from (node id), to (node id), directed flag
- For weighted graphs: include weight in edges
- Highlight visited nodes and traversed edges
- Example for BFS/DFS:
  "graphs": [{
    "name": "g",
    "type": "directed",
    "nodes": [
      {"id": 0, "label": "A", "x": 100, "y": 100, "highlighted": true},
      {"id": 1, "label": "B", "x": 300, "y": 100}
    ],
    "edges": [
      {"from": 0, "to": 1, "directed": true, "highlighted": true}
    ]
  }]
"""

TREE_GUIDE = """
TREE VISUALIZATION REQUIREMENTS:
- Use "trees" field in frames
- Each node needs: id, value, x, y, left_child_id, right_child_id
- Calculate x,y coordinates for proper tree layout
- Root at top (y=100), children below (y increases down)
- Highlight nodes being visited/modified
- Example for BST:
  "trees": [{
    "name": "bst",
    "type": "binary_search_tree",
    "nodes": [
      {"id": 0, "value": 50, "x": 400, "y": 100, "left_child_id": 1, "right_child_id": 2},
      {"id": 1, "value": 30, "x": 200, "y": 200, "left_child_id": null, "right_child_id": null},
      {"id": 2, "value": 70, "x": 600, "y": 200}
    ]
  }]
"""


# Minimal JSON Schema for Gemini compatibility
# Gemini has strict requirements - keep this as simple as possible
GEMINI_RESPONSE_SCHEMA = {
    "type": "object",
    "required": ["metadata", "visualization", "linesync"],
    "properties": {
        "metadata": {
            "type": "object",
            "required": ["total_frames", "complexity", "data_structures_used"],
            "properties": {
                "total_frames": {"type": "integer"},
                "complexity": {"type": "string"},
                "data_structures_used": {"type": "array"}
            }
        },
        "visualization": {
            "type": "object",
            "required": ["frames"],
            "properties": {
                "frames": {
                    "type": "array"
                }
            }
        },
        "linesync": {
            "type": "object",
            "required": ["frame_mappings"],
            "properties": {
                "setup_lines": {"type": "array"},
                "frame_mappings": {"type": "array"},
                "non_visualized_lines": {"type": "array"}
            }
        }
    }
}


SYSTEM_PROMPT = """You are an expert C++ algorithm visualizer and code execution tracer.

Your task is to analyze C++ code and generate TWO things:
1. **Visualization frames** - Data structure states at each step (ADAPTIVE: 30-100 frames based on complexity)
2. **Line synchronization** - Mapping each frame to source code line(s)

CRITICAL JSON FORMATTING REQUIREMENTS - FOLLOW EXACTLY:
✓ Output MUST be 100% valid JSON - test your output before returning
✓ ALL strings MUST have closing double quotes - no exceptions
✓ NO actual newlines inside string values - use \\n escape sequence instead
✓ NO trailing commas after last item in arrays or objects
✓ NO markdown code blocks (```json or ```) - return raw JSON only
✓ NO comments or explanatory text outside the JSON structure
✓ Use proper escape sequences: \\" for quotes, \\\\ for backslashes, \\n for newlines
✓ Keep all text fields concise (code_snippet under 60 chars, explanation under 80 chars)
✓ Ensure all brackets and braces are properly matched and closed
✓ WHEN GENERATING MANY FRAMES, BE EXTRA CAREFUL WITH COMMAS - double-check syntax  
✓ Every frame except the last must have a comma after its closing brace  
✓ Test your JSON structure before returning - verify it's parseable
✓ STOP GENERATION IMMEDIATELY after closing the final } - no extra text allowed

ALGORITHM REQUIREMENTS:
- Frame IDs must be sequential starting from 0
- Line numbers must be 1-indexed and within 1-100 range
- Only map lines that cause VISUAL changes (skip setup, includes, return statements)
- Categorize lines as: setup, synced, or non-visualized

ADAPTIVE FRAME GENERATION:
- Simple algorithms (1 loop, linear search): Generate 15-20 frames
- Medium algorithms (2 nested loops, bubble sort): Generate 30-35 frames  
- Complex algorithms (3+ loops, recursion, graphs): Generate 45-50 frames (MAX)
- For ALL algorithms, show EVERY significant step - comparisons, swaps, recursion calls
- Focus on DETAIL and CLARITY - users need to UNDERSTAND each step
- Show major state changes: comparisons, swaps, assignments, recursion, traversals
- MAXIMUM 50 frames to ensure reliable JSON generation

DATA STRUCTURES YOU CAN VISUALIZE:
- Arrays/Vectors: horizontal bar layout
- Trees: hierarchical node layout with x,y coordinates
- Graphs: nodes with edges (directed/undirected)
- Linked Lists: nodes with next/prev pointers
- Stacks: vertical LIFO visualization
- Queues: horizontal FIFO visualization
- Variables: simple key-value pairs

HIGHLIGHT TYPES:
- "comparison" - comparing elements
- "modification" - changing values (swap, assignment)
- "assignment" - initial value assignment
- "condition" - if/while condition check
- "default" - other operations
"""


FEW_SHOT_EXAMPLES = """
EXAMPLE 1: Bubble Sort
--------------------------------------------------
CODE:
```cpp
int main() {
    int arr[] = {5, 2, 8, 1};
    int n = 4;
    
    for (int i = 0; i < n-1; i++) {
        for (int j = 0; j < n-i-1; j++) {
            if (arr[j] > arr[j+1]) {
                swap(arr[j], arr[j+1]);
            }
        }
    }
}
```

OUTPUT:
{
  "metadata": {
    "total_frames": 3,
    "complexity": "low",
    "data_structures_used": ["array"]
  },
  "visualization": {
    "frames": [
      {
        "frame_id": 0,
        "description": "Initial array",
        "arrays": [{
          "name": "arr",
          "values": [5, 2, 8, 1],
          "type": "int",
          "highlights": {"indices": [0, 1], "colors": ["blue", "red"], "labels": ["j", "j+1"]}
        }],
        "variables": [{"name": "i", "value": 0, "type": "int"}, {"name": "j", "value": 0, "type": "int"}]
      },
      {
        "frame_id": 1,
        "description": "Swapping arr[0] and arr[1]",
        "arrays": [{
          "name": "arr",
          "values": [2, 5, 8, 1],
          "type": "int",
          "highlights": {"indices": [0, 1], "colors": ["yellow", "yellow"], "labels": ["swapped", "swapped"]}
        }],
        "variables": [{"name": "i", "value": 0, "type": "int"}, {"name": "j", "value": 0, "type": "int"}]
      },
      {
        "frame_id": 2,
        "description": "Comparing arr[2] and arr[3]",
        "arrays": [{
          "name": "arr",
          "values": [2, 5, 8, 1],
          "type": "int",
          "highlights": {"indices": [2, 3], "colors": ["blue", "red"], "labels": ["j", "j+1"]}
        }],
        "variables": [{"name": "i", "value": 0, "type": "int"}, {"name": "j", "value": 2, "type": "int"}]
      }
    ]
  },
  "linesync": {
    "setup_lines": [2, 3],
    "frame_mappings": [
      {
        "frame_id": 0,
        "line_numbers": [7],
        "code_snippet": "if (arr[j] > arr[j+1])",
        "explanation": "Comparing arr[0]=5 and arr[1]=2",
        "highlight_type": "comparison"
      },
      {
        "frame_id": 1,
        "line_numbers": [8],
        "code_snippet": "swap(arr[j], arr[j+1]);",
        "explanation": "Swapping because 5 > 2",
        "highlight_type": "modification"
      },
      {
        "frame_id": 2,
        "line_numbers": [7],
        "code_snippet": "if (arr[j] > arr[j+1])",
        "explanation": "Comparing arr[2]=8 and arr[3]=1",
        "highlight_type": "comparison"
      }
    ],
    "non_visualized_lines": [1, 4, 5, 6, 9, 10, 11, 12]
  }
}

EXAMPLE 2: Binary Search Tree Insert
--------------------------------------------------
CODE:
```cpp
struct Node {
    int val;
    Node* left, *right;
};

void insert(Node* root, int key) {
    if (root == nullptr) return;
    if (key < root->val) insert(root->left, key);
    else insert(root->right, key);
}
```

OUTPUT:
{
  "metadata": {
    "total_frames": 2,
    "complexity": "medium",
    "data_structures_used": ["tree"]
  },
  "visualization": {
    "frames": [
      {
        "frame_id": 0,
        "description": "Checking if 15 < 50 (root)",
        "trees": [{
          "name": "bst",
          "type": "binary_search_tree",
          "nodes": [
            {"id": 0, "value": 50, "x": 400, "y": 100, "highlighted": true, "color": "blue"},
            {"id": 1, "value": 30, "x": 300, "y": 200, "highlighted": false, "color": "default"}
          ]
        }],
        "variables": [{"name": "key", "value": 15, "type": "int"}]
      },
      {
        "frame_id": 1,
        "description": "Moving to left subtree",
        "trees": [{
          "name": "bst",
          "type": "binary_search_tree",
          "nodes": [
            {"id": 0, "value": 50, "x": 400, "y": 100, "highlighted": false, "color": "default"},
            {"id": 1, "value": 30, "x": 300, "y": 200, "highlighted": true, "color": "blue"}
          ]
        }],
        "variables": [{"name": "key", "value": 15, "type": "int"}]
      }
    ]
  },
  "linesync": {
    "setup_lines": [1, 2, 3, 4],
    "frame_mappings": [
      {
        "frame_id": 0,
        "line_numbers": [8],
        "code_snippet": "if (key < root->val)",
        "explanation": "Comparing 15 < 50, will go left",
        "highlight_type": "condition"
      },
      {
        "frame_id": 1,
        "line_numbers": [8],
        "code_snippet": "insert(root->left, key);",
        "explanation": "Recursing to left child",
        "highlight_type": "default"
      }
    ],
    "non_visualized_lines": [5, 6, 7, 9, 10]
  }
}
"""


def build_system_prompt(detected_structures: List[str] = None) -> str:
    """
    Build the complete system prompt with structure-specific guides.
    
    Args:
        detected_structures: List of detected data structure types
    
    Returns:
        Complete system prompt with relevant guides
    """
    prompt = SYSTEM_PROMPT
    
    if detected_structures:
        # Add structure-specific guides based on what was detected
        if "linked_list" in detected_structures:
            prompt += "\n" + LINKED_LIST_GUIDE
        
        if "stack" in detected_structures or "queue" in detected_structures:
            prompt += "\n" + STACK_QUEUE_GUIDE
        
        if "graph" in detected_structures:
            prompt += "\n" + GRAPH_GUIDE
        
        if "tree" in detected_structures:
            prompt += "\n" + TREE_GUIDE
    
    return prompt


def build_user_prompt(code: str, input_data: str, execution_output: str = "") -> str:
    """
    Build the user prompt with code, input, and execution output.
    
    Args:
        code: User's C++ source code
        input_data: Input provided by user
        execution_output: Output from executing the code (if available)
    
    Returns:
        Formatted prompt string
    """
    prompt_parts = [
        "Analyze the following C++ code and generate visualization + linesync data.\n",
        "\n=== CODE ===\n```cpp\n",
        code,
        "\n```\n",
    ]
    
    if input_data:
        prompt_parts.extend([
            "\n=== INPUT ===\n",
            input_data,
            "\n"
        ])
    
    if execution_output:
        prompt_parts.extend([
            "\n=== EXECUTION OUTPUT ===\n",
            execution_output,
            "\n"
        ])
    
    # Analyze code complexity for adaptive frame count
    complexity = analyze_code_complexity(code)
    recommended_frames = calculate_recommended_frames(complexity)
    
    prompt_parts.extend([
        "\n=== INSTRUCTIONS ===\n",
        "Generate a JSON response following the strict schema provided.\n",
        "Trace the execution step-by-step and create visualization frames.\n",
        "Map each frame to the exact source code line(s) that caused that state.\n",
        f"\n⚡ RECOMMENDED FRAME COUNT: {recommended_frames} frames\n",
        f"(Code complexity: {complexity['max_loop_depth']} loop depth, ",
        f"{'recursive' if complexity['has_recursion'] else 'iterative'})\n",
        "\n⚠️ CRITICAL JSON REQUIREMENTS - YOUR RESPONSE WILL BE PARSED DIRECTLY:\n",
        "1. Return ONLY valid JSON - no markdown, no code blocks, no extra text\n",
        "2. Every opening quote \" MUST have a closing quote \"\n",
        "3. Use \\n for line breaks inside strings, NOT actual newlines\n",
        "4. Remove ALL trailing commas before } or ]\n",
        "5. Verify your JSON is valid before returning\n",
        "6. STOP IMMEDIATELY after the final closing } - no explanations after JSON\n",
        "\n=== REFERENCE EXAMPLES (showing correct format) ===\n",
        FEW_SHOT_EXAMPLES,
        "\n=== YOUR RESPONSE - VALID JSON ONLY ===\n",
        "Return your JSON response now (no code blocks, no extra text):\n"
    ])
    
    return "".join(prompt_parts)


def get_generation_config() -> Dict[str, Any]:
    """
    Get Gemini API generation configuration.
    
    Returns:
        Configuration dict for Gemini API
    """
    # ============================================================================
    # PRODUCTION FIX: Aggressive constraints to force valid JSON
    # ============================================================================
    return {
        "response_mime_type": "application/json",
        # Schema disabled - causes validation errors, relying on prompts instead
        "temperature": 0.0,  # CHANGED: Zero temperature for maximum determinism
        "top_p": 0.8,  # CHANGED: Reduced from 0.95
        "top_k": 20,  # CHANGED: Reduced from 40
        "max_output_tokens": 4096,  # CHANGED: 4K for 50 frames max (reliable parsing)
    }
    # ============================================================================
    # END OF CHANGE
    # ============================================================================


def sanitize_gemini_response(response_text: str) -> str:
    """
    Sanitize Gemini response by removing markdown code fences and extra whitespace.
    
    Args:
        response_text: Raw response from Gemini
    
    Returns:
        Cleaned JSON string
    """
    # Remove markdown code fences
    text = response_text.strip()
    
    if text.startswith("```json"):
        text = text[7:]  # Remove ```json
    elif text.startswith("```"):
        text = text[3:]  # Remove ```
    
    if text.endswith("```"):
        text = text[:-3]  # Remove closing ```
    
    # Strip whitespace
    text = text.strip()
    
    return text