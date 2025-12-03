"""
Simple Text Parser for AI-Generated Visualizations

Parses pipe-delimited text into structured JSON for all data structure types.
This approach is MORE RELIABLE than asking AI for complex JSON.

Format: FRAME|id|type|data|vars|line|desc
Example: FRAME|0|array|5,2,8,1|i=0 j=0|7|Comparing elements
"""

import re
from typing import Dict, Any, List


def parse_array_data(data: str) -> Dict[str, Any]:
    """
    Parse array values with optional highlights.
    
    Format: '5,2,8,1' or '5,2,8,1 highlights:indices=0,2 colors=yellow,green'
    """
    if not data or data == 'null':
        return {"name": "arr", "values": [], "type": "int", "highlights": {"indices": [], "colors": [], "labels": []}}
    
    # Split data and highlights
    parts = data.split(' highlights:')
    values_str = parts[0]
    
    # Parse values - detect if float or int
    values = []
    for x in values_str.split(','):
        if x.strip():
            # Check if float (has decimal point) or int
            if '.' in x:
                values.append(float(x.strip()))
            else:
                values.append(int(x.strip()))
    
    # Parse highlights if present
    highlight_indices = []
    highlight_colors = []
    
    if len(parts) > 1:
        highlight_str = parts[1]
        # Format: indices=0,1,2 colors=yellow,grey,green
        for segment in highlight_str.split():
            if segment.startswith('indices='):
                indices_str = segment.split('=')[1]
                highlight_indices = [int(i.strip()) for i in indices_str.split(',') if i.strip()]
            elif segment.startswith('colors='):
                colors_str = segment.split('=')[1]
                highlight_colors = [c.strip() for c in colors_str.split(',') if c.strip()]
    
    return {
        "name": "arr",
        "values": values,
        "type": "int",
        "highlights": {
            "indices": highlight_indices,
            "colors": highlight_colors,
            "labels": []
        }
    }


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


def parse_tree_data(data: str) -> Dict[str, Any]:
    """
    Parse tree nodes and build proper tree structure for TreeVisualizer.
    
    Format: 'values:20,8,22,4,12,10,14 structure:0L1-0R2-1L3-1R4-4L5-4R6'
    OR simple: '20,8,22,4,12' (values in level-order)
    
    Returns tree dict with nodes array containing id, value, x, y, left_child_id, right_child_id
    """
    if not data or data == 'null':
        return {"name": "Tree", "type": "Binary Tree", "nodes": []}
    
    nodes = []
    
    # Parse format: values:20,8,22 structure:0L1-0R2
    if 'values:' in data and 'structure:' in data:
        parts = data.split()
        values_str = next((p.split(':')[1] for p in parts if p.startswith('values:')), '')
        structure_str = next((p.split(':')[1] for p in parts if p.startswith('structure:')), '')
        
        # Parse values, skip NULL (represents deleted/missing nodes)
        values = []
        for v in values_str.split(','):
            v_clean = v.strip().upper()
            if v_clean and v_clean != 'NULL':
                values.append(int(v.strip()))
        
        # Build nodes with IDs
        for i, val in enumerate(values):
            nodes.append({
                "id": i,
                "value": val,
                "x": 0,  # Will calculate layout
                "y": 0,
                "highlighted": False,
                "left_child_id": None,
                "right_child_id": None,
                "color": "default"
            })
        
        # Parse structure links: 0L1 means node 0's left child is node 1
        if structure_str:
            for link in structure_str.split('-'):
                if 'L' in link:
                    parent_id, child_id = link.split('L')
                    nodes[int(parent_id)]["left_child_id"] = int(child_id)
                elif 'R' in link:
                    parent_id, child_id = link.split('R')
                    nodes[int(parent_id)]["right_child_id"] = int(child_id)
    
    else:
        # Simple format: just values (build BST structure)
        values = [int(v.strip()) for v in data.split(',') if v.strip() and v.strip() != 'null']
        for i, val in enumerate(values):
            nodes.append({
                "id": i,
                "value": val,
                "x": 0,
                "y": 0,
                "highlighted": False,
                "left_child_id": None,
                "right_child_id": None,
                "color": "default"
            })
    
    # Calculate x, y positions (simple binary tree layout)
    if nodes:
        _calculate_tree_layout(nodes)
    
    return {"name": "Tree", "type": "Binary Tree", "nodes": nodes}


