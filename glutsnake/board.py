# -*- coding:utf-8 -*-
import random
import pygame


class BoardManager:
    WALL = 0
    FOOD = 1
    NONE = 2
    HEAD = 3
    BODY = 4

    def __init__(self, x_blocks, y_blocks, block_width, origin_x, origin_y, caption):
        self.x_blocks = x_blocks
        self.y_blocks = y_blocks
        # NONE的方块
        self.non_blocks = None
        self.total_len = x_blocks * y_blocks
        self.blocks_status = None
        self.block_width = block_width
        self.screen = None
        self.origin_x = origin_x
        self.origin_y = origin_y
        self.caption = caption

    def init_board(self, bg_color=(0, 0, 0), caption=None):
        pygame.init()
        pygame.display.set_caption(caption or self.caption)
        board_x, board_y = self.x_blocks * (1 + self.block_width) + \
                           2 * self.origin_x, (self.y_blocks + 1) * (self.block_width + 1) + self.origin_y
        self.screen = pygame.display.set_mode((board_x, board_y), 0, 32)
        self.blocks_status = [[self.NONE for _ in range(self.y_blocks)] for _ in range(self.x_blocks)]
        self.non_blocks = self._gen_non_blocks()
        pygame.display.update()
        self.set_bg_color(bg_color)

    def set_bg_color(self, color=(0, 0, 0)):
        self.screen.fill(color)
        pygame.display.update()

    def _gen_non_blocks(self):
        non_blocks = []
        for i in range(0, self.x_blocks):
            for j in range(0, self.y_blocks):
                non_blocks.append((i, j))
        return non_blocks

    # 显示网格线
    def show_pods(self, color=(255, 255, 255)):
        start_pos_x, start_pos_y = self.origin_x, self.origin_y
        end_pos_x, end_pos_y = self.origin_x, (self.block_width + 1) * self.y_blocks + self.origin_y
        # 先画竖线
        for c_index in range(0, self.x_blocks + 1):
            pygame.draw.line(self.screen, color, (start_pos_x, start_pos_y), (end_pos_x, end_pos_y), 1)
            start_pos_x = end_pos_x = start_pos_x + 1 + self.block_width

        start_pos_x, start_pos_y = self.origin_x, self.origin_y
        end_pos_x, end_pos_y = self.origin_x + (self.block_width + 1) * self.x_blocks, self.origin_y

        # 画横线
        for r_index in range(0, self.y_blocks + 1):
            pygame.draw.line(self.screen, color, (start_pos_x, start_pos_y), (end_pos_x, end_pos_y), 1)
            start_pos_y = end_pos_y = start_pos_y + 1 + self.block_width

        pygame.display.flip()

    def draw_block(self, x, y, color=(111, 111, 111)):
        pos_x = self.origin_x + x * (self.block_width + 1) + 1
        pos_y = self.origin_y + y * (self.block_width + 1) + 1
        pygame.draw.rect(self.screen, color, (pos_x, pos_y, self.block_width, self.block_width), 0)
        pygame.display.update((pos_x, pos_y, self.block_width, self.block_width))

    def set_block(self, x, y, status):
        self.blocks_status[x][y] = status
        if status == self.NONE:
            self.non_blocks.append((x, y))
        else:
            self.non_blocks.remove((x, y))

    def get_status(self, x, y):
        return self.blocks_status[x][y]

    def gen_food(self, color = ()):
        index = random.randint(0, len(self.non_blocks) - 1)
        block_pos = self.non_blocks[index]
        rect = (self.block_width * block_pos[0], self.block_width * block_pos[1],
                self.block_width, self.block_width)
        pygame.draw.rect(self.screen, (44, 44, 44), rect, 0)
        pygame.display.update(rect)
