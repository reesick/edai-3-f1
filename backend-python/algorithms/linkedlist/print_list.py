"""Print/Traverse Linked List - Production Grade with Progressive Building"""

CODE_SAMPLE = """#include <iostream>
using namespace std;

struct Node {
    int d; Node* next;
    Node(int v): d(v), next(NULL) {}
};

void print(Node* h){
    while(h){ cout << h->d << " "; h = h->next; }
}

int main(){
    Node* head = new Node(1);
    head->next = new Node(2);
    head->next->next = new Node(3);

    cout << "List: ";
    print(head);
}
"""

def execute(params):
    frames = []
    full_values = list(params.get('list', [10, 20, 30]))
    
    # Frame 0: Intro - show EMPTY initially
    frames.append({
        "description": "📋 Print List: Traverse and display all nodes",
        "data": {"values": [], "highlights": {}}
    })
    
    # Frame 1: Show full list
    frames.append({
        "description": f"🔗 Linked list exists: {' → '.join(map(str, full_values))} → NULL",
        "data": {"values": full_values, "highlights": {}}
    })
    
    # Frame 2: Goal
    frames.append({
        "description": "🎯 Goal: Visit each node sequentially and print its value",
        "data": {"values": full_values, "highlights": {}}
    })
    
    # Frame 3: Strategy
    frames.append({
        "description": "📚 Strategy: Start at HEAD, print current value, move to next until NULL",
        "data": {"values": full_values, "highlights": {}}
    })
    
    # Frame 4: Initialize - show only first node
    frames.append({
        "description": "🎬 Initialize: Set pointer to HEAD (first node)",
        "data": {
            "values": full_values[0:1],  # Only show first node
            "highlights": {"indices": [0], "colors": ["#3498db"], "labels": ["HEAD"]}
        }
    })
    
    # Traverse each node - progressively build visualization
    for i in range(len(full_values)):
        # Visit node - show up to current node
        visible_so_far = full_values[0:i+1]
        
        frames.append({
            "description": f"📍 Step {i+1}: At node {i} (value={full_values[i]})",
            "data": {
                "values": visible_so_far,
                "highlights": {"indices": [i], "colors": ["#f39c12"], "labels": ["CURRENT"]}
            }
        })
        
        # Print value
        frames.append({
            "description": f"🖨️ Print: {full_values[i]} (reading data field)",
            "data": {
                "values": visible_so_far,
                "highlights": {"indices": [i], "colors": ["#2ecc71"], "labels": ["PRINTING"]}
            }
        })
        
        # Move to next
        if i < len(full_values) - 1:
            frames.append({
                "description": f"➡️ Move: pointer = pointer->next (advance to next node)",
                "data": {
                    "values": visible_so_far,
                    "highlights": {"indices": [i], "colors": ["#95a5a6"], "labels": ["DONE"]}
                }
            })
        else:
            frames.append({
                "description": "🛑 Next: pointer->next = NULL (reached end)",
                "data": {
                    "values": visible_so_far,
                    "highlights": {"indices": [i], "colors": ["#95a5a6"], "labels": ["LAST"]}
                }
            })
    
    # Complete - show full list
    frames.append({
        "description": "✅ Traversal complete! All nodes visited",
        "data": {"values": full_values, "highlights": {}}
    })
    
    frames.append({
        "description": f"📊 Output printed: {' '.join(map(str, full_values))}",
        "data": {"values": full_values, "highlights": {}}
    })
    
    frames.append({
        "description": "⏱️ Time: O(n) - visit each node once | Space: O(1) - only pointer used",
        "data": {"values": full_values, "highlights": {}}
    })
    
    return frames
