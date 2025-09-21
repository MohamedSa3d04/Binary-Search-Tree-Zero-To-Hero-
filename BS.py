from collections import deque

class Node:
    def __init__(self, value=None):
        self.value = value
        self.left = None
        self.right = None
        self.parent = None # Excellent utility for successor finding

class Binary_Search_Tree:
    def __init__(self, root:Node):
        self.root = root
    
    def insert(self, root, value): #5
        if root:
            if value < root.value:
                if root.left:
                    self.insert(root.left, value)
                else:
                    root.left = Node(value)
                    root.left.parent = root

            else:
                if root.right:
                    self.insert(root.right, value)
                else:
                    root.right = Node(value)
                    root.right.parent = root
    
    def search(self, root, value):
        if root:
            if value == root.value:
                return root
            
            elif value < root.value:
                return self.search(root.left, value)
            
            else:
                return self.search(root.right, value)

        return False
    
    def in_order(self, root):
        if root:
            self.in_order(root.left)
            print(root.value, end=' --> ')
            self.in_order(root.right)
    
    def pre_order(self, root):
        nodes_lst = []

        def process(current):
            if not current:
                return

            nodes_lst.append(current.value)
            process(current.left)
            process(current.right)

        process(root)
        return nodes_lst
    
    def post_order(self, root):
        if root:
            self.post_order(root.left)
            self.post_order(root.right)
            print(root.value, end=' --> ')

    def level_traverse(self, root):
        q = deque([root])
        list_values = []
        while q:
            cur_node = q.popleft()
            list_values.append(cur_node.value)
            if cur_node.left:
                q.append(cur_node.left)
            
            if cur_node.right:
                q.append(cur_node.right)
        return list_values
    
    def get_minmum(self, root):
        if root:
            if root.left:
                return self.get_minmum(root.left)
            else:
                return root.value
        

    def get_maximum(self, root):
        if root:
            if root.right:
                self.get_maximum(root.right)
            else:
                print(root.value)


    ## Following codes is to get the successor:
    def get_successor(self, root, value):
        chain_list = [] # Initalize the stack
        def get_chain(current, value):
            if not current: # Base Case 1
                return False  
            
            chain_list.append(current)

            # Base Case 2
            if value == current.value:
                return True
            
            if value < current.value:
                return get_chain(current.left, value)
            else:
                return get_chain(current.right, value)
        
        get_chain(root, value)
        if not chain_list:
            return None
        
        node = chain_list.pop()

        if not chain_list and root.value != value:
            return None

        
        # First Case: I have a right subtree(So the minmum of this sub tree is my successor 
        # (exist in the leaf of the left sub - tree) )
        if node.right: # Exist
            sub_minmun = self.get_minmum(node.right) # Get it's minmun
            return sub_minmun

        # Now we don't have number bigger than us, Nor the number above us
        # That's mean that the ancestor's parent is the possible to be least bigger than us
        # (Just!!!) of we were in the left of it

        parent = chain_list.pop()
        child = node
        while parent and parent.right == child:
            child = parent
            parent = None if not chain_list else chain_list.pop()
        
        if not parent: # Our ancestor is the root
            return None
        
        return parent.value # Even is our parent if we in the left, or our ancestor's parent if we right 

    ## Soloution for parent link
    def get_successor_v2(self, root, value):
        node = self.search(root, value)
        if node.right:
            sub_minmun = self.get_minmum(node.right) # Get it's minmun
            return sub_minmun # Sub-Tree Minmum
        
        else:
            child = node
            parent_node = node.parent
            while parent_node and parent_node.right == child:
                child = parent_node
                parent_node = parent_node.parent
            
            if not parent_node:
                return None
            
            return parent_node.value


    def queries_of_successors(self, queue_nodes:deque):  
        copy_queue = queue_nodes.copy()
        lst_successors = []  
        last_node = None
        def in_order(current, queue_nodes):
            if current:
                if len(queue_nodes) == 0:
                    return
                
                nonlocal last_node
                in_order(current.left, queue_nodes)
                if last_node and last_node.value == queue_nodes[0]:
                    queue_nodes.popleft()
                    lst_successors.append(current.value)
                last_node = current
                in_order(current.right, queue_nodes)

        in_order(self.root, queue_nodes)
        return list(zip(copy_queue, lst_successors))
            
    
    def delete_node(self, root, value):
        def process(current, value):
            if current.value > value:
                current.left = process(current.left, value)
                return current
            
            if current.value < value:
                current.right = process(current.right, value)
                return current

            # When we delete a node we have 3 cases:
            # 1. Node dosn't have a child, then we just make its pointer points to None
            if not current.left and not current.right:
                return None
            
            # 2. Node have only one child, then we just replace it with this child
            if not current.left:
                return current.right

            if not current.right:
                return current.left
            
            # 3. Node have left and right, then replace it with its successor 
            # then apply previous two methos on successor place
            successor = self.get_successor(root, value) # get the successor
            current.value = successor # replace values
            current.right = process(current.right, successor) # replace right branch with new one
            return current # return the current node to be replaced with old one
        process(root, value)         
            
    @staticmethod
    def is_degenerate(list_nodes):
        if not list_nodes:
            return True
        if len(list_nodes) <= 2:
            return True  # always degenerate with 0, 1, or 2 nodes

        stk = [list_nodes[0]]
        prim_direction = None

        def right_or_left(parent, cur_value):
            return 'l' if cur_value < parent else 'r'

        for i in range(1, len(list_nodes)): # Loop for all numbers except first
            cur_value = list_nodes[i]
            cur_dir = right_or_left(stk[-1], cur_value) # current direction (Left, right)

            if prim_direction is None: # Primary Direction
                prim_direction = cur_dir
            elif cur_dir != prim_direction: # Zig-Zag State
                if cur_dir == 'r': # If we were going left but current direction is right,
                    # so current value must be less Than parent's previous node

                    if cur_value < stk[-2]:
                        prim_direction = 'r'
                    else:
                        return False
                else:# If we were going right but current direction is left,
                    # so current value must be bigger Than parent's previous node's value

                    if cur_value > stk[-2]:
                        prim_direction = 'f'
                    else:
                        return False



            stk.append(cur_value)

        return True

    def build_tree_from_preorder_v1(self, values):
        # First soloution is the normal insert (O(n*h))

        # Seconed is O(n^2): find the bigger from the cur_root O(n), split nodes > bigger , < bigger
        def recursive_process(values):
            #base case: if values is none, then no child
            if len(values) == 0:
                return None
            
            # we want to find the root and bigger
            bigger_idx = None
            cur_root = Node(values[0])
            for idx in range(len(values)):
                if values[idx] > cur_root.value:
                    bigger_idx = values[idx]
                    break
            
            if not bigger_idx:
                left = values[1:bigger_idx]
                cur_root.left = recursive_process(left)
            else:
                left = values[1:bigger_idx]
                right = values[bigger_idx:]

                cur_root.left = recursive_process(left)
                cur_root.right = recursive_process(right)
            return cur_root
        return Binary_Search_Tree(recursive_process(values)) 

    def build_tree_from_preorder_v2(self, values):
        nodes_deque = deque(values)
        # Useing Min-Max Way
        def recursive_process(min, max, nodes_deque):
            if len(nodes_deque) == 0:
                return None
            cur_node = Node(nodes_deque[0])
            if cur_node.value > max or cur_node.value < min:
                return None
            
            cur_node = Node(nodes_deque.popleft())
            cur_node.left = recursive_process(min, cur_node.value, nodes_deque)
            cur_node.right = recursive_process(cur_node.value, max, nodes_deque)
            return cur_node

        return Binary_Search_Tree(recursive_process(float('-inf'), float('inf'), nodes_deque))


    def get_tree_from_traversal(self, nodes_deque):
        def next_between(nodes_deque, mn, mx):
            return nodes_deque and mn < nodes_deque[0] < mx

        nodes_queue = deque()

        tree = Binary_Search_Tree(Node(nodes_deque.popleft()))
        nodes_queue.append([tree.root, float('-inf'), float('inf')])

        while nodes_queue:
            cur, mn, mx = nodes_queue.popleft()

            if next_between(nodes_deque, mn, cur.value):
                cur.left = Node(nodes_deque.popleft())
                nodes_queue.append([cur.left, mn, cur.value])

            if next_between(nodes_deque, cur.value, mx):
                cur.right = Node(nodes_deque.popleft())
                nodes_queue.append([cur.right, cur.value, mx])

        return tree
        

            


