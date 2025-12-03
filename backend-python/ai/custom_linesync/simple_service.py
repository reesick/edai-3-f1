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

For tree traversal:
FRAME|0|tree|node:5,left:3,right:7|current=5|10|Visit root
FRAME|1|tree|node:3,left:1,right:4|current=3|12|Traverse left

For graph:
FRAME|0|graph|edges:0-1,0-2|visited:0|15|Start at node 0
FRAME|1|graph|edges:0-1,0-2,1-3|visited:0,1|16|Visit neighbor 1

IMPORTANT: Generate 25-30 frames minimum showing EVERY significant step.
For recursive algorithms (Quick Sort, DFS, etc.), show EACH recursive call.
For sorting, show EACH comparison and swap.

Return ONLY the FRAME lines, nothing else. Do not stop early.
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
    Generate visualization by asking AI for simple text, not JSON.
    
    Process:
    1. Detect data structures
    2. Add line numbers to code
    3. Ask AI for pipe-delimited text
    4. Parse text into structured JSON
    5. Return JSON (frontend unchanged)
    
    Args:
        code: C++ source code
        input_data: Input data
        gemini_model: Gemini model name
    
    Returns:
        Complete visualization dict matching GeminiResponse schema
    """
    try:
        logger.info("Starting simple text-based visualization")
        
        # Detect data structures
        data_structures = detect_data_structures(code)
        logger.info(f"Detected data structures: {data_structures}")
        
        # Add line numbers
        numbered_code = add_line_numbers(code)
        
        # Build prompt
        prompt = SIMPLE_PROMPT_TEMPLATE.format(
            numbered_code=numbered_code,
            input_data=input_data or "No input",
            data_structures=", ".join(data_structures)
        )
        
        # Call AI (asking for TEXT, not JSON)
        model = genai.GenerativeModel(model_name=gemini_model)
        response = model.generate_content(
            prompt,
            generation_config={
                "temperature": 0.0,
                "max_output_tokens": 4096  # INCREASED: More tokens for complex algorithms like Quick Sort
            }
        )
        
        ai_text = response.text.strip()
        logger.info(f"AI returned {len(ai_text)} characters of text")
        
        # Parse text into JSON
        result = parse_ai_text_output(ai_text)
        
        logger.info(f"Successfully parsed {result['metadata']['total_frames']} frames")
        return result
        
    except Exception as e:
        logger.error(f"Simple visualization failed: {e}")
        raise GeminiServiceError(f"Visualization generation failed: {e}")
