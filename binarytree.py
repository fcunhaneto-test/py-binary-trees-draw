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

            return self.nodes_dict

        return None

    def recover_nodes_dict(self):
        pass

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
                print('{0}\t{1}\t{2}\t{3}\t{4}'.format(node.key, node.parent.key, node.left.key, node.right.key, node.height))
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

    def search(self, value):
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

    def search_all_childs(self, key, child_list, child_keys):
        if key in self.nodes_dict:
            child_list += self.nodes_dict[key]
            left, right = self.nodes_dict[key]
            _, height = key
            if left:
                if (left, height + 1) in self.nodes_dict:
                    child_keys.append((left, height + 1))
                    return self.search_all_childs((left, height + 1), child_list, child_keys)
            if right:
                if (right, height + 1) in self.nodes_dict:
                    child_keys.append((right, height + 1))
                    return self.search_all_childs((right, height + 1), child_list, child_keys)

            return child_list, child_keys
        else:
            return None, None

    def remove(self, value):
        """
        Remove node where key is equal of given value.
        :param value: numeric
        """
        node = self.search(value)
        if not node:
            return False
        if node == self.root:
            return self._remove_root(node)
        elif node.left == self.leaf and node.right == self.leaf:
            return self._remove_if_leaf(node)
        elif (node.left == self.leaf) ^ (node.right == self.leaf):
            self._remove_if_one_child(node)
        else:
            self._remove_if_two_children(node)

        del node

        return True

    def _remove_if_leaf(self, node):
        if node.parent.left == node:
            node.parent.left = self.leaf
        else:
            node.parent.right = self.leaf

        if node.parent.left.key:
            self.nodes_dict[node.parent.key, node.height] = (node.parent.left.key, None)
        elif node.parent.right.key:
            self.nodes_dict[node.parent.key, node.height] = (None, node.parent.right.key)
        else:
            del self.nodes_dict[node.parent.key, node.height]

        return self.nodes_dict



    def _remove_if_one_child(self, node):
        if node.parent.left == node:
            self._recover_if_rm_one_child(node)

            # tree remove
            if node.right == self.leaf:
                node.parent.left = node.left
                # We have to correct the height of the substitute node
                node.left.height -= 1
            else:
                node.parent.left = node.right
                node.right.height -= 1

        else:
            self._recover_if_rm_one_child(node)

            # tree remove
            if node.right == self.leaf:
                node.parent.right = node.left
                node.left.height -= 1
            else:
                node.parent.right = node.right
                node.right.height -= 1

        node.left.parent = node.parent
        node.right.parent = node.parent

        return self.nodes_dict

    def _remove_if_two_children(self, node):
        successor = self.successor(node.key)

        if successor == node.right:
            self._recovery_if_two_children_case_1(node, successor)
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

    def _remove_root(self, node):
        if node.left == self.leaf and node.right == self.leaf:
            self.root = None
        elif (node.left == self.leaf) ^ (node.right == self.leaf):
            if node.left != self.leaf:
                self.root = node.left
            else:
                self.root = node.right

            self.root.parent = None
        else:
            successor = self.successor(node.key)
            if successor == node.right:

                successor.parent = None
                successor.left = self.root.left
                self.root.left.parent = successor
                self.root = successor
            else:
                if successor.right:
                    successor.right.parent = successor.parent

                successor.parent.left = successor.right
                successor.left = node.left
                successor.right = node.right

                node.left.parent = successor
                node.right.parent = successor
                successor.parent = None
                self.root = successor

    def _recover_if_rm_one_child(self, node):
            # nodes dict recover for tree remove if one child
            _, keys = self.search_all_childs((node.key, node.height + 1), list(), list())

            for key in keys:
                parent, height = key
                x, y = self.nodes_dict[key]
                del self.nodes_dict[key]
                self.nodes_dict[(parent, height-1)] = [x, y]

                # The heights of the children of the substitute node are correct in the dictionary but we have to
                # correct them within the node objects.
                if x:
                    n = self.search(x)
                    n.height -= 1
                if y:
                    n = self.search(y)
                    n.height -= 1

            ch_left, ch_right = self.nodes_dict[(node.key, node.height + 1)]
            if ch_left:
                change = ch_left
            else:
                change = ch_right
            left, right = self.nodes_dict[(node.parent.key, node.height)]
            if left == node.key:
                self.nodes_dict[(node.parent.key, node.height)] = [change, right]

            else:
                self.nodes_dict[(node.parent.key, node.height)] = [left, change]

            del self.nodes_dict[node.key, node.height + 1]
            self.arrange_nodes_dict()

    def _recovery_if_two_children_case_1(self, node, successor):
        children, keys = self.search_all_childs((node.key, node.height + 1), list(), list())

        # for child in children:
        #     if child:
        #         change = self.search_node(child)
        #         change.height -= 1

        if keys:
            for key in keys:
                parent, height = key
                x, y = self.nodes_dict[key]
                del self.nodes_dict[key]
                self.nodes_dict[(parent, height - 1)] = [x, y]

                # The heights of the children of the substitute node are correct in the dictionary but we have to
                # correct them within the node objects.
                if x:
                    n = self.search(x)
                    n.height -= 1
                if y:
                    n = self.search(y)
                    n.height -= 1

        if node == node.parent.left:
            self.nodes_dict[(node.parent.key, node.height)] = [successor.key, node.parent.right.key]
        else:
            self.nodes_dict[(node.parent.key, node.height)] = [node.parent.left.key, successor.key]
        self.nodes_dict[successor.key, successor.height] = [node.left.key, successor.right.key]
        successor.height -= 1
        del self.nodes_dict[(node.key, node.height + 1)]

        # print('recovery:', self.nodes_dict)
        self.arrange_nodes_dict()

    def arrange_nodes_dict(self):
        aux1 = sorted(self.nodes_dict.keys(), key=lambda key: key[1])
        aux2 = {}
        for key in aux1:
            aux2[key] = self.nodes_dict[key]
        self.nodes_dict = aux2

    def clear_tree(self, node):
        pass


if __name__ == '__main__':
    bt = BinaryTree()
    print('node\tparent\tleft\tright\theight\tfb')
    print('***********************************************')
    bt.insert(50)
    bt.insert(25)
    bt.insert(75)
    bt.insert(15)
    bt.insert(80)
    bt.insert(78)
    bt.insert(40)
    bt.insert(45)
    bt.walk_in_order()
    print('***********************************************')
    print(bt.nodes_dict)
    print('***********************************************')
    suc = bt.successor(25)
    print(suc.key)
    bt.remove(25)
    print('node\tparent\tleft\tright\theight\tfb')
    print('***********************************************')
    bt.walk_in_order()
    print('***********************************************')
    print(bt.nodes_dict)
    print('***********************************************')
