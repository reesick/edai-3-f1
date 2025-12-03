"""
Chunked AI Visualization Service

Production-grade service that generates visualizations in small chunks (5 frames each)
to ensure reliable JSON parsing. Follows the same structure as service.py.

Call sequence:
1. Metadata (complexity, frames needed)
2. Frame chunks (5 frames per call)
3. LineSync (map frames to code lines)
"""

import json
import logging
import re
from typing import Dict, Any, List, Optional
from tenacity import retry, stop_after_attempt, wait_exponential
import google.generativeai as genai

from .exceptions import GeminiServiceError, ValidationFailedError
from .prompts import get_generation_config

logger = logging.getLogger(__name__)


# ============================================================================
# JSON REPAIR UTILITIES (Copied from service.py for independence)
# ============================================================================

def repair_json_simple(text: str) -> str:
    """Quick JSON repair - remove markdown, fix trailing commas, close brackets"""
    text = text.strip()
    
    #Remove markdown fences
    if text.startswith("```json"):
        text = text[7:]
    elif text.startswith("```"):
        text = text[3:]
    if text.endswith("```"):
        text = text[:-3]
    text = text.strip()
    
    # Remove trailing commas
    text = re.sub(r',(\s*[}\]])', r'\1', text)
    
    # Close unclosed structures
    open_braces = text.count('{') - text.count('}')
    open_brackets = text.count('[') - text.count(']')
    
    if open_braces > 0:
        text += '}' * open_braces
    if open_brackets > 0:
        text += ']' * open_brackets
    
    return text


def parse_json_safe(text: str) -> Dict[str, Any]:
    """Parse JSON with repair attempt"""
    try:
        return json.loads(text)
    except json.JSONDecodeError:
        repaired = repair_json_simple(text)
        return json.loads(repaired)


# ============================================================================
# CHUNKED PROMPTS (Following prompts.py style)
# ============================================================================

METADATA_PROMPT = """You are analyzing C++ code to extract metadata for visualization.

TASK: Return ONLY a JSON object with metadata about this code.

CRITICAL JSON REQUIREMENTS:
✓ Return ONLY valid JSON - no markdown, no explanations
✓ ALL strings must have closing quotes
✓ NO trailing commas
✓ Stop immediately after closing }

Required JSON structure:
{
  "complexity": "low" | "medium" | "high",
  "data_structures_used": ["array", "tree", etc.],
  "setup_lines": [line numbers that are setup/includes],
  "recommended_frames": <15-25 based on complexity>
}

FRAME RECOMMENDATIONS:
- Low complexity (1 loop, simple): 15 frames
- Medium complexity (2 nested loops): 20 frames  
- High complexity (3+ loops, recursion): 25 frames MAX
"""


FRAMES_CHUNK_PROMPT_TEMPLATE = """You are generating visualization frames {{start_id}} to {{end_id}} (exactly 5 frames).

CONTEXT:
- Data structures in code: {{data_structures}}
- Total frames needed: {{total_frames}}
{{context_state}}

TASK: Generate EXACTLY 5 frames (frame_id {{start_id}} through {{end_id}}).

CRITICAL JSON REQUIREMENTS:
✓ Return ONLY valid JSON - no markdown, no explanations
✓ Generate EXACTLY 5 frames
✓ Frame IDs must be {{start_id}}, {{start_id}}+1, {{start_id}}+2, {{start_id}}+3, {{start_id}}+4
✓ Each frame must show state evolution
✓ ALL strings must have closing quotes
✓ NO trailing commas
✓ Stop immediately after final }}

Required JSON structure:
{{{{
  "frames": [
    {{{{
      "frame_id": {{start_id}},
      "description": "What happened in this step",
      "arrays": [...if using arrays],
      "variables": [...always include loop vars],
      "trees": [...if using trees],
      "graphs": [...if using graphs],
      "linked_lists": [...if using linked lists],
      "stacks": [...if using stacks],
      "queues": [...if using queues]
    }}}},
    ...4 more frames (total 5)
  ]
}}}}

Show EVERY significant step: comparisons, swaps, assignments, traversals.
"""


