#!/home/francisco/Projects/Pycharm/pyalgorithms/venv/bin/python3
# -*- coding: utf-8 -*-

from math import inf
from node import Node

BLACK = 1
RED = 0


class RBTree:
    def __init__(self):
        self.root = None
        self.nodes_dict_aux = {}
        self.nodes_dict = {}

    def insert(self, key):
        node = Node(key)
        node.left = Node(None)
        node.left.parent = node
        node.right = Node(None)
        node.right.parent = node

        if not self.root:
            self.root = node
            self.root.color = BLACK
            self.root.parent = Node(None)
            node.left = Node(None)
            node.right = Node(None)
        else:
            current = self.root
            parent = current
            while current.key:
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

            self._recovery_nodes_dict()

    def walk_in_order(self, node=None):
        if not node:
            node = self.root

        if node.key:

            self.walk_in_order(node.left)

            if node.parent:

                print('{0}\t{1}\t{2}\t{3}\t{4}\t{5}'.format(node.key, node.parent.key, node.left.key, node.right.key,
                                                            node.height, node.color))
            else:
                print('{0}\t{1}\t{2}\t{3}\t{4}\t{5}'.format(node.key, None, node.left.key, node.right.key, node.height,
                                                            node.color))

            self.walk_in_order(node.right)

    def walk_pos_order(self, node=None):
        if not node:
            node = self.root

        if node.key:

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

        while node.left.key:
            node = node.left

        return node

    def maximum(self, node=None):
        if not node:
            node = self.root

        while node.right.key:
            node = node.right

        return node

    def successor(self, value):
        current = self.search(value)
        if not current:
            return False
        elif current.right.key:
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
        elif current.left.key:
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
        node = self.search(value)

        if node == self.root:
            return self._remove_root()
        elif (not node.left.key) and (not node.right.key):
            return self._remove_if_one_child(node)
        elif (not node.left.key) ^ (not node.right.key):
            return self._remove_if_one_child(node)
        else:
            return self._remove_if_two_children(node)

    def _remove_if_one_child(self, node):
        remove_key = node.key

        color = node.color
        if node.parent.left == node:
            if not node.right.key:
                node.parent.left = node.left
                recovery_node = node.left
            else:
                node.parent.left = node.right
                recovery_node = node.right
        else:
            if not node.right.key:
                node.parent.right = node.left
                recovery_node = node.left
            else:
                node.parent.right = node.right
                recovery_node = node.left

        node.left.parent = node.parent
        node.right.parent = node.parent

        del node

        self._recovery_height_sub(recovery_node)

        if color == BLACK:
            self._remove_fix_violation(recovery_node)

        self._recovery_nodes_dict()

        return remove_key, None

    def _remove_if_two_children(self, node):
        remove_key = node.key
        successor = self.successor(node.key)
        color = successor.color

        successor.color = node.color
        successor.height = node.height

        recovery_node = successor.right

        if successor.parent == node:
            if node == node.parent.left:
                node.parent.left = successor
            else:
                node.parent.right = successor

            successor.parent = node.parent
            successor.left = node.left
            successor.left.parent = successor

            recovery_node.parent = successor
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

        self._recovery_height_sub(recovery_node)

        if color == BLACK:
            self._remove_fix_violation(recovery_node)

        self._recovery_nodes_dict()

        return remove_key, successor.key

    def _remove_root(self):
        if (not self.root.left.key) and (not self.root.right.key):
            self.root = None
            self.nodes_dict = {}
        elif (not self.root.left.key) ^ (not self.root.right.key):
            if self.root.left.key:
                self.root = self.root.left
            else:
                self.root = self.root.right

            self.root.color = BLACK
            self.root.height = 0
            self.root.parent = Node(None)
        else:
            successor = self.successor(self.root.key)
            remove_key = self.root.key
            color = successor.color
            recovery_node = successor.right

            if successor == self.root.right:
                successor.parent = None
                successor.left = self.root.left
                self.root.left.parent = successor
                self.root = successor
                recovery_node.parent = successor
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

            self.root.height = 0
            self.root.color = BLACK

            self._recovery_height_sub(recovery_node)

            if color == BLACK:
                self._remove_fix_violation(recovery_node)

            self._recovery_nodes_dict()

            return remove_key, successor.key

    def _remove_fix_violation(self, x):
        while x != self.root and x.color == BLACK:
            if x == x.parent.left:
                w = x.parent.right
                if w.color == RED:
                    w.color = BLACK
                    x.parent.color = RED
                    self._rotate_left(x.parent)
                    w = x.parent.right

                if w.left.color == BLACK and w.right.color == BLACK:
                    w.color = RED
                    x = x.parent
                else:
                    if w.right.color == BLACK:
                        w.left.color = BLACK
                        w.color = RED
                        self._rotate_right(w)
                        w = x.parent.right

                    w.color = x.parent.color
                    x.parent.color = BLACK
                    w.right.color = BLACK
                    self._rotate_left(x.parent)
                    x = self.root
            else:
                w = x.parent.left
                if w.color == RED:
                    w.color = BLACK
                    x.parent.color = RED
                    self._rotate_right(x.parent)
                    w = x.parent.left

                if w.right.color == BLACK and w.left.color == BLACK:
                    w.color = RED
                    x = x.parent
                else:
                    if w.left.color == BLACK:
                        w.right.color = BLACK
                        w.color = RED
                        self._rotate_left(w)
                        w = x.parent.left

                    w.color = x.parent.color
                    x.parent.color = BLACK
                    w.left.color = BLACK
                    self._rotate_right(x.parent)
                    x = self.root

        x.color = BLACK

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

        y.height -= 1
        x.height += 1

        y.left = x  # y left now is x
        x.parent = y  # x parent now is y

        self._recovery_height_sub(y.right)
        self._recovery_height_add(x.left)

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

        y.height -= 1
        x.height += 1

        y.right = x
        x.parent = y

        self._recovery_height_sub(y.left)
        self._recovery_height_add(x.right)

    def _recovery_height_sub(self, node=None):

        if node.key:
            self._recovery_height_sub(node.left)

            node.height -= 1

            self._recovery_height_sub(node.right)

    def _recovery_height_add(self, node=None):
        if node.key:
            self._recovery_height_add(node.left)

            node.height += 1

            self._recovery_height_add(node.right)

    def _recovery_nodes_dict(self):
        self.nodes_dict_aux = {}
        self._make_nodes_dict_aux()

        self.nodes_dict = {}
        self._make_nodes_dict()

    def _make_nodes_dict_aux(self, node=None, flag=0):
        if not node:
            node = self.root

        if node != self.root and node.key:
            if not ((node.parent.key, node.parent.height) in self.nodes_dict_aux):
                self.nodes_dict_aux[node.parent.key, node.parent.height] = [None, None]
            self.nodes_dict_aux[node.parent.key, node.parent.height][flag] = (node.key, node.color)

        if node.key:
            self._make_nodes_dict_aux(node.left, 0)
            self._make_nodes_dict_aux(node.right, 1)

    def _make_nodes_dict(self):
        for key_height in self.nodes_dict_aux:
            key, height = key_height
            left, right = self.nodes_dict_aux[key_height]
            if left and right:
                node_left, color_left = left
                node_right, color_right = right
                self.nodes_dict[key, height+1] = [[node_left, color_left], [node_right, color_right]]
            else:
                if left:
                    node_left, color_left = left
                    self.nodes_dict[key, height+1] = [[node_left, color_left], None]
                else:
                    node_right, color_right = right
                    self.nodes_dict[key, height+1] = [None, [node_right, color_right]]


