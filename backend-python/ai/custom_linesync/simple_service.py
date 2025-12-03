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
   - Use 'queue' for ANY queue structure (std::queue, circular queue, custom queue struct)
   - Use 'stack' for ANY stack structure (std::stack, custom stack struct)
   - Look for queue operations: enqueue/dequeue/push+pop, front/rear pointers
   - Look for stack operations: push/pop, top pointer
4. data: comma-separated values ONLY - NO metadata like "f:0 r:0" in data field!
   - CORRECT: "10,20,30 front_index:0 rear_index:2"
   - WRONG: "10,20,30, , ,  f:0 r:0 size:0" (no empty commas, no metadata mixed in!)
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

For linked list operations (format: value1->value2->value3->NULL with highlights):

CRITICAL LINKEDLIST RULES:
- **ALWAYS show the COMPLETE list in EVERY frame**
- NEVER show partial fragments or disconnected nodes
- Only ONE linked list per frame
- Format: number->number->number->NULL (NO SPACES!)
- NEVER use multiple "->NULL" in one line
- Show list changes across FRAMES, not in one line
- Example WRONG: "1->NULL 2->3->NULL" (TWO lists in one frame!)
- Example WRONG: "3->NULL" when full list is "1->2->3->4->5" (partial fragment!)
- Example CORRECT: Frame 1: "1->2->3->4->5->NULL", Frame 2: "2->1->3->4->5->NULL" (COMPLETE lists)

For CREATE/TRAVERSE (print list 1->2->3):
FRAME|0|linkedlist|1->2->3->NULL highlights:indices=0 colors=green|head=1|5|Create node 1 (head)
FRAME|1|linkedlist|1->2->3->NULL highlights:indices=1 colors=green|head=1|6|Create node 2
FRAME|2|linkedlist|1->2->3->NULL highlights:indices=2 colors=green|head=1|7|Create node 3
FRAME|3|linkedlist|1->2->3->NULL highlights:indices=0 colors=yellow|current=1|10|Traverse: at node 1
FRAME|4|linkedlist|1->2->3->NULL highlights:indices=1 colors=yellow|current=2|10|Traverse: at node 2
FRAME|5|linkedlist|1->2->3->NULL highlights:indices=2 colors=yellow|current=3|10|Traverse: at node 3

For REVERSE in groups of K=2 (reverse 1->2->3->4->5):
IMPORTANT: Show COMPLETE list at EVERY step, not partial fragments!
FRAME|0|linkedlist|1->2->3->4->5->NULL|k=2|20|Original complete list
FRAME|1|linkedlist|1->2->3->4->5->NULL highlights:indices=0,1 colors=yellow,yellow|k=2|23|Reversing nodes 1,2 (FULL list shown)
FRAME|2|linkedlist|2->1->3->4->5->NULL highlights:indices=0,1 colors=green,green|k=2|26|Reversed first pair (FULL list shown)
FRAME|3|linkedlist|2->1->3->4->5->NULL highlights:indices=2,3 colors=yellow,yellow|k=2|28|Reversing nodes 3,4 (FULL list shown)
FRAME|4|linkedlist|2->1->4->3->5->NULL highlights:indices=2,3 colors=green,green|k=2|30|Reversed second pair (FULL list shown)
FRAME|5|linkedlist|2->1->4->3->5->NULL|k=2|32|Final complete list

- Data: "value1->value2->value3->NULL"
- Highlights: "highlights:indices=0,1,2 colors=yellow,green,red"
- ALWAYS end with "->NULL"
- Show step-by-step pointer movements

For stack (LIFO - Last In First Out) operations:
IMPORTANT: Stack format is bottom-to-top (first element = bottom, last element = top)
Example: 5,3,8 means 5 is at bottom, 8 is at top

Push operations (adding to stack):
FRAME|0|stack|5 highlights:indices=0 colors=yellow|top=5 size=1|10|Push 5 - stack now has 1 element (5 is top)
FRAME|1|stack|5,3 highlights:indices=1 colors=yellow|top=3 size=2|11|Push 3 - new top element (3 on top of 5)
FRAME|2|stack|5,3,8 highlights:indices=2 colors=yellow|top=8 size=3|12|Push 8 - new top element (8 on top of 3)
FRAME|3|stack|5,3,8,12 highlights:indices=3 colors=yellow|top=12 size=4|13|Push 12 - new top element

Pop operations (removing from stack):
FRAME|4|stack|5,3,8 highlights:indices=2 colors=green|top=8 size=3|16|Pop 12 - removed top, 8 is new top
FRAME|5|stack|5,3 highlights:indices=1 colors=green|top=3 size=2|17|Pop 8 - removed top, 3 is new top
FRAME|6|stack|5 highlights:indices=0 colors=green|top=5 size=1|18|Pop 3 - removed top, 5 is new top

