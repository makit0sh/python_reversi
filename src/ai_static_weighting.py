# -*- coding: utf-8 -*-

"""reversiモジュール用のプレーヤープログラム。
盤面の位置に点数を割り当て，その時打てる位置の中で最も点数が高かったものを返す AI。先読みはしない。"""
import reversi

def putStone(board):
    """静的重み付けにより置く場所を決定する

    Args:
        board (reversi.board): 盤面

    Returns:
        tuple/None: 置いた位置もしくはパスの時はNone
    """
    puttable_positions = board.puttablePositions()
    if len(puttable_positions) == 0:
        return None

    if board.turn ==reversi.StoneColor.black:
        gGain = [( 30, -12,  0, -1, -1,  0, -12,  30), \
             (-12, -15, -3, -3, -3, -3, -15, -12), \
             (  0,  -3,  0, -1, -1,  0,  -3,   0), \
             ( -1,  -3, -1, -1, -1, -1,  -3,  -1), \
             ( -1,  -3, -1, -1, -1, -1,  -3,  -1), \
             (  0,  -3,  0, -1, -1,  0,  -3,   0), \
             (-12, -15, -3, -3, -3, -3, -15, -12), \
             ( 30, -12,  0, -1, -1,  0, -12,  30)]
    else:
        gGain = [(120, -20, 20,  5,  5, 20, -20, 120), \
                 (-20, -40, -5, -5, -5, -5, -40, -20), \
                 ( 20,  -5, 15,  3,  3, 15,  -5,  20), \
                 (  5,  -5,  3,  3,  3,  3,  -5,   5), \
                 (  5,  -5,  3,  3,  3,  3,  -5,   5), \
                 ( 20,  -5, 15,  3,  3, 15,  -5,  20), \
                 (-20, -40, -5, -5, -5, -5, -40, -20), \
                 (120, -20, 20,  5,  5, 20, -20, 120)]

    selected_position = max(puttable_positions, key=lambda x: gGain[x[0]][x[1]])
    board.putStone(selected_position)
    return selected_position

