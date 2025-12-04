"""Stack Push - Production Grade"""

CODE_SAMPLE = """#include <iostream>
#include <stack>
using namespace std;

int main() {
    stack<int> s;
    s.push(10);
    s.push(20);
    s.push(30);
    
    cout << "Top: " << s.top() << endl;
    return 0;
}
"""

def execute(params):
    frames = []
    original_stack = list(params.get('stack', [10, 20, 30]))
    push_value = params.get('value', 40)
    
    # Frame 0: Intro
    frames.append({
        "description": "📚 Stack Push: Add element to top (LIFO)",
        "data": {"values": original_stack.copy(), "highlights": {}}
    })
    
    # Frame 1: Current stack
    frames.append({
        "description": f"📋 Current stack: {' → '.join(map(str, original_stack))} (→ is TOP)",
        "data": {
            "values": original_stack.copy(),
            "highlights": {"indices": [len(original_stack)-1], "colors": ["#3498db"], "labels": ["TOP"]}
        }
    })
    
    # Frame 2: Goal
    frames.append({
        "description": f"🎯 Goal: Push value {push_value} onto stack",
        "data": {"values": original_stack.copy(), "highlights": {}}
    })
    
    # Frame 3: Strategy
    frames.append({
        "description": "📚 Strategy: Stack follows LIFO (Last In, First Out) - add at top",
        "data": {"values": original_stack.copy(), "highlights": {}}
    })
    
    # Frame 4: Create element
    frames.append({
        "description": f"🆕 Step 1: Create new element with value {push_value}",
        "data": {"values": original_stack.copy(), "highlights": {}}
    })
    
    # Frame 5: Explain LIFO
    frames.append({
        "description": "💡 WHY push at top: Stack is LIFO - newest element must be accessible first",
        "data": {"values": original_stack.copy(), "highlights": {}}
    })
    
    # Frame 6: Show top position
    frames.append({
        "description": f"📍 Top position: After {original_stack[-1]} (rightmost)",
        "data": {
            "values": original_stack.copy(),
            "highlights": {"indices": [len(original_stack)-1], "colors": ["#f39c12"], "labels": ["CURRENT TOP"]}
        }
    })
    
    # Frame 7: Ready to push
    frames.append({
        "description": f"🔄 Step 2: Place {push_value} at new top position",
        "data": {"values": original_stack.copy(), "highlights": {}}
    })
    
    # Frame 8: PUSH HAPPENS - element appears!
    new_stack = original_stack + [push_value]
    frames.append({
        "description": f"✅ PUSH! Element {push_value} added to stack",
        "data": {
            "values": new_stack,
            "highlights": {"indices": [len(new_stack)-1], "colors": ["#2ecc71"], "labels": ["NEW TOP"]}
        }
    })
    
    # Frame 9: Show new stack
    frames.append({
        "description": f"📊 Updated stack: {' → '.join(map(str, new_stack))}",
        "data": {"values": new_stack, "highlights": {}}
    })
    
    # Frame 10: Stack size
    frames.append({
        "description": f"📏 Stack size: {len(original_stack)} → {len(new_stack)} (increased by 1)",
        "data": {"values": new_stack, "highlights": {}}
    })
    
    # Frame 11: Complexity
    frames.append({
        "description": "⏱️ Time: O(1) - constant time | Space: O(1) - one element",
        "data": {"values": new_stack, "highlights": {}}
    })
    
    return frames
