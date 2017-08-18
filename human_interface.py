# -*- coding: utf-8 -*-
"""reversiモジュール用のプレーヤープログラム。
人間の手を読み取るインターフェースです。"""

import reversi

def putStone(board):
    """入力を読み取り，その位置に石を置く

    Args:
        board (reversi.board):  盤面

    Returns:
        tuple/None 置いた位置もしくはパスの時はNone
    """
    if len(board.puttablePositions())==0:
        print('you cannot put stone.')
        return None

    while True:
        print("where do you want to put next? (example: e6)")
        pos_name = input('> ')
        pos = board.posName2Position(pos_name)
        if pos != False and board.putStone(pos) != False:
            return pos
        print("you cannnot put stone on", pos_name)

