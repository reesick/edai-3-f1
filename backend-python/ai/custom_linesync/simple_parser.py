"""
Simple Text Parser for AI-Generated Visualizations

Parses pipe-delimited text into structured JSON for all data structure types.
This approach is MORE RELIABLE than asking AI for complex JSON.

Format: FRAME|id|type|data|vars|line|desc
Example: FRAME|0|array|5,2,8,1|i=0 j=0|7|Comparing elements
"""

import re
from typing import Dict, Any, List


def parse_array_data(data: str) -> List[int]:
    """Parse array values: '5,2,8,1' -> [5,2,8,1]"""
    if not data or data == 'null':
        return []
    return [int(x.strip()) for x in data.split(',') if x.strip()]


def parse_variables(vars_str: str) -> List[Dict[str, Any]]:
    """Parse variables: 'i=0 j=1' -> [{'name':'i','value':0},{'name':'j','value':1}]"""
    if not vars_str or vars_str == 'null':
        return []
    
    variables = []
    for pair in vars_str.split():
        if '=' in pair:
            name, value = pair.split('=', 1)
            variables.append({
                "name": name.strip(),
                "value": value.strip(),
                "type": "int"
            })
    return variables


def parse_tree_data(data: str) -> List[Dict[str, Any]]:
    """Parse tree nodes: 'node:5,left:3,right:7' -> tree structure"""
    if not data or data == 'null':
        return []
    
    trees = []
    # Simple parser for now - can enhance later
    parts = data.split(',')
    for part in parts:
        if ':' in part:
            key, val = part.split(':', 1)
            if key.strip() == 'node':
                trees.append({
                    "value": int(val.strip()),
                    "x": 0,
                    "y": 0,
                    "highlighted": True
                })
    return trees


def parse_graph_data(data: str) -> Dict[str, Any]:
    """Parse graph: 'edges:0-1,0-2 visited:0,1' -> graph structure"""
    if not data or data == 'null':
        return {"nodes": [], "edges": []}
    
    nodes = []
    edges = []
    
    # Parse format: edges:0-1,0-2 visited:0,1
    parts = data.split()
    for part in parts:
        if part.startswith('edges:'):
            edge_list = part[6:].split(',')
            for edge in edge_list:
                if '-' in edge:
                    from_node, to_node = edge.split('-')
                    edges.append({
                        "from": int(from_node.strip()),
                        "to": int(to_node.strip()),
                        "weight": 1
                    })
    
    return {"nodes": nodes, "edges": edges}


def parse_linkedlist_data(data: str) -> List[Dict[str, Any]]:
    """Parse linked list: '1->2->3->NULL' -> list structure"""
    if not data or data == 'null' or data == 'NULL':
        return []
    
    nodes = []
    parts = data.replace('->NULL', '').split('->')
    for i, val in enumerate(parts):
        if val.strip():
            nodes.append({
                "value": int(val.strip()),
                "next": i + 1 if i < len(parts) - 1 else None
            })
    return nodes


def parse_stack_data(data: str) -> List[int]:
    """Parse stack: '5,3,8' (top to bottom) -> [5,3,8]"""
    return parse_array_data(data)


def parse_queue_data(data: str) -> List[int]:
    """Parse queue: '1,2,3,4' (front to rear) -> [1,2,3,4]"""
    return parse_array_data(data)


def build_frame_from_line(line: str, frame_id: int) -> Dict[str, Any]:
    """
    Parse one pipe-delimited line into a frame dict.
    
    Format: FRAME|id|type|data|vars|line|desc
    Example: FRAME|0|array|5,2,8,1|i=0 j=0|7|Comparing elements
    
    Returns:
        Frame dict with proper structure for visualizers
    """
    parts = line.strip().split('|')
    
    if len(parts) < 7:
        raise ValueError(f"Invalid frame format: {line}")
    
    _, _, ds_type, data, vars_str, line_num, desc = parts
    
    frame = {
        "frame_id": frame_id,
        "description": desc.strip(),
        "arrays": [],
        "variables": parse_variables(vars_str),
        "trees": [],
        "graphs": [],
        "linked_lists": [],
        "stacks": [],
        "queues": [],
        "pointers": []
    }
    
    # Add data structure based on type
    if ds_type == 'array':
        frame["arrays"] = [{
            "name": "arr",
            "values": parse_array_data(data),
            "type": "int",
            "highlights": {"indices": [], "colors": [], "labels": []}
        }]
    elif ds_type == 'tree':
        frame["trees"] = parse_tree_data(data)
    elif ds_type == 'graph':
        graph_data = parse_graph_data(data)
        frame["graphs"] = [graph_data]
    elif ds_type == 'linkedlist':
        frame["linked_lists"] = parse_linkedlist_data(data)
    elif ds_type == 'stack':
        frame["stacks"] = [{
            "name": "stk",
            "elements": parse_stack_data(data)
        }]
    elif ds_type == 'queue':
        frame["queues"] = [{
            "name": "q",
            "elements": parse_queue_data(data)
        }]
    
    return frame, int(line_num.strip())


def parse_ai_text_output(text: str) -> Dict[str, Any]:
    """
    Parse complete AI text output into structured visualization data.
    
    Args:
        text: Multi-line pipe-delimited text from AI
    
    Returns:
        Complete visualization dict matching GeminiResponse schema
    """
    lines = [l.strip() for l in text.strip().split('\n') if l.strip() and l.startswith('FRAME')]
    
    frames = []
    line_mappings = []
    
    for i, line in enumerate(lines):
        try:
            frame, line_num = build_frame_from_line(line, i)
            frames.append(frame)
            
            # Build line sync mapping
            line_mappings.append({
                "frame_id": i,
                "line_numbers": [line_num],
                "code_snippet": f"Line {line_num}",
                "explanation": frame["description"],
                "highlight_type": "default"
            })
        except Exception as e:
            print(f"Error parsing line {i}: {e}")
            continue
    
    # Detect data structure type from first frame
    ds_type = "array"
    if frames and frames[0].get("trees"):
        ds_type = "tree"
    elif frames and frames[0].get("graphs"):
        ds_type = "graph"
    elif frames and frames[0].get("linked_lists"):
        ds_type = "linkedlist"
    elif frames and frames[0].get("stacks"):
        ds_type = "stack"
    elif frames and frames[0].get("queues"):
        ds_type = "queue"
    
    return {
        "metadata": {
            "total_frames": len(frames),
            "complexity": "medium" if len(frames) > 15 else "low",
            "data_structures_used": [ds_type]
        },
        "visualization": {
            "frames": frames
        },
        "linesync": {
            "setup_lines": [1, 2],
            "frame_mappings": line_mappings,
            "non_visualized_lines": []
        }
    }
