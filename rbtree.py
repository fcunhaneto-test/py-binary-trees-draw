#!/home/francisco/Projects/Pycharm/pyalgorithms/venv/bin/python3
# -*- coding: utf-8 -*-


#!/home/francisco/Projects/Pycharm/pyalgorithms/venv/bin/python3
# -*- coding: utf-8 -*-

BLACK = 1
RED = 0


class RBNode:
    def __init__(self, value):
        self.key = value
        self.left = None
        self.right = None
        self.parent = None
        self.color = BLACK


class RBTree:
    def __init__(self):
        self.root = None
        self.leaf = RBNode(None)
        self.leaf.color = BLACK
        self.node_list =[]

    def insert(self, key):
        node = RBNode(key)
        node.left = self.leaf
        node.right = self.leaf

        if not self.root:
            self.root = node
        else:
            current = self.root
            parent = current
            while current != self.leaf:
                parent = current
                if node.key < current.key:
                    current = current.left
                elif node.key > current.key:
                    current = current.right
                else:
                    return False

            node.parent = parent

            if node.key < parent.key:
                parent.left = node
            else:
                parent.right = node

            node.color = RED

            self._fix_violation(node)

    def _fix_violation(self, z):
        while z != self.root and z.parent.color == RED:
            if z.parent == z.parent.parent.left:  # verifies if parent of z is on left or right of his grandfather
                y = z.parent.parent.right  # y is uncle of z
                if y.color == RED:
                    z.parent.color = BLACK
                    y.color = BLACK
                    z.parent.parent.color = RED
                    z = z.parent.parent
                else:
                    if z == z.parent.right:
                        z = z.parent
                        self._rotate_left(z)

                    z.parent.color = BLACK
                    z.parent.parent.color = RED
                    self._rotate_right(z.parent.parent)
            else:
                y = z.parent.parent.left  # y é igual ao tio de z
                if y.color == RED:
                    z.parent.color = BLACK
                    y.color = BLACK
                    z.parent.parent.color = RED
                    z = z.parent.parent
                else:
                    if z == z.parent.left:
                        z = z.parent
                        self._rotate_right(z)

                    z.parent.color = BLACK
                    z.parent.parent.color = RED
                    self._rotate_left(z.parent.parent)

        self.root.color = BLACK

    def _rotate_left(self, x):
        y = x.right  # define y
        x.right = y.left  # x right now igual y left
        y.left.parent = x  # y left now is x left
        y.parent = x.parent  # y parent is x parent

        if x == self.root:  # if x is root now y is root
            self.root = y
        elif x == x.parent.left:
            x.parent.left = y  # if x is the left child, then y is the left child
        else:
            x.parent.right = y  # if x is the right child, then y is the right child

        y.left = x  # y left now is x
        x.parent = y  # x parent now is y

    def _rotate_right(self, x):
        y = x.left
        x.left = y.right
        y.right.parent = x
        y.parent = x.parent

        if x == self.root:  # if x is root now y is root
            self.root = y
        elif x == x.parent.left:
            x.parent.left = y  # if x is the left child, then y is the left child
        else:
            x.parent.right = y  # if x is the right child, then y is the right child

        y.right = x
        x.parent = y

    def walk_in_order(self, node=None):
        if not node:
            node = self.root

        if node != self.leaf:

            self.walk_in_order(node.left)

            if node.parent:

                print('{0}\t{1}\t{2}\t{3}\t{4}'.format(node.key, node.parent.key, node.left.key, node.right.key,
                                                            node.color))
            else:
                print('{0}\t{1}\t{2}\t{3}\t{4}'.format(node.key, None, node.left.key, node.right.key,
                                                            node.color))

            self.walk_in_order(node.right)

    def walk_pos_order(self, node=None):
        if not node:
            node = self.root

        if node != self.leaf:

            self.walk_pos_order(node.right)

            if node.parent:

                print('{0}\t{1}\t{2}\t{3}\t{4}'.format(node.key, node.parent.key, node.left.key, node.right.key,
                                                            node.color))
            else:
                print('{0}\t{1}\t{2}\t{3}\t{4}'.format(node.key, None, node.left.key, node.right.key,
                                                            node.color))

            self.walk_pos_order(node.left)

    def search(self, value):
        current = self.root
        while current and value != current.key:
            if not current.key:
                return False

            if current.key > value:
                current = current.left
            else:
                current = current.right

        return current

    def minimum(self, node=None):
        if not node:
            node = self.root

        while node.left != self.leaf:
            node = node.left

        return node

    def maximum(self, node=None):
        if not node:
            node = self.root

        while node.right != self.leaf:
            node = node.right

        return node

    def successor(self, value):
        current = self.search(value)
        if not current:
            return False
        elif current.right != self.leaf:
            node = self.minimum(current.right)
            return node

        node = current.parent
        while node and current == node.right:
            current = node
            node = current.parent

        if not node:
            return self.maximum()

        return node

    def predecessor(self, value):
        current = self.search(value)
        if not current:
            return False
        elif current.left != self.leaf:
            node = self.maximum(current.left)
            return node

        node = current.parent
        while node and current == node.left:
            current = node
            node = current.parent

        if not node:
            return self.minimum()

        return node

    def remove(self, value):
        """
        Remove node where key is equal of given value.
        :param value: numeric
        """
        print(value)
        node = self.search(value)

        if node == self.root:
            return self._remove_root()
        elif node.left == self.leaf and node.right == self.leaf:
            return self._remove_if_leaf(node)
        elif (node.left == self.leaf) ^ (node.right == self.leaf):
            return self._remove_if_one_child(node)
        else:
            return self._remove_if_two_children(node)

    def _remove_if_leaf(self, node):
        parent = node.parent
        if parent.left == node:
            parent.left = self.leaf
        else:
            parent.right = self.leaf

        del node

    def _remove_if_one_child(self, node):
        if node.parent.left == node:
            if node.right == self.leaf:
                node.parent.left = node.left
            else:
                node.parent.left = node.right
        else:
            if node.right == self.leaf:
                node.parent.right = node.left
            else:
                node.parent.right = node.right

        node.left.parent = node.parent
        node.right.parent = node.parent

        del node

    def _remove_if_two_children(self, node):
        remove_key = node.key
        successor = self.successor(node.key)

        if successor == node.right:
            if node == node.parent.left:
                node.parent.left = successor
            else:
                node.parent.right = successor

            successor.parent = node.parent
            successor.left = node.left
            successor.left.parent = successor
        else:
            if node == node.parent.left:
                node.parent.left = successor
            else:
                node.parent.right = successor

            successor.parent.left = successor.right
            successor.left = node.left
            successor.right = node.right

            node.right.parent = successor
            node.left.parent = successor
            successor.parent = node.parent

        del node

        return remove_key, successor.key

    def _remove_root(self):
        remove_key = self.root.key
        successor = None
        if self.root.left == self.leaf and self.root.right == self.leaf:
            self.root = None
        elif (self.root.left == self.leaf) ^ (self.root.right == self.leaf):
            if self.root.left != self.leaf:
                self.root = self.root.left
            else:
                self.root = self.root.right

            self.root.parent = None
        else:
            successor = self.successor(self.root.key)
            if successor == self.root.right:

                successor.parent = None
                successor.left = self.root.left
                self.root.left.parent = successor
                self.root = successor
            else:
                if successor.right:
                    successor.right.parent = successor.parent

                successor.parent.left = successor.right
                successor.left = self.root.left
                successor.right = self.root.right

                self.root.left.parent = successor
                self.root.right.parent = successor
                successor.parent = None
                self.root = successor


if __name__ == '__main__':
    # from trees import handletrees
    # handletrees.handle_trees()
    bt = RBTree()
    print('node\tparent\tleft\tright\tcolor')
    print('***********************************************')
    # bt.insert(11)
    # bt.insert(2)
    # bt.insert(14)
    # bt.insert(1)
    # bt.insert(7)
    # bt.insert(15)
    # bt.insert(5)
    # bt.insert(8)
    # bt.insert(4)
    # bt.walk_in_order()

    bt.insert(2)
    bt.insert(1)
    bt.insert(4)
    bt.insert(5)
    bt.insert(9)
    bt.insert(3)
    bt.insert(6)
    bt.insert(7)
    bt.walk_in_order()