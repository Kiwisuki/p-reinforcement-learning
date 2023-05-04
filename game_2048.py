import random
from IPython.display import clear_output
import numpy as np 
import gymnasium as gym
from gymnasium import spaces
import copy
import sys

import torch as th
from stable_baselines3 import A2C, DQN, PPO

class Game2048:

    def __init__(self, seed=None):
        if seed is not None:
            random.seed(seed)
            np.random.seed(seed)
        self.board = [[0 for _ in range(4)] for _ in range(4)]
        self.board = Game2048.add_tile(self.board)
        self.board = Game2048.add_tile(self.board)
        self.total_score = 0
    
    @staticmethod
    def add_tile(board):
        empty_cells = [(i, j) for i in range(4) for j in range(4) if board[i][j] == 0]
        if empty_cells:
            row, col = random.choice(empty_cells)
            board[row][col] = 2 if random.random() < 0.9 else 4
        return board

    @staticmethod
    def left(board):
        new_board = []
        score = 0
        for row in board:
            new_row = [tile for tile in row if tile != 0]
            for i in range(len(new_row) - 1):
                if new_row[i] == new_row[i + 1]:
                    new_row[i] *= 2
                    score += new_row[i]
                    new_row[i + 1] = 0
            new_row = [tile for tile in new_row if tile != 0]
            new_row += [0] * (4 - len(new_row))
            new_board.append(new_row)
        board = new_board
        return board, score
    
    @staticmethod
    def right(board):
        board = [row[::-1] for row in board]
        board, score = Game2048.left(board)
        board = [row[::-1] for row in board]
        return board, score

    @staticmethod
    def up(board):
        board = [list(row) for row in zip(*board)]
        board, score = Game2048.left(board)
        board = [list(row) for row in zip(*board)]
        return board, score

    @staticmethod
    def down(board):
        board = [list(row) for row in zip(*board)]
        board, score = Game2048.right(board)
        board = [list(row) for row in zip(*board)]
        return board, score
        
    @staticmethod
    def is_game_over(board):
         # if any tile is 2048, the game is won
        for row in board:
            if 2048 in row:
                return True
            
        # if there is an empty cell, the game is not over
        # if there are two adjacent tiles with the same value, the game is not over
        for i in range(4):
            for j in range(4):
                if board[i][j] == 0:
                    return False
                if j < 3 and board[i][j] == board[i][j + 1]:
                    return False
                if i < 3 and board[i][j] == board[i + 1][j]:
                    return False
       
        return True

    @staticmethod
    def render_board(board):
        print("+-------------------+")
        for row in board:
            print("|", end="")
            for tile in row:
                if tile == 0:
                    print("{:^4}".format("."), end="|")
                else:
                    print("{:^4}".format(tile), end="|")
            print()
            print("+-------------------+")

    def move(self, action):
        if action == 0:
            self.board, score = Game2048.left(self.board)
        elif action == 1:
            self.board, score = Game2048.right(self.board)
        elif action == 2:
            self.board, score = Game2048.up(self.board)
        elif action == 3:
            self.board, score = Game2048.down(self.board)
        self.board = Game2048.add_tile(self.board)
        self.total_score += score

        return self.board, score, Game2048.is_game_over(self.board)
    