Stack colors: yellow=push operation, green=pop operation
Always highlight the TOP element (last index)
Always show size and top value in variables

CRITICAL FOR EXPRESSION PARSING (INFIX TO POSTFIX):
Only show OPERATORS in stack, NOT operands!
Operands (A,B,C) go directly to output - DO NOT add to stack data!

Example - Infix "A+B*C" to postfix:
FRAME|0|stack||out="" c='A'|10|A is operand, add to output (stack unchanged)
FRAME|1|stack||out="A" c='+'|12|+ is operator, stack empty, push +
FRAME|2|stack|+ highlights:indices=0 colors=yellow|out="A" c='+'|12|Pushed + to stack
FRAME|3|stack|+|out="A" c='B'|10|B is operand, add to output (stack unchanged)
FRAME|4|stack|+|out="AB" c='*'|12|* is operator, higher precedence than +
FRAME|5|stack|+,* highlights:indices=1 colors=yellow|out="AB" c='*'|12|Pushed * to stack
FRAME|6|stack|+,*|out="AB" c='C'|10|C is operand, add to output (stack unchanged)
FRAME|7|stack|+,*|out="ABC"|15|End of input, pop all from stack
FRAME|8|stack|+ highlights:indices=0 colors=green|out="ABC*"|15|Popped * to output
FRAME|9|stack| highlights:indices=0 colors=green|out="ABC*+"|15|Popped + to output
FRAME|10|stack||out="ABC*+"|20|Final: stack empty, output complete

Stack contents = ONLY operators (+, -, *, /, (, ))
Output builds with operands (A, B, C) and operators in postfix order

For queue (FIFO - First In First Out) operations:
IMPORTANT: Queue format is front-to-rear (first element = front, last element = rear)
Always specify front_index and rear_index

Enqueue operations (adding to rear):
FRAME|0|queue|5 front_index:0 rear_index:0 highlights:indices=0 colors=yellow|front=0 rear=0 size=1|10|Enqueue 5 - first element (front and rear at 0)
FRAME|1|queue|5,3 front_index:0 rear_index:1 highlights:indices=1 colors=yellow|front=0 rear=1 size=2|11|Enqueue 3 - added to rear (rear moves to 1)
FRAME|2|queue|5,3,8 front_index:0 rear_index:2 highlights:indices=2 colors=yellow|front=0 rear=2 size=3|12|Enqueue 8 - added to rear (rear moves to 2)
FRAME|3|queue|5,3,8,12 front_index:0 rear_index:3 highlights:indices=3 colors=yellow|front=0 rear=3 size=4|13|Enqueue 12 - added to rear

Dequeue operations (removing from front):
FRAME|4|queue|3,8,12 front_index:0 rear_index:2 highlights:indices=0 colors=green|front=0 rear=2 size=3|16|Dequeue 5 - removed from front (3 is new front)
FRAME|5|queue|8,12 front_index:0 rear_index:1 highlights:indices=0 colors=green|front=0 rear=1 size=2|17|Dequeue 3 - removed from front (8 is new front)
FRAME|6|queue|12 front_index:0 rear_index:0 highlights:indices=0 colors=green|front=0 rear=0 size=1|18|Dequeue 8 - removed from front (12 is new front)

Queue colors: yellow=enqueue operation, green=dequeue operation
Always show front_index and rear_index in data field
Always show front, rear, and size in variables
Highlight operation element (newly added or about to be removed)

For circular queue or custom queue structs (detect ANY queue operations):
If you see: enqueue/dequeue, push+pop together, front/rear pointers, CQueue/CircularQueue struct
=> Use 'queue' type, NOT 'array'!

Example - Custom circular queue with array a[5], front f, rear r:
FRAME|0|queue|10 front_index:0 rear_index:0 highlights:indices=0 colors=yellow|f=0 r=0 size=1|10|Enqueue 10 (first element)
FRAME|1|queue|10,20 front_index:0 rear_index:1 highlights:indices=1 colors=yellow|f=0 r=1 size=2|11|Enqueue 20
FRAME|2|queue|10,20,30 front_index:0 rear_index:2 highlights:indices=2 colors=yellow|f=0 r=2 size=3|12|Enqueue 30
FRAME|3|queue|20,30 front_index:0 rear_index:1 highlights:indices=0 colors=green|f=1 r=2 size=2|15|Dequeue 10 (removed from front)

CRITICAL: Use 'queue' type for ALL queue structures, custom or standard!


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
        
        # DEBUG: Print AI's raw output to terminal
        print("\n" + "="*80)
        print("AI RAW OUTPUT (FRAMES):")
        print("="*80)
        print(ai_text)
        print("="*80 + "\n")
        
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
