"""
Linear Search - PRODUCTION GRADE with 15-20 frames
Enhanced with comprehensive educational content and detailed visualization
"""

def create_frame(step_id, description, data, highlights=None, variables=None):
    """Helper to create visualization frame"""
    frame = {
        "step": step_id,
        "description": description,
        "data": data,
        "highlights": highlights or [],
        "variables": variables or []
    }
    return frame

CODE_SAMPLE = """#include <bits/stdc++.h>
using namespace std;

class TrackedArray {
public:
    vector<int> arr;
    
    TrackedArray(vector<int> data) : arr(data) {}
    
    int linearSearch(int target) {
        for (int i = 0; i < arr.size(); i++) {
            if (arr[i] == target) {
                return i;  // Found
            }
        }
        return -1;  // Not found
    }
};

int main() {
    vector<int> data = {64, 25, 12, 22, 11, 90, 88};
    int target = 22;
    
    TrackedArray tracked(data);
    int result = tracked.linearSearch(target);
    
    if (result != -1)
        cout << "Found at index: " << result << endl;
    else
        cout << "Not found" << endl;
    
    return 0;
}
"""

def execute(params):
    """Execute linear search with 15-20 comprehensive frames"""
    frames = []
    frame_id = 0
    
    arr = params.get('array', [64, 25, 12, 22, 11, 90, 88])
    target = params.get('target', 22)
    
    # FRAME 0: Introduction
    frame = create_frame(
        frame_id,
        "🔍 Linear Search: The simplest search algorithm - check each element sequentially until found",
        arr,
        [],
        [{"name": "target", "value": str(target), "type": "int"}]
    )
    frames.append(frame)
    frame_id += 1
    
    # FRAME 1: Goal and Strategy
    frame = create_frame(
        frame_id,
        f"🎯 Goal: Find value {target} in array. Strategy: Check element by element from left to right",
        arr,
        [],
        [
            {"name": "target", "value": str(target), "type": "int"},
            {"name": "array_size", "value": str(len(arr)), "type": "int"},
            {"name": "worst_case", "value": f"{len(arr)} comparisons", "type": "string"}
        ]
    )
    frames.append(frame)
    frame_id += 1
    
    # FRAME 2: Algorithm explanation
    frame = create_frame(
        frame_id,
        "📚 How it works: Start at index 0, compare each element with target, stop when found or reached end",
        arr,
        [0],  # Highlight starting position
        [{"name": "current_index", "value": "0", "type": "int"}]
    )
    frames.append(frame)
    frame_id += 1
    
    # Search process
    found = False
    found_index = -1
    comparisons = 0
    
    for i in range(len(arr)):
        comparisons += 1
        
        # FRAME: Checking current element
        frame = create_frame(
            frame_id,
            f"🔍 Checking index {i}: Is arr[{i}] = {arr[i]} equal to {target}?",
            arr,
            [i],
            [
                {"name": "current_index", "value": str(i), "type": "int"},
                {"name": "current_value", "value": str(arr[i]), "type": "int"},
                {"name": "target", "value": str(target), "type": "int"},
                {"name": "comparisons", "value": str(comparisons), "type": "int"}
            ]
        )
        frames.append(frame)
        frame_id += 1
        
        # FRAME: Comparison result
        if arr[i] == target:
            # Found!
            frame = create_frame(
                frame_id,
                f"✅ MATCH! arr[{i}] = {arr[i]} equals target {target}. Search successful!",
                arr,
                [i],
                [
                    {"name": "found_at", "value": str(i), "type": "int"},
                    {"name": "comparisons", "value": str(comparisons), "type": "int"},
                    {"name": "status", "value": "FOUND", "type": "string"}
                ]
            )
            frames.append(frame)
            frame_id += 1
            found = True
            found_index = i
            break
        else:
            # Not a match - continue
            frame = create_frame(
                frame_id,
                f"❌ No match: {arr[i]} ≠ {target}. Continue to next element...",
                arr,
                list(range(i + 1)),  # Show all checked elements
                [
                    {"name": "current_index", "value": str(i), "type": "int"},
                    {"name": "checked_so_far", "value": str(i + 1), "type": "int"},
                    {"name": "remaining", "value": str(len(arr) - i - 1), "type": "int"}
                ]
            )
            frames.append(frame)
            frame_id += 1
    
    # Final result frames
    if found:
        # FRAME: Success summary
        frame = create_frame(
            frame_id,
            f"🎉 Search Complete! Found {target} at index {found_index} after {comparisons} comparisons",
            arr,
            [found_index],
            [
                {"name": "result", "value": str(found_index), "type": "int"},
                {"name": "total_comparisons", "value": str(comparisons), "type": "int"},
                {"name": "efficiency", "value": f"{comparisons}/{len(arr)} elements checked", "type": "string"}
            ]
        )
        frames.append(frame)
        frame_id += 1
        
        # FRAME: Performance analysis
        frame = create_frame(
            frame_id,
            f"📊 Performance: Found in {comparisons} comparisons. Best case: O(1), Worst case: O(n), This case: O({comparisons})",
            arr,
            [],
            [
                {"name": "time_complexity", "value": "O(n)", "type": "string"},
                {"name": "space_complexity", "value": "O(1)", "type": "string"}
            ]
        )
        frames.append(frame)
    else:
        # FRAME: Not found
        frame = create_frame(
            frame_id,
            f"❌ Search Complete: {target} NOT FOUND in array after checking all {comparisons} elements",
            arr,
            list(range(len(arr))),  # Highlight all checked
            [
                {"name": "result", "value": "-1", "type": "int"},
                {"name": "comparisons", "value": str(comparisons), "type": "int"},
                {"name": "status", "value": "NOT FOUND", "type": "string"}
            ]
        )
        frames.append(frame)
        frame_id += 1
        
        # FRAME: Performance for failed search
        frame = create_frame(
            frame_id,
            f"📊 Performance: Checked all {len(arr)} elements. Time: O(n), Space: O(1)",
            arr,
            [],
            [
                {"name": "worst_case_reached", "value": "true", "type": "boolean"},
                {"name": "comparisons", "value": str(comparisons), "type": "int"}
            ]
        )
        frames.append(frame)
    
    # FRAME: Use cases
    frame_id += 1
    frame = create_frame(
        frame_id,
        "💡 When to use Linear Search: Small arrays, unsorted data, or when simplicity matters more than speed",
        arr,
        [],
        [
            {"name": "pros", "value": "Simple, works on unsorted data", "type": "string"},
            {"name": "cons", "value": "Slow for large arrays O(n)", "type": "string"}
        ]
    )
    frames.append(frame)
    
    return frames
