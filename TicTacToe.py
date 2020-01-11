from abc import ABC,abstractmethod
from enum import Enum
from copy import deepcopy
from random import choice

# 裁判判断结果
class GameResult(Enum):
    Continue = 0
    BlackWin = 1
    WhiteWin = 2
    Draw = 3
# black = -1,X
# white = 1,O

# 棋手对自己的主观判断
class Prediction(Enum):
    Draw = 1
    Win = 2
    Lose = 3

class Board:
    def __init__(self):
        self.__model = [[0,0,0],[0,0,0],[0,0,0]] # 空棋盘

    def add_move(self,position,color):
        if self.__model[position[0]][position[1]] != 0:
            return False
        self.__model[position[0]][position[1]] = color
        return True

    def draw(self):
        symbols = {-1:'X',0:' ',1:'O'}
        print('---')
        for row in self.__model:
            for item in row:
                print(symbols[item],end ='',sep ='')
            print('')
        print('---')

    def get_model(self):
        return self.__model.copy()

def test():
    board = Board()
    board.add_move((1,1),-1)
    board.add_move((0,0),1)
    board.draw()

class Player(ABC): # abstract base class
    @abstractmethod
    def move(self,model):
        pass 

class HumanPlayer(Player):
    def move(self,model,color):
        row = int(input('row: '))
        column = int(input('column: '))
        return row,column


class AiPlayer(Player):
    def move(self,model,color):
        return self.find_move(model,color)[1]

    def find_move(self,model,color):
        if model[1][1] == 0:
            return Prediction.Draw,(1,1)
        #走一步直接赢
        for row in range(0,3):
            for column in range(0,3):
                if model[row][column] != 0:continue
                private_model = deepcopy(model)
                private_model[row][column] = color
                result = Judge().judge(private_model)
                if result == ( GameResult.BlackWin if color == -1 else GameResult.WhiteWin):
                     return Prediction.Win,(row,column)
                elif result == GameResult.Draw:
                    return Prediction.Draw,(row,column)
        # 走一步对方会输
        #
        draw_moves = list()         
        lose_moves = list()
        for row in range(0,3):
            for column in range(0,3):
                if model[row][column] != 0:continue
                private_model = deepcopy(model)
                private_model[row][column] = color
                oppoent_result = self.find_move(private_model,color * -1)
                if oppoent_result[0] == Prediction.Lose:
                    return Prediction.Win,(row,column)
                elif oppoent_result[0] == Prediction.Draw:
                    draw_moves.append((row,column))
                else:
                    lose_moves.append((row,column))
        
        if draw_moves:
            return Prediction.Draw,choice(draw_moves)
        
        return Prediction.Lose,choice(lose_moves)

   

class Judge:
    def judge(self,model):
        if self.is_win(model,-1):
            return GameResult.BlackWin
        if self.is_win(model,1):
            return GameResult.WhiteWin
        if self.is_full(model):
            return GameResult.Draw
        else:
            return GameResult.Continue
   
    def is_full(self,model):
        for row in model:
            if not all(row):
                return False

        return True

    def is_win(self,model,color):
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



    

def run():
    players = [AiPlayer(),HumanPlayer()]
    board = Board()
    judge = Judge()
    board.draw()
    index = 0
    color = -1 
    result = GameResult.Continue
    while result == GameResult.Continue:

        while not board.add_move(players[index].move(board.get_model(),color),color):
            pass
        #position = players[index].move(board.get_model())
        #print(position)
        #board.add_move(position,color)
        board.draw()
        result = judge.judge(board.get_model())
        judge.judge(board.get_model())
        index = 1 - index
        color = -1 * color
    if result == GameResult.BlackWin:
        print('Black wins!')
    elif result == GameResult.WhiteWin:
        print('White wins!')
    else:
        print('Draw')


if  __name__ == "__main__":
     run()