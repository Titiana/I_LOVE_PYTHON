from abc import ABC, abstractmethod
from enum import Enum
from copy import deepcopy
from random import choice


# 裁判判断结果
class GameResult(Enum):
    Continue = 0
    BlackWin = 1
    WhiteWin = 2
    Draw = 3


# 棋手对自己的主观判断
class Prediction(Enum):
    Draw = 1
    Win = 2
    Lose = 3


class Board:
    def __init__(self):
        self.__model = [[0, 0, 0], [0, 0, 0], [0, 0, 0]]  # 空棋盘

    def add_move(self, position, color):
        if self.__model[position[0]][position[1]] != 0:
            return False
        self.__model[position[0]][position[1]] = color
        return True

    def draw(self):
        symbols = {-1: 'X', 0: ' ', 1: 'O'}
        print('\t', end="")
        print("\n\t— — —\n\t".join(["|".join([symbols[item] for item in row]) for row in self.__model]))
        print('\n', end="")

    def get_model(self):
        return self.__model.copy()


def test():
    board = Board()
    board.add_move((1, 1), -1)
    board.add_move((0, 0), 1)
    board.draw()


# abstract base class
class Player(ABC):
    @abstractmethod
    def move(self, model, color):
        pass

    def count(self, model, color):
        pass


class HumanPlayer(Player):
    def move(self, model, color):
        row = int(input('\trow: '))
        column = int(input('\tcolumn: '))
        return row, column

    def count(self, model, color):
        num = int(input("PLZ enter a number between 1 to 9:"))
        row = (num - 1) // 3
        column = num % 3 - 1
        print("\tYou entered " + str(num))
        return row, column


class AiPlayer(Player):
    def move(self, model, color):
        return self.find_move(model, color)[1]

    def count(self, model, color):
        row, column = self.find_move(model, color)[1]
        print("\tAiPlayer entered " + str(row * 3 + column + 1))
        return row, column

    def find_move(self, model, color):
        if model[1][1] == 0:
            return Prediction.Draw, (1, 1)
        # 走一步直接赢
        for row in range(0, 3):
            for column in range(0, 3):
                if model[row][column] != 0:
                    continue
                private_model = deepcopy(model)
                private_model[row][column] = color
                result = Judge().judge(private_model)
                if result == (GameResult.BlackWin if color == -1 else GameResult.WhiteWin):
                    return Prediction.Win, (row, column)
                elif result == GameResult.Draw:
                    return Prediction.Draw, (row, column)
        # 走一步对方会输
        draw_moves = list()
        lose_moves = list()
        for row in range(0, 3):
            for column in range(0, 3):
                if model[row][column] != 0:
                    continue
                private_model = deepcopy(model)
                private_model[row][column] = color
                opponent_result = self.find_move(private_model, color * -1)
                if opponent_result[0] == Prediction.Lose:
                    return Prediction.Win, (row, column)
                elif opponent_result[0] == Prediction.Draw:
                    draw_moves.append((row, column))
                else:
                    lose_moves.append((row, column))
        if draw_moves:
            return Prediction.Draw, choice(draw_moves)
        return Prediction.Lose, choice(lose_moves)


class Judge:
    def judge(self, model):
        if self.is_win(model, -1):
            return GameResult.BlackWin
        if self.is_win(model, 1):
            return GameResult.WhiteWin
        if self.is_full(model):
            return GameResult.Draw
        else:
            return GameResult.Continue

    @staticmethod
    def is_full(model):
        for row in model:
            if not all(row):
                return False
        return True

    @staticmethod
    def is_win(model, color):
        return any([
            model[0][0] == model[1][1] == model[2][2] == color,
            model[0][2] == model[1][1] == model[2][0] == color,
            model[0][0] == model[0][1] == model[0][2] == color,
            model[1][0] == model[1][1] == model[1][2] == color,
            model[2][0] == model[2][1] == model[2][2] == color,
            model[0][0] == model[1][0] == model[2][0] == color,
            model[0][1] == model[1][1] == model[2][1] == color,
            model[0][2] == model[1][2] == model[2][2] == color
        ])


class Mode:
    def __init__(self):
        self.__players = [AiPlayer(), HumanPlayer()]
        self.__board = Board()
        self.__judge = Judge()
        self.__index = 0
        self.__color = -1
        self.__result = GameResult.Continue
        self.menu()

    def menu(self):
        print("\t\t1: Position Mode")
        print("\t\t2: Number Mode")
        print("\t\t3: Pure Number Mode")
        print("\t\t4: Exit Game")
        a = input("PLZ enter a number to choose an option:")
        if a == "1":
            self.position_mode()
        elif a == "2":
            self.number_mode()
        elif a == "3":
            self.pure_number_mode()
        elif a == "4":
            exit(0)
        else:
            print("\tPLZ enter a true option!!!")
            self.__init__()

    def position_mode(self):
        # self.__board.draw()
        while self.__result == GameResult.Continue:
            while not self.__board.add_move(self.__players[self.__index].move(self.__board.get_model(), self.__color), self.__color):
                pass
            # position = players[index].move(board.get_model())
            # print(position)
            # board.add_move(position,color)
            self.__board.draw()
            self.__result = self.__judge.judge(self.__board.get_model())
            self.__judge.judge(self.__board.get_model())
            self.__index = 1 - self.__index
            self.__color = -1 * self.__color
        if self.__result == GameResult.BlackWin:
            print('\tAI wins!')
        elif self.__result == GameResult.WhiteWin:
            print('\tPlayer wins!')
        else:
            print('\tDraw')
        print("Play again?")
        self.menu()

    def number_mode(self):
        while self.__result == GameResult.Continue:
            while not self.__board.add_move(self.__players[self.__index].count(self.__board.get_model(), self.__color),
                                            self.__color):
                pass
            self.__board.draw()
            self.__result = self.__judge.judge(self.__board.get_model())
            self.__judge.judge(self.__board.get_model())
            self.__index = 1 - self.__index
            self.__color = -1 * self.__color
        if self.__result == GameResult.BlackWin:
            print('\tAI reached 15 quickly!')
        elif self.__result == GameResult.WhiteWin:
            print('\tPlayer reached 15 quickly!')
        else:
            print('\tNobody reached 15!')
        print("Play again?")
        self.menu()

    def pure_number_mode(self):
        while self.__result == GameResult.Continue:
            while not self.__board.add_move(self.__players[self.__index].count(self.__board.get_model(), self.__color),
                                            self.__color):
                pass
            self.__result = self.__judge.judge(self.__board.get_model())
            self.__judge.judge(self.__board.get_model())
            self.__index = 1 - self.__index
            self.__color = -1 * self.__color
        if self.__result == GameResult.BlackWin:
            print('\tAI reached 15 quickly!')
        elif self.__result == GameResult.WhiteWin:
            print('\tHuman reached 15 quickly!')
        else:
            print('\tNobody reached 15!')
        print("Play again?")
        self.menu()


if __name__ == "__main__":
    myMode = Mode()
