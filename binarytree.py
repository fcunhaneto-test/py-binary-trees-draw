#!/home/francisco/Projects/Pycharm/py-binary-trees-draw/venv/bin/python

from node import Node


class BinaryTree:
    def __init__(self):
        self.root = None
        self.leaf = Node(None)
        self.nodes_dict = {}

    def insert(self, key):
        """
        Insert key values in tree.
        :param key:
        :return: self.nodes_dict a dict where keys are tuple (parent, height) and values are the children.
        """
        node = Node(key)
        node.left = self.leaf
        node.right = self.leaf

        if not self.root:
            self.root = node
        else:
            current = self.root
            parent = current
            while current != self.leaf:
                parent = current
                node.height += 1
                if node.key < current.key:
                    current = current.left
                elif node.key > current.key:
                    current = current.right
                else:
                    return False

            node.parent = parent

            if not ((node.parent.key, node.height) in self.nodes_dict):
                self.nodes_dict[(node.parent.key, node.height)] = [None, None]

            if node.key < parent.key:
                parent.left = node
                self.nodes_dict[(node.parent.key, node.height)][0] = node.key
            else:
                parent.right = node
                self.nodes_dict[(node.parent.key, node.height)][1] = node.key

    def walk_in_order(self, node=None):
        """
        Walking tree in pre-order.
        :param node: node object.
        """
        if not node:
            node = self.root

        if node != self.leaf:

            self.walk_in_order(node.left)
            if node.parent:
                print('{0}\t{1}\t{2}\t{3}\t{4}'.format(node.key, node.parent.key, node.left.key, node.right.key,
                                                       node.height))
            else:
                print('{0}\t{1}\t{2}\t{3}\t{4}'.format(node.key, None, node.left.key, node.right.key, node.height))
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
                print('{0}\t{1}\t{2}\t{3}'.format(node.key, node.parent.key, node.left.key, node.right.key))
            else:
                print('{0}\t{1}\t{2}\t{3}'.format(node.key, None, node.left.key, node.right.key))
            self.walk_pos_order(node.left)

    def search_node(self, value):
        """
        Search the node object that key is equal for given value.
        :param value: numeric.
        :return: node object.
                """
        current = self.root
        if value == current.key:
            return self.root

        while value != current.key and current != self.leaf:
            if current.key > value:
                current = current.left
            else:
                current = current.right

        if current == self.leaf:
            return False

        return current

    def search_children(self, node, children_list, flag=False):

        if node != self.leaf:
            self.search_children(node.right, children_list, True)
            if flag:
                children_list.append(node)
            self.search_children(node.left, children_list, True)

        return children_list

    def minimum(self, node=None):
        """
        Search the minimum key in subtree that start from given node.
        :param node:
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
        :param node:
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
        current = self.search_node(value)
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
        current = self.search_node(value)
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
        node = self.search_node(value)
        if not node:
            return False
        if node == self.root:
            return self._remove_root()
        elif node.left == self.leaf and node.right == self.leaf:
            return self._remove_if_leaf(node)
        elif (node.left == self.leaf) ^ (node.right == self.leaf):
            return self._remove_if_one_child(node)
        else:
            return self._remove_if_two_children(node)

    def _remove_if_leaf(self, node):
        remove_key = node.key
        if node.parent.left == node:
            node.parent.left = self.leaf
        else:
            node.parent.right = self.leaf

        if node.parent.left.key:
            self.nodes_dict[node.parent.key, node.height] = [node.parent.left.key, None]
        elif node.parent.right.key:
            self.nodes_dict[node.parent.key, node.height] = [None, node.parent.right.key]
        else:
            del self.nodes_dict[node.parent.key, node.height]

        del node

        return remove_key, None

    def _remove_if_one_child(self, node):
        remove_key = node.key
        self._recovery_children_height(node)

        left, right = self.nodes_dict[(node.parent.key, node.height)]

        # replace the node with your child
        # reset node key by new key in nodes dict
        if node.parent.left == node:
            # tree remove
            if node.right == self.leaf:
                node.parent.left = node.left
                self.nodes_dict[(node.parent.key, node.height)] = [node.left.key, right]
            else:
                node.parent.left = node.right
                self.nodes_dict[(node.parent.key, node.height)] = [node.right.key, right]
        else:
            # tree remove
            if node.right == self.leaf:
                node.parent.right = node.left
                self.nodes_dict[(node.parent.key, node.height)] = [left, node.left.key]
            else:
                node.parent.right = node.right
                self.nodes_dict[(node.parent.key, node.height)] = [left, node.right.key]

        node.left.parent = node.parent
        node.right.parent = node.parent

        del node

        self.arrange_nodes_dict()

        return remove_key, None

    def _remove_if_two_children(self, node):
        remove_key = node.key
        successor = self.successor(node.key)

        if successor == node.right:  # case 1
            self._recover_nd_rm_two_children_case1(node, successor)
            if node == node.parent.left:
                node.parent.left = successor
            else:
                node.parent.right = successor

            successor.parent = node.parent
            successor.left = node.left
            successor.left.parent = successor
        else:  # case 2
            self._recover_nd_rm_two_children_case2(node, successor)
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
        if self.root.left == self.leaf and self.root.right == self.leaf:
            self.root = None
            self.nodes_dict = {}

            return remove_key, None
        elif (self.root.left == self.leaf) ^ (self.root.right == self.leaf):
            self._recovery_children_height(self.root)
            self.arrange_nodes_dict()
            if self.root.left != self.leaf:
                self.root = self.root.left
            else:
                self.root = self.root.right

            self.root.parent = None

            return remove_key, None
        else:
            successor = self.successor(self.root.key)
            if successor == self.root.right:
                self._recover_nd_rm_two_ch_case1_root(successor)
                successor.parent = None
                successor.left = self.root.left
                self.root.left.parent = successor
                self.root = successor
            else:
                self._recover_nd_rm_two_ch_case2_root(successor)
                if successor.right:
                    successor.right.parent = successor.parent

                successor.parent.left = successor.right
                successor.left = self.root.left
                successor.right = self.root.right

                self.root.left.parent = successor
                self.root.right.parent = successor
                successor.parent = None
                self.root = successor

            return remove_key, successor.key

    def _recover_nd_rm_two_children_case1(self, node, successor):
        left, right = self.nodes_dict[(node.parent.key, node.height)]
        if node == node.parent.left:
            self.nodes_dict[(node.parent.key, node.height)] = [successor.key, right]
        else:
            self.nodes_dict[(node.parent.key, node.height)] = [left, successor.key]

        # in nodes we have to del where remove node is key
        del self.nodes_dict[(node.key, node.height + 1)]

        # in nodes dict we have to recreate where successor is key and delete the old key
        # but we have to test if successor is a leaf when that key don't exist
        if (successor.key, successor.height + 1) in self.nodes_dict:
            del self.nodes_dict[(successor.key, successor.height + 1)]
            self.nodes_dict[(successor.key, node.height + 1)] = [node.left.key, successor.right.key]
        elif node.left != self.leaf:
            self.nodes_dict[(successor.key, node.height + 1)] = [node.left.key, None]

        # reset node class heights
        successor.height -= 1

        self._recovery_children_height(successor)

        self.arrange_nodes_dict()

    def _recover_nd_rm_two_children_case2(self, node, successor):
        left, right = self.nodes_dict[(node.parent.key, node.height)]
        if node == node.parent.left:
            self.nodes_dict[(node.parent.key, node.height)] = [successor.key, right]
        else:
            self.nodes_dict[(node.parent.key, node.height)] = [left, successor.key]

        self.nodes_dict[(successor.key, node.height + 1)] = [node.left.key, node.right.key]
        del self.nodes_dict[(node.key, node.height + 1)]

        if successor.right != self.leaf and successor.parent.right != self.leaf:
            self.nodes_dict[(successor.parent.key, successor.height)] = [successor.right.key,
                                                                         successor.parent.right.key]
        elif successor.right != self.leaf and successor.parent.right == self.leaf:
            self.nodes_dict[(successor.parent.key, successor.height)] = [successor.right.key, None]
        elif successor.right == self.leaf and successor.parent.right != self.leaf:
            self.nodes_dict[(successor.parent.key, successor.height)] = [None, successor.parent.right.key]
        else:
            del self.nodes_dict[(successor.parent.key, successor.height)]

        # the successor replaces the node so it receives the height of the node
        successor.height = node.height

        self._recovery_children_height(successor)

        self.arrange_nodes_dict()

    def _recover_nd_rm_two_ch_case1_root(self, successor):
        right = successor.right
        left = self.root.left

        if left != self.leaf and right != self.leaf:
            self.nodes_dict[(successor.key, 1)] = [left.key, right.key]
        elif left != self.leaf and right == self.leaf:
            self.nodes_dict[(successor.key, 1)] = [left.key, None]
        elif left == self.leaf and right != self.leaf:
            self.nodes_dict[(successor.parent.key, successor.height)] = [None, successor.right.key]
        else:
            self.nodes_dict[(successor.key, 1)] = [None, None]

        del self.nodes_dict[self.root.key, 1]

        successor.height -= 1

        self._recovery_children_height(successor)

        self.arrange_nodes_dict()

    def _recover_nd_rm_two_ch_case2_root(self, successor):
        left, right = self.nodes_dict[self.root.key, 1]
        if self.root.left != self.leaf:
            self.nodes_dict[(successor.key, 1)] = [left, self.root.right.key]
        else:
            self.nodes_dict[(successor.key, 1)] = [None, self.root.right.key]

        if successor.right != self.leaf and successor.parent.right != self.leaf:
            self.nodes_dict[(successor.parent.key, successor.height)] = [successor.right.key,
                                                                         successor.parent.right.key]
        elif successor.right != self.leaf and successor.parent.right == self.leaf:
            self.nodes_dict[(successor.parent.key, successor.height)] = [successor.right.key, None]
        elif successor.right == self.leaf and successor.parent.right != self.leaf:
            self.nodes_dict[(successor.parent.key, successor.height)] = [None, successor.parent.right.key]
        else:
            del self.nodes_dict[(successor.parent.key, successor.height)]

        del self.nodes_dict[self.root.key, 1]

        successor.height -= 1

        self._recovery_children_height(successor)

        self.arrange_nodes_dict()

    def _recovery_children_height(self, node):
        children = self.search_children(node, list())
        keys = set()

        for child in children:
            # create a key set with children of node
            # we have do to this before we reset node key by new key in nodes dict
            if (child.parent.key, child.height) in self.nodes_dict:
                keys.add((child.parent.key, child.height))
            # reset the height in node class
            child.height -= 1

        # reset keys for children of node by new keys with new heights
        for key in keys:
            node_key, height = key
            if node_key == node.key:
                del self.nodes_dict[key]
            else:
                left, right = self.nodes_dict[key]
                del self.nodes_dict[key]
                self.nodes_dict[(node_key, height - 1)] = [left, right]

    def arrange_nodes_dict(self):
        aux1 = sorted(self.nodes_dict.keys(), key=lambda key: key[1])
        aux2 = {}
        for key in aux1:
            aux2[key] = self.nodes_dict[key]
        self.nodes_dict = aux2


if __name__ == '__main__':
    bt = BinaryTree()
    print('node\tparent\tleft\tright\theight\tfb')
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
    # print('***********************************************')
    # print(bt.nodes_dict)
    # print('***********************************************')
    # bt.remove(50)
    # print('***********************************************')
    # print('node\tparent\tleft\tright\theight\tfb')
    # print('***********************************************')
    # bt.walk_in_order()
    # print('***********************************************')
    # print(bt.nodes_dict)
    # print('***********************************************')
