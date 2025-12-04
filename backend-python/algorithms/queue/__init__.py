"""Queue algorithms package"""
from .enqueue import execute as enqueue_execute, CODE_SAMPLE as enqueue_sample
from .dequeue import execute as dequeue_execute, CODE_SAMPLE as dequeue_sample
from .circular_queue import execute as circular_execute, CODE_SAMPLE as circular_sample
from .priority_queue import execute as priority_execute, CODE_SAMPLE as priority_sample
from .input_restricted_deque import execute as input_deque_execute, CODE_SAMPLE as input_deque_sample
from .output_restricted_deque import execute as output_deque_execute, CODE_SAMPLE as output_deque_sample

OPERATIONS = [
    {"id": "enqueue", "name": "Enqueue"},
    {"id": "dequeue", "name": "Dequeue"},
    {"id": "circular", "name": "Circular Queue"},
    {"id": "priority", "name": "Priority Queue"},
    {"id": "input_deque", "name": "Input-Restricted Deque"},
    {"id": "output_deque", "name": "Output-Restricted Deque"},
]

CODE_SAMPLES = {
    "enqueue": enqueue_sample,
    "dequeue": dequeue_sample,
    "circular": circular_sample,
    "priority": priority_sample,
    "input_deque": input_deque_sample,
    "output_deque": output_deque_sample,
}

def execute(operation, params):
    if operation == "enqueue":
        return enqueue_execute(params)
    elif operation == "dequeue":
        return dequeue_execute(params)
    elif operation == "circular":
        return circular_execute(params)
    elif operation == "priority":
        return priority_execute(params)
    elif operation == "input_deque":
        return input_deque_execute(params)
    elif operation == "output_deque":
        return output_deque_execute(params)
    raise ValueError(f"Unknown operation: {operation}")
