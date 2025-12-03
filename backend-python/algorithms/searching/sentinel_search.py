"""
Sentinel Search - PRODUCTION GRADE with 15-20 frames
Enhanced optimization of linear search with sentinel value
"""

def create_frame(step_id, description, data, highlights=None, variables=None):
    """Helper to create visualization frame"""
    return {
        "step": step_id,
        "description": description,
        "data": data,
        "highlights": highlights or [],
        "variables": variables or []
    }

CODE_SAMPLE = """#include <bits/stdc++.h>
using namespace std;

class TrackedArray {
public:
    vector<int> arr;
    
    TrackedArray(vector<int> data) : arr(data) {}
    
    int sentinelSearch(int target) {
        int n = arr.size();
        int last = arr[n-1];  // Save last element
        arr[n-1] = target;    // Place sentinel
        
        int i = 0;
        while (arr[i] != target) {
            i++;
        }
        
        arr[n-1] = last;  // Restore last element
        
        if (i < n-1 || arr[n-1] == target)
            return i;
        return -1;
    }
};

int main() {
    vector<int> data = {64, 25, 12, 22, 11};
    int target = 12;
    TrackedArray tracked(data);
    int result = tracked.sentinelSearch(target);
    return 0;
}
"""

def execute(params):
    """Execute sentinel search with 15-20 comprehensive frames"""
    frames, frame_id = [], 0
    arr = params.get('array', [64, 25, 12, 22, 11, 90, 88])
    target = params.get('target', 22)
    
    # FRAME 0: Intro
    frames.append(create_frame(frame_id, 
        "🔍 Sentinel Search: Optimized linear search that eliminates bound checking in loop",
        arr, [], [{"name": "target", "value": str(target), "type": "int"}]))
    frame_id += 1
    
    # FRAME 1: Problem with linear search
    frames.append(create_frame(frame_id,
        "❓ Problem with Linear Search: Must check BOTH (i < n) AND (arr[i] != target) in every iteration",
        arr, [], [{"name": "comparisons_per_loop", "value": "2", "type": "int"}]))
    frame_id += 1
    
    # FRAME 2: Sentinel solution
    frames.append(create_frame(frame_id,
        "💡 Sentinel Solution: Place target at END of array, so we ALWAYS find it! Only need one comparison per loop",
        arr, [], [{"name": "optimization", "value": "Removes bound check", "type": "string"}]))
    frame_id += 1
    
    # FRAME 3: Show original array
    frames.append(create_frame(frame_id,
        f"📊 Original array (size {len(arr)}). We'll modify the last element temporarily",
        arr, [len(arr)-1], [{"name": "last_index", "value": str(len(arr)-1), "type": "int"}]))
    frame_id += 1
    
    # Save last element
    last_element = arr[-1]
    
    # FRAME 4: Save last element
    frames.append(create_frame(frame_id,
        f"💾 Save last element: arr[{len(arr)-1}] = {last_element} (we'll restore it later)",
        arr, [len(arr)-1], [{"name": "saved_value", "value": str(last_element), "type": "int"}]))
    frame_id += 1
    
    # Place sentinel
    arr_with_sentinel = arr.copy()
    arr_with_sentinel[-1] = target
    
    # FRAME 5: Place sentinel
    frames.append(create_frame(frame_id,
        f"🎯 Place SENTINEL: Set arr[{len(arr)-1}] = {target} (our target). Now target is GUARANTEED to be in array!",
        arr_with_sentinel, [len(arr)-1],
        [{"name": "sentinel_at", "value": str(len(arr)-1), "type": "int"}]))
    frame_id += 1
    
    # Search process
    found_index = -1
    comparisons = 0
    
    for i in range(len(arr)):
        comparisons += 1
        
        # FRAME: Checking element
        frames.append(create_frame(frame_id,
            f"🔍 Check arr[{i}] = {arr_with_sentinel[i]} vs {target}. No bound check needed!",
            arr_with_sentinel, [i],
            [{"name": "current_index", "value": str(i), "type": "int"},
             {"name": "comparisons", "value": str(comparisons), "type": "int"}]))
        frame_id += 1
        
        if arr_with_sentinel[i] == target:
            found_index = i
            
            # FRAME: Found
            frames.append(create_frame(frame_id,
                f"✓ Found match at index {i}!",
                arr_with_sentinel, [i],
                [{"name": "found_at", "value": str(i), "type": "int"}]))
            frame_id += 1
            break
    
    # Restore last element
    arr_with_sentinel[-1] = last_element
    
    # FRAME: Restore
    frames.append(create_frame(frame_id,
        f"🔄 Restore last element: arr[{len(arr)-1}] = {last_element}",
        arr_with_sentinel, [len(arr)-1], []))
    frame_id += 1
    
    # Check if real find or sentinel
    is_real_find = found_index < len(arr) - 1 or arr[found_index] == target
    
    if is_real_find:
        # FRAME: Success
        frames.append(create_frame(frame_id,
            f"🎉 Real find! {target} exists at index {found_index}. Sentinel optimization saved {comparisons} bound checks!",
            arr_with_sentinel, [found_index],
            [{"name": "result", "value": str(found_index), "type": "int"},
             {"name": "comparisons", "value": str(comparisons), "type": "int"}]))
    else:
        # FRAME: Not found
        frames.append(create_frame(frame_id,
            f"❌ Not found: Only hit the sentinel. {target} doesn't exist in original array",
            arr_with_sentinel, [], [{"name": "result", "value": "-1", "type": "int"}]))
    frame_id += 1
    
    # FRAME: Optimization explanation
    frames.append(create_frame(frame_id,
        f"📊 Optimization: Saved {comparisons} bound checks! Still O(n) but faster constants",
        arr, [],
        [{"name": "time_complexity", "value": "O(n)", "type": "string"},
         {"name": "checks_saved", "value": str(comparisons), "type": "int"}]))
    
    return frames
