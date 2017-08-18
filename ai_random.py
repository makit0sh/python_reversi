# -*- coding: utf-8 -*-

"""reversiモジュール用のプレーヤープログラム。
ランダムに次の手を選ぶAI。"""
import reversi
import random

def putStone(board):
    """ランダムに石を置く

    Args:
        board (reversi.board):  盤面

    Returns:
        tuple/None: 置いた場所もしくはパスの時はNone
    """
    puttable_positions = board.puttablePositions()
    if len(puttable_positions) == 0:
        return None

    selected_position = puttable_positions[ random.randint(0,len(puttable_positions)-1)]
    board.putStone(selected_position)
    return selected_position

