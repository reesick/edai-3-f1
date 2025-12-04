"""Circular Queue - Production Grade"""

CODE_SAMPLE = """#include <iostream>
using namespace std;

class CircularQueue {
    int *arr;
    int front, rear, size, capacity;
public:
    CircularQueue(int cap) {
        capacity = cap;
        arr = new int[capacity];
        front = rear = -1;
        size = 0;
    }
    
    void enqueue(int val) {
        if((rear + 1) % capacity == front) {
            cout << "Queue Full" << endl;
            return;
        }
        if(front == -1) front = 0;
        rear = (rear + 1) % capacity;
        arr[rear] = val;
        size++;
    }
    
    int dequeue() {
        if(front == -1) return -1;
        int val = arr[front];
        if(front == rear) front = rear = -1;
        else front = (front + 1) % capacity;
        size--;
        return val;
    }
};
"""

def execute(params):
    frames = []
    capacity = params.get('capacity', 5)
    initial_queue = params.get('queue', [10, 20, 30])
    operation = params.get('operation', 'enqueue')  # 'en queue' or 'dequeue'
    value = params.get('value', 40)
    
    #Create fixed-size array representation
    arr = [None] * capacity
    for i, val in enumerate(initial_queue):
        arr[i] = val
    
    front_idx = 0 if initial_queue else -1
    rear_idx = len(initial_queue) - 1 if initial_queue else -1
    
    # Frame 0: Intro
    frames.append({
        "description": f"🔄 Circular Queue (Capacity: {capacity}) - Wrap-around when full",
        "data": {"values": [str(v) if v is not None else '_' for v in arr], "highlights": {}}
    })
    
    # Frame 1: Show array with pointers
    highlights = {}
    if front_idx >= 0:
        highlights = {"indices": [front_idx, rear_idx], "colors": ["#3498db", "#f39c12"], 
                     "labels": ["FRONT", "REAR"]}
    
    frames.append({
        "description": f"📋 Array: Front={front_idx}, Rear={rear_idx}",
        "data": {"values": [str(v) if v is not None else '_' for v in arr], "highlights": highlights}
    })
    
    if operation == 'enqueue':
        # Enqueue operation
        frames.append({
            "description": f"🎯 Enqueue {value} to circular queue",
            "data": {"values": [str(v) if v is not None else '_' for v in arr], "highlights": highlights}
        })
        
        # Check full
        next_rear = (rear_idx + 1) % capacity
        if next_rear == front_idx:
            frames.append({
                "description": f"❌ Queue FULL! (rear+1) % {capacity} == front",
                "data": {"values": [str(v) if v is not None else '_' for v in arr], "highlights": highlights}
            })
        else:
            # Calculate new rear
            new_rear = (rear_idx + 1) % capacity
            frames.append({
                "description": f"📍 New rear = (rear + 1) % {capacity} = {new_rear}",
                "data": {"values": [str(v) if v is not None else '_' for v in arr], "highlights": highlights}
            })
            
            # Insert
            arr[new_rear] = value
            frames.append({
                "description": f"✅ ENQUEUE! arr[{new_rear}] = {value}",
                "data": {
                    "values": [str(v) if v is not None else '_' for v in arr],
                    "highlights": {"indices": [front_idx, new_rear], "colors": ["#3498db", "#2ecc71"],
                                  "labels": ["FRONT", "NEW REAR"]}
                }
            })
            
            if new_rear < rear_idx:
                frames.append({
                    "description": f"🔄 WRAP-AROUND! Rear wrapped from {rear_idx} to {new_rear}",
                    "data": {"values": [str(v) if v is not None else '_' for v in arr], "highlights": {}}
                })
    
    frames.append({
        "description": "⏱️ Time: O(1) | Space: O(n) for fixed array",
        "data": {"values": [str(v) if v is not None else '_' for v in arr], "highlights": {}}
    })
    
    return frames
