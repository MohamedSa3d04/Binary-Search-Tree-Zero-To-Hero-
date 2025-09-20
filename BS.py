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
        if root:
            print(root.value, end=' --> ')
            self.pre_order(root.left)
            self.pre_order(root.right)
    
    def post_order(self, root):
        if root:
            self.post_order(root.left)
            self.post_order(root.right)
            print(root.value, end=' --> ')

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
            
    # @staticmethod
    # def is_degenerate(list_nodes):
    #     prev = list_nodes.pop()
    #     cur = list_nodes.pop()

    #     left = False
    #     right = False
    #     for value in list_nodes:


        

        



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

tree = Binary_Search_Tree(Node(50))
values = [20, 60, 15, 45, 70, 35, 73]
for i in range(0, len(values)):
    tree.insert(tree.root, values[i])

tree.pre_order(tree.root)

# tree2 = tree.get_tree_from_preorder(lst1.copy())
# lst2 = tree2.preorder()

# assert lst1 == lst2
