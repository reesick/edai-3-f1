"""Insert at Position - Production Grade"""

CODE_SAMPLE = """#include <iostream>
using namespace std;

struct Node{
    int d; Node* next;
    Node(int v): d(v), next(NULL) {}
};

Node* insertPos(Node* h, int pos, int val){
    Node* n = new Node(val);
    if(pos == 0){
        n->next = h;
        return n;
    }
    Node* cur = h;
    for(int i=0;i<pos-1 && cur;i++)
        cur = cur->next;

    if(!cur) return h;
    n->next = cur->next;
    cur->next = n;
    return h;
}

void print(Node* h){
    while(h){ cout<<h->d<<" "; h=h->next; }
}

int main(){
    Node* h = new Node(1);
    h->next = new Node(2);
    h->next->next = new Node(4);

    h = insertPos(h, 2, 3);
    print(h);
}
"""

def execute(params):
    frames = []
    original_list = list(params.get('list', [1, 2, 4]))
    insert_pos = params.get('position', 2)
    insert_value = params.get('value', 3)
    
    # Frame 0: Intro - show ORIGINAL list only
    frames.append({
        "description": "📌 Insert at Position: Add node at specific index",
        "data": {"values": original_list.copy(), "highlights": {}}
    })
    
    # Frame 1: Current
    frames.append({
        "description": f"🔗 Current list: {' → '.join(map(str, original_list))} → NULL",
        "data": {"values": original_list.copy(), "highlights": {}}
    })
    
    # Frame 2: Goal
    frames.append({
        "description": f"🎯 Goal: Insert value {insert_value} at position {insert_pos}",
        "data": {"values": original_list.copy(), "highlights": {}}
    })
    
    # Frame 3: Strategy
    frames.append({
        "description": "📚 Strategy: (1) Create node (2) Traverse to pos-1 (3) Adjust pointers",
        "data": {"values": original_list.copy(), "highlights": {}}
    })
    
    # Frame 4: Create new node
    frames.append({
        "description": f"🆕 Step 1: Create new node with value {insert_value} (not linked yet)",
        "data": {"values": original_list.copy(), "highlights": {}}
    })
    
    # Frame 5-N: Traverse
    frames.append({
        "description": f"🚶 Step 2: Traverse to position {insert_pos-1} (node BEFORE insertion)",
        "data": {"values": original_list.copy(), "highlights": {}}
    })
    
    for i in range(min(insert_pos, len(original_list))):
        is_target = (i == insert_pos - 1)
        frames.append({
            "description": f"At position {i}: value={original_list[i]}{' (STOP - previous node!)' if is_target else ' (continue)'}",
            "data": {
                "values": original_list.copy(),
                "highlights": {"indices": [i], "colors": ["#3498db" if is_target else "#f39c12"],
                              "labels": ["PREV" if is_target else "CURRENT"]}
            }
        })
        if is_target:
            break
    
    # Show context
    if insert_pos < len(original_list):
        frames.append({
            "description": f"📍 Inserting between: {original_list[insert_pos-1]} and {original_list[insert_pos]}",
            "data": {
                "values": original_list.copy(),
                "highlights": {"indices": [insert_pos-1, insert_pos],
                              "colors": ["#3498db", "#f39c12"], "labels": ["PREV", "NEXT"]}
            }
        })
    else:
        frames.append({
            "description": f"📍 Inserting at end (after {original_list[insert_pos-1]})",
            "data": {
                "values": original_list.copy(),
                "highlights": {"indices": [insert_pos-1], "colors": ["#3498db"], "labels": ["PREV"]}
            }
        })
    
    # Pointer logic - STILL showing original
    frames.append({
        "description": f"🔗 Step 3a: new->next = curr->next (link to rest of list)",
        "data": {"values": original_list.copy(), "highlights": {}}
    })
    
    frames.append({
        "description": "💡 WHY: Must preserve connection before breaking chain",
        "data": {"values": original_list.copy(), "highlights": {}}
    })
    
    frames.append({
        "description": f"🔗 Step 3b: curr->next = new (insert into chain)",
        "data": {"values": original_list.copy(), "highlights": {}}
    })
    
    # NOW insert - this is where the new node appears!
    new_list = original_list[:insert_pos] + [insert_value] + original_list[insert_pos:]
    
    frames.append({
        "description": f"✅ Insertion complete! Value {insert_value} added",
        "data": {
            "values": new_list,
            "highlights": {"indices": [insert_pos], "colors": ["#2ecc71"], "labels": ["NEW"]}
        }
    })
    
    frames.append({
        "description": f"📊 Updated list: {' → '.join(map(str, new_list))} → NULL",
        "data": {"values": new_list, "highlights": {}}
    })
    
    frames.append({
        "description": "⏱️ Time: O(n) - traverse to position | Space: O(1) - one new node",
        "data": {"values": new_list, "highlights": {}}
    })
    
    return frames
