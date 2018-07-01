#!/home/francisco/Projects/Pycharm/py-binary-trees-draw/venv/bin/python
# -*- coding: utf-8 -*-


import sys
import os
dir_module = os.path.dirname(os.path.abspath(__file__))
dir_module, _ = dir_module.rsplit('/', 1)
sys.path.extend([dir_module])

import binarytree
import avltree
import uteis


def handle_trees(bt=None):
    uteis.clear()
    if not bt:
        print('***************************')
        print('1 - Create binary tree')
        print('2 - Create avl tree')
        print('0 - Exit')
        print('***************************')

        op = input('Enter the option: ')
        try:
            op = int(op)
        except TypeError:
            print('Invalid option.')
            input('Press enter to return for options.\n')
            handle_trees()

        if op == 1:
            bt = binarytree.BinaryTree()
        elif op == 2:
            bt = avltree.AVLTree()
        elif op == 0:
            exit(0)
        else:
            print('Invalid option.')
            input('Press enter to continue.')
            handle_trees()

    uteis.clear()
    while op != 0:
        print('Options:')
        print('***************************')
        print('1 - Enter nodes')
        print('2 - Walk in order')
        print('3 - Walk pos order')
        print('4 - Remove node')
        print('5 - Successor')
        print('6 - Predecessor')
        print('7 - cls tree')
        print('0 - Exit')
        print('***************************')
        print()
        op = input('Enter the option: ')
        try:
            op = int(op)
        except TypeError:
            print('Invalid option.')
            input('Press enter to return for options.\n')
            handle_trees()

        uteis.clear()

        if op == 1:
            print('Enter the nodes (enter none to end):')
            print('*********************************************')
            key = input('node: ')
            while key:
                key = int(key)
                bt.insert(key)
                key = input('node: ')
            print('*********************************************\n')
        elif op == 2:
            print('Walk In Order:')
            print('node\tparent\tleft\tright\theight\tfb')
            print('***********************************************')
            bt.walk_in_order()
            print('***********************************************\n')
        elif op == 3:
            print('Walk In Order:')
            print('node\tparent\tleft\tright\theight\tfb')
            print('***********************************************')
            bt.walk_pos_order()
            print('***********************************************\n')
        elif op == 4:
            print('***********************************************')
            key = int(input("To remove node enter it's key: "))
            if bt.remove(key):
                print('Successfully removed {0}'.format(key))
            else:
                print('Failed to remove {0}. Make sure it exists on the tree'.format(key))
            print('***********************************************\n')
        elif op == 5:
            print('*********************************************************')
            key = int(input("Enter the key of the node you want the successor: "))
            successor = bt.successor(key)
            if successor:
                print('Sucessor is: {0}'.format(successor.key))
            else:
                print('Not found.')
            print('*********************************************************')
        elif op == 6:
            print('*********************************************************')
            key = int(input("Enter the key of the node you want the predecessor: "))
            predecessor = bt.predecessor(key)
            if predecessor:
                print('Predecessor is: {0}'.format(predecessor.key))
            else:
                print('Not found.')
                print('*********************************************************')
        elif op == 7:
            del bt
            handle_trees()
        elif op == 0:
            return bt
        else:
            print('Invalid option.')
            input('Press enter to return for options.\n')


if __name__ == '__main__':
    handle_trees()