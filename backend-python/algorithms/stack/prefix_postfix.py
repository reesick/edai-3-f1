"""Prefix to Postfix Conversion - Production Grade with Logical Frames"""

CODE_SAMPLE = """#include <iostream>
#include <stack>
#include <string>
#include <algorithm>
using namespace std;

string prefixToPostfix(string prefix) {
    stack<string> s;
    
    // Scan from right to left
    for(int i = prefix.length() - 1; i >= 0; i--) {
        char c = prefix[i];
        
        if(isalnum(c)) {
            s.push(string(1, c));
        } else {
            string op1 = s.top(); s.pop();
            string op2 = s.top(); s.pop();
            string exp = op1 + op2 + c;
            s.push(exp);
        }
    }
    
    return s.top();
}
"""

def execute(params):
    frames = []
    prefix = params.get('expression', "+*23/84")
    
    # Frame 0: Intro
    frames.append({
        "description": f"🔄 Prefix → Postfix: '{prefix}'",
        "data": {"values": [], "highlights": {}}
    })
    
    # Frame 1: Strategy
    frames.append({
        "description": "📚 Strategy: Scan RIGHT to LEFT, build postfix",
        "data": {"values": [], "highlights": {}}
    })
    
    # Frame 2: Initial
    stack = []
    frames.append({
        "description": f"📋 Input: '{prefix}' | Stack: []",
        "data": {"values": stack.copy(), "highlights": {}}
    })
    
    # Scan right to left
    for i in range(len(prefix) - 1, -1, -1):
        char = prefix[i]
        
        frames.append({
            "description": f"📍 Scan from RIGHT: '{char}' at position {i}",
            "data": {"values": stack.copy(), "highlights": {}}
        })
        
        if char.isalnum():
            stack.append(char)
            frames.append({
                "description": f"🔤 '{char}' is operand → Push",
                "data": {
                    "values": stack.copy(),
                    "highlights": {"indices": [len(stack)-1], "colors": ["#2ecc71"], "labels": ["PUSHED"]}
                }
            })
        
        elif char in '+-*/':
            if len(stack) < 2:
                frames.append({
                    "description": "❌ Error: Need 2 operands!",
                    "data": {"values": stack.copy(), "highlights": {}}
                })
                continue
            
            # Pop two operands
            op1 = stack.pop()
            frames.append({
                "description": f"⬆️ Pop first: '{op1}'",
                "data": {"values": stack.copy(), "highlights": {}}
            })
            
            op2 = stack.pop()
            frames.append({
                "description": f"⬆️ Pop second: '{op2}'",
                "data": {"values": stack.copy(), "highlights": {}}
            })
            
            # Form postfix expression
            exp = f"{op1}{op2}{char}"
            frames.append({
                "description": f"🔗 Form postfix: {op1} {op2} {char} = '{exp}'",
                "data": {"values": stack.copy(), "highlights": {}}
            })
            
            stack.append(exp)
            frames.append({
                "description": f"📌 Push sub-expression: '{exp}'",
                "data": {
                    "values": stack.copy(),
                    "highlights": {"indices": [len(stack)-1], "colors": ["#3498db"], "labels": ["SUB-EXP"]}
                }
            })
    
    # Final
    if stack and len(stack) == 1:
        result = stack[0]
        frames.append({
            "description": f"✅ COMPLETE! Postfix: '{result}'",
            "data": {
                "values": [result],
                "highlights": {"indices": [0], "colors": ["#2ecc71"], "labels": ["RESULT"]}
            }
        })
        
        frames.append({
            "description": f"📊 '{prefix}' (prefix) = '{result}' (postfix)",
            "data": {"values": [result], "highlights": {}}
        })
    else:
        frames.append({
            "description": "❌ Error: Invalid expression",
            "data": {"values": stack.copy(), "highlights": {}}
        })
    
    frames.append({
        "description": "⏱️ Time: O(n) | Space: O(n)",
        "data": {"values": stack.copy(), "highlights": {}}
    })
    
    return frames
