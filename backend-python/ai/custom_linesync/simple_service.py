"""
Simple AI Service - Text-Based Output

Instead of asking AI for complex JSON, we ask for simple pipe-delimited text.
This is MUCH more reliable and works for all 50 algorithms.

AI generates: FRAME|id|type|data|vars|line|desc
Backend parses into proper JSON structure.
"""

import logging
from typing import Dict, Any
import google.generativeai as genai
from tenacity import retry, stop_after_attempt, wait_exponential

from .simple_parser import parse_ai_text_output
from .exceptions import GeminiServiceError
from .prompts import detect_data_structures

logger = logging.getLogger(__name__)


# Simple prompt template
SIMPLE_PROMPT_TEMPLATE = """You are visualizing a C++ algorithm step-by-step.

CODE (with line numbers):
{numbered_code}

INPUT: {input_data}

DATA STRUCTURES DETECTED: {data_structures}

TASK: Generate visualization frames in this EXACT format:
FRAME|frameId|dataStructureType|data|variables|lineNumber|description

RULES:
1. One line per frame
2. frameId starts at 0
3. dataStructureType: array, tree, graph, linkedlist, stack, or queue
4. data: comma-separated values (e.g., "5,2,8,1" for arrays)
5. variables: space-separated name=value pairs (e.g., "i=0 j=1")
6. lineNumber: the code line causing this state (1-indexed)
7. description: brief description of what happened

EXAMPLES:

For array sorting:
FRAME|0|array|5,2,8,1|i=0 j=0|7|Initial array state
FRAME|1|array|2,5,8,1|i=0 j=1|9|Swapped arr[0] and arr[1]
FRAME|2|array|2,5,8,1|i=0 j=2|7|Comparing arr[2] and arr[3]

For tree (BST with nodes 20,8,22,4,12):
FRAME|0|tree|values:20,8,22,4,12 structure:0L1-0R2-1L3-1R4|root=20|10|Insert node 20 as root
FRAME|1|tree|values:20,8,22,4,12 structure:0L1-0R2-1L3-1R4|root=20 current=8|12|Insert node 8 to left

Format for tree:
- values: comma-separated node values
- structure: parent-child links (0L1 = node 0's left child is node 1, 0R2 = node 0's right child is node 2)

For graph (Topological Sort with 6 nodes):
FRAME|0|graph|nodes:0,1,2,3,4,5 edges:5-2,5-0,4-0,4-1,2-3,3-1 visited:|indegree computed|15|Computed indegrees
FRAME|1|graph|nodes:0,1,2,3,4,5 edges:5-2,5-0,4-0,4-1,2-3,3-1 visited:4,5|queue=4,5|18|Nodes with indegree 0
FRAME|2|graph|nodes:0,1,2,3,4,5 edges:5-2,5-0,4-0,4-1,2-3,3-1 visited:4,5,0|processing 4|25|Process node 4

Format for graph:
- nodes: comma-separated node IDs (0,1,2,3)
- edges: directed edges with - or > (5-2 means edge from 5 to 2)
- visited: comma-separated visited node IDs (color green)

IMPORTANT: Generate as many frames as needed (no limit) to show COMPLETE algorithm execution.
For recursive algorithms (Quick Sort, DFS, etc.), show EACH recursive call.
For sorting, show EACH comparison and swap.

🚨 CRITICAL COMPLETION REQUIREMENTS 🚨
1. For SORTING algorithms: Last frame MUST show FULLY SORTED ARRAY
2. For SEARCHING algorithms: Last frame MUST show "Element FOUND at index X" or "Element NOT FOUND"
3. For TREE algorithms: Last frame MUST show complete tree structure
4. For GRAPH algorithms: Last frame MUST show all visited nodes or complete path
5. DO NOT STOP until algorithm is 100% COMPLETE

Example for Quick Sort:
- Show EVERY partition step
- Show EVERY recursive call (left and right)
- Show EVERY swap
- FINAL FRAME must show: [11, 12, 22, 25, 34, 45, 50, 64, 88, 90] (fully sorted)

Return ONLY the FRAME lines, nothing else. Generate AS MANY FRAMES AS NEEDED until algorithm COMPLETES.
"""