LINESYNC_PROMPT = """You are mapping visualization frames to source code lines.

CONTEXT:
- Total frames: {{total_frames}}
- Code has {{total_lines}} lines

TASK: Map each frame to the exact source code line(s) that caused that state.

CRITICAL JSON REQUIREMENTS:
✓ Return ONLY valid JSON - no markdown, no explanations  
✓ Create EXACTLY {{total_frames}} mappings
✓ Line numbers must be 1 to {{total_lines}}
✓ ALL strings must have closing quotes
✓ NO trailing commas
✓ Stop immediately after final }}}}

Required JSON structure:
{{{{
  "frame_mappings": [
    {{{{
      "frame_id": 0,
      "line_numbers": [7],
      "code_snippet": "if (arr[j] > arr[j+1])",
      "explanation": "Comparing elements",
      "highlight_type": "comparison"
    }}}},
    ...{{total_frames}} total mappings
  ],
  "non_visualized_lines": [1, 2, 10]
}}}}

highlight_type options: "comparison", "modification", "assignment", "condition", "default"
Only map lines that cause VISUAL changes in data structures.
"""


# ============================================================================
# CHUNKED AI CALLS
# ============================================================================

@retry(
    stop=stop_after_attempt(3),
    wait=wait_exponential(multiplier=1, min=2, max=10),
    reraise=True
)
async def call_metadata(code: str, model: genai.GenerativeModel) -> Dict[str, Any]:
    """
    Call 1: Get metadata (complexity, data structures, recommended frames).
    
    Returns:
        dict with: complexity, data_structures_used, setup_lines, recommended_frames
    """
    try:
        prompt = f"{METADATA_PROMPT}\n\nCODE:\n```cpp\n{code}\n```\n\nReturn JSON:"
        
        response = model.generate_content(
            prompt,
            generation_config={
                "response_mime_type": "application/json",
                "temperature": 0.0,
                "max_output_tokens": 512
            }
        )
        
        metadata = parse_json_safe(response.text)
        
        # Validate
        if 'recommended_frames' not in metadata:
            metadata['recommended_frames'] = 20
        metadata['recommended_frames'] = min(25, max(15, metadata['recommended_frames']))
        
        logger.info(f"Metadata: {metadata['complexity']} complexity, {metadata['recommended_frames']} frames")
        return metadata
        
    except Exception as e:
        logger.error(f"Metadata call failed: {e}")
        raise GeminiServiceError(f"Metadata failed: {e}")


@retry(
    stop=stop_after_attempt(3),
    wait=wait_exponential(multiplier=1, min=2, max=10),
    reraise=True
)
async def call_frames_chunk(
    code: str,
    input_data: str,
    start_id: int,
    end_id: int,
    total_frames: int,
    data_structures: List[str],
    previous_state: Optional[str],
    model: genai.GenerativeModel
) -> List[Dict[str, Any]]:
    """
    Call N: Get 5 frames (chunk).
    
    Args:
        code: C++ code
        input_data: Input data
        start_id: Starting frame ID (e.g., 0, 5, 10)
        end_id: Ending frame ID (e.g., 4, 9, 14)
        total_frames: Total frames in visualization
        data_structures: List of data structures being used
        previous_state: JSON string of last frame from previous chunk (for continuity)
        model: Gemini model
    
    Returns:
        List of 5 frame dicts
    """
    try:
        context = ""
        if previous_state:
            context = f"\nPrevious frame state:\n{previous_state}\n\nContinue from this state."
        
        prompt = FRAMES_CHUNK_PROMPT_TEMPLATE.format(
            start_id=start_id,
            end_id=end_id,
            data_structures=", ".join(data_structures),
            total_frames=total_frames,
            context_state=context
        )
        
        prompt += f"\n\nCODE:\n```cpp\n{code}\n```\n\nINPUT:\n{input_data}\n\nReturn JSON with 5 frames:"
        
        response = model.generate_content(
            prompt,
            generation_config={
                "response_mime_type": "application/json",
                "temperature": 0.0,
                "max_output_tokens": 2048
            }
        )
        
        chunk_data = parse_json_safe(response.text)
        frames = chunk_data.get('frames', [])
        
        # Validate frame count
        if len(frames) != 5:
            logger.warning(f"Expected 5 frames, got {len(frames)}")
        
        # Fix frame IDs if needed
        for i, frame in enumerate(frames):
            expected_id = start_id + i
            if frame.get('frame_id') != expected_id:
                frame['frame_id'] = expected_id
        
        logger.info(f"Chunk {start_id}-{end_id}: Generated {len(frames)} frames")
        return frames
        
    except Exception as e:
        logger.error(f"Frames chunk {start_id}-{end_id} failed: {e}")
        raise GeminiServiceError(f"Frames chunk failed: {e}")


