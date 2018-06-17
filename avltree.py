#!/home/francisco/Projects/Pycharm/py-draw-binary-trees/venv/bin/python3
# -*- coding: utf-8 -*-

from node import Node
import drawtree

class AVLTree:
    def __init__(self):
        self.root = None
        self.leaf = Node(None)
        self.leaf.height = -1

        self.nodes_dict = {}
        self.nodes_height_dict = {}

    def insert(self, key):
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

            self.calculate_height(node)
            self.fix_violation(node)

            self.nodes_dict = {}
            self.prepare_nodes_dict()

            self.nodes_height_dict = {}
            self.prepare_points()

            return self.nodes_height_dict

        return None

    def prepare_nodes_dict(self, node=None, flag=0):
        if not node:
            node = self.root

        if node != self.root and node != self.leaf:
            height = self.calculate_real_height(node)
            if not (node.parent.key in self.nodes_dict):
                self.nodes_dict[node.parent.key] = [None, None]
            self.nodes_dict[node.parent.key][flag] = (node.key, height)

        if node != self.leaf:
            self.prepare_nodes_dict(node.left, 0)
            self.prepare_nodes_dict(node.right, 1)

    def prepare_points(self, node=None, flag=0):
        for key in self.nodes_dict:
            nodes = self.nodes_dict[key]
            if nodes[0] and nodes[1]:
                _, height = min(nodes, key=lambda x:x[:][1])
                # print(nodes[0][0], nodes[1][0], height)
                self.nodes_height_dict[key, height] = [nodes[0][0], nodes[1][0]]
            else:
                if nodes[0]:
                    height = nodes[0][1]
                    self.nodes_height_dict[key, height] = [nodes[0][0], None]
                else:
                    height = nodes[1][1]
                    self.nodes_height_dict[key, height] = [None, nodes[1][0]]

    def calculate_real_height(self, node):
        height = 0
        current = node
        while current != self.root:
            height += 1
            current = current.parent

        return height

    def calculate_height(self, node):
        current = node
        while current:
            current.height = max(current.left.height, current.right.height) + 1
            current = current.parent

    def fix_violation(self, node):
        previous = node
        current = node.parent
        while current:
            fb1 = current.left.height - current.right.height
            fb2 = previous.left.height - previous.right.height
            if fb1 >= 2 and fb2 >= 0:
                self.rotate_right(current)
                break
            if fb1 <= -2 and fb2 <= 0:
                self.rotate_left(current)
                break
            if fb1 >= +2 and fb2 <= 0:
                self.rotate_left(previous)
                self.rotate_right(current)
                break
            if fb1 <= -2 and fb2 >= 0:
                self.rotate_right(previous)
                self.rotate_left(current)
                break
            previous = current
            current = current.parent

    def rotate_left(self, x):
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
        self.calculate_height(x)

    def rotate_right(self, x):
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
        self.calculate_height(x)

    def walk_in_order(self, node=None):
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
        node = self.search(value)

        if node.left == self.leaf and node.right == self.leaf:
            self._remove_if_leaf(node)
        elif (node.left == self.leaf) ^ (node.right == self.leaf):
            self._remove_if_one_child(node)

    def _remove_if_leaf(self, node):
        parent = node.parent
        if parent.left == node:
            parent.left = self.leaf
        else:
            parent.right = self.leaf

        node = None
        del node

        self.calculate_height(parent)
        self.fix_violation(parent)

    def _remove_if_one_child(self, node):
        parent = node.parent
        if parent.left == node:
            if node.right == self.leaf:
                parent.left = node.left
            else:
                parent.left = node.right
        else:
            if node.right == self.leaf:
                parent.right = node.left
            else:
                parent.right = node.right

        node = None
        del node

        self.calculate_height(parent)
        self.fix_violation(parent)


if __name__ == '__main__':
    bt = AVLTree()

    bt.insert(11)
    bt.insert(-2)
    bt.insert(14)
    bt.insert(-1)
    bt.insert(7)
    bt.insert(15)
    bt.insert(5)
    bt.insert(8)
    bt.insert(4)
    # bt.bt_draw()

    # bt.insert(44)
    # bt.insert(17)
    # bt.insert(78)
    # bt.insert(32)
    # bt.insert(50)
    # bt.insert(88)
    # bt.insert(48)
    # bt.insert(62)
    # bt.insert(84)
    # bt.insert(92)
    # bt.insert(80)
    # bt.insert(82)
    # bt.bt_draw()

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

