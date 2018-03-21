# -*- coding: utf-8 -*-
"""reversiモジュール用のプレーヤープログラム。
ミニマックス法で先読みし，その時打てる位置の中で最も評価が高い位置に石を置く AI。"""

import reversi
import copy

def putStone(board):
    """静的重み付けと確定石の数を用いた評価関数により,ミニマックス法で置く場所を決定する

    Args:
        board (reversi.board): 盤面

    Returns:
        str: 置いた場所もしくはpass
    """
    puttable_positions = board.puttablePositions()
    if len(puttable_positions) == 0:
        return None

    selected_position = minimax(board, board.turn, 3)[1]
    board.putStone(selected_position)
    return selected_position

def minimax(board, current_turn, depth):
    """ミニマックス法で盤面を評価する

    Args:
        board (reversi.board): 評価する盤面
        depth (int): 先読みの深さ

    Returns:
        int: 評価値
        tuple: 最良の位置
    """
    if depth == 0:
        return static_evaluation(board), None

    puttable_positions = board.puttablePositions()
    if len(puttable_positions) == 0:
        return static_evaluation(board), None
    next_boards = []
    for i, next_pos in enumerate(puttable_positions):
        next_boards.append( copy.deepcopy(board) )
        next_boards[i].putStone(next_pos)
    
    if board.turn == current_turn:
        best, best_index = min( [ ( minimax(b, current_turn, depth-1)[0], i ) for i, b in enumerate(next_boards) ])
        best_pos = puttable_positions[best_index]
    else:
        best, best_index = max( [ ( minimax(b, current_turn, depth-1)[0], i ) for i, b in enumerate(next_boards) ])
        best_pos = puttable_positions[best_index]

    return (best, best_pos)

def static_evaluation(board):
    """重み付けと固定石かどうかにより盤面を評価する

    Args:
        board (reversi.board): 評価する盤面

    Returns:
        int: 盤面の評価値
    """
    gGain = [( 45, -11,  4, -1, -1,  4, -11,  45), \
             (-11, -16, -1, -3, -3,  2, -16, -11), \
             (  4,  -1,  2, -1, -1,  2,  -1,   4), \
             ( -1,  -3, -1,  0,  0, -1,  -3,  -1), \
             ( -1,  -3, -1,  0,  0, -1,  -3,  -1), \
             (  4,  -1,  2, -1, -1,  2,  -1,   4), \
             (-11, -16, -1, -3, -3,  2, -16, -11), \
             ( 45, -11,  4, -1, -1,  4, -11,  45)]
    value = 0
    for i, row in enumerate(board.state):
        for j, pos in enumerate(row):
            value += pos.value * board.turn.value * gGain[i][j]
            if isFixedStone(board, (i,j)):
                value += pos.value * board.turn.value * 30
    return value

def isFixedStone(board, position):
    """その石が固定石かを調べる, 判定は四辺のみ

    Args:
        board (reversi.Board): 評価する盤面

    Returns:
        tuple:  評価する石の位置
    """
    if position in [(0,0), (0,7), (7,0), (7,7)]:
        return True
    elif position[0] == 0 or position[0] == 7:
        return board.getStoneColor(position) == board.state[position[0]][position[1]-1] or \
                board.getStoneColor(position) == board.state[position[0]][position[1]+1]
    elif position[1] == 0 or position[1] == 7:
        return board.getStoneColor(position) == board.state[position[0]-1][position[1]] or \
                board.getStoneColor(position) == board.state[position[0]+1][position[1]]
    else:
        return False
