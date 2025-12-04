"""Delete at Position - Production Grade"""

CODE_SAMPLE = """#include <iostream>
using namespace std;

struct Node{
    int d; Node* next;
    Node(int v): d(v), next(NULL) {}
};

Node* delPos(Node* h, int pos){
    if(!h) return h;
    if(pos == 0){
        Node* t = h->next;
        delete h;
        return t;
    }
    Node* cur = h;
    for(int i=0;i<pos-1 && cur;i++)
        cur = cur->next;

    if(!cur || !cur->next) return h;
    Node* t = cur->next;
    cur->next = t->next;
    delete t;
    return h;
}

void print(Node* h){
    while(h){ cout<<h->d<<" "; h=h->next; }
}

int main(){
    Node* h=new Node(10);
    h->next=new Node(20);
    h->next->next=new Node(30);

    h = delPos(h,1);
    print(h);
}
"""

def execute(params):
    frames = []
    original_values = list(params.get('list', [10, 20, 30]))
    delete_pos = params.get('position', 1)
    
    # Work with copy, don't modify yet
    values = list(original_values)
    
    # Frame 0: Intro
    frames.append({
        "description": "🗑️ Delete at Position: Remove node at specific index",
        "data": {"values": values, "highlights": {}}
    })
    
    # Frame 1: Current
    frames.append({
        "description": f"🔗 Current list: {' → '.join(map(str, values))} → NULL",
        "data": {"values": values, "highlights": {}}
    })
    
    # Frame 2: Goal
    if delete_pos < len(values):
        frames.append({
            "description": f"🎯 Goal: Delete node at position {delete_pos} (value = {values[delete_pos]})",
            "data": {
                "values": values,
                "highlights": {"indices": [delete_pos], "colors": ["#e74c3c"], "labels": ["TARGET"]}
            }
        })
    else:
        frames.append({
            "description": f"⚠️ Position {delete_pos} out of bounds (list size = {len(values)})",
            "data": {"values": values, "highlights": {}}
        })
        return frames
    
    # Frame 3: Strategy
    frames.append({
        "description": "📚 Strategy: (1) Find node before target (2) Bypass target (3) Delete",
        "data": {"values": values, "highlights": {}}
    })
    
    # Edge case
    if delete_pos == 0:
        frames.append({
            "description": "⚠️ Special case: pos == 0 (delete HEAD)",
            "data": {
                "values": values,
                "highlights": {"indices": [0], "colors": ["#e74c3c"], "labels": ["HEAD"]}
            }
        })
        
        frames.append({
            "description": "💾 Save: temp = head (store reference for deletion)",
            "data": {
                "values": values,
                "highlights": {"indices": [0], "colors": ["#e74c3c"], "labels": ["TEMP"]}
            }
        })
        
        frames.append({
            "description": "🔄 Update: head = head->next (move HEAD to second node)",
            "data": {
                "values": values,
                "highlights": {"indices": [0, 1] if len(values) > 1 else [0],
                              "colors": ["#e74c3c", "#2ecc71"], "labels": ["OLD", "NEW HEAD"]}
            }
        })
        
        deleted_val = values[0]
        
        frames.append({
            "description": f"🗑️ delete temp (free memory of node {deleted_val})",
            "data": {"values": values, "highlights": {}}  # Still showing old list
        })
        
        # NOW remove it
        values = values[1:]
        
        frames.append({
            "description": f"✅ HEAD deleted! Node {deleted_val} removed from memory",
            "data": {"values": values, "highlights": {}}  # NOW shows updated list
        })
        
        frames.append({
            "description": f"New list: {' → '.join(map(str, values)) if values else 'EMPTY'} → NULL",
            "data": {"values": values, "highlights": {}}
        })
    else:
        frames.append({
            "description": f"✓ Position {delete_pos} is not 0, proceed with normal deletion",
            "data": {"values": values, "highlights": {}}
        })
        
        # Traverse
        frames.append({
            "description": f"🚶 Step 1: Traverse to position {delete_pos-1} (node BEFORE target)",
            "data": {"values": values, "highlights": {}}
        })
        
        for i in range(delete_pos):
            is_prev = (i == delete_pos - 1)
            frames.append({
                "description": f"At position {i}: value = {values[i]}{' (STOP - this is previous node)' if is_prev else ' (continue)'}",
                "data": {
                    "values": values,
                    "highlights": {"indices": [i], "colors": ["#3498db" if is_prev else "#f39c12"],
                                  "labels": ["PREV" if is_prev else "CURRENT"]}
                }
            })
            if is_prev:
                break
        
        # Show 3 nodes
        if delete_pos < len(values) - 1:
            frames.append({
                "description": f"📍 Context: PREV({values[delete_pos-1]}) → DELETE({values[delete_pos]}) → NEXT({values[delete_pos+1]})",
                "data": {
                    "values": values,
                    "highlights": {"indices": [delete_pos-1, delete_pos, delete_pos+1],
                                  "colors": ["#3498db", "#e74c3c", "#2ecc71"],
                                  "labels": ["PREV", "DELETE", "NEXT"]}
                }
            })
        else:
            frames.append({
                "description": f"📍 Deleting last node (after {values[delete_pos-1]})",
                "data": {
                    "values": values,
                    "highlights": {"indices": [delete_pos-1, delete_pos],
                                  "colors": ["#3498db", "#e74c3c"], "labels": ["PREV", "DELETE"]}
                }
            })
        
        # Save reference
        frames.append({
            "description": f"💾 Step 2: temp = curr->next (save reference to node {values[delete_pos]})",
            "data": {
                "values": values,
                "highlights": {"indices": [delete_pos], "colors": ["#e74c3c"], "labels": ["TEMP"]}
            }
        })
        
        frames.append({
            "description": "💡 WHY save: Need pointer to delete it from memory",
            "data": {"values": values, "highlights": {}}
        })
        
        # Bypass
        frames.append({
            "description": "🔗 Step 3: curr->next = temp->next (bypass target node)",
            "data": {
                "values": values,
                "highlights": {"indices": [delete_pos], "colors": ["#e74c3c"], "labels": ["BYPASS"]}
            }
        })
        
        frames.append({
            "description": f"➡️ Arrow update: Node {delete_pos-1} now points to node {delete_pos+1 if delete_pos < len(values)-1 else 'NULL'}",
            "data": {"values": values, "highlights": {}}  # Still showing original
        })
        
        # Delete - NOW remove it
        deleted_val = values[delete_pos]
        
        frames.append({
            "description": f"🗑️ delete temp (deallocating node with value {deleted_val})",
            "data": {"values": values, "highlights": {}}  # Still showing before deletion
        })
        
        # NOW actually remove from visualization
        values = values[:delete_pos] + values[delete_pos+1:]
        
        frames.append({
            "description": f"✅ Node {deleted_val} DELETED! Removed from memory",
            "data": {"values": values, "highlights": {}}  # NOW shows without deleted node
        })
        
        frames.append({
            "description": f"Memory freed! Node is gone",
            "data": {"values": values, "highlights": {}}
        })
    
    # Final
    frames.append({
        "description": f"📊 Updated list: {' → '.join(map(str, values)) if values else 'EMPTY'} → NULL",
        "data": {"values": values, "highlights": {}}
    })
    
    frames.append({
        "description": f"📏 List size: {len(values)} (reduced by 1)",
        "data": {"values": values, "highlights": {}}
    })
    
    frames.append({
        "description": "⏱️ Time: O(n) - traverse to position | Space: O(1) - only temp pointer",
        "data": {"values": values, "highlights": {}}
    })
    
    return frames
