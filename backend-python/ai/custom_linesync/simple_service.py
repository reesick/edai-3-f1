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

EXAMPLES FOR EACH ALGORITHM TYPE:

For array searching (Linear Search - target 8 in [5,2,8,1]):
IMPORTANT: Show WHICH element is being checked with highlights!

FRAME|0|array|5,2,8,1 highlights:indices=0 colors=yellow|i=0 target=8|7|Start search - checking index 0
FRAME|1|array|5,2,8,1 highlights:indices=0 colors=grey|i=0 target=8|8|Checked arr[0]=5, not equal to 8
FRAME|2|array|5,2,8,1 highlights:indices=0,1 colors=grey,yellow|i=1 target=8|8|Checking arr[1]=2
FRAME|3|array|5,2,8,1 highlights:indices=0,1 colors=grey,grey|i=1 target=8|8|Checked arr[1]=2, not equal
FRAME|4|array|5,2,8,1 highlights:indices=0,1,2 colors=grey,grey,yellow|i=2 target=8|8|Checking arr[2]=8
FRAME|5|array|5,2,8,1 highlights:indices=2 colors=green|i=2 target=8 found=true index=2|8|FOUND at index 2
FRAME|6|array|5,2,8,1 highlights:indices=2 colors=green|found=true index=2|10|Element 8 found at index 2

For Binary Search (target 22 in sorted [11,12,22,25,34,45,50,64,88,90]):
FRAME|0|array|11,12,22,25,34,45,50,64,88,90 highlights:indices=4 colors=yellow|left=0 right=9 mid=4 target=22|11|Check mid=4, arr[4]=34
FRAME|1|array|11,12,22,25,34,45,50,64,88,90 highlights:indices=1 colors=yellow|left=0 right=3 mid=1 target=22|11|Target<34, check left half mid=1
FRAME|2|array|11,12,22,25,34,45,50,64,88,90 highlights:indices=2 colors=yellow|left=2 right=3 mid=2 target=22|11|Target>12, check right half mid=2
FRAME|3|array|11,12,22,25,34,45,50,64,88,90 highlights:indices=2 colors=green|found=true index=2|15|Element 22 FOUND at index 2

For Sentinel Search (target 7 in [4,1,9,2,7]):
FRAME|0|array|4,1,9,2,7,7 highlights:indices=5 colors=blue|i=0 target=7|10|Added sentinel 7 at end (blue)
FRAME|1|array|4,1,9,2,7,7 highlights:indices=0,5 colors=yellow,blue|i=0 target=7|12|Checking arr[0]=4
FRAME|2|array|4,1,9,2,7,7 highlights:indices=0,1,5 colors=grey,yellow,blue|i=1 target=7|12|Checking arr[1]=1
FRAME|3|array|4,1,9,2,7,7 highlights:indices=0,1,2,5 colors=grey,grey,yellow,blue|i=2 target=7|12|Checking arr[2]=9
FRAME|4|array|4,1,9,2,7,7 highlights:indices=0,1,2,3,5 colors=grey,grey,grey,yellow,blue|i=3 target=7|12|Checking arr[3]=2
FRAME|5|array|4,1,9,2,7,7 highlights:indices=4 colors=green|i=4 target=7|12|Found at index 4 (not sentinel)
FRAME|6|array|4,1,9,2,7 highlights:indices=4 colors=green|found=true index=4|15|Element 7 FOUND at index 4

For Fibonacci Search (target 45 in sorted [11,12,22,25,34,45,50]):
FRAME|0|array|11,12,22,25,34,45,50 highlights:indices=3 colors=yellow|fib=8 i=3 target=45|15|Check position 3 (Fibonacci), arr[3]=25
FRAME|1|array|11,12,22,25,34,45,50 highlights:indices=3,5 colors=grey,yellow|fib=5 i=5 target=45|18|Target>25, check position 5, arr[5]=45
FRAME|2|array|11,12,22,25,34,45,50 highlights:indices=5 colors=green|found=true index=5|20|Element 45 FOUND at index 5

For Indexed Sequential Search (indexed blocks, target 45):
FRAME|0|array|11,12,22,25,34,45,50,64 highlights:indices=0,2,4,6 colors=blue,blue,blue,blue|block search|10|Check index blocks
FRAME|1|array|11,12,22,25,34,45,50,64 highlights:indices=4,5 colors=yellow,yellow|linear in block|15|Search in block starting at 4
FRAME|2|array|11,12,22,25,34,45,50,64 highlights:indices=5 colors=green|found=true index=5|18|Element 45 FOUND at index 5

