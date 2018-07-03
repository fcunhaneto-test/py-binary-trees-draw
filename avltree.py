#!/home/francisco/Projects/Pycharm/py-binary-trees-draw/venv/bin/python
# -*- coding: utf-8 -*-

from node import Node
import drawtree


class AVLTree:
    def __init__(self):
        self.root = None
        self.leaf = Node(None)
        self.leaf.height = -1

        self.nodes_dict_aux = {}
        self.nodes_dict = {}

    def insert(self, key):
        """
        Insert key values in tree
        :param key: numeric.
        :return: self.nodes_height_dict a dict where keys are tuple (parent, height) and values are the children.
        """
        node = Node(key)
        node.left = self.leaf
        node.right = self.leaf

        if not self.root:
            self.root = node
        else:
            current = self.root
            parent = current

            while current:
                if current == self.leaf:
                    break
                node.height += 1
                parent = current
                if node.key < current.key:
                    current = current.left
                elif node.key > current.key:
                    current = current.right
                elif node.key == current.key:
                    return False

            node.parent = parent

            if node.key < parent.key:
                parent.left = node
            else:
                parent.right = node

            self._calculate_height(node)
            self._fix_violation(node)

            self._recovery_nodes_dict()

            return self.nodes_dict

        return None

    def walk_in_order(self, node=None):
        """
        Walking tree in pre-order.
        :param node: node object.
        """
        if not node:
            node = self.root

        if node != self.leaf:
            self.walk_in_order(node.left)

            fb = node.left.height - node.right.height
            if node.parent:
                print('{0}\t{1}\t{2}\t{3}\t{4}\t{5}'.format(node.key, node.parent.key, node.left.key, node.right.key,
                                                            node.height, fb))
            else:
                print('{0}\t{1}\t{2}\t{3}\t{4}\t{5}'.format(node.key, None, node.left.key, node.right.key,
                                                            node.height, fb))

            self.walk_in_order(node.right)

    def walk_pos_order(self, node=None):
        """
        Walking tree in pos-order.
        :param node: node object.
        """
        if not node:
            node = self.root

        if node != self.leaf:

            self.walk_pos_order(node.right)
            if node.parent:
                print('{0}\t{1}\t{2}\t{3}\t{4}'.format(node.key, node.parent.key, node.left.key, node.right.key,
                                                       node.height, ))
            else:
                print('{0}\t{1}\t{2}\t{3}\t{4}'.format(node.key, None, node.left.key, node.right.key, node.height))

            self.walk_pos_order(node.left)

    def search(self, value):
        """
        Search the node object that key is equal for given value.
        :param value: numeric.
        :return: node object.
        """
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
        """
        Search the minimum key in subtree that start from given node.
        :param node: node object.
        :return: node object.
        """
        if not node:
            node = self.root

        while node.left != self.leaf:
            node = node.left

        return node

    def maximum(self, node=None):
        """
        Search the maximum key in subtree that start from given node.
        :param node: node object.
        :return: node object.
        """
        if not node:
            node = self.root

        while node.right != self.leaf:
            node = node.right

        return node

    def successor(self, value):
        """
        Find the largest value in the tree directly above the given value.
        :param value: numeric.
        :return: object node.
        """
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
        """
        It finds in the tree the lowest value directly below the given number.
        :param value: numeric.
        :return: node object.
        """
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
        node = self.search(value)

        if node == self.root:
            self._remove_root()
        elif node.left == self.leaf and node.right == self.leaf:
            self._remove_if_leaf(node)
        elif (node.left == self.leaf) ^ (node.right == self.leaf):
            self._remove_if_one_child(node)
        else:
            self._remove_if_two_childs(node)

    def _remove_if_leaf(self, node):
        parent = node.parent
        if parent.left == node:
            parent.left = self.leaf
        else:
            parent.right = self.leaf

        node = None
        del node

        self._calculate_height(parent)
        self._fix_violation(parent)

        self._recovery_nodes_dict()

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

        self._calculate_height(node.parent)
        self._fix_violation(node.parent)

        self._recovery_nodes_dict()

    def _remove_if_two_childs(self, node):
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

        self._calculate_height(node.parent)
        self._fix_violation(node.parent)

        self._recovery_nodes_dict()

    def _remove_root(self):
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

        self._calculate_height(self.root)
        self._fix_violation(self.root)

        self._recovery_nodes_dict()

    def _recovery_nodes_dict(self):
        # Because fixing the violations mess up the heights of each node we have to first create a dict where the
        # keys are the parents and the values are a list of tuples with the childs and their heights.
        self.nodes_dict_aux = {}  # a dict where keys are parent and values is tuples with child and ir height.
        self._make_nodes_dict_aux()

        self.nodes_dict = {}  # a dict where keys are tuple with parent and chid height and values is tuples
        # with child.
        self._make_nodes_dict()

    def _make_nodes_dict_aux(self, node=None, flag=0):
        """
        Recursion function to create dict where the keys are the parents and the values are a list of tuples with the
        childs and their heights.
        :param node: node object.
        :param flag: integer who indicate if node is left or right child.
        """
        if not node:
            node = self.root

        if node != self.root and node != self.leaf:
            height = self._calculate_real_height(node)
            if not (node.parent.key in self.nodes_dict_aux):
                self.nodes_dict_aux[node.parent.key] = [None, None]
            self.nodes_dict_aux[node.parent.key][flag] = (node.key, height)

        if node != self.leaf:
            self._make_nodes_dict_aux(node.left, 0)
            self._make_nodes_dict_aux(node.right, 1)

    def _make_nodes_dict(self):
        for key in self.nodes_dict_aux:
            nodes = self.nodes_dict_aux[key]
            if nodes[0] and nodes[1]:
                _, height = min(nodes, key=lambda x: x[:][1])
                # print(nodes[0][0], nodes[1][0], height)
                self.nodes_dict[key, height] = [nodes[0][0], nodes[1][0]]
            else:
                if nodes[0]:
                    height = nodes[0][1]
                    self.nodes_dict[key, height] = [nodes[0][0], None]
                else:
                    height = nodes[1][1]
                    self.nodes_dict[key, height] = [None, nodes[1][0]]

    def _calculate_real_height(self, node):
        """
        Calculate real height in tree of given node.
        :param node: node object.
        :return: numeric.
        """
        height = 0
        current = node
        while current != self.root:
            height += 1
            current = current.parent

        return height

    def _calculate_height(self, node):
        """
        Calculate left and right height of node.
        :param node: node object.
        """
        current = node
        while current:
            current.height = max(current.left.height, current.right.height) + 1
            current = current.parent

    def _fix_violation(self, node):
        """
        Verify if is necessary rotate the node.
        :param node: node object.
        """
        flag = False
        previous = node
        current = node.parent
        while current:
            fb1 = current.left.height - current.right.height
            fb2 = previous.left.height - previous.right.height
            if fb1 >= 2 and fb2 >= 0:
                self._rotate_right(current)
                flag = True
                break
            if fb1 <= -2 and fb2 <= 0:
                self._rotate_left(current)
                flag = True
                break
            if fb1 >= +2 and fb2 <= 0:
                self._rotate_left(previous)
                self._rotate_right(current)
                flag = True
                break
            if fb1 <= -2 and fb2 >= 0:
                self._rotate_right(previous)
                self._rotate_left(current)
                flag = True
                break
            previous = current
            current = current.parent

        return flag

    def _rotate_left(self, x):
        """
        Rotate node to left.
        :param x: node object.
        """
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

        x.height -= 2
        self._calculate_height(x)

    def _rotate_right(self, x):
        """
        Rotate node to right.
        :param x: node object.
        """
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

        x.height -= 2
        self._calculate_height(x)


