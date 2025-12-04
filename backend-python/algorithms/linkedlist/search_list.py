"""Search by Value (Find Index) - Production Grade"""

CODE_SAMPLE = """#include <iostream>
using namespace std;

struct Node {
    int d; Node* next;
    Node(int v): d(v), next(NULL) {}
};

int search(Node* h, int key){
    int idx = 0;
    while(h){
        if(h->d == key) return idx;
        h = h->next;
        idx++;
    }
    return -1;
}

int main(){
    Node* h = new Node(10);
    h->next = new Node(20);
    h->next->next = new Node(30);

    cout << "Index: " << search(h, 20);
}
"""

def execute(params):
    frames = []
    values = list(params.get('list', [10, 20, 30]))
    search_value = params.get('value', 20)
    
    # Frame 0: Intro
    frames.append({
        "description": "🔍 Search in List: Find index of target value",
        "data": {"values": values, "highlights": {}}
    })
    
    # Frame 1: Current list
    frames.append({
        "description": f"🔗 Current list: {' → '.join(map(str, values))} → NULL",
        "data": {"values": values, "highlights": {}}
    })
    
    # Frame 2: Goal
    frames.append({
        "description": f"🎯 Goal: Find the index (position) of value {search_value}",
        "data": {
            "values": values,
            "highlights": {"indices": [values.index(search_value) if search_value in values else 0],
                          "colors": ["#3498db"], "labels": ["TARGET?"]}
        }
    })
    
    # Frame 3: Strategy
    frames.append({
        "description": "📚 Strategy: Traverse with counter, compare each node's data with key",
        "data": {"values": values, "highlights": {}}
    })
    
    # Frame 4: Initialize
    frames.append({
        "description": "🎬 Initialize: idx = 0, pointer = head",
        "data": {
            "values": values,
            "highlights": {"indices": [0], "colors": ["#f39c12"], "labels": ["START"]}
        }
    })
    
    # Search process
    found_idx = -1
    for i in range(len(values)):
        # At node
        frames.append({
            "description": f"📍 At index {i}: Checking node (value = {values[i]})",
            "data": {
                "values": values,
                "highlights": {"indices": [i], "colors": ["#f39c12"], "labels": [f"idx={i}"]}
            }
        })
        
        # Compare
        is_match = values[i] == search_value
        if is_match:
            frames.append({
                "description": f"🎯 Compare: {values[i]} == {search_value}? YES! ✅",
                "data": {
                    "values": values,
                    "highlights": {"indices": [i], "colors": ["#2ecc71"], "labels": ["FOUND!"]}
                }
            })
            
            frames.append({
                "description": f"✅ Match found at index {i}! Return immediately",
                "data": {
                    "values": values,
                    "highlights": {"indices": [i], "colors": ["#2ecc71"], "labels": ["MATCH"]}
                }
            })
            
            frames.append({
                "description": f"💡 WHY return early: No need to check remaining nodes",
                "data": {"values": values, "highlights": {}}
            })
            
            found_idx = i
            break
        else:
            frames.append({
                "description": f"❌ Compare: {values[i]} == {search_value}? NO",
                "data": {
                    "values": values,
                    "highlights": {"indices": [i], "colors": ["#e74c3c"], "labels": ["NO MATCH"]}
                }
            })
            
            if i < len(values) - 1:
                frames.append({
                    "description": f"➡️ Move forward: idx = {i+1}, pointer = pointer->next",
                    "data": {
                        "values": values,
                        "highlights": {"indices": [i+1], "colors": ["#f39c12"], "labels": ["NEXT"]}
                    }
                })
    
    # Result
    if found_idx >= 0:
        frames.append({
            "description": f"📊 Result: Value {search_value} found at index {found_idx}",
            "data": {
                "values": values,
                "highlights": {"indices": [found_idx], "colors": ["#2ecc71"], "labels": ["RESULT"]}
            }
        })
    else:
        frames.append({
            "description": "🛑 Reached end: pointer = NULL",
            "data": {"values": values, "highlights": {}}
        })
        
        frames.append({
            "description": f"❌ Result: Value {search_value} not found in list (return -1)",
            "data": {"values": values, "highlights": {}}
        })
    
    frames.append({
        "description": "⏱️ Time: O(n) - worst case visit all nodes | Space: O(1) - only counter",
        "data": {"values": values, "highlights": {}}
    })
    
    return frames
