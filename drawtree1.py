#!/home/francisco/Projects/Pycharm/py-draw-binary-trees/venv/bin/python
# -*- coding: utf-8 -*-

import os
import pygame
import binarytree
import avltree


class DrawTree:
    def __init__(self):
        pygame.init()

        self.key_dict = {256: '0', 48: '0', 257: '1', 49: '1', 258: '2', 50: '2', 259: '3', 51: '3', 260: '4', 52: '4',
                         261: '5', 53: '5', 262: '6', 54: '6', 263: '7', 55: '7', 264: '8', 56: '8', 265: '9', 57: '9',
                         266: '.', 46: '.',
                         97: 'a', 98: 'b', 99: 'c', 100: 'd', 101: 'e', 102: 'f', 103: 'g', 104: 'h', 105: 'i', 106: 'j',
                         107: 'k', 108: 'l', 109: 'm', 110: 'n', 111: 'o', 112: 'p', 113: 'q', 114: 'r', 115: 's',
                         116: 't', 117: 'u', 118: 'v', 119: 'w', 120: 'x', 121: 'y', 122: 'z',
                         65: 'A', 66: 'B', 67: 'C', 68: 'D', 69: 'E', 70: 'F', 71: 'G', 72: 'H', 73: 'I', 74: 'J',
                         75: 'K', 76: 'L', 77: 'M', 78: 'N', 79: 'O', 80: 'P', 81: 'Q', 82: 'R', 83: 'S', 84: 'T',
                         85: 'U', 86: 'V', 87: 'W', 88: 'X', 89: 'Y', 90: 'Z',
                         } # 32: 'space', 27: 'esc', 273: 'up', 274: 'down', 276: 'left', 275: 'right'

        self.BLACK = (0, 0, 0)
        self.WHITE = (255, 255, 255)
        self.RED = (255, 0, 0)
        self.BLUE = (0, 0, 255)

        self.RADIUS = 25

        # Define windows size
        self.window_x = 1024
        self.window_y = 768

        self.y_factor = 100
        self.x_factor = None

        windowInfo = pygame.display.Info()
        monitorWidth = windowInfo.current_w
        monitorHeight = windowInfo.current_h
        os.environ['SDL_VIDEO_WINDOW_POS'] = "%d,%d" % ((monitorWidth - self.window_x) / 2, (monitorHeight - self.window_y) / 2)

        self.screen = pygame.display.set_mode((self.window_x, self.window_y), 0, 32)
        pygame.display.set_caption("Draw Tree")

        self.font_1 = pygame.font.SysFont('Arial', 16, True, False)
        self.font_2 = pygame.font.SysFont('Arial', 12, True, False)

        self.points_dict = {}
        self.lines_dict = {}

        self.bt = None

        self.nodes_dict = {}
        self.value_list = []
        self.enter_value = ""

        self.draw_tree()

    def draw_input(self):
        pygame.draw.rect(self.screen, self.BLACK, [5, 5, 60, 30], 1)
        pygame.draw.rect(self.screen, self.BLACK, [70, 5, 150, 30], 1)

        text_1 = self.font_1.render('value:', True, self.BLACK)
        self.screen.blit(text_1, [10, 12])

        text_2 = self.font_1.render(str(self.enter_value), True, self.BLACK)

        self.screen.blit(text_2, [75, 12])

    def type_is_numeric(self, num):
        if num.isnumeric():
            value = int(self.enter_value)
            return value
        else:
            try:
                value = float(self.enter_value)
                return value
            except ValueError:
                return False

    def make_points_lines(self, value):
        self.nodes_dict = self.bt.insert(value)

        if not self.nodes_dict:
            x_division_center = int(2 / 2)
            division_pixel = int(self.window_x / 3)
            division_pixel_center = int(division_pixel / 2)

            root_x = (x_division_center * division_pixel) + division_pixel_center
            root_y = 0

            self.points_dict[self.bt.root.key] = (root_x, root_y + self.RADIUS)
        else:
            _, tree_height = max(self.nodes_dict.keys(), key=lambda x: x[1])


            leaf_num = 2 ** tree_height
            division = leaf_num + 1
            x_division_center = int(leaf_num / 2)
            division_pixel = int(self.window_x / division)
            division_pixel_center = int(division_pixel / 2)

            root_x = (x_division_center * division_pixel) + division_pixel_center
            root_y = 0

            self.points_dict[self.bt.root.key] = (root_x, root_y + self.RADIUS)

            lines = {}
            for node in self.nodes_dict:
                parent, height = node
                left, right = self.nodes_dict[node]
                parent_x, parent_y = self.points_dict[parent]
                if left:
                    x = abs(parent_x - int(root_x / (2**height)))
                    y = self.y_factor * height
                    self.points_dict[left] = (x, y)
                    line = [(parent_x, parent_y + self.RADIUS), (x, y - self.RADIUS)]
                    lines[(parent, left)] = line
                if right:
                    x = abs(parent_x + int(root_x / (2 ** height)))
                    y = self.y_factor * height
                    self.points_dict[right] = (x, y)
                    line = [(parent_x, parent_y + self.RADIUS), (x, y - self.RADIUS)]
                    lines[(parent, right)] = line

                self.lines_dict = lines

    def draw_nodes(self):
        if self.points_dict:
            for node in self.points_dict:
                x, y = self.points_dict[node]

                text = self.font_2.render(str(node), True, self.BLACK)
                _, _, font_x, font_y = text.get_rect()
                font_x_delta = int(font_x - (self.RADIUS / 4))
                font_y_delta = int(font_y - (self.RADIUS / 4))

                pygame.draw.circle(self.screen, self.RED, (x, y), self.RADIUS, 2)
                self.screen.blit(text, [x - font_x_delta, y - font_y_delta])

            for line in self.lines_dict:
                line_points = self.lines_dict[line]

                x, y = line_points[0]
                r, s = line_points[1]

                pygame.draw.aaline(self.screen, self.BLACK, [x, y], [r, s], 2)

    def draw_tree(self):
        clock = pygame.time.Clock()

        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    exit()
                if event.type == pygame.KEYUP:
                    if (256 <= event.key <= 266) or (48 <= event.key <= 57) or event == 46:
                        pressed = self.key_dict[event.key]
                        self.enter_value += pressed
                    elif (97 <= event.key <= 122) or (65 <= event.key <= 90):
                        pressed = str.lower(self.key_dict[event.key])
                        self.enter_value += pressed
                        print(self.enter_value)
                    elif event.key == 13 or event.key == 271:
                        value = self.type_is_numeric(self.enter_value)
                        if value:
                            self.make_points_lines(value)
                            self.value_list.append(self.enter_value)
                        else:
                            if self.enter_value == 'bin':
                                self.bt = binarytree.BinaryTree()
                            elif self.enter_value == 'avl':
                                self.bt = avltree.AVLTree()
                        self.enter_value = ""
                    elif event.key == 27:
                        pygame.quit()
                        exit()
                    elif event.key == 8:
                        if self.enter_value:
                            x = len(self.enter_value)
                            self.enter_value = self.enter_value[0:x - 1]

            self.screen.fill(self.WHITE)

            self.draw_input()

            self.draw_nodes()

            clock.tick(30)

            pygame.display.update()


if __name__ == '__main__':
    DrawTree()