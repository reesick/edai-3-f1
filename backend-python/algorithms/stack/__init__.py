"""Stack algorithms package"""
from .push_stack import execute as push_execute, CODE_SAMPLE as push_sample
from .pop_stack import execute as pop_execute, CODE_SAMPLE as pop_sample
from .infix_to_postfix import execute as infix_postfix_execute, CODE_SAMPLE as infix_postfix_sample
from .postfix_eval import execute as postfix_eval_execute, CODE_SAMPLE as postfix_eval_sample
from .prefix_postfix import execute as prefix_postfix_execute, CODE_SAMPLE as prefix_postfix_sample
from .balanced_parens import execute as balanced_execute, CODE_SAMPLE as balanced_sample

OPERATIONS = [
    {"id": "push", "name": "Stack Push"},
    {"id": "pop", "name": "Stack Pop"},
    {"id": "infix_postfix", "name": "Infix → Postfix Conversion"},
    {"id": "postfix_eval", "name": "Postfix Evaluation"},
    {"id": "prefix_postfix", "name": "Prefix/Postfix Conversion"},
    {"id": "balanced", "name": "Balanced Parentheses"},
]

CODE_SAMPLES = {
    "push": push_sample,
    "pop": pop_sample,
    "infix_postfix": infix_postfix_sample,
    "postfix_eval": postfix_eval_sample,
    "prefix_postfix": prefix_postfix_sample,
    "balanced": balanced_sample,
}

def execute(operation, params):
    if operation == "push":
        return push_execute(params)
    elif operation == "pop":
        return pop_execute(params)
    elif operation == "infix_postfix":
        return infix_postfix_execute(params)
    elif operation == "postfix_eval":
        return postfix_eval_execute(params)
    elif operation == "prefix_postfix":
        return prefix_postfix_execute(params)
    elif operation == "balanced":
        return balanced_execute(params)
    raise ValueError(f"Unknown operation: {operation}")
