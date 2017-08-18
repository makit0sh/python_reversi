# -*- coding: utf-8 -*-
"""ボードゲームのリバーシの汎用モジュール
"""

import enum

class StoneColor(enum.Enum):
    """石の色を表すenumクラス"""
    none = 0
    black = 1
    white = -1

class Board():
    """リバーシの盤面クラス

    Attributes:
        state (8x8 list): state of board
        turn (StoneColor): current turn
    """
    def __init__(self, turn=StoneColor.black):
        """コンストラクタ。黒石から始める。"""
        self.state = self.resetBoard()
        self.turn = turn

    def resetBoard(self):
        """初期状態の盤面を生成する。引数はなし。

        Returns:
            list: 8x8のリスト.盤面の状態
        """
        new_state = [ [StoneColor.none for i in range(8)] for j in range(8) ]
        new_state[3][3] = StoneColor.white
        new_state[4][4] = StoneColor.white
        new_state[3][4] = StoneColor.black
        new_state[4][3] = StoneColor.black
        return new_state

    def getStoneColor(self, position):
        """positionの石の色を返す

        Args:
            position (tupple): 位置のタプル

        Returns:
            bool: 石が置ける時True
        """
        return self.state[position[0]][position[1]]

    def position2Name(self, position):
        """位置を表すタプルを文字列に変換。

        Args:
            poosition (tuple): 盤面の位置

        Returns:
            str: 位置の名前（例：e6）
        """
        if position == None:
            return "pass"
        else:
            return ['A','B','C','D','E','F','G','H'][position[1]] + str(position[0]+1)

    def posName2Position(self,pos_name):
        """入力を位置のタプルに変換する。

        Args:
            pos_name (str): 打った場所の名前(例:"e6"), 大文字と小文字の区別はなし

        Returns:
            tuple/False: 変換に成功した場合はその位置のタプル，失敗した場合はFalse
        """
        column_names = ['A','B','C','D','E','F','G','H']
        if len(pos_name) != 2:
            if pos_name[0].upper() in column_names and pos_name[1].isdigit() and int(pos_name[1]) in range(1,9):
                return  int(pos_name[1])-1, column_names.index(pos_name[0].upper())
        return False

    def isPuttable(self, position):
        """ある位置に石が置けるかを確認

        Args:
            position (tupple): 位置のタプル

        Returns:
            bool: 石が置ける時True
        """
        if len(self.reversiblePositions(position)) == 0:
            return False
        else:
            return True
    
    def reverseColor(self):
        """現在のターンの色と逆の色を返す。引数はなし。

        Returns:
            StoneColor: 現在のターンと逆の色
        """
        if self.turn == StoneColor.black:
            return StoneColor.white
        else:
            return StoneColor.black


    def vecScan(self, position, direction):
        """positionからdirectionの方向にどれだけ石が取れるかを返す。

        Args:
            position (tuple): 起点となる位置
            direction (tuple): 石を取る方向

        Returns:
            list: 取ることのできる位置のリスト，何も取れない時は空のリスト[]
        """
        if direction == (0, 0):
            return []
        if self.state[position[0]][position[1]] != StoneColor.none:
            return []
        rev_list = []
        
        while position[0] >= 0 and position[0]<8 and position[1] >= 0 and position[0]<8:
            position = [x+y for (x, y) in zip(position, direction) ]
            if not(position[0] >= 0 and position[0]<8 and position[1] >= 0 and position[1]<8):
                return []
            elif self.state[position[0]][position[1]] == self.reverseColor():
                rev_list.append((position[0], position[1]))
            elif self.state[position[0]][position[1]] == self.turn:
                return rev_list
            else:
                return []

    def reversiblePositions(self, position):
        """positionに置いた時，裏返せる位置のリストを返す。

        Args:
            position (tuple): 起点となる位置

        Returns:
            list: 取ることのできる位置のリスト。取ることができない，もしくはpositionに置くことのできない時は空のリスト
        """
        reversible_positions = []
        for i in [-1, 0, 1]:
            for j in [-1, 0, 1]:
                reversible_positions += self.vecScan(position, (i, j))
        return reversible_positions

    def putStone(self, position):
        """positionの位置に石を置く

        Args:
            position (tuple): 置く位置

        Returns:
            bool: 置くことができた場合True
        """
        if self.isPuttable(position) == False:
            return False
        for pos in self.reversiblePositions(position):
            self.state[pos[0]][pos[1]] = self.turn
        self.state[position[0]][position[1]] = self.turn
        self.turn = self.reverseColor()
        return True
    
    def evaluateBoard(self):
        """盤面の石の数を数える。引数はなし。

        Returns:
            tuple: (int, int)の形で，(黒石の数, 白石の数)
        """
        black_number = 0
        white_number = 0
        for i in range(8):
            for j in range(8):
                if self.state[i][j] == StoneColor.black:
                    black_number += 1
                elif self.state[i][j] == StoneColor.white:
                    white_number += 1
        return black_number, white_number

    def winner(self):
        """現在の盤面の時の数の多い方の色を返す。引数はなし

        Returns:
            StoneColor/None: 引き分けの時はnone
        """
        black_number, white_number = self.evaluateBoard()
        if black_number > white_number:
            return StoneColor.black
        elif black_number < white_number:
            return StoneColor.white
        else:
            return StoneColor.none
    
    def puttablePositions(self):
        """置くことのできる場所を全て返す。引数はなし。

        Returns:
            list: 置くことができる場所のリスト
        """
        puttable_positions = []
        for i in range(8):
            for j in range(8):
                if self.isPuttable((i,j)):
                    puttable_positions.append((i, j))
        return puttable_positions


