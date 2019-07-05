# -*- coding:utf-8 -*-
import sys
import time
import random
import pygame
from pygame.locals import *
from glutsnake.board import BoardManager
from glutsnake.snake import Snake, KEY_DIRECTION_MAP


class Game:

    valid_keys = set()
    valid_keys.update(set(KEY_DIRECTION_MAP.keys()))

    dir_map = {
        0: Snake.MOVE_LEFT,
        1: Snake.MOVE_DOWN,
        2: Snake.MOVE_RIGHT,
        3: Snake.MOVE_UP,
    }

    stop_keys = {ord('p'), ord('P'), ord("h"), ord('H'), ord("enter")}

    exit_keys = {ord("q"), ord("Q"), ord("eas")}
    valid_keys.update(stop_keys)
    valid_keys.update(exit_keys)

    direction_keys = set(KEY_DIRECTION_MAP.keys())

    class EventRes:
        none = "none"
        quit = "quit"
        re_loop = "re_loop"

    class MoveRes:
        none = "none"
        move = "move"

    def __init__(self):
        self.bm = BoardManager(30, 30, 15, 80, 10, "贪吃蛇Python")
        self.snake = Snake(3, 30, 30, self.dir_map.get(random.randint(0, 3)))
        self.total_slice = 10
        self.direction = Snake.MOVE_UP
        self.key_press = False

    def show_speed(self):
        pass

    def show_score(self):
        pass

    def init_game(self, direction):
        self.bm = BoardManager(15, 15, 15, 80, 10, "贪吃蛇Python")
        self.snake = Snake(3, 15, 15, direction)

        print(self.snake.body(), self.snake.head_pos())

        red = (255, 0, 0)
        self.bm.init_board()
        self.bm.show_wall()
        head_pos = self.snake.head_pos()
        self.bm.set_block(head_pos, self.bm.HEAD)

        self.bm.draw_block(*head_pos, red)

        for body in self.snake.body():
            self.bm.set_block(body, self.bm.BODY)
            self.bm.draw_block(*body, red)

        self.bm.gen_food()

    def set_head(self, color=(255, 0, 0)):
        self.bm.set_block(*self.snake.head_pos(), self.bm.HEAD)
        self.bm.draw_block(*self.snake.head_pos(), color=color)

    def set_bodies(self, body, color=(255, 0, 0)):
        for body_pos in body:
            self.bm.set_block(*body_pos, self.bm.BODY)
            self.bm.draw_block(*body_pos, color=color)

    def rm_tail(self):
        tail_pos = self.snake.rm_tail()
        self.bm.set_block(*tail_pos, self.bm.NONE)
        self.bm.draw_block(*tail_pos, (0, 0, 0))

    def stop(self):
        while True:
            for event in pygame.event.get():
                if event.type == QUIT:
                    sys.exit()

                if event.type == KEYDOWN:
                    if event.key in self.exit_keys:
                        sys.exit()
                    if event.key in self.stop_keys:
                        return

    # 结束画面
    def game_over_s(self):
        pass

    # 开始画面
    def game_start_s(self):
        pass

    def wait_start(self):
        """
        等待游戏开始
        :return:
        """
        pass

    def process_move(self, direction):
        red = (255, 0, 0)
        if direction is None:
            return self.snake.NONE

        if self.snake.move(direction) == self.snake.NONE:
            return self.snake.NONE
        time.sleep(self.snake.max_speed)
        head_pos = self.snake.head_pos()
        pos_status = self.bm.get_status(head_pos)
        if pos_status == self.bm.WALL or pos_status == self.bm.BODY:
            """
            等待游戏重新开始
            """
            self.wait_start()

        if pos_status == self.bm.NONE:
            tail_pos = self.snake.rm_tail()
            self.bm.set_block(tail_pos, self.bm.NONE)
            self.bm.draw_block(*tail_pos, (0, 0, 0))
            self.bm.draw_block(*head_pos, red)
            self.bm.set_block(self.snake.head_next_pos(), self.bm.BODY)
            return self.snake.CRAWL

        if pos_status == self.bm.FOOD:
            self.bm.draw_block(*head_pos, red)
            self.bm.gen_food()

        return self.snake.CRAWL

    def process_event(self):
        move = False
        # 先sleep一下

        for event in pygame.event.get():

            # 退出
            if event.type == QUIT:
                return self.EventRes.quit

            # 只接受合法的按键响应
            if event.type not in (KEYDOWN, KEYUP) or event.key not in self.valid_keys:
                continue

            # 方向按键起来
            if event.type == KEYUP and event.key in self.direction_keys:
                self.key_press = False
                continue

            # 如果是退出按键
            if event.key in self.exit_keys:
                return self.EventRes.quit

            # 暂停按键
            if event.key in self.stop_keys:
                self.stop()
                return self.EventRes.re_loop

            # 方向按键
            direction = KEY_DIRECTION_MAP.get(event.key)
            # 无效按键
            if self.process_move(direction) == self.snake.NONE:
                continue

            # 有效按键
            self.direction = direction
            time.sleep(self.snake.speed / self.total_slice)
            move = True
            self.key_press = True

        if self.key_press:
            move = True
            self.process_move(self.direction)
            time.sleep(self.snake.speed / self.total_slice)

        if move:
            return self.EventRes.re_loop
        else:
            time.sleep(self.snake.speed / self.total_slice)
            return self.EventRes.none

    def run_game(self):
        """
        分片sleep可以更及时的响应各种事件
        :return:
        """
        current_slice = 0
        while True:
            while current_slice < self.total_slice:
                es = self.process_event()
                if es == self.EventRes.quit:
                    sys.exit()

                elif es == self.EventRes.re_loop:
                    current_slice = 0
                else:
                    current_slice += 1

            self.process_move(self.direction)


if __name__ == "__main__":
    game = Game()
    game.run_game()