def _calculate_tree_layout(nodes: List[Dict[str, Any]], node_id: int = 0, x: int = 200, y: int = 50, h_spacing: int = 100, v_spacing: int = 80, level: int = 0):
    """Calculate x,y coordinates for tree nodes (recursive layout)"""
    if node_id >= len(nodes):
        return
    
    node = nodes[node_id]
    node["x"] = x
    node["y"] = y
    
    # Layout left and right children
    offset = h_spacing / (2 ** level) if level > 0 else h_spacing
    
    if node["left_child_id"] is not None:
        _calculate_tree_layout(nodes, node["left_child_id"], x - offset, y + v_spacing, h_spacing, v_spacing, level + 1)
    
    if node["right_child_id"] is not None:
        _calculate_tree_layout(nodes, node["right_child_id"], x + offset, y + v_spacing, h_spacing, v_spacing, level + 1)


def parse_graph_data(data: str) -> Dict[str, Any]:
    """
    Parse graph: 'nodes:0,1,2,3,4,5 edges:5-2,5-0,4-0,4-1,2-3,3-1 visited:4,5'
    
    Returns graph dict with nodes and edges arrays for GraphVisualizer
    """
    if not data or data == 'null':
        return {"name": "Graph", "directed": True, "nodes": [], "edges": []}
    
    nodes = []
    edges = []
    visited_set = set()
    
    # Parse format: nodes:0,1,2 edges:0-1,0-2 visited:0,1
    parts = data.split()
    
    # Extract nodes
    nodes_str = next((p.split(':')[1] for p in parts if p.startswith('nodes:')), '')
    if nodes_str:
        node_ids = [int(n.strip()) for n in nodes_str.split(',') if n.strip()]
        for nid in node_ids:
            nodes.append({
                "id": nid,
                "label": str(nid),
                "visited": False,
                "color": "#555"
            })
    
    # Extract edges
    edges_str = next((p.split(':')[1] for p in parts if p.startswith('edges:')), '')
    if edges_str:
        edge_list = edges_str.split(',')
        for edge in edge_list:
            if '-' in edge or '>' in edge:
                # Support both 0-1 and 0>1 formats
                separator = '>' if '>' in edge else '-'
                from_node, to_node = edge.split(separator)
                edges.append({
                    "from": int(from_node.strip()),
                    "to": int(to_node.strip()),
                    "weight": 1,
                    "highlighted": False
                })
    
    # Extract visited nodes
    visited_str = next((p.split(':')[1] for p in parts if p.startswith('visited:')), '')
    if visited_str:
        visited_ids = [int(v.strip()) for v in visited_str.split(',') if v.strip()]
        visited_set = set(visited_ids)
        # Mark visited nodes
        for node in nodes:
            if node["id"] in visited_set:
                node["visited"] = True
                node["color"] = "#4CAF50"  # Green for visited
    
    return {
        "name": "Graph",
        "directed": True,
        "nodes": nodes,
        "edges": edges
    }


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
    parts = line.strip().split('|', 6)  # FIXED: maxsplit=6 to handle pipes in description
    
    if len(parts) < 7:
        raise ValueError(f"Invalid frame format (expected 7 parts, got {len(parts)}): {line}")
    
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
        frame["arrays"] = [parse_array_data(data)]
    elif ds_type == 'tree':
        tree_data = parse_tree_data(data)
        if tree_data and tree_data.get("nodes"):
            frame["trees"] = [tree_data]
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
            
            # Skip blank frames (no data structures)
            has_data = (
                frame.get("arrays") or 
                frame.get("trees") or 
                frame.get("graphs") or 
                frame.get("linked_lists") or 
                frame.get("stacks") or 
                frame.get("queues")
            )
            
            if not has_data:
                print(f"Skipping blank frame {i}")
                continue
            
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
            print(f"  Line content: {line[:100]}...")  # Show first 100 chars
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