values = [3, 1, 5, -1, 6, -4, 0]
# bst = Binary_Search_Tree(Node(values[0]))
# for i in range(1, len(values)):
#     bst.insert(bst.root, values[i])

# bst.in_order(bst.root)
# print()
# print(bst.search(bst.root, -4))
# bst.get_maximum(bst.root)
# bst.get_minmum(bst.root)

# bst.delete_node(bst.root, 3)
# bst.in_order(bst.root)

# values = deque(sorted([3, -1, 5, 6]))
# print(bst.queries_of_successors(values))

# tree = Binary_Search_Tree(Node(50))
# values = [20, 60, 15, 45, 70, 35, 73]
# for i in range(0, len(values)):
#     tree.insert(tree.root, values[i])

# tree.pre_order(tree.root)

# tree2 = tree.get_tree_from_preorder(lst1.copy())
# lst2 = tree2.preorder()

# assert lst1 == lst2

# tree = Binary_Search_Tree(Node(0))
# print(tree.is_degenerate([100, 70, 101]))
# print(tree.is_degenerate([100, 70, 60, 75]))
# print(tree.is_degenerate([500, 400, 300, 200 , 250 , 275, 245]))


tree = Binary_Search_Tree(Node(50))
for value in [20, 60, 15, 45, 70, 35, 73]:
    tree.insert(tree.root, value)
level_list = tree.level_traverse(tree.root)
print(level_list)
tree2 = tree.get_tree_from_traversal(deque(level_list.copy()))
lst2 = tree2.level_traverse(tree2.root)
print(lst2)
assert level_list == lst2
