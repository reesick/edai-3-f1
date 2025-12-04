from algorithms.stack.postfix_eval import execute as postfix_execute
from algorithms.stack.balanced_parens import execute as balanced_execute
from algorithms.stack.prefix_postfix import execute as prefix_execute

print("=" * 60)
print("POSTFIX EVALUATION: '23*'")
print("=" * 60)
frames = postfix_execute({'expression': '23*'})
for i, frame in enumerate(frames):
    print(f"Frame {i:2d}: {frame['description'][:50]:<50} | Stack: {frame['data']['values']}")

print("\n" + "=" * 60)
print("BALANCED PARENTHESES: '{()}'")
print("=" * 60)
frames = balanced_execute({'expression': '{()}'})
for i, frame in enumerate(frames):
    print(f"Frame {i:2d}: {frame['description'][:50]:<50} | Stack: {frame['data']['values']}")

print("\n" + "=" * 60)
print("PREFIX TO POSTFIX: '+ab'")
print("=" * 60)
frames = prefix_execute({'expression': '+ab'})
for i, frame in enumerate(frames):
    print(f"Frame {i:2d}: {frame['description'][:50]:<50} | Stack: {frame['data']['values']}")
