"""Output-Restricted Deque - Production Grade"""

CODE_SAMPLE = """#include <iostream>
#include <deque>
using namespace std;

// Output-Restricted: INSERT at BOTH ends, DELETE only from FRONT

int main() {
    deque<int> dq = {10, 20, 30};
    
    dq.push_front(5);   // Insert at front
    dq.push_back(40);   // Insert at rear
    dq.pop_front();     // Delete from front only
    
    return 0;
}
"""

def execute(params):
    frames = []
    original_deque = list(params.get('deque', [10, 20, 30, 40]))
    operation = params.get('operation', 'insert_front')  # 'insert_front', 'insert_rear', 'delete_front'
    value = params.get('value', 5)
    
    # Frame 0: Intro
    frames.append({
        "description": "🔀 Output-Restricted Deque: INSERT at BOTH ends, DELETE from FRONT only",
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
    
    if operation == 'insert_front':
        frames.append({
            "description": f"🎯 Insert {value} at FRONT",
            "data": {"values": original_deque.copy(), "highlights": {}}
        })
        
        new_deque = [value] + original_deque
        frames.append({
            "description": f"✅ INSERTED! {value} added at FRONT",
            "data": {
                "values": new_deque,
                "highlights": {"indices": [0], "colors": ["#2ecc71"], "labels": ["NEW"]}
            }
        })
    
    elif operation == 'insert_rear':
        frames.append({
            "description": f"🎯 Insert {value} at REAR",
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
            "description": f"🎯 Delete from FRONT (only deletion point): {val}",
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
    
    frames.append({
        "description": "📊 Restriction: Can INSERT at both ends, but DELETE only from front",
        "data": {"values": new_deque, "highlights": {}}
    })
    
    frames.append({
        "description": "⏱️ Time: O(1) for all operations | Space: O(1)",
        "data": {"values": new_deque, "highlights": {}}
    })
    
    return frames
