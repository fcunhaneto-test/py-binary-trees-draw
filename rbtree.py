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
                node.height += 1
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


if __name__ == '__main__':
    # from trees import handletrees
    # handletrees.handle_trees()
    bt = RBTree()
    print('node\tparent\tleft\tright\tcolor')
    print('***********************************************')
    bt.insert(11)
    bt.insert(2)
    bt.insert(14)
    bt.insert(1)
    bt.insert(7)
    bt.insert(15)
    bt.insert(5)
    bt.insert(8)
    bt.insert(4)
    bt.walk_in_order()

    # bt.insert(2)
    # bt.insert(1)
    # bt.insert(4)
    # bt.insert(5)
    # bt.insert(9)
    # bt.insert(3)
    # bt.insert(6)
    # bt.insert(7)
    # bt.walk_in_order()