@retry(
    stop=stop_after_attempt(3),
    wait=wait_exponential(multiplier=1, min=2, max=10),
    reraise=True
)
async def call_linesync(
    code: str,
    total_frames: int,
    model: genai.GenerativeModel
) -> Dict[str, Any]:
    """
    Call LAST: Get line synchronization mappings.
    
    Returns:
        dict with: frame_mappings, non_visualized_lines
    """
    try:
        total_lines = len(code.split('\n'))
        
        prompt = LINESYNC_PROMPT.format(
            total_frames=total_frames,
            total_lines=total_lines
        )
        
        prompt += f"\n\nCODE:\n```cpp\n{code}\n```\n\nReturn JSON:"
        
        response = model.generate_content(
            prompt,
            generation_config={
                "response_mime_type": "application/json",
                "temperature": 0.0,
                "max_output_tokens": 2048
            }
        )
        
        linesync = parse_json_safe(response.text)
        
        logger.info(f"LineSync: {len(linesync.get('frame_mappings', []))} mappings")
        return linesync
        
    except Exception as e:
        logger.error(f"LineSync call failed: {e}")
        raise GeminiServiceError(f"LineSync failed: {e}")


# ============================================================================
# MAIN ORCHESTRATOR
# ============================================================================

async def chunked_visualization(
    code: str,
    input_data: str,
    gemini_model: str = "gemini-2.0-flash-exp"
) -> Dict[str, Any]:
    """
    Main function: Generate visualization using chunked calls.
    
    Process:
    1. Get metadata (1 call)
    2. Get frames in chunks of 5 (multiple calls)
    3. Get linesync (1 call)
    4. Merge and return
    
    Args:
        code: C++ source code
        input_data: Input data for execution
        gemini_model: Model name
    
    Returns:
        Complete visualization dict matching GeminiResponse schema
    """
    try:
        model = genai.GenerativeModel(model_name=gemini_model)
        
        logger.info("Starting chunked visualization (chunks of 5 frames)")
        
        # Call 1: Metadata
        metadata = await call_metadata(code, model)
        total_frames = metadata['recommended_frames']
        data_structures = metadata['data_structures_used']
        
        # Calls 2-N: Frame chunks (5 frames each)
        all_frames = []
        previous_state = None
        
        for start in range(0, total_frames, 5):
            end = min(start + 4, total_frames - 1)
            
            chunk_frames = await call_frames_chunk(
                code, input_data, start, end, total_frames,
                data_structures, previous_state, model
            )
            
            all_frames.extend(chunk_frames)
            
            # Save last frame state for next chunk
            if chunk_frames:
                previous_state = json.dumps(chunk_frames[-1], indent=2)
        
        # Call LAST: LineSync
        linesync = await call_linesync(code, len(all_frames), model)
        
        # Merge results
        result = {
            "metadata": {
                "total_frames": len(all_frames),
                "complexity": metadata.get('complexity', 'medium'),
                "data_structures_used": data_structures
            },
            "visualization": {
                "frames": all_frames
            },
            "linesync": {
                "setup_lines": metadata.get('setup_lines', []),
                "frame_mappings": linesync.get('frame_mappings', []),
                "non_visualized_lines": linesync.get('non_visualized_lines', [])
            }
        }
        
        logger.info(f"Chunked visualization complete: {len(all_frames)} frames total")
        return result
        
    except Exception as e:
        logger.error(f"Chunked visualization failed: {e}")
        raise GeminiServiceError(f"Chunked visualization failed: {e}")