if __name__ == '__main__':
    bt = AVLTree()
    print('node\tparent\tleft\tright\theight\tfb')
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
    # print('***********************************************')
    # print(bt.nodes_dict)
    # print('***********************************************')

    bt.insert(44)
    bt.insert(17)
    bt.insert(78)
    bt.insert(32)
    bt.insert(50)
    bt.insert(88)
    bt.insert(48)
    bt.insert(62)
    bt.insert(84)
    bt.insert(92)
    bt.insert(80)
    bt.insert(82)
    bt.walk_in_order()
    print('***********************************************')
    print(bt.nodes_dict)
    print('***********************************************')
    bt.remove(32)
    print('remove 32')
    print('node\tparent\tleft\tright\theight\tfb')
    print('***********************************************')
    bt.walk_in_order()
    print('***********************************************')
    print(bt.nodes_dict)
    print('***********************************************')
    bt.remove(84)
    print('remove 84')
    print('node\tparent\tleft\tright\theight\tfb')
    print('***********************************************')
    bt.walk_in_order()
    print('***********************************************')
    print(bt.nodes_dict)
    print('***********************************************')
    bt.remove(82)
    print('remove 82')
    print('node\tparent\tleft\tright\theight\tfb')
    print('***********************************************')
    bt.walk_in_order()
    print('***********************************************')
    print(bt.nodes_dict)
    print('***********************************************')

    # bt.insert(4)
    # bt.insert(2)
    # bt.insert(6)
    # bt.insert(1)
    # bt.insert(3)
    # bt.insert(5)
    # bt.insert(15)
    # bt.insert(7)
    # bt.insert(16)
    # bt.insert(14)
    # bt.bt_draw()

    # bt.insert(10)
    # bt.insert(5)
    # bt.insert(16)
    # bt.insert(2)
    # bt.insert(8)
    # bt.insert(1)
    # bt.bt_draw()
