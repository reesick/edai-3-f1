"""Balanced Parentheses - Production Grade with Logical Frames"""

CODE_SAMPLE = """#include <iostream>
#include <stack>
#include <string>
using namespace std;

bool isBalanced(string expr) {
    stack<char> s;
    
    for(char c : expr) {
        if(c == '(' || c == '[' || c == '{') {
            s.push(c);
        }
        else if(c == ')' || c == ']' || c == '}') {
            if(s.empty()) return false;
            
            char top = s.top();
            if((c == ')' && top == '(') ||
               (c == ']' && top == '[') ||
               (c == '}' && top == '{')) {
                s.pop();
            } else {
                return false;
            }
        }
    }
    
    return s.empty();
}
"""

def execute(params):
    frames = []
    expression = params.get('expression', "{[()]}")
    
    def matches(open_b, close_b):
        pairs = {'(': ')', '[': ']', '{': '}'}
        return pairs.get(open_b) == close_b
    
    # Frame 0: Intro
    frames.append({
        "description": f"🔍 Balanced Parentheses: Check '{expression}'",
        "data": {"values": [], "highlights": {}}
    })
    
    # Frame 1: Strategy
    frames.append({
        "description": "📚 Strategy: Push opening, pop & match closing",
        "data": {"values": [], "highlights": {}}
    })
    
    # Frame 2: Initial
    stack = []
    frames.append({
        "description": f"📋 Expression: '{expression}' | Stack: []",
        "data": {"values": stack.copy(), "highlights": {}}
    })
    
    balanced = True
    
    for i, char in enumerate(expression):
        frames.append({
            "description": f"📍 Scanning: '{char}' at position {i}",
            "data": {"values": stack.copy(), "highlights": {}}
        })
        
        if char in '([{':
            stack.append(char)
            frames.append({
                "description": f"📌 Opening '{char}' → Push to stack",
                "data": {
                    "values": stack.copy(),
                    "highlights": {"indices": [len(stack)-1], "colors": ["#2ecc71"], "labels": ["PUSHED"]}
                }
            })
        
        elif char in ')]}':
            if not stack:
                frames.append({
                    "description": f"❌ Closing '{char}' but stack EMPTY → UNBALANCED!",
                    "data": {"values": [], "highlights": {}}
                })
                balanced = False
                break
            
            top = stack[-1]
            frames.append({
                "description": f"🔍 Check: Does '{top}' match '{char}'?",
                "data": {
                    "values": stack.copy(),
                    "highlights": {"indices": [len(stack)-1], "colors": ["#f39c12"], "labels": ["CHECK"]}
                }
            })
            
            if matches(top, char):
                stack.pop()
                frames.append({
                    "description": f"✅ MATCH! '{top}' matches '{char}' → Pop",
                    "data": {"values": stack.copy(), "highlights": {}}
                })
            else:
                frames.append({
                    "description": f"❌ NO MATCH! '{top}' ≠ '{char}' → UNBALANCED!",
                    "data": {"values": stack.copy(), "highlights": {}}
                })
                balanced = False
                break
    
    # Final check
    if balanced:
        if not stack:
            frames.append({
                "description": "✅ Stack EMPTY → All matched → BALANCED!",
                "data": {"values": [], "highlights": {}}
            })
            
            frames.append({
                "description": f"📊 Result: '{expression}' is BALANCED ✓",
                "data": {"values": [], "highlights": {}}
            })
        else:
            frames.append({
                "description": f"❌ Stack NOT EMPTY (has {stack}) → UNBALANCED!",
                "data": {"values": stack.copy(), "highlights": {}}
            })
            
            frames.append({
                "description": f"📊 Result: '{expression}' is UNBALANCED ✗",
                "data": {"values": stack.copy(), "highlights": {}}
            })
    else:
        frames.append({
            "description": f"📊 Result: '{expression}' is UNBALANCED ✗",
            "data": {"values": stack.copy(), "highlights": {}}
        })
    
    frames.append({
        "description": "⏱️ Time: O(n) | Space: O(n)",
        "data": {"values": stack.copy() if stack else [], "highlights": {}}
    })
    
    return frames
