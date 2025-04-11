# -*- coding: utf-8 -*-
""" タイピングゲーム """

import random
import sys

import pygame


def select_word():
    """ 単語帳からランダムに単語を選ぶ """
    word_list = [
        'apple',
        'banana',
        'cherry',
        'melon',
        'orange'
    ]

    num_of_elements = len(word_list)
    i = random.randint(0, num_of_elements - 1)
    return word_list[i]


def cut_head_char(word):
    """ 文字列の先頭を削除する """
    return word[1:]


def is_empty_word(word):
    """ 単語が空かチェック
    空の時はTrueを返す。"""
    return not word


def run_game():
    """ ゲーム実行 """
    pygame.init()
    screen = pygame.display.set_mode((720, 480))
    font_big = pygame.font.SysFont(None, 128)
    word = select_word()

    while True:
        screen.fill((200, 200, 200))

        sf_word = font_big.render(word, True, (0, 0, 0))
        center_x = screen.get_rect().width / 2 - sf_word.get_rect().width / 2
        screen.blit(sf_word, (center_x, 200))

        pygame.display.update()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if chr(event.key) == word[0]:
                    word = cut_head_char(word)
                    if is_empty_word(word):
                        word = select_word()


run_game()