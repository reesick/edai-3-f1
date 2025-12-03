"""
Binary Search - PRODUCTION GRADE with 18-20 frames
Divide and conquer on sorted arrays with visual range elimination
"""

def create_frame(step_id, description, values, highlights=None, variables=None, 
                 search_range=None, eliminated_ranges=None, target=None, comparison_idx=None):
    """Helper to create enhanced visualization frame"""
    data = {
        "step": step_id,
        "description": description,
        "values": values,
        "name": "Sorted Array",
        "targetValue": target,
        "searchRange": search_range,  # {start, end}
        "eliminatedRanges": eliminated_ranges or [],  # [{start, end}]
        "comparisonIndex": comparison_idx
    }
    
    if highlights:
        data["highlights"] = highlights
    if variables:
        data["variables"] = variables
        
    return {"data": data, "highlights": highlights or {}}

CODE_SAMPLE = """#include <bits/stdc++.h>
using namespace std;

int binarySearch(vector<int>& arr, int target) {
    int left = 0, right = arr.size() - 1;
    
    while (left <= right) {
        int mid = left + (right - left) / 2;
        
        if (arr[mid] == target)
            return mid;  // Found
        else if (arr[mid] < target)
            left = mid + 1;  // Search right half
        else
            right = mid - 1;  // Search left half
    }
    return -1;  // Not found
}

int main() {
    vector<int> arr = {10, 20, 30, 40, 50, 60, 70, 80, 90, 100};
    int target = 70;
    int result = binarySearch(arr, target);
    return 0;
}
"""

def execute(params):
    """Execute binary search with 18-20 comprehensive frames"""
    frames, frame_id = [], 0
    arr = params.get('array', [10, 20, 30, 40, 50, 60, 70, 80, 90, 100])
    target = params.get('target', 70)
    
    # FRAME 0: Intro
    frames.append(create_frame(frame_id,
        "🔍 Binary Search: Divide and Conquer on SORTED arrays - O(log n) efficiency!",
        arr, None, [{"name": "target", "value": str(target), "type": "int"}], 
        None, None, target, None))
    frame_id += 1
    
    # FRAME 1: Strategy
    frames.append(create_frame(frame_id,
        "🧭 Strategy: Compare with MIDDLE element, eliminate half of search space each time",
        arr, None, [{"name": "requirement", "value": "Array MUST be sorted", "type": "string"}],
        None, None, target, None))
    frame_id += 1
    
    # Search
    left, right = 0, len(arr) - 1
    comparisons = 0
    eliminated = []
    
    while left <= right:
        # FRAME: Show current search range
        frames.append(create_frame(frame_id,
            f"📍 Current search space: indices [{left}..{right}] = {len([i for i in range(left, right+1)])} elements",
            arr, None,
            [{"name": "left", "value": str(left), "type": "int"},
             {"name": "right", "value": str(right), "type": "int"}],
            {"start": left, "end": right}, eliminated, target, None))
        frame_id += 1
        
        mid = left + (right - left) // 2
        comparisons += 1
        
        # FRAME: Calculate mid
        frames.append(create_frame(frame_id,
            f"📐 Calculate middle: mid = ({left} + {right}) / 2 = {mid}",
            arr, 
            {"indices": [mid], "colors": ["#f39c12"], "labels": ["MID"]},
            [{"name": "mid", "value": str(mid), "type": "int"}],
            {"start": left, "end": right}, eliminated, target, mid))
        frame_id += 1
        
        # FRAME: Comparison
        frames.append(create_frame(frame_id,
            f"🔍 Compare: arr[{mid}] = {arr[mid]} vs target = {target}",
            arr,
            {"indices": [mid], "colors": ["#f39c12"], "labels": ["CHECKING"]},
            [{"name": "arr[mid]", "value": str(arr[mid]), "type": "int"},
             {"name": "target", "value": str(target), "type": "int"},
             {"name": "comparisons", "value": str(comparisons), "type": "int"}],
            {"start": left, "end": right}, eliminated, target, mid))
        frame_id += 1
        
        if arr[mid] == target:
            # FOUND!
            frames.append(create_frame(frame_id,
                f"✅ MATCH! arr[{mid}] = {arr[mid]} equals {target}. Target found!",
                arr,
                {"indices": [mid], "colors": ["#2ecc71"], "labels": ["FOUND!"]},
                [{"name": "found_at", "value": str(mid), "type": "int"}],
                {"start": mid, "end": mid}, eliminated, target, mid))
            frame_id += 1
            
            frames.append(create_frame(frame_id,
                f"🎉 Binary Search Complete! Found {target} at index {mid} after only {comparisons} comparisons",
                arr,
                {"indices": [mid], "colors": ["#2ecc71"], "labels": ["✓"]},
                [{"name": "result", "value": str(mid), "type": "int"},
                 {"name": "efficiency", "value": f"{comparisons} vs {len(arr)} linear", "type": "string"}],
                None, eliminated, target, None))
            frame_id += 1
            
            frames.append(create_frame(frame_id,
                f"📊 Performance: log₂({len(arr)}) ≈ {comparisons} comparisons. Time: O(log n), Space: O(1)",
                arr, None,
                [{"name": "time_complexity", "value": "O(log n)", "type": "string"},
                 {"name": "comparisons", "value": str(comparisons), "type": "int"}],
                None, None, target, None))
            return frames
            
        elif arr[mid] < target:
            # Go right
            frames.append(create_frame(frame_id,
                f"➡️ {arr[mid]} < {target}: Target is in RIGHT half. Eliminate left [{left}..{mid}]",
                arr,
                {"indices": list(range(left, mid+1)), "colors": ["#95a5a6"]*(mid-left+1), "labels": ["ELIMINATED"]*(mid-left+1)},
                [{"name": "decision", "value": "GO RIGHT", "type": "string"}],
                {"start": mid+1, "end": right}, eliminated + [{"start": left, "end": mid}], target, None))
            frame_id += 1
            
            eliminated.append({"start": left, "end": mid})
            left = mid + 1
            
        else:
            # Go left
            frames.append(create_frame(frame_id,
                f"⬅️ {arr[mid]} > {target}: Target is in LEFT half. Eliminate right [{mid}..{right}]",
                arr,
                {"indices": list(range(mid, right+1)), "colors": ["#95a5a6"]*(right-mid+1), "labels": ["ELIMINATED"]*(right-mid+1)},
                [{"name": "decision", "value": "GO LEFT", "type": "string"}],
                {"start": left, "end": mid-1}, eliminated + [{"start": mid, "end": right}], target, None))
            frame_id += 1
            
            eliminated.append({"start": mid, "end": right})
            right = mid - 1
    
    # NOT FOUND
    frames.append(create_frame(frame_id,
        f"❌ Search space exhausted. {target} NOT in array after {comparisons} comparisons",
        arr, None,
        [{"name": "result", "value": "-1", "type": "int"},
         {"name": "comparisons", "value": str(comparisons), "type": "int"}],
        None, eliminated, target, None))
    
    return frames