if __name__ == '__main__':
    # from trees import handletrees
    # handletrees.handle_trees()
    bt = RBTree()

    # bt.insert(11)
    # bt.insert(2)
    # bt.insert(14)
    # bt.insert(1)
    # bt.insert(7)
    # bt.insert(15)
    # bt.insert(5)
    # bt.insert(8)
    # # bt.insert(4)
    # print('***********************************************')
    # print('node\tparent\tleft\tright\theight\tcolor')
    # print('***********************************************')
    # bt.walk_in_order()
    # print('***********************************************')
    # print(bt.nodes_dict)
    # print('***********************************************')
    # bt.remove(11)
    # print('Remove 11')
    # print('***********************************************')
    # print('node\tparent\tleft\tright\theight\tcolor')
    # print('***********************************************')
    # bt.walk_in_order()
    # print('***********************************************')
    # print(bt.nodes_dict)
    # print('***********************************************')
    # bt.remove(2)
    # print('Remove 2')
    # print('***********************************************')
    # print('node\tparent\tleft\tright\theight\tcolor')
    # print('***********************************************')
    # bt.walk_in_order()
    # print('***********************************************')
    # print(bt.nodes_dict)
    # print('***********************************************')

    bt.insert(13)
    bt.insert(8)
    bt.insert(17)
    bt.insert(1)
    bt.insert(11)
    bt.insert(15)
    bt.insert(25)
    bt.insert(6)
    bt.insert(14)
    bt.insert(22)
    bt.insert(27)
    print('***********************************************')
    print('node\tparent\tleft\tright\theight\tcolor')
    print('***********************************************')
    bt.walk_in_order()
    print('***********************************************')
    print(bt.nodes_dict)
    print('***********************************************')
    bt.remove(13)
    print('Remove 13')
    print('***********************************************')
    print('node\tparent\tleft\tright\theight\tcolor')
    print('***********************************************')
    bt.walk_in_order()
    print('***********************************************')
    print(bt.nodes_dict)
    print('***********************************************')

    # bt.insert(30)
    # bt.insert(20)
    # bt.insert(40)
    # bt.insert(35)
    # bt.insert(50)
    # print('***********************************************')
    # print('node\tparent\tleft\tright\theight\tcolor')
    # print('***********************************************')
    # bt.walk_in_order()
    # print('***********************************************')
    # bt.remove(20)
    # print('Remove 20')
    # print('***********************************************')
    # print('node\tparent\tleft\tright\theight\tcolor')
    # print('***********************************************')
    # bt.walk_in_order()
    # print('***********************************************')

    # bt.insert(2)
    # bt.insert(1)
    # bt.insert(4)
    # bt.insert(5)
    # bt.insert(9)
    # bt.insert(3)
    # bt.insert(6)
    # bt.insert(7)
    # print('***********************************************')
    # print('node\tparent\tleft\tright\theight\tcolor')
    # print('***********************************************')
    # bt.walk_in_order()
    # print('***********************************************')
