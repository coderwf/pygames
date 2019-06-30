# -*- coding:utf-8 -*-

import sys
import pygame
import random
from pygame.locals import *
from glutsnake.board import BoardManager
from glutsnake.snake import Snake, KEY_DIRECTION_MAP


def run_game():
    init_move = {
        1: Snake.MOVE_RIGHT,
        2: Snake.MOVE_UP,
        3: Snake.MOVE_DOWN,
        4: Snake.MOVE_LEFT,
    }

    bm = BoardManager(30, 30, 15, 10, 100, "贪吃蛇python")
    bm.init_board()
    bm.show_pods()
    red = (255, 0, 0)
    direction = init_move.get(random.randint(1, 4))
    snake = Snake(3, 25, 25, direction)
    head_pos = snake.head_pos()
    bm.draw_block(*head_pos, red)
    body_poses = snake.body()
    for body_pos in body_poses:
        bm.draw_block(*body_pos, red)

    while True:
        for event in pygame.event.get():
            if event.type == QUIT:
                sys.exit()

            if event.type == KEYDOWN:
                direction = KEY_DIRECTION_MAP.get(event.key)
                status = snake.move(direction)

                if status == Snake.NONE:
                    continue

                head_pos = snake.head_pos()
                bm.draw_block(*head_pos, red)
                bm.draw_block(*snake.tail_pos(), (0, 0, 0))
                snake.rm_tail()

if __name__ == "__main__":
    run_game()