For NOT FOUND case (target 99 in [5,2,8,1]):
FRAME|0|array|5,2,8,1 highlights:indices=0 colors=yellow|i=0 target=99|7|Checking index 0
FRAME|1|array|5,2,8,1 highlights:indices=0,1 colors=grey,yellow|i=1 target=99|8|Checking index 1
FRAME|2|array|5,2,8,1 highlights:indices=0,1,2 colors=grey,grey,yellow|i=2 target=99|8|Checking index 2
FRAME|3|array|5,2,8,1 highlights:indices=0,1,2,3 colors=grey,grey,grey,yellow|i=3 target=99|8|Checking index 3
FRAME|4|array|5,2,8,1 highlights:indices=0,1,2,3 colors=grey,grey,grey,grey|i=4 target=99|8|Checked all elements
FRAME|5|array|5,2,8,1|found=false|11|Element 99 NOT FOUND in array

HIGHLIGHT FORMAT:
- highlights:indices=0,1,2 colors=grey,yellow,green
- Yellow = currently checking
- Grey = already checked  
- Green = found element
- Show progression of search through array!

For tree (BST with nodes 20,8,22,4,12):
CRITICAL: values and structure MUST be in ONE data field, separated by SPACE not pipe!

CORRECT FORMAT:
FRAME|0|tree|values:20,8,22,4,12 structure:0L1-0R2-1L3-1R4|root=20|10|Insert node 20 as root
FRAME|1|tree|values:20,8,22,4,12 structure:0L1-0R2-1L3-1R4|root=20 current=8|12|Insert node 8 to left

WRONG FORMAT (do NOT use):
FRAME|0|tree|values:20,8,22|structure:0L1-0R2|...  ❌ TOO MANY PIPES!

Format for tree:
- Data field contains: "values:X,Y,Z structure:0L1-0R2" (space-separated, NOT pipe-separated)
- values: comma-separated node values
- structure: parent-child links (0L1 = node 0's left child is node 1, 0R2 = node 0's right child is node 2)
- DO NOT add extra pipes between values and structure!

For graph (Topological Sort with 6 nodes):
IMPORTANT: For graph algorithms, ALWAYS show the GRAPH structure (nodes + edges), NOT arrays.

Example - Topological Sort of graph with edges: 5→2, 5→0, 4→0, 4→1, 2→3, 3→1

FRAME|0|graph|nodes:0,1,2,3,4,5 edges:5-2,5-0,4-0,4-1,2-3,3-1 visited:|i=0 V=6|10|Computing indegrees for all nodes
FRAME|1|graph|nodes:0,1,2,3,4,5 edges:5-2,5-0,4-0,4-1,2-3,3-1 visited:|Indegrees computed|17|Found nodes 4 and 5 with indegree 0
FRAME|2|graph|nodes:0,1,2,3,4,5 edges:5-2,5-0,4-0,4-1,2-3,3-1 visited:4|u=4 queue|25|Processing node 4 from queue
FRAME|3|graph|nodes:0,1,2,3,4,5 edges:5-2,5-0,4-0,4-1,2-3,3-1 visited:4,5|u=5 queue|25|Processing node 5 from queue
FRAME|4|graph|nodes:0,1,2,3,4,5 edges:5-2,5-0,4-0,4-1,2-3,3-1 visited:4,5,2|u=2 queue|25|Processing node 2 from queue
FRAME|5|graph|nodes:0,1,2,3,4,5 edges:5-2,5-0,4-0,4-1,2-3,3-1 visited:4,5,2,0,3,1|All nodes|40|Topological sort complete

Format for graph algorithms:
- nodes: ALL graph nodes (0,1,2,3,4,5) - list EVERY node
- edges: directed edges (5-2 means edge from node 5 to node 2)
- visited: nodes that have been processed (will be colored green)
- DO NOT show indegree array as ARR - show the GRAPH structure instead

IMPORTANT: Generate as many frames as needed (no limit) to show COMPLETE algorithm execution.
For recursive algorithms (Quick Sort, DFS, etc.), show EACH recursive call.
For sorting, show EACH comparison and swap.

🚨 CRITICAL COMPLETION REQUIREMENTS 🚨
1. For SORTING algorithms: Last frame MUST show FULLY SORTED ARRAY
2. For SEARCHING algorithms: Last frame MUST show "Element X FOUND at index Y" or "Element X NOT FOUND"
   - Include found=true/false in variables
   - Include index if found
3. For TREE algorithms: Last frame MUST show complete tree structure
4. For GRAPH algorithms: Last frame MUST show all visited nodes or complete path
5. DO NOT STOP until algorithm is 100% COMPLETE

SEARCHING ALGORITHMS MUST:
- Show EVERY comparison step
- Final frame description must contain "FOUND at index" or "NOT FOUND"
- Add variable: found=true or found=false
- If found, add variable: index=X

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
