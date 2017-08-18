# -*- coding: utf-8 -*-
"""AIのプレーヤー同士を自動対戦させて，対戦結果を出力します"""

import sys
from tqdm import tqdm, trange
import reversi
import ai_random
import ai_static_weighting
import ai_static_weighting_rev
import ai_minimax

ai_player_type_list = [ai_static_weighting, ai_static_weighting_rev]

def roundRobin(n):
    """AI同士の総当たり戦を実施する。返り値なし。
    
    Args:
        n (int): 対戦回数
    """
    black_result = [ [0,0,0] for i in range(len(ai_player_type_list)) ]
    white_result = [ [0,0,0] for i in range(len(ai_player_type_list)) ]

    
    for i , black_player in enumerate(tqdm(ai_player_type_list)):
        for j in trange(n, leave=False):
            game = reversi.Reversi(black_player, ai_random)
            winner = game.startGame(isPrint=False)
            if winner == reversi.StoneColor.black:
                black_result[i][0] += 1
            elif winner == reversi.StoneColor.white:
                black_result[i][1] += 1
            else:
                black_result[i][2] += 1

    for i , white_player in enumerate(tqdm(ai_player_type_list)):
        for j in trange(n, leave = False):
            game = reversi.Reversi(black_player, ai_random)
            winner = game.startGame(isPrint=False)
            if winner == reversi.StoneColor.black:
                white_result[i][0] += 1
            elif winner == reversi.StoneColor.white:
                white_result[i][1] += 1
            else:
                white_result[i][2] += 1
    print('black')
    print(black_result)
    print('white')
    print(white_result)


def main():
    """main関数。主にコマンドライン引数の処理"""
    if len(sys.argv) != 2:
        print('usage: "python roundRobin.py [number of match]"')
    else:
        roundRobin(int(sys.argv[1]))

if __name__ == '__main__':
    main()
