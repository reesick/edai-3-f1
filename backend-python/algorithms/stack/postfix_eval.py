"""Postfix Evaluation - Production Grade with Logical Frames"""

CODE_SAMPLE = """#include <iostream>
#include <stack>
#include <string>
using namespace std;

int evaluatePostfix(string postfix) {
    stack<int> s;
    
    for(char c : postfix) {
        if(isdigit(c)) {
            s.push(c - '0');
        } else {
            int b = s.top(); s.pop();
            int a = s.top(); s.pop();
            
            switch(c) {
                case '+': s.push(a + b); break;
                case '-': s.push(a - b); break;
                case '*': s.push(a * b); break;
                case '/': s.push(a / b); break;
            }
        }
    }
    
    return s.top();
}
"""

def execute(params):
    frames = []
    postfix = params.get('expression', "23*5+")
    
    # Frame 0: Intro
    frames.append({
        "description": f"📊 Postfix Evaluation: '{postfix}'",
        "data": {"values": [], "highlights": {}}
    })
    
    # Frame 1: Initial
    stack = []
    frames.append({
        "description": f"📋 Expression: '{postfix}' | Stack: []",
        "data": {"values": stack.copy(), "highlights": {}}
    })
    
    for i, char in enumerate(postfix):
        # Scan
        frames.append({
            "description": f"📍 Scanning: '{char}' at position {i}",
            "data": {"values": stack.copy(), "highlights": {}}
        })
        
        if char.isdigit():
            val = int(char)
            stack.append(val)
            frames.append({
                "description": f"🔢 '{char}' is operand → Push {val}",
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
            
            # Pop operands
            b = stack.pop()
            frames.append({
                "description": f"⬆️ Pop operand: {b}",
                "data": {"values": stack.copy(), "highlights": {}}
            })
            
            a = stack.pop()
            frames.append({
                "description": f"⬆️ Pop operand: {a}",
                "data": {"values": stack.copy(), "highlights": {}}
            })
            
            # Calculate
            if char == '+':
                result = a + b
            elif char == '-':
                result = a - b
            elif char == '*':
                result = a * b
            elif char == '/':
                result = a // b if b != 0 else 0
            
            frames.append({
                "description": f"🧮 Calculate: {a} {char} {b} = {result}",
                "data": {"values": stack.copy(), "highlights": {}}
            })
            
            stack.append(result)
            frames.append({
                "description": f"📌 Push result: {result}",
                "data": {
                    "values": stack.copy(),
                    "highlights": {"indices": [len(stack)-1], "colors": ["#3498db"], "labels": ["RESULT"]}
                }
            })
    
    # Final
    if stack:
        result = stack[0]
        frames.append({
            "description": f"✅ COMPLETE! Final result: {result}",
            "data": {
                "values": stack.copy(),
                "highlights": {"indices": [0], "colors": ["#2ecc71"], "labels": ["ANSWER"]}
            }
        })
        
        frames.append({
            "description": f"📊 '{postfix}' = {result}",
            "data": {"values": [result], "highlights": {}}
        })
    else:
        frames.append({
            "description": "❌ Error: Invalid expression",
            "data": {"values": [], "highlights": {}}
        })
    
    frames.append({
        "description": "⏱️ Time: O(n) | Space: O(n)",
        "data": {"values": stack.copy(), "highlights": {}}
    })
    
    return frames
