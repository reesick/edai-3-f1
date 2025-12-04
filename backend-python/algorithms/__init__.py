"""Algorithms package - organized by category"""

# Import category modules
from .sorting import OPERATIONS as SORTING_OPS, CODE_SAMPLES as SORTING_SAMPLES, execute as sorting_execute
from .searching import OPERATIONS as SEARCHING_OPS, CODE_SAMPLES as SEARCHING_SAMPLES, execute as searching_execute
from .trees import OPERATIONS as TREES_OPS, CODE_SAMPLES as TREES_SAMPLES, execute as trees_execute
from .linkedlist import OPERATIONS as LINKEDLIST_OPS, CODE_SAMPLES as LINKEDLIST_SAMPLES, execute as linkedlist_execute
from .stack import OPERATIONS as STACK_OPS, CODE_SAMPLES as STACK_SAMPLES, execute as stack_execute
from .queue import OPERATIONS as QUEUE_OPS, CODE_SAMPLES as QUEUE_SAMPLES, execute as queue_execute

# Module registry
MODULES = {
    "sorting": {
        "name": "Sorting Algorithms",
        "icon": "↕️",
        "operations": SORTING_OPS,
        "code": SORTING_SAMPLES,
        "execute": sorting_execute,
    },
    "searching": {
        "name": "Searching Algorithms",
        "icon": "🔍",
        "operations": SEARCHING_OPS,
        "code": SEARCHING_SAMPLES,
        "execute": searching_execute,
    },
    "trees": {
        "name": "Tree Algorithms",
        "icon": "🌲",
        "operations": TREES_OPS,
        "code": TREES_SAMPLES,
        "execute": trees_execute,
    },
    "linkedlist": {
        "name": "Linked Lists",
        "icon": "🔗",
        "operations": LINKEDLIST_OPS,
        "code": LINKEDLIST_SAMPLES,
        "execute": linkedlist_execute,
    },
    "stack": {
        "name": "Stack",
        "icon": "📚",
        "operations": STACK_OPS,
        "code": STACK_SAMPLES,
        "execute": stack_execute,
    },
    "queue": {
        "name": "Queue",
        "icon": "📬",
        "operations": QUEUE_OPS,
        "code": QUEUE_SAMPLES,
        "execute": queue_execute,
    },
}

def get_module(module_name):
    """Get module configuration"""
    return MODULES.get(module_name)

def execute_module(module_name, operation, params):
    """Execute algorithm"""
    module = MODULES.get(module_name)
    if not module:
        raise ValueError(f"Module not found: {module_name}")
    
    return module["execute"](operation, params)