class Reversi():
    """リバーシのゲームを実行するクラス。

    プレーヤを担当するプログラムは別にモジュールとして与える必要がある。
    そのモジュールは，putStoneという引数を一つ受け取る関数を含む必要があり，その関数は引数として reversi.Board クラスオブジェクトを受け取り，盤面を評価し，次の手を決め，返り値として返す必要がある。
    返り値は，置いた位置の座標を表すタプル(例えば，E6を選んだならば，(5, 4)のように0~7までのint型の整数二つの組)を返し，パスを選んだ時には，Noneとする必要がある。
    (Tips: 位置を表す整数値のタプルは，reversi.Board.posName2Positionメソッドに位置の名前のstr型文字列(例"E6")を渡すことで得ることができる)

    Atrributes:
        board (Board): 盤面のオブジェクト
        black_player_type (module): 黒石のプレーヤーの種類
        white_player_type (module): 白石のプレーヤーの種類
    """
    def __init__(self, black_player_type, white_player_type):
        """コンストラクタ。

        Args:
            black_player_type (module): 黒石のプレーヤーの種類
            white_player_type (module): 白石のプレーヤーの種類
        """
        self.board = Board()
        self.black_player_type = black_player_type
        self.white_player_type = white_player_type

    def putNext(self):
        """次の石を打つ。引数はなし。

        Returns:
            str: 打った場所(例："e6")。パスの時は"pass"
        """
        if self.board.turn == StoneColor.black:
            return self.black_player_type.putStone(self.board)
        else:
            return self.white_player_type.putStone(self.board)
    
    def startGame(self, isPrint=True, isRecord=False):
        """ゲームを開始する

        Args:
            isPrint = True (bool): 標準出力に進行を出力するかどうか
            isRecord = False (bool): 標準出力に棋譜を出力するかどうか

        Returns:
            reversi.StoneColor: 勝者の石の色
        """
        consecutive_pass_flag = False
        while True:
            if isPrint == True:
                self.printState()
            selected_position = self.putNext()
            if isPrint == True:
                print("selected", self.board.position2Name(selected_position), "\n")
            elif isRecord == True:
                print(self.board.position2Name(selected_position))
            if selected_position == None:
                if consecutive_pass_flag == False:
                    consecutive_pass_flag = True
                else:
                    if isPrint == True or isRecord == True:
                        self.printWinner()
                    return self.board.winner()
            else:
                consecutive_pass_flag = False

    def printState(self):
        """盤面の状態を表示する。返り値，引数なし。"""
        if self.board.turn == StoneColor.black:
            print("black's turn")
        else:
            print("white's turn")
        print("black: %d, white: %d" % self.board.evaluateBoard())
        print()
        print("  a b c d e f g h")
        for i in range(8):
            tmp_str = str(i+1)+" "
            for j in range(8):
                if self.board.state[i][j] == StoneColor.black:
                    tmp_str += "@ "
#                    tmp_str += u"○ "
                elif self.board.state[i][j] == StoneColor.white:
                    tmp_str += "O "
#                    tmp_str += u"● "
                else:
                    tmp_str += ". "
#                    tmp_str += u". "
            print(tmp_str)
        print()

    def printWinner(self):
        """ゲーム終了時に勝者を表示する。引数，返り値なし。"""
        if self.board.winner() == StoneColor.black:
            print("winner is black")
        elif self.board.winner() == StoneColor.white:
            print("winner is white")
        else:
            print("the game is draw")


