# Binary Search Tree example


class BinarySearchTree():
    def __init__(self):
        self.root = None
    def find(self, value): # self attempt to provide find
        current = self.root 
        while True:
            print("current",current)

            if current.left is None and current.right is None:
                print("no value found")
                return False            
            elif value == current.value:
                print("yay")
                return True
            elif value < current.value: 
                current = current.left
            elif value > current.value:
                current = current.right

    def findv2(self): # find provided by tutorial solution
        pass


    def insert(self, value):
        new_node = Node(value)
        if self.root is None: 
            self.root = new_node
            return self
        else:
            current = self.root
            while True:
                # check if value is < or > current
                if value < current.value:
                    if current.left is None:
                        current.left = Node(value)
                    # go left 
                        return self
                    else:
                        current = current.left
                elif value > current.value:
                    if current.right is None:
                        current.right = Node(value)
                        return self
                    else:
                        current = current.right
                else:
                    return None

class Node():
    def __init__(self, value):
        self.value = value
        self.left = None
        self.right = None





if __name__ == "__main__":
    tree = BinarySearchTree()
    tree.insert(10)
    tree.insert(5)
    tree.insert(2)
    tree.insert(7)
    tree.insert(13)
    tree.insert(11)
    tree.insert(16)
    tree.insert(10)
    tree.find(11)
    pass
    # tree.root = Node(10)
    # tree.root.right = Node(15)
    # tree.root.left = Node(7)
    # tree.root.left.right = Node(9)