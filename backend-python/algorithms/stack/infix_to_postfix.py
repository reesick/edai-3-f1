"""Infix to Postfix Conversion - Production Grade with Logical Frames"""

CODE_SAMPLE = """#include <iostream>
#include <stack>
#include <string>
using namespace std;

int precedence(char op) {
    if(op == '+' || op == '-') return 1;
    if(op == '*' || op == '/') return 2;
    return 0;
}

string infixToPostfix(string infix) {
    stack<char> s;
    string postfix = "";
    
    for(char c : infix) {
        if(isalnum(c)) {
            postfix += c;
        } else if(c == '(') {
            s.push(c);
        } else if(c == ')') {
            while(!s.empty() && s.top() != '(') {
                postfix += s.top();
                s.pop();
            }
            s.pop();
        } else {
            while(!s.empty() && precedence(s.top()) >= precedence(c)) {
                postfix += s.top();
                s.pop();
            }
            s.push(c);
        }
    }
    
    while(!s.empty()) {
        postfix += s.top();
        s.pop();
    }
    
    return postfix;
}
"""

def execute(params):
    frames = []
    infix = params.get('expression', "a+b*c")
    
    def precedence(op):
        if op in '+-': return 1
        if op in '*/': return 2
        return 0
    
    # Frame 0: Intro
    frames.append({
        "description": f"🔄 Infix → Postfix: Convert '{infix}'",
        "data": {"values": [], "highlights": {}}
    })
    
    # Frame 1: Initial state
    stack = []
    output = ""
    frames.append({
        "description": f"📋 Input: '{infix}' | Stack: [] | Output: \"\"",
        "data": {"values": stack.copy(), "highlights": {}}
    })
    
    # Process each character
    for i, char in enumerate(infix):
        # Show scanning
        frames.append({
            "description": f"📍 Scanning character '{char}' at position {i}",
            "data": {"values": stack.copy(), "highlights": {}}
        })
        
        if char.isalnum():  # Operand
            output += char
            frames.append({
                "description": f"✓ '{char}' is operand → Add to output: \"{output}\"",
                "data": {"values": stack.copy(), "highlights": {}}
            })
        
        elif char == '(':
            stack.append(char)
            frames.append({
                "description": f"📌 '(' pushed to stack",
                "data": {
                    "values": stack.copy(),
                    "highlights": {"indices": [len(stack)-1], "colors": ["#3498db"], "labels": ["PUSHED"]}
                }
            })
        
        elif char == ')':
            frames.append({
                "description": f"🔍 ')' found → Pop until '('",
                "data": {"values": stack.copy(), "highlights": {}}
            })
            
            while stack and stack[-1] != '(':
                op = stack.pop()
                output += op
                frames.append({
                    "description": f"⬆️ Pop '{op}' to output: \"{output}\"",
                    "data": {"values": stack.copy(), "highlights": {}}
                })
            
            if stack and stack[-1] == '(':
                stack.pop()
                frames.append({
                    "description": f"🗑️ Remove matching '(' from stack",
                    "data": {"values": stack.copy(), "highlights": {}}
                })
        
        elif char in '+-*/':  # Operator
            # Pop higher/equal precedence
            while stack and stack[-1] != '(' and precedence(stack[-1]) >= precedence(char):
                op = stack.pop()
                output += op
                frames.append({
                    "description": f"⬆️ '{op}' has ≥ precedence → Pop to output: \"{output}\"",
                    "data": {"values": stack.copy(), "highlights": {}}
                })
            
            stack.append(char)
            frames.append({
                "description": f"📌 Push '{char}' to stack",
                "data": {
                    "values": stack.copy(),
                    "highlights": {"indices": [len(stack)-1], "colors": ["#2ecc71"], "labels": ["PUSHED"]}
                }
            })
    
    # Pop remaining
    frames.append({
        "description": f"🏁 End of input → Pop remaining operators",
        "data": {"values": stack.copy(), "highlights": {}}
    })
    
    while stack:
        op = stack.pop()
        output += op
        frames.append({
            "description": f"⬆️ Pop '{op}' to output: \"{output}\"",
            "data": {"values": stack.copy(), "highlights": {}}
        })
    
    # Final
    frames.append({
        "description": f"✅ COMPLETE! Postfix: \"{output}\"",
        "data": {"values": [], "highlights": {}}
    })
    
    frames.append({
        "description": f"📊 {infix} (infix) = {output} (postfix)",
        "data": {"values": [], "highlights": {}}
    })
    
    frames.append({
        "description": "⏱️ Time: O(n) | Space: O(n)",
        "data": {"values": [], "highlights": {}}
    })
    
    return frames
