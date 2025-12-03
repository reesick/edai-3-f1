"""
Indexed Sequential Search - PRODUCTION GRADE with 16-18 frames  
Jump through index blocks then linear search within block
"""

def create_frame(step_id, description, data, highlights=None, variables=None):
    return {
        "step": step_id,
        "description": description,
        "data": data,
        "highlights": highlights or [],
        "variables": variables or []
    }

CODE_SAMPLE = """#include <bits/stdc++.h>
using namespace std;

int indexedSequentialSearch(vector<int>& arr, int target) {
    int n = arr.size();
    int jump = sqrt(n);  // Block size
    
    // Jump through blocks
    int prev = 0;
    while (arr[min(jump, n)-1] < target) {
        prev = jump;
        jump += sqrt(n);
        if (prev >= n)
            return -1;
    }
    
    // Linear search in block
    while (arr[prev] < target) {
        prev++;
        if (prev == min(jump, n))
            return -1;
    }
    
    if (arr[prev] == target)
        return prev;
    return -1;
}

int main() {
    vector<int> arr = {10, 20, 30, 40, 50, 60, 70, 80, 90, 100};
    int target = 70;
    int result = indexedSequentialSearch(arr, target);
    return 0;
}
"""

def execute(params):
    frames, frame_id = [], 0
    arr = params.get('array', [10, 20, 30, 40, 50, 60, 70, 80, 90, 100])
    target = params.get('target', 70)
    
    import math
    n = len(arr)
    jump = int(math.sqrt(n))
    
    # FRAME 0: Intro
    frames.append(create_frame(frame_id,
        "🎯 Indexed Sequential Search: Divide array into blocks, jump through blocks, then linear search within block",
        arr, [], [{"name": "target", "value": str(target), "type": "int"}]))
    frame_id += 1
    
    # FRAME 1: Block size calculation
    frames.append(create_frame(frame_id,
        f"📐 Calculate block size: √{n} = {jump}. Array divided into ~{math.ceil(n/jump)} blocks of size {jump}",
        arr, [], [
            {"name": "array_size", "value": str(n), "type": "int"},
            {"name": "block_size", "value": str(jump), "type": "int"}
        ]))
    frame_id += 1
    
    # FRAME 2: Strategy
    frames.append(create_frame(frame_id,
        "🧭 Strategy: (1) Jump through blocks checking last element (2) Linear search within found block",
        arr, [], [{"name": "time_complexity", "value": "O(√n)", "type": "string"}]))
    frame_id += 1
    
    # Phase 1: Jump through blocks
    prev = 0
    current_jump = jump
    jumps_made = 0
    
    while current_jump < n and arr[current_jump - 1] < target:
        jumps_made += 1
        
        # FRAME: Jump
        block_end = min(current_jump - 1, n - 1)
        frames.append(create_frame(frame_id,
            f"🦘 Jump {jumps_made}: Check block end arr[{block_end}] = {arr[block_end]} vs {target}",
            arr, [block_end], [
                {"name": "block_end", "value": str(block_end), "type": "int"},
                {"name": "block_end_value", "value": str(arr[block_end]), "type": "int"}
            ]))
        frame_id += 1
        
        frames.append(create_frame(frame_id,
            f"➡️ {arr[block_end]} < {target}: Jump to next block!",
            arr, list(range(prev, current_jump)), [{"name": "jumping", "value": "true", "type": "boolean"}]))
        frame_id += 1
        
        prev = current_jump
        current_jump += jump
    
    # Check if out of bounds
    if prev >= n:
        frames.append(create_frame(frame_id,
            f"❌ Jumped past array end. {target} not in array",
            arr, [], [{"name": "result", "value": "-1", "type": "int"}]))
        return frames
    
    # FRAME: Found block
    block_start = prev
    block_end = min(current_jump, n)
    frames.append(create_frame(frame_id,
        f"✓ Found target block! Must be in range [{block_start}..{block_end-1}]  ",
        arr, list(range(block_start, block_end)), [
            {"name": "block_start", "value": str(block_start), "type": "int"},
            {"name": "block_end", "value": str(block_end-1), "type": "int"}
        ]))
    frame_id += 1
    
    # FRAME: Linear search phase
    frames.append(create_frame(frame_id,
        f"🔍 Phase 2: Linear search within block [{block_start}..{block_end-1}]",
        arr, list(range(block_start, block_end)), []))
    frame_id += 1
    
    # Linear search in block
    comparisons_in_block = 0
    found_index = -1
    
    for i in range(block_start, min(block_end, n)):
        comparisons_in_block += 1
        
        frames.append(create_frame(frame_id,
            f"🔍 Check arr[{i}] = {arr[i]} vs {target}",
            arr, [i], [
                {"name": "checking_index", "value": str(i), "type": "int"},
                {"name": "comparisons_in_block", "value": str(comparisons_in_block), "type": "int"}
            ]))
        frame_id += 1
        
        if arr[i] == target:
            found_index = i
            frames.append(create_frame(frame_id,
                f"✅ MATCH! Found {target} at index {i}",
                arr, [i], [{"name": "found_at", "value": str(i), "type": "int"}]))
            frame_id += 1
            break
        elif arr[i] > target:
            frames.append(create_frame(frame_id,
                f"❌ {arr[i]} > {target}: Target would be before this. Not found!",
                arr, [], [{"name": "result", "value": "-1", "type": "int"}]))
            frame_id += 1
            found_index = -1
            break
    
    # Final summary
    if found_index != -1:
        frames.append(create_frame(frame_id,
            f"🎉 Success! Found {target} after {jumps_made} jumps + {comparisons_in_block} linear checks = {jumps_made + comparisons_in_block} total",
            arr, [found_index], [
                {"name": "jumps", "value": str(jumps_made), "type": "int"},
                {"name": "linear_checks", "value": str(comparisons_in_block), "type": "int"}
            ]))
        frame_id += 1
        
        frames.append(create_frame(frame_id,
            f"📊 Indexed Sequential: O(√n) time - efficient when jump table can be cached!",
            arr, [], [{"name": "time_complexity", "value": "O(√n)", "type": "string"}]))
    else:
        frames.append(create_frame(frame_id,
            f"❌ {target} not found in array",
            arr, [], [{"name": "result", "value": "-1", "type": "int"}]))
    
    return frames
