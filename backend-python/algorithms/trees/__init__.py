"""Tree Algorithms - BST operations and traversals"""

from .bst_insert import METADATA as BST_INSERT_META, execute as insert_execute
from .bst_search import METADATA as BST_SEARCH_META, execute as search_execute
from .bst_delete import METADATA as BST_DELETE_META, execute as delete_execute
from .binary_tree_traversals import METADATA as BT_TRAVERSALS_META, execute as traversals_execute
from .lca_in_bst import METADATA as LCA_META, execute as lca_execute

# Operations registry - ARRAY format for frontend
OPERATIONS = [
    {
        "id": "bst_insert",
        "name": BST_INSERT_META["name"],
        "description": BST_INSERT_META["description"],
        "time_complexity": BST_INSERT_META["time_complexity"],
        "space_complexity": BST_INSERT_META["space_complexity"]
    },
    {
        "id": "bst_search",
        "name": BST_SEARCH_META["name"],
        "description": BST_SEARCH_META["description"],
        "time_complexity": BST_SEARCH_META["time_complexity"],
        "space_complexity": BST_SEARCH_META["space_complexity"]
    },
    {
        "id": "bst_delete",
        "name": BST_DELETE_META["name"],
        "description": BST_DELETE_META["description"],
        "time_complexity": BST_DELETE_META["time_complexity"],
        "space_complexity": BST_DELETE_META["space_complexity"]
    },
    {
        "id": "binary_tree_traversals",
        "name": BT_TRAVERSALS_META["name"],
        "description": BT_TRAVERSALS_META["description"],
        "time_complexity": BT_TRAVERSALS_META["time_complexity"],
        "space_complexity": BT_TRAVERSALS_META["space_complexity"]
    },
    {
        "id": "lca_in_bst",
        "name": LCA_META["name"],
        "description": LCA_META["description"],
        "time_complexity": LCA_META["time_complexity"],
        "space_complexity": LCA_META["space_complexity"]
    }
]

