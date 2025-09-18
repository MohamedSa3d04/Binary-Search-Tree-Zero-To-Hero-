class Node:
    def __init__(self, value=None):
        self.value = value
        self.left = None
        self.right = None

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

            else:
                if root.right:
                    self.insert(root.right, value)
                else:
                    root.right = Node(value)
    
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
            if value == current:
                return True
            
            if value < current:
                return get_chain(current.left, value)
            else:
                return get_chain(current.right, value)
        

        if not chain_list:
            return None
        
        node = chain_list.pop()

        if not chain_list:
            return None

        
        # First Case: I have a right subtree(So the minmum of this sub tree is my successor 
        # (exist in the leaf of the left sub - tree) )
        if node.right: # Exist
            sub_minmun = self.get_minmum(node.right) # Get it's minmun
            return sub_minmun

        # Now we don't have number bigger than us, Nor the number above us
        # That's mean that the root's parent is the possible to be least bigger than us
        # (Just!!!) of we were in the left of it

        parent = chain_list.pop()
        child = node
        while parent and parent.right == child:
            child = parent
            parent = chain_list.pop()
        
        if not parent:
            return None
        

        

        



values = [3, 1, 5, -1, 6, -4]
bst = Binary_Search_Tree(Node(values[0]))
for i in range(1, len(values)):
    bst.insert(bst.root, values[i])

# bst.in_order(bst.root)
# print()
# print(bst.search(bst.root, -4))
# bst.get_maximum(bst.root)
# bst.get_minmum(bst.root)

print(bst.get_successor(bst.root, 6))