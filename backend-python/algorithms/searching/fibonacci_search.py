"""
Fibonacci Search - PRODUCTION GRADE with 18-20 frames
Uses Fibonacci numbers to divide search space efficiently
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

int fibonacciSearch(vector<int>& arr, int target) {
    int n = arr.size();
    int fib2 = 0, fib1 = 1, fib = fib1 + fib2;
    
    while (fib < n) {
        fib2 = fib1;
        fib1 = fib;
        fib = fib1 + fib2;
    }
    
    int offset = -1;
    while (fib > 1) {
        int i = min(offset + fib2, n-1);
        
        if (arr[i] < target) {
            fib = fib1;
            fib1 = fib2;
            fib2 = fib - fib1;
            offset = i;
        } else if (arr[i] > target) {
            fib = fib2;
            fib1 = fib1 - fib2;
            fib2 = fib - fib1;
        } else {
            return i;
        }
    }
    
    if (fib1 && offset+1 < n && arr[offset+1] == target)
        return offset+1;
    return -1;
}

int main() {
    vector<int> arr = {10, 22, 35, 40, 45, 50, 80, 82, 85, 90, 100};
    int target = 85;
    int result = fibonacciSearch(arr, target);
    return 0;
}
"""

def execute(params):
    frames, frame_id = [], 0
    arr = params.get('array', [10, 22, 35, 40, 45, 50, 80, 82, 85, 90, 100])
    target = params.get('target', 85)
    
    # FRAME 0: Intro
    frames.append(create_frame(frame_id,
        "🔢 Fibonacci Search: Uses Fibonacci numbers to divide sorted array efficiently (like Binary but with Fibonacci intervals)",
        arr, [], [{"name": "target", "value": str(target), "type": "int"}]))
    frame_id += 1
    
    # FRAME 1: Fibonacci sequence
    frames.append(create_frame(frame_id,
        "📚 Fibonacci Sequence: 0, 1, 1, 2, 3, 5, 8, 13, 21... Each number = sum of previous two",
        arr, [], [{"name": "formula", "value": "F(n) = F(n-1) + F(n-2)", "type": "string"}]))
    frame_id += 1
    
    # Find smallest Fibonacci >= n
    n = len(arr)
    fib2, fib1 = 0, 1
    fib = fib1 + fib2
    
    fib_sequence = [fib2, fib1]
    while fib < n:
        fib2 = fib1
        fib1 = fib
        fib = fib1 + fib2
        fib_sequence.append(fib)
    
    # FRAME 2: Find Fibonacci number
    frames.append(create_frame(frame_id,
        f"🔍 Find smallest Fibonacci ≥ array size ({n}). Sequence: {fib_sequence}. Using fib={fib}",
        arr, [], [
            {"name": "array_size", "value": str(n), "type": "int"},
            {"name": "fib_m", "value": str(fib), "type": "int"},
            {"name": "fib_m1", "value": str(fib1), "type": "int"},
            {"name": "fib_m2", "value": str(fib2), "type": "int"}
        ]))
    frame_id += 1
    
    # Search
    offset = -1
    comparisons = 0
    
    while fib > 1:
        comparisons += 1
        i = min(offset + fib2, n-1)
        
        # FRAME: Calculate index
        frames.append(create_frame(frame_id,
            f"📍 Calculate index: i = min(offset({offset}) + fib_m2({fib2}), {n-1}) = {i}",
            arr, [i], [
                {"name": "checking_index", "value": str(i), "type": "int"},
                {"name": "offset", "value": str(offset), "type": "int"}
            ]))
        frame_id += 1
        
        # FRAME: Comparison
        frames.append(create_frame(frame_id,
            f"🔍 Compare: arr[{i}] = {arr[i]} vs target = {target}",
            arr, [i], [
                {"name": "current_value", "value": str(arr[i]), "type": "int"},
                {"name": "target", "value": str(target), "type": "int"},
                {"name": "comparisons", "value": str(comparisons), "type": "int"}
            ]))
        frame_id += 1
        
        if arr[i] < target:
            # Move offset forward
            frames.append(create_frame(frame_id,
                f"➡️ {arr[i]} < {target}: Search RIGHT. Shift Fibonacci numbers down: fib={fib1}, fib1={fib2}",
                arr, list(range(i+1, n)), [
                    {"name": "direction", "value": "RIGHT", "type": "string"},
                    {"name": "new_offset", "value": str(i), "type": "int"}
                ]))
            frame_id += 1
            
            fib = fib1
            fib1 = fib2
            fib2 = fib - fib1
            offset = i
            
        elif arr[i] > target:
            # Stay in left part
            frames.append(create_frame(frame_id,
                f"⬅️ {arr[i]} > {target}: Search LEFT. Use smaller Fibonacci: fib={fib2}",
                arr, list(range(offset+1, i)), [
                    {"name": "direction", "value": "LEFT", "type": "string"}
                ]))
            frame_id += 1
            
            fib = fib2
            fib1 = fib1 - fib2
            fib2 = fib - fib1
            
        else:
            # Found!
            frames.append(create_frame(frame_id,
                f"✅ MATCH! arr[{i}] = {arr[i]} equals {target}",
                arr, [i], [
                    {"name": "found_at", "value": str(i), "type": "int"},
                    {"name": "comparisons", "value": str(comparisons), "type": "int"}
                ]))
            frame_id += 1
            
            frames.append(create_frame(frame_id,
                f"🎉 Search complete! Found {target} at index {i} after {comparisons} Fibonacci divisions",
                arr, [i], [{"name": "result", "value": str(i), "type": "int"}]))
            frame_id += 1
            
            frames.append(create_frame(frame_id,
                f"📊 Performance: O(log n) time like Binary, but uses Fibonacci divisions. Good for slow comparisons!",
                arr, [], [{"name": "time_complexity", "value": "O(log n)", "type": "string"}]))
            
            return frames
    
    # Check last element manually
    if fib1 and offset+1 < n and arr[offset+1] == target:
        frames.append(create_frame(frame_id,
            f"✅ Found {target} at final position {offset+1}!",
            arr, [offset+1], [{"name": "result", "value": str(offset+1), "type": "int"}]))
    else:
        frames.append(create_frame(frame_id,
            f"❌ {target} not found after {comparisons} comparisons",
            arr, [], [{"name": "result", "value": "-1", "type": "int"}]))
    
    return frames
