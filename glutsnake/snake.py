# -*- coding:utf-8 -*-
import random


class Snake:
    MOVE_UP = 0
    MOVE_LEFT = 1
    MOVE_RIGHT = 2
    MOVE_DOWN = 3

    NONE = 11
    CRAWL = 12

    def __init__(self, init_len, x_blocks, y_blocks, direction):
        self.sections = []

        self.move_funcs = {
            self.MOVE_DOWN: self.move_down,
            self.MOVE_LEFT: self.move_left,
            self.MOVE_RIGHT: self.move_right,
            self.MOVE_UP: self.move_up,
        }
        self.x_blocks = x_blocks
        self.y_blocks = y_blocks

        self.init(init_len, x_blocks, y_blocks, direction)

    def set_food_pos(self, x, y):
        assert 0 <= x < self.x_blocks
        assert 0 <= y < self.y_blocks

    def init(self, init_len, x_blocks, y_blocks, direction):
        assert init_len > 1
        assert x_blocks > init_len + 1
        assert y_blocks > init_len + 1

        if direction == self.MOVE_UP:
            x_add = 0
            y_add = 1
            head_x_range = (0, x_blocks - 1)
            head_y_range = (2, y_blocks - init_len)

        elif direction == self.MOVE_DOWN:
            x_add = 0
            y_add = -1
            head_x_range = (0, x_blocks - 1)
            head_y_range = (init_len - 1, y_blocks - 2)

        elif direction == self.MOVE_RIGHT:
            x_add = -1
            y_add = 0
            head_x_range = (init_len - 1, x_blocks - 2)
            head_y_range = (0, y_blocks - 1)

        else:
            x_add = 1
            y_add = 0
            head_x_range = (2, x_blocks - init_len)
            head_y_range = (0, y_blocks - 1)

        head_x, head_y = random.randint(*head_x_range), random.randint(*head_y_range)
        self.sections = [(head_x, head_y)]
        for _ in range(1, init_len):
            x, y = head_x + x_add, head_y + y_add
            self.sections.append((x, y))
            head_x, head_y = x, y

    def head_pos(self):
        assert len(self.sections) > 0
        return self.sections[0]

    def head_next_pos(self):
        assert len(self.sections) > 1
        return self.sections[1]

    def tail_pos(self):
        assert len(self.sections) > 1
        return self.sections[-1]

    def rm_tail(self):
        assert len(self.sections) > 1
        return self.sections.pop()

    def body(self):
        assert len(self.sections) > 1
        return self.sections[1:]

    def move_down(self):
        head_pos_x, head_pos_y = self.sections[0]
        next_sec_x, next_sec_y = self.sections[1]
        if head_pos_y + 1 == next_sec_y:
            return self.NONE
        new_head_x, new_head_y = head_pos_x, head_pos_y + 1
        self.sections.insert(0, (new_head_x, new_head_y))
        return self.CRAWL

    def move_up(self):
        head_pos_x, head_pos_y = self.sections[0]
        next_sec_x, next_sec_y = self.sections[1]
        if head_pos_y - 1 == next_sec_y:
            return self.NONE
        new_head_x, new_head_y = head_pos_x, head_pos_y - 1
        self.sections.insert(0, (new_head_x, new_head_y))
        return self.CRAWL

    def move_right(self, ):
        head_pos_x, head_pos_y = self.sections[0]
        next_sec_x, next_sec_y = self.sections[1]
        if head_pos_x + 1 == next_sec_x:
            return self.NONE
        new_head_x, new_head_y = head_pos_x + 1, head_pos_y
        self.sections.insert(0, (new_head_x, new_head_y))
        return self.CRAWL

    def move_left(self):
        head_pos_x, head_pos_y = self.sections[0]
        next_sec_x, next_sec_y = self.sections[1]
        if head_pos_x - 1 == next_sec_x:
            return self.NONE
        new_head_x, new_head_y = head_pos_x - 1, head_pos_y
        self.sections.insert(0, (new_head_x, new_head_y))
        return self.CRAWL

    def move(self, direction):
        assert len(self.sections) > 1
        move_func = self.move_funcs.get(direction)
        if move_func is None:
            return self.NONE
        return move_func()


KEY_DIRECTION_MAP = {
    ord('w'): Snake.MOVE_UP,
    ord('W'): Snake.MOVE_UP,
    273: Snake.MOVE_UP,

    ord('a'): Snake.MOVE_LEFT,
    ord('A'): Snake.MOVE_LEFT,
    276: Snake.MOVE_LEFT,

    ord('d'): Snake.MOVE_RIGHT,
    ord('D'): Snake.MOVE_RIGHT,
    275: Snake.MOVE_RIGHT,

    ord('s'): Snake.MOVE_DOWN,
    ord('S'): Snake.MOVE_DOWN,
    274: Snake.MOVE_DOWN,
}