# C++ code samples for each operation
CODE_SAMPLES = {
    "bst_insert": """#include <bits/stdc++.h>
using namespace std;

struct Node {
    int data;
    Node *left, *right;
    Node(int val) : data(val), left(NULL), right(NULL) {}
};

class TrackedTree {
public:
    Node* root;
    
    TrackedTree() : root(NULL) {}
    
    Node* insert(Node* node, int val) {
        if (!node) return new Node(val);
        
        if (val < node->data)
            node->left = insert(node->left, val);
        else if (val > node->data)
            node->right = insert(node->right, val);
        
        return node;
    }
    
    void insertValue(int val) {
        root = insert(root, val);
    }
};

int main() {
    vector<int> tree_values = {50, 30, 70, 20, 40, 60, 80};
    TrackedTree tree;
    
    for (int val : tree_values) {
        tree.insertValue(val);
    }
    
    // Insert new value
    int insert_value = 45;
    tree.insertValue(insert_value);
    
    return 0;
}""",
    
    "bst_search": """#include <bits/stdc++.h>
using namespace std;

struct Node {
    int data;
    Node *left, *right;
    Node(int val) : data(val), left(NULL), right(NULL) {}
};

class TrackedTree {
public:
    Node* root;
    
    TrackedTree() : root(NULL) {}
    
    bool search(Node* node, int val) {
        if (!node) return false;
        if (node->data == val) return true;
        
        if (val < node->data)
            return search(node->left, val);
        else
            return search(node->right, val);
    }
    
    bool searchValue(int val) {
        return search(root, val);
    }
};

int main() {
    vector<int> tree_values = {50, 30, 70, 20, 40, 60, 80};
    TrackedTree tree;
    
    // Build tree (simplified)
    // tree.root = buildTree(tree_values);
    
    int search_value = 40;
    bool found = tree.searchValue(search_value);
    
    cout << (found ? "Found" : "Not found") << endl;
    return 0;
}""",
    
    "bst_delete": """#include <bits/stdc++.h>
using namespace std;

struct Node {
    int data;
    Node *left, *right;
    Node(int val) : data(val), left(NULL), right(NULL) {}
};

Node* minValueNode(Node* node) {
    while (node->left) node = node->left;
    return node;
}

Node* deleteNode(Node* root, int val) {
    if (!root) return NULL;
    
    if (val < root->data)
        root->left = deleteNode(root->left, val);
    else if (val > root->data)
        root->right = deleteNode(root->right, val);
    else {
        // Node found - delete it
        if (!root->left) return root->right;
        if (!root->right) return root->left;
        
        // Node with two children
        Node* temp = minValueNode(root->right);
        root->data = temp->data;
        root->right = deleteNode(root->right, temp->data);
    }
    return root;
}

int main() {
    vector<int> tree_values = {50, 30, 70, 20, 40, 60, 80};
    // Build BST from values
    
    int delete_value = 30;
    // Delete node
    
    return 0;
}""",
    
    "binary_tree_traversals": """#include <bits/stdc++.h>
using namespace std;

struct Node {
    int data;
    Node *left, *right;
    Node(int val) : data(val), left(NULL), right(NULL) {}
};

void inorder(Node* root) {
    if (!root) return;
    inorder(root->left);
    cout << root->data << " ";
    inorder(root->right);
}

void preorder(Node* root) {
    if (!root) return;
    cout << root->data << " ";
    preorder(root->left);
    preorder(root->right);
}

void postorder(Node* root) {
    if (!root) return;
    postorder(root->left);
    postorder(root->right);
    cout << root->data << " ";
}

int main() {
    vector<int> tree_values = {50, 30, 70, 20, 40, 60, 80};
    // Build BST from values
    
    cout << "Inorder: ";
    // inorder(root);
    cout << endl;
    
    cout << "Preorder: ";
    // preorder(root);
    cout << endl;
    
    cout << "Postorder: ";
    // postorder(root);
    cout << endl;
    
    return 0;
}""",
    
    "lca_in_bst": """#include <bits/stdc++.h>
using namespace std;

struct Node {
    int data;
    Node *left, *right;
    Node(int val) : data(val), left(NULL), right(NULL) {}
};

Node* LCA(Node* root, int n1, int n2) {
    if (!root) return NULL;
    
    // Both nodes in left subtree
    if (root->data > n1 && root->data > n2)
        return LCA(root->left, n1, n2);
    
    // Both nodes in right subtree
    if (root->data < n1 && root->data < n2)
        return LCA(root->right, n1, n2);
    
    // Split point - this is LCA
    return root;
}

int main() {
    vector<int> tree_values = {50, 30, 70, 20, 40, 60, 80};
    // Build BST from values
    
    int node1 = 20, node2 = 60;
    // Node* lca = LCA(root, node1, node2);
    
    // cout << "LCA: " << lca->data << endl;
    
    return 0;
}"""
}


def execute(operation, params):
    """Execute tree algorithm and return visualization frames"""
    executors = {
        "bst_insert": insert_execute,
        "bst_search": search_execute,
        "bst_delete": delete_execute,
        "binary_tree_traversals": traversals_execute,
        "lca_in_bst": lca_execute
    }
    
    metadata = {
        "bst_insert": BST_INSERT_META,
        "bst_search": BST_SEARCH_META,
        "bst_delete": BST_DELETE_META,
        "binary_tree_traversals": BT_TRAVERSALS_META,
        "lca_in_bst": LCA_META
    }
    
    if operation not in executors:
        raise ValueError(f"Unknown tree operation: {operation}")
    
    # Trees don't use code param - always use default_input
    # If params only has 'code', replace with default_input
    if params and 'code' in params and len(params) == 1:
        params = {}
    
    # Merge default input with params
    if operation in metadata and 'default_input' in metadata[operation]:
        final_params = {**metadata[operation]['default_input'], **(params or {})}
    else:
        final_params = params or {}
    
    return executors[operation](final_params)
