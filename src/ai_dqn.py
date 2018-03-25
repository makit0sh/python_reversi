# -*- coding: utf-8 -*-

import reversi
import numpy as np

from keras import backend as K
from keras.models import Sequential, Model
from keras.layers import Dense, Activation, Input, Conv2D, MaxPooling2D, Flatten, Lambda, Add
from keras.engine.topology import Layer
from keras.optimizers import RMSprop
from keras import initializers
from keras.engine import InputSpec
from keras import regularizers
from keras import activations
from keras import constraints
from keras.models import model_from_json

with open('dqn_model.json', 'r') as f:
    model = model_from_json(f.read())
    model.compile(RMSprop(), 'mse')
model.load_weights('dqn_params.hdf5')

#from keras.utils.vis_utils import model_to_dot
#
#with open('model_dqn.svg', 'wb') as f:
#    f.write(model_to_dot(model).create(prog='dot', format='svg'))
def load_model_param(filename):
    model.load_weights(filename)

def board2state(board):
    state = np.zeros([8, 8, 3])

    for i in range(8):
        for j in range(8):
            if board.state[i][j] == reversi.StoneColor.black:
                state[i, j, 0] = 1
            elif board.state[i][j] == reversi.StoneColor.white:
                state[i, j, 1] = 1
            else:
                state[i, j, 2] = 1
    return state

def board2turn(board):
    turn = np.zeros([2])
    turn[board.turn.value] = 1
    return turn

def putStone(board):
    """学習済みDQNを使用して次の手をきめる
    
    Args:
        board (reversi.board):  盤面

    Returns:
        tuple/None: 置いた場所もしくはパスの時はNone
    """
    puttable_positions = board.puttablePositions()
    if len(puttable_positions) == 0:
        return None

    state = board2state(board)
    turn  = board2turn(board)
    q = model.predict([state[np.newaxis, :], turn[np.newaxis, :]]).flatten()
    #print(np.argsort(q)[::-1])
    #print( [ pos[0]*8+pos[1] for pos in puttable_positions ])
    #print( [board.position2Name((i//8, i%8)) for i in  np.argsort(q.reshape((8,8)), axis=None)[::-1]])
    #print( [board.position2Name(pos) for pos in puttable_positions] )

    maxq = -100000
    for pos in [ pos[0]*8+pos[1] for pos in puttable_positions ]:
        if q[pos] >= maxq:
            argmaxq = pos
            maxq = q[pos]

    selected_position = ( int(argmaxq//8), argmaxq%8 )
    board.putStone(selected_position)
    return selected_position

