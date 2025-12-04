"""Queue Dequeue - Production Grade"""

CODE_SAMPLE = """#include <iostream>
#include <queue>
using namespace std;

int main() {
    queue<int> q;
    q.push(10);
    q.push(20);
    q.push(30);
    
    int front = q.front();
    q.pop();
    cout << "Dequeued: " << front << endl;
    return 0;
}
"""

def execute(params):
    frames = []
    original_queue = list(params.get('queue', [10, 20, 30, 40]))
    
    # Frame 0: Intro
    frames.append({
        "description": "📤 Queue Dequeue: Remove element from FRONT (FIFO)",
        "data": {"values": original_queue.copy(), "highlights": {}}
    })
    
    # Frame 1: Current queue
    frames.append({
        "description": f"📋 Current queue: FRONT ← {' | '.join(map(str, original_queue))} ← REAR",
        "data": {
            "values": original_queue.copy(),
            "highlights": {"indices": [0, len(original_queue)-1], "colors": ["#3498db", "#f39c12"], 
                          "labels": ["FRONT", "REAR"]}
        }
    })
    
    # Frame 2: Goal
    frames.append({
        "description": f"🎯 Goal: Dequeue element from FRONT ({original_queue[0]})",
        "data": {
            "values": original_queue.copy(),
            "highlights": {"indices": [0], "colors": ["#e74c3c"], "labels": ["REMOVE"]}
        }
    })
    
    # Frame 3: Check empty
    frames.append({
        "description": f"🔍 Check: Queue empty? NO (size = {len(original_queue)})",
        "data": {"values": original_queue.copy(), "highlights": {}}
    })
    
    # Frame 4: FIFO
    frames.append({
        "description": "📚 FIFO: Remove oldest element (front)",
        "data": {"values": original_queue.copy(), "highlights": {}}
    })
    
    # Frame 5: Front element
    front_value = original_queue[0]
    frames.append({
        "description": f"📍 Front element identified: {front_value}",
        "data": {
            "values": original_queue.copy(),
            "highlights": {"indices": [0], "colors": ["#e74c3c"], "labels": ["DELETE"]}
        }
    })
    
    # Frame 6: Save value
    frames.append({
        "description": f"💾 Save front value: {front_value}",
        "data": {
            "values": original_queue.copy(),
            "highlights": {"indices": [0], "colors": ["#f39c12"], "labels": ["SAVE"]}
        }
    })
    
    # Frame 7: WHY
    frames.append({
        "description": "💡 WHY dequeue from front: Maintain FIFO order",
        "data": {"values": original_queue.copy(), "highlights": {}}
    })
    
    # Frame 8: Adjust front
    frames.append({
        "description": "🔄 Move front pointer forward",
        "data": {
            "values": original_queue.copy(),
            "highlights": {"indices": [0], "colors": ["#e74c3c"], "labels": ["REMOVE"]}
        }
    })
    
    # Frame 9: DEQUEUE HAPPENS!
    new_queue = original_queue[1:]
    frames.append({
        "description": f"✅ DEQUEUE! Element {front_value} removed from FRONT",
        "data": {"values": new_queue, "highlights": {}}
    })
    
    # Frame 10: New front
    if new_queue:
        frames.append({
            "description": f"📍 New front element: {new_queue[0]}",
            "data": {
                "values": new_queue,
                "highlights": {"indices": [0], "colors": ["#2ecc71"], "labels": ["NEW FRONT"]}
            }
        })
    else:
        frames.append({
            "description": "Queue is now EMPTY",
            "data": {"values": [], "highlights": {}}
        })
    
    # Frame 11: Result
    frames.append({
        "description": f"📊 Updated queue: FRONT ← {' | '.join(map(str, new_queue)) if new_queue else 'EMPTY'} ← REAR",
        "data": {"values": new_queue, "highlights": {}}
    })
    
    # Frame 12: Dequeued value
    frames.append({
        "description": f"🔢 Dequeued value: {front_value}",
        "data": {"values": new_queue, "highlights": {}}
    })
    
    # Frame 13: Complexity
    frames.append({
        "description": "⏱️ Time: O(1) - constant time | Space: O(1)",
        "data": {"values": new_queue, "highlights": {}}
    })
    
    return frames
