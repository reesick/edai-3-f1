"""Priority Queue - Production Grade"""

CODE_SAMPLE = """#include <iostream>
#include <queue>
using namespace std;

int main() {
    priority_queue<int> pq;  // Max heap
    
    pq.push(30);
    pq.push(10);
    pq.push(40);
    pq.push(20);
    
    cout << "Highest: " << pq.top() << endl;  // 40
    pq.pop();  // Removes 40
    
    return 0;
}
"""

def execute(params):
    frames = []
    # Elements as (value, priority) pairs
    queue_items = params.get('queue', [(30, 2), (10, 1), (40, 3), (20, 2)])
    
    # Frame 0: Intro
    frames.append({
        "description": "⭐ Priority Queue: Dequeue based on PRIORITY (not FIFO)",
        "data": {"values": [f"{v}(P{p})" for v, p in queue_items], "highlights": {}}
    })
    
    # Frame 1: Current queue
    frames.append({
        "description": "📋 Elements: (value, priority)",
        "data": {"values": [f"{v}(P{p})" for v, p in queue_items], "highlights": {}}
    })
    
    # Frame 2: Goal
    frames.append({
        "description": "🎯 Dequeue: Remove element with HIGHEST priority",
        "data": {"values": [f"{v}(P{p})" for v, p in queue_items], "highlights": {}}
    })
    
    # Frame 3: Scan for max priority
    frames.append({
        "description": "🔍 Scanning for highest priority...",
        "data": {"values": [f"{v}(P{p})" for v, p in queue_items], "highlights": {}}
    })
    
    # Find max priority
    max_priority = max(queue_items, key=lambda x: x[1])
    max_idx = queue_items.index(max_priority)
    
    # Frame 4: Found max
    frames.append({
        "description": f"✓ Found: {max_priority[0]} has highest priority {max_priority[1]}",
        "data": {
            "values": [f"{v}(P{p})" for v, p in queue_items],
            "highlights": {"indices": [max_idx], "colors": ["#2ecc71"], "labels": ["MAX"]}
        }
    })
    
    # Frame 5: Remove
    new_queue = queue_items[:max_idx] + queue_items[max_idx+1:]
    frames.append({
        "description": f"⬆️ DEQUEUE! Removed {max_priority[0]} (priority {max_priority[1]})",
        "data": {"values": [f"{v}(P{p})" for v, p in new_queue], "highlights": {}}
    })
    
    # Frame 6: Result
    frames.append({
        "description": f"📊 Updated queue: {len(new_queue)} elements",
        "data": {"values": [f"{v}(P{p})" for v, p in new_queue], "highlights": {}}
    })
    
    frames.append({
        "description": "⏱️ Time: O(n) scan + O(1) remove | Space: O(n)",
        "data": {"values": [f"{v}(P{p})" for v, p in new_queue], "highlights": {}}
    })
    
    return frames
