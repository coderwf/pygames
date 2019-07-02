# -*- coding:utf-8 -*-
import sys
import time
import random
import pygame
from pygame.locals import *
from glutsnake.board import BoardManager
from glutsnake.snake import Snake, KEY_DIRECTION_MAP


class Game:
    dir_map = {
        0: Snake.MOVE_LEFT,
        1: Snake.MOVE_DOWN,
        2: Snake.MOVE_RIGHT,
        3: Snake.MOVE_UP,
    }

    stop_key = {ord('p'), ord('P'), ord("h"), ord('H')}

    def __init__(self):
        self.bm = BoardManager(30, 30, 15, 80, 10, "贪吃蛇Python")
        self.snake = Snake(3, 30, 30, self.dir_map.get(random.randint(0, 3)))

    def init_game(self, direction):
        self.bm = BoardManager(30, 30, 15, 80, 10, "贪吃蛇Python")
        self.snake = Snake(3, 30, 30, self.dir_map.get(random.randint(0, 3)))
        self.snake = Snake(3, 30, 30, direction)

        red = (255, 0, 0)
        self.bm.init_board()
        self.bm.show_pods()
        head_pos = self.snake.head_pos()
        self.bm.set_block(head_pos, self.bm.HEAD)
        self.bm.draw_block(*head_pos, red)

        for body in self.snake.body():
            self.bm.set_block(body, self.bm.BODY)
            self.bm.draw_block(*body, red)

        self.bm.gen_food()

    def set_head(self, head_pos, color=(255, 0, 0)):
        pass

    def set_bodies(self, body, color=(255, 0, 0)):
        pass

    def rm_tail(self, tail_pos):
        pass

    def stop(self):
        pass

    def process_move(self, direction):
        red = (255, 0, 0)
        if direction is None:
            return

        if self.snake.move(direction) == self.snake.NONE:
            return

        head_pos = self.snake.head_pos()
        pos_status = self.bm.get_status(head_pos)
        if pos_status == self.bm.WALL or pos_status == self.bm.BODY:
            sys.exit()

        if pos_status == self.bm.NONE:
            tail_pos = self.snake.rm_tail()
            self.bm.set_block(tail_pos, self.bm.NONE)
            self.bm.draw_block(*tail_pos, (0, 0, 0))
            self.bm.draw_block(*head_pos, red)
            self.bm.set_block(self.snake.head_next_pos(), self.bm.BODY)
            return

        if pos_status == self.bm.FOOD:
            self.bm.draw_block(*head_pos, red)
            self.bm.gen_food()

    def run_game(self):
        direction = self.dir_map.get(random.randint(0, 3))
        self.init_game(direction)

        key_press = False

        while True:
            for event in pygame.event.get():
                if event.type == QUIT:
                    sys.exit()

                if event.type == KEYUP:
                    key_press = False

                if event.type == KEYDOWN:
                    if event.key in self.stop_key:
                        self.stop()

                    direction = KEY_DIRECTION_MAP.get(event.key)
                    self.process_move(direction)
                    key_press = True

            self.process_move(direction)

            if key_press:
                time.sleep(0.1)
            else:
                time.sleep(0.5)


if __name__ == "__main__":
    game = Game()
    game.run_game()



