"""Input-Restricted Deque - Production Grade"""

CODE_SAMPLE = """#include <iostream>
#include <deque>
using namespace std;

// Input-Restricted: INSERT only at REAR, DELETE from BOTH ends

int main() {
    deque<int> dq = {10, 20, 30};
    
    dq.push_back(40);   // Insert at rear only
    dq.pop_front();     // Delete from front
    dq.pop_back();      // Delete from rear
    
    return 0;
}
"""

def execute(params):
    frames = []
    original_deque = list(params.get('deque', [10, 20, 30, 40]))
    operation = params.get('operation', 'delete_front')  # 'insert_rear', 'delete_front', 'delete_rear'
    value = params.get('value', 50)
    
    # Frame 0: Intro
    frames.append({
        "description": "🔀 Input-Restricted Deque: INSERT at REAR only, DELETE from BOTH ends",
        "data": {"values": original_deque.copy(), "highlights": {}}
    })
    
    # Frame 1: Current
    frames.append({
        "description": f"📋 Current deque: FRONT ← {' | '.join(map(str, original_deque))} ← REAR",
        "data": {
            "values": original_deque.copy(),
            "highlights": {"indices": [0, len(original_deque)-1], "colors": ["#3498db", "#f39c12"],
                          "labels": ["FRONT", "REAR"]}
        }
    })
    
    if operation == 'insert_rear':
        frames.append({
            "description": f"🎯 Insert {value} at REAR (only insertion point)",
            "data": {"values": original_deque.copy(), "highlights": {}}
        })
        
        new_deque = original_deque + [value]
        frames.append({
            "description": f"✅ INSERTED! {value} added at REAR",
            "data": {
                "values": new_deque,
                "highlights": {"indices": [len(new_deque)-1], "colors": ["#2ecc71"], "labels": ["NEW"]}
            }
        })
    
    elif operation == 'delete_front':
        val = original_deque[0]
        frames.append({
            "description": f"🎯 Delete from FRONT: {val}",
            "data": {
                "values": original_deque.copy(),
                "highlights": {"indices": [0], "colors": ["#e74c3c"], "labels": ["DELETE"]}
            }
        })
        
        new_deque = original_deque[1:]
        frames.append({
            "description": f"✅ DELETED! {val} removed from FRONT",
            "data": {"values": new_deque, "highlights": {}}
        })
    
    elif operation == 'delete_rear':
        val = original_deque[-1]
        frames.append({
            "description": f"🎯 Delete from REAR: {val}",
            "data": {
                "values": original_deque.copy(),
                "highlights": {"indices": [len(original_deque)-1], "colors": ["#e74c3c"], "labels": ["DELETE"]}
            }
        })
        
        new_deque = original_deque[:-1]
        frames.append({
            "description": f"✅ DELETED! {val} removed from REAR",
            "data": {"values": new_deque, "highlights": {}}
        })
    
    frames.append({
        "description": "📊 Restriction: Can only INSERT at rear, but DELETE from both ends",
        "data": {"values": new_deque, "highlights": {}}
    })
    
    frames.append({
        "description": "⏱️ Time: O(1) for all operations | Space: O(1)",
        "data": {"values": new_deque, "highlights": {}}
    })
    
    return frames
