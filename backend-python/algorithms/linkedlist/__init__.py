"""Linked List algorithms package - Only the 4 core algorithms"""
from .print_list import execute as print_execute, CODE_SAMPLE as print_sample
from .search_list import execute as search_execute, CODE_SAMPLE as search_sample
from .insert_at_pos import execute as insert_pos_execute, CODE_SAMPLE as insert_pos_sample
from .delete_at_pos import execute as delete_pos_execute, CODE_SAMPLE as delete_pos_sample

OPERATIONS = [
    {"id": "print", "name": "Print/Traverse List"},
    {"id": "search", "name": "Search by Value (Find Index)"},
    {"id": "insert_pos", "name": "Insert at Position"},
    {"id": "delete_pos", "name": "Delete at Position"},
]

CODE_SAMPLES = {
    "print": print_sample,
    "search": search_sample,
    "insert_pos": insert_pos_sample,
    "delete_pos": delete_pos_sample,
}

def execute(operation, params):
    if operation == "print":
        return print_execute(params)
    elif operation == "search":
        return search_execute(params)
    elif operation == "insert_pos":
        return insert_pos_execute(params)
    elif operation == "delete_pos":
        return delete_pos_execute(params)
    raise ValueError(f"Unknown operation: {operation}")
