# Split-Call Prompt Templates
# These prompts are used for the 3-call split system to ensure reliable JSON parsing

METADATA_ONLY_PROMPT = """You are analyzing C++ code to extract metadata.

TASK: Analyze the code and return ONLY metadata in JSON format.

Your response MUST be valid JSON with this EXACT structure:
{
  "complexity": "low" | "medium" | "high",
  "data_structures_used": ["array", "tree", etc.],
  "setup_lines": [1, 2, 3],
  "recommended_frames": <number between 15-50>
}

RULES:
- Return ONLY the JSON object above
- No markdown, no code blocks, no explanations
- Determine complexity from loop depth and recursion
- Identify which data structures are used in the code
- List setup lines (includes, initial declarations that aren't visualized)
- Recommend frame count: 15-20 (simple), 30-35 (medium), 45-50 (complex)

Remember: ONLY return the JSON, nothing else.
"""

FRAMES_ONLY_PROMPT_TEMPLATE = """You are generating visualization frames for C++ code execution.

CONTEXT FROM PREVIOUS ANALYSIS:
- Complexity: {complexity}
- Data structures: {data_structures}
- Recommended frames: {frames_count}

TASK: Generate EXACTLY {frames_count} visualization frames showing algorithm execution.

Your response MUST be valid JSON with this EXACT structure:
{{
  "frames": [
    {{
      "frame_id": 0,
      "description": "Initial state",
      "arrays": [...],
      "variables": [...],
      (other data structures as needed)
    }},
    ... {frames_count} frames total
  ]
}}

RULES:
- Generate EXACTLY {frames_count} frames (no more, no less)
- Frame IDs must be 0, 1, 2, ... {frames_count_minus_1}
- Use ONLY these data structures: {data_structures}
- Show every significant step: comparisons, swaps, assignments
- Each frame must have a clear description
- Return ONLY the JSON object above
- No markdown, no code blocks, no explanations

Remember: ONLY return the JSON with frames array, nothing else.
"""

LINESYNC_ONLY_PROMPT_TEMPLATE = """You are mapping visualization frames to source code lines.

CONTEXT:
- Total frames: {frames_count}
- Code has {total_lines} lines

TASK: Map each of the {frames_count} frames to the source code line(s) that caused that state.

Your response MUST be valid JSON with this EXACT structure:
{{
  "frame_mappings": [
    {{
      "frame_id": 0,
      "line_numbers": [7],
      "code_snippet": "int arr[5] = {{...}}",
      "explanation": "Initialize array",
      "highlight_type": "assignment"
    }},
    ... {frames_count} mappings total
  ],
  "non_visualized_lines": [1, 2, 10, 15]
}}

RULES:
- Create EXACTLY {frames_count} mappings (one for each frame 0 to {frames_count_minus_1})
- Line numbers must be between 1 and {total_lines}
- Only map lines that cause VISUAL changes (skip includes, return statements)
- code_snippet should be under 60 characters
- explanation should be under 80 characters
- highlight_type: "comparison", "modification", "assignment", "condition", or "default"
- List lines that aren't visualized in non_visualized_lines
- Return ONLY the JSON object above
- No markdown, no code blocks, no explanations

Remember: ONLY return the JSON with linesync data, nothing else.
"""