def add_line_numbers(code: str) -> str:
    """Add line numbers to code for clarity"""
    lines = code.split('\n')
    return '\n'.join(f"{i+1}: {line}" for i, line in enumerate(lines))


@retry(
    stop=stop_after_attempt(3),
    wait=wait_exponential(multiplier=1, min=2, max=10),
    reraise=True
)
async def generate_simple_visualization(
    code: str,
    input_data: str,
    gemini_model: str = "gemini-2.0-flash-exp"
) -> Dict[str, Any]:
    """
    Generate visualization using category-based system with validation.
    
    Process:
    1. Detect algorithm category
    2. Use category-specific max frames and prompt focus
    3. Generate frames (multi-part if needed)
    4. Validate completion
    5. Request more frames if incomplete
    
    Args:
        code: C++ source code
        input_data: Input data
        gemini_model: Gemini model name
    
    Returns:
        Complete visualization dict matching GeminiResponse schema
    """
    try:
        from .category_config import (
            detect_algorithm_category,
            get_category_max_frames,
            get_category_prompt_focus,
            validate_visualization_complete
        )
        
        logger.info("Starting category-based visualization")
        
        # Detect category
        category = detect_algorithm_category(code)
        max_frames = get_category_max_frames(category)
        prompt_focus = get_category_prompt_focus(category)
        
        logger.info(f"Detected category: {category}, max_frames: {max_frames}")
        
        # Detect data structures
        data_structures = detect_data_structures(code)
        
        # Add line numbers
        numbered_code = add_line_numbers(code)
        
        # Build category-optimized prompt
        prompt = SIMPLE_PROMPT_TEMPLATE.format(
            numbered_code=numbered_code,
            input_data=input_data or "No input",
            data_structures=", ".join(data_structures)
        )
        
        # Add category-specific instructions
        prompt += f"\n\nCATEGORY: {category.upper()}\n"
        prompt += f"FOCUS: {prompt_focus}\n"
        prompt += "🚨 GENERATE AS MANY FRAMES AS NEEDED - NO LIMIT\n"
        prompt += "Show COMPLETE algorithm execution from start to FINAL STATE.\n"
        
        # Call AI
        model = genai.GenerativeModel(model_name=gemini_model)
        response = model.generate_content(
            prompt,
            generation_config={
                "temperature": 0.0,
                "max_output_tokens": 8192  # INCREASED: No frame limits, allow complete execution
            }
        )
        
        ai_text = response.text.strip()
        logger.info(f"AI returned {len(ai_text)} characters")
        
        # Parse text into JSON
        result = parse_ai_text_output(ai_text)
        frames = result['visualization']['frames']
        
        logger.info(f"Generated {len(frames)} frames")
        
        # Validate completion
        is_complete = validate_visualization_complete(category, frames)
        
        if not is_complete:
            logger.warning(f"Visualization incomplete for {category}. Requesting completion frames...")
            
            # Request completion frames
            completion_prompt = f"""The previous visualization was incomplete.
            
LAST FRAME WAS:
{frames[-1] if frames else 'None'}

Generate 10-15 MORE frames to COMPLETE the algorithm.
For sorting: Show the FINAL SORTED ARRAY.
For searching: Show element FOUND or NOT FOUND.
Continue in same format: FRAME|id|type|data|vars|line|desc
Start from frame {len(frames)}
"""
            
            completion_response = model.generate_content(
                completion_prompt,
                generation_config={
                    "temperature": 0.0,
                    "max_output_tokens": 2048
                }
            )
            
            # Parse completion frames
            completion_text = completion_response.text.strip()
            completion_result = parse_ai_text_output(completion_text)
            completion_frames = completion_result['visualization']['frames']
            
            # Merge frames
            for cf in completion_frames:
                cf['frame_id'] = len(frames)
                frames.append(cf)
                len(frames)
            
            result['visualization']['frames'] = frames
            result['metadata']['total_frames'] = len(frames)
            
            logger.info(f"Added {len(completion_frames)} completion frames. Total: {len(frames)}")
        
        logger.info(f"Category-based visualization complete: {len(frames)} frames")
        return result
        
    except Exception as e:
        logger.error(f"Category-based visualization failed: {e}")
        raise GeminiServiceError(f"Visualization generation failed: {e}")
