# -*- coding: utf-8 -*-

"""cuiでインタラクティブにリバーシを楽しむことができます"""
import reversi
import human_interface
import ai_random
import ai_static_weighting
import ai_minimax
import ai_dqn

player_type_list = [human_interface, ai_random, ai_static_weighting, ai_minimax, ai_dqn]

def main():
    """main関数。プレーヤータイプを選択し，ゲームを実行する"""
    print("available player types:")
    print("0: human, 1: AI level0 (random), 2: AI level1 (static weighting), 3: AI level2 (minimax) 4: AI level3 (DQN)")
    print("select black player type in number")
    black_type_number = input("> ")
    black_player_type = player_type_list[int(black_type_number)]

    print("select white player type in number")
    white_type_number = input("> ")
    white_player_type = player_type_list[int(white_type_number)]

    print("\nnote: 黒石： @, 白石: O\n")
    game = reversi.Reversi(black_player_type, white_player_type)
    game.startGame()

if __name__ == '__main__':
    main()
