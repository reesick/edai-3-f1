"""Queue Enqueue - Production Grade"""

CODE_SAMPLE = """#include <iostream>
#include <queue>
using namespace std;

int main() {
    queue<int> q;
    q.push(10);
    q.push(20);
    q.push(30);
    
    cout << "Front: " << q.front() << endl;
    return 0;
}
"""

def execute(params):
    frames = []
    original_queue = list(params.get('queue', [10, 20, 30]))
    enqueue_value = params.get('value', 40)
    
    # Frame 0: Intro
    frames.append({
        "description": "📥 Queue Enqueue: Add element at REAR (FIFO)",
        "data": {"values": original_queue.copy(), "highlights": {}}
    })
    
    # Frame 1: Current queue
    frames.append({
        "description": f"📋 Current queue: FRONT ← {' | '.join(map(str, original_queue))} ← REAR",
        "data": {
            "values": original_queue.copy(),
            "highlights": {"indices": [0], "colors": ["#3498db"], "labels": ["FRONT"]}
        }
    })
    
    # Frame 2: Goal
    frames.append({
        "description": f"🎯 Goal: Enqueue {enqueue_value} at REAR",
        "data": {"values": original_queue.copy(), "highlights": {}}
    })
    
    # Frame 3: FIFO explanation
    frames.append({
        "description": "📚 FIFO: First In, First Out - Add at REAR, Remove from FRONT",
        "data": {"values": original_queue.copy(), "highlights": {}}
    })
    
    # Frame 4: Check capacity (assume unlimited for simple queue)
    frames.append({
        "description": "🔍 Check: Queue full? NO (unlimited capacity)",
        "data": {"values": original_queue.copy(), "highlights": {}}
    })
    
    # Frame 5: Rear position
    frames.append({
        "description": f"📍 REAR position: After {original_queue[-1]} (rightmost)",
        "data": {
            "values": original_queue.copy(),
            "highlights": {"indices": [len(original_queue)-1], "colors": ["#f39c12"], "labels": ["REAR"]}
        }
    })
    
    # Frame 6: Create element
    frames.append({
        "description": f"🆕 Create element with value {enqueue_value}",
        "data": {"values": original_queue.copy(), "highlights": {}}
    })
    
    # Frame 7: WHY
    frames.append({
        "description": "💡 WHY enqueue at rear: Maintain FIFO order",
        "data": {"values": original_queue.copy(), "highlights": {}}
    })
    
    # Frame 8: ENQUEUE HAPPENS!
    new_queue = original_queue + [enqueue_value]
    frames.append({
        "description": f"✅ ENQUEUE! Element {enqueue_value} added at REAR",
        "data": {
            "values": new_queue,
            "highlights": {"indices": [len(new_queue)-1], "colors": ["#2ecc71"], "labels": ["NEW"]}
        }
    })
    
    # Frame 9: New queue
    frames.append({
        "description": f"📊 Updated queue: FRONT ← {' | '.join(map(str, new_queue))} ← REAR",
        "data": {"values": new_queue, "highlights": {}}
    })
    
    #Frame 10: Size
    frames.append({
        "description": f"📏 Queue size: {len(original_queue)} → {len(new_queue)} (increased by 1)",
        "data": {"values": new_queue, "highlights": {}}
    })
    
    # Frame 11: Complexity
    frames.append({
        "description": "⏱️ Time: O(1) - constant time | Space: O(1)",
        "data": {"values": new_queue, "highlights": {}}
    })
    
    return frames
