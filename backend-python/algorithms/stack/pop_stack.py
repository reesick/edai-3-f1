"""Stack Pop - Production Grade"""

CODE_SAMPLE = """#include <iostream>
#include <stack>
using namespace std;

int main() {
    stack<int> s;
    s.push(10);
    s.push(20);
    s.push(30);
    
    int top = s.top();
    s.pop();
    cout << "Popped: " << top << endl;
    return 0;
}
"""

def execute(params):
    frames = []
    original_stack = list(params.get('stack', [10, 20, 30, 40]))
    
    # Frame 0: Intro
    frames.append({
        "description": "🗑️ Stack Pop: Remove element from top (LIFO)",
        "data": {"values": original_stack.copy(), "highlights": {}}
    })
    
    # Frame 1: Current stack
    frames.append({
        "description": f"📋 Current stack: {' → '.join(map(str, original_stack))}",
        "data": {
            "values": original_stack.copy(),
            "highlights": {"indices": [len(original_stack)-1], "colors": ["#3498db"], "labels": ["TOP"]}
        }
    })
    
    # Frame 2: Goal
    frames.append({
        "description": f"🎯 Goal: Remove top element ({original_stack[-1]})",
        "data": {
            "values": original_stack.copy(),
            "highlights": {"indices": [len(original_stack)-1], "colors": ["#e74c3c"], "labels": ["POP THIS"]}
        }
    })
    
    # Frame 3: Check empty
    frames.append({
        "description": f"🔍 Step 1: Check if stack empty? NO (size = {len(original_stack)})",
        "data": {"values": original_stack.copy(), "highlights": {}}
    })
    
    # Frame 4: Strategy
    frames.append({
        "description": "📚 Strategy: LIFO - remove most recently added element (top)",
        "data": {"values": original_stack.copy(), "highlights": {}}
    })
    
    # Frame 5: Highlight top
    frames.append({
        "description": f"📍 Top element identified: {original_stack[-1]}",
        "data": {
            "values": original_stack.copy(),
            "highlights": {"indices": [len(original_stack)-1], "colors": ["#e74c3c"], "labels": ["DELETE"]}
        }
    })
    
    # Frame 6: Save value
    popped_value = original_stack[-1]
    frames.append({
        "description": f"💾 Step 2: Save top value: {popped_value}",
        "data": {
            "values": original_stack.copy(),
            "highlights": {"indices": [len(original_stack)-1], "colors": ["#f39c12"], "labels": ["SAVE"]}
        }
    })
    
    # Frame 7: WHY
    frames.append({
        "description": "💡 WHY pop from top: Stack follows LIFO principle",
        "data": {"values": original_stack.copy(), "highlights": {}}
    })
    
    # Frame 8: Adjust pointer
    frames.append({
        "description": "🔄 Step 3: Move top pointer down (decrement)",
        "data": {
            "values": original_stack.copy(),
            "highlights": {"indices": [len(original_stack)-1], "colors": ["#e74c3c"], "labels": ["REMOVE"]}
        }
    })
    
    # Frame 9: POP HAPPENS - element disappears!
    new_stack = original_stack[:-1]
    frames.append({
        "description": f"✅ POP! Element {popped_value} removed from stack",
        "data": {"values": new_stack, "highlights": {}}
    })
    
    # Frame 10: Show new top
    if new_stack:
        frames.append({
            "description": f"📍 New top element: {new_stack[-1]}",
            "data": {
                "values": new_stack,
                "highlights": {"indices": [len(new_stack)-1], "colors": ["#2ecc71"], "labels": ["NEW TOP"]}
            }
        })
    else:
        frames.append({
            "description": "Stack is now EMPTY",
            "data": {"values": [], "highlights": {}}
        })
    
    # Frame 11: Result
    frames.append({
        "description": f"📊 Updated stack: {' → '.join(map(str, new_stack)) if new_stack else 'EMPTY'}",
        "data": {"values": new_stack, "highlights": {}}
    })
    
    # Frame 12: Popped value
    frames.append({
        "description": f"🔢 Popped value: {popped_value}",
        "data": {"values": new_stack, "highlights": {}}
    })
    
    # Frame 13: Complexity
    frames.append({
        "description": "⏱️ Time: O(1) - constant time | Space: O(1)",
        "data": {"values": new_stack, "highlights": {}}
    })
    
    return frames
