# -*- coding: utf-8 -*-

import reversi
import ai_random
import ai_static_weighting, ai_minimax
import roundRobin

import copy
import numpy as np
import matplotlib.pyplot as plt

from keras import backend as K
from keras.models import Sequential, Model
from keras.layers import Dense, Activation, Input, Conv2D, MaxPooling2D, Flatten, Dropout, Lambda, Add, Reshape, concatenate
from keras.layers.normalization import BatchNormalization
from keras.engine.topology import Layer
from keras.optimizers import RMSprop, Adam
from keras import initializers
from keras.engine import InputSpec
from keras import regularizers
from keras import activations
from keras import constraints

def build_mlp_model():
    '''mlpモデルを作成する'''

    board_input = Input(shape=[8, 8, 3]) # 盤面をnone, black, whiteの3種類用意
    color = Input(shape=[2]) # one hot vector として自分の石の色を入力

    color_reshape = Reshape( [1, 1, 2] )(color) # 1x1x2
    color_reshape = Lambda(lambda x: K.ones([8, 8, 2])*x)(color_reshape) # 1x1x2 -> 8x8x2
    color_input = concatenate([board_input, color_reshape], axis=-1) # 8x8x5

    #x = Conv2D(64, (4, 4), padding='same')(color_input)
    #x = Dropout(0.15)(x)
    #x = BatchNormalization()(x)
    #x = Activation('relu')(x)
    #x = Conv2D(128, (2, 2), padding='same')(x)
    #x = Dropout(0.15)(x)
    #x = BatchNormalization()(x)
    #x = Activation('relu')(x)
    #x = Conv2D(256, (2, 2), padding='same')(x)
    #x = Dropout(0.15)(x)
    #x = BatchNormalization()(x)
    #x = Activation('relu')(x)
    #x = Conv2D(128, (1, 1), padding='same')(x)
    #x = Dropout(0.15)(x)
    #x = BatchNormalization()(x)
    #x = Activation('relu')(x)
    #x = Conv2D(32, (1, 1), padding='same')(x)
    #x = Dropout(0.15)(x)
    #x = BatchNormalization()(x)
    #x = Activation('relu')(x)
    #x = Conv2D(1, (1, 1), padding='same')(x)
    #x = Flatten()(x)
    #model_output = Activation('tanh')(x)
    #model = Model([board_input, color], model_output)
    #model.compile(RMSprop(), 'mse')

    x = Conv2D(32, kernel_size=(6,6), padding='same', activation='relu')(color_input)
    #x = Conv2D(32, kernel_size=(4,4), padding='same', activation='relu')(color_input)
    x = Conv2D(64, kernel_size=(2,2), padding='same', activation='relu')(x)
    x = Conv2D(64, kernel_size=(1,1), padding='same', activation='relu')(x)
    x = Flatten()(x)
    x = Dense(128, activation='relu')(x)
    #model_output = Dense(64, activation='linear')(x)
    model_output = Dense(64, activation='tanh')(x)
    model = Model([board_input, color], model_output)
    model.compile(RMSprop(), 'mse')

    return model

class ReplayMemory:
    def __init__(self, memory_size=10**4):
        self.memory_size = memory_size
        self.memory = []

    def __len__(self):
        return len(self.memory)

    def append(self, transition):
        self.memory.append(transition)
        self.memory = self.memory[-self.memory_size:]

    def sample(self, batch_size):
        batch_indexes = np.random.randint(0, len(self.memory), size=batch_size).tolist()
        states      = np.array([self.memory[index]['state'] for index in batch_indexes])
        turns       = np.array([self.memory[index]['turn'] for index in batch_indexes])
        next_states = np.array([self.memory[index]['next_state'] for index in batch_indexes])
        next_turns  = np.array([self.memory[index]['next_turn'] for index in batch_indexes])
        rewards     = np.array([self.memory[index]['reward'] for index in batch_indexes])
        actions     = np.array([self.memory[index]['action'] for index in batch_indexes])
        dones       = np.array([self.memory[index]['done'] for index in batch_indexes])
        return {'states': states, 'turns': turns, 'next_states': next_states, 'next_turns': next_turns, 'rewards': rewards, 'actions': actions, 'dones': dones}

def copy_weights(model_original, model_target):
    for i, layer in enumerate(model_original.layers):
        model_target.layers[i].set_weights(layer.get_weights())
    return model_target

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

def DQNAgent_putStone(board):
    puttable_positions = board.puttablePositions()
    if len(puttable_positions) == 0:
        return None

    state = board2state(board)
    turn  = board2turn(board)
    q = model.predict([state[np.newaxis, :], turn[np.newaxis, :]]).flatten()
    if np.random.random() < eps:
        action = ai_random.putStone(board)
    else:
        #argmaxq = np.argmax(q)
        maxq = -100000
        for pos in [ pos[0]*8+pos[1] for pos in puttable_positions ]:
            if q[pos] >= maxq:
                argmaxpos = pos
                maxq = q[pos]
        game.board.putStone((argmaxpos//8, argmaxpos%8))
        action = ( int(argmaxpos//8), argmaxpos%8 )

    return action


# ここからmain

# Replay Memory への貯蓄P'
memory_size = 10**4 # Replay Memory の大きさ
gamma = 0.95 # 割引率
batch_size = 32

model = build_mlp_model() # Q-Network
model_target = build_mlp_model() # Target-Network
with open('dqn_model.json', 'w') as f:
    f.write(model.to_json())

replay_memory = ReplayMemory(memory_size)

n_frames = 0

while True:

    rand_tmp = np.random.randint(4)
    if rand_tmp == 0:
        game = reversi.Reversi(ai_random, ai_static_weighting)
    elif rand_tmp == 1:
        game = reversi.Reversi(ai_static_weighting, ai_random)
    elif rand_tmp == 2:
        game = reversi.Reversi(ai_random, ai_minimax)
    else:
        game = reversi.Reversi(ai_minimax, ai_random)

    boards = []
    actions = []
    consecutive_pass_flag = False

    while True:
        # Act
        boards.append(copy.copy(game.board))
        action = game.putNext()
        actions.append(action)
        if action == None:
            if consecutive_pass_flag == False:
                consecutive_pass_flag = True
            else:
                break
        else:
            consecutive_pass_flag = False

    winner = game.board.winner()
    for i, (board, action) in enumerate(zip(boards, actions)):
        transition = {
                'state': board2state(board),
                'turn': board2turn(board),
                'next_state': board2state(boards[min(i+2, len(boards)-2)]),
                'next_turn': board2turn(boards[min(i+2, len(boards)-2)]),
                'reward': 1 if board.turn == winner else ( 0 if board.turn == None else -1 ),
                'action': action,
                'done': 1 if i==len(boards)-1 else 0,
                }
        replay_memory.append(transition)
        n_frames += 1
        if (n_frames) % 1000 == 0:
            print('Number of frames:', n_frames)

    if n_frames >= memory_size:
        break

# 学習
eps = 0.9
eps_end = 0.1
tau = (eps - eps_end) / 1000

n_episodes = 10000
n_check = 50
n_train_per_episode = 2
target_update_interval = 20 # Target Networkを更新する間隔
n_frames = 0

for episode in range(n_episodes):

    game = reversi.Reversi(None, None)

    while True:
        # Act
        boards.append(copy.copy(game.board))
        action = DQNAgent_putStone(game.board)
        actions.append(action)
        if action == None:
            if consecutive_pass_flag == False:
                consecutive_pass_flag = True
            else:
                break
        else:
            consecutive_pass_flag = False

    winner = game.board.winner()
    for i, (board, action) in enumerate(zip(boards, actions)):
        transition = {
                'state': board2state(board),
                'turn': board2turn(board),
                'next_state': board2state(boards[min(i+2, len(boards)-2)]),
                'next_turn': board2turn(boards[min(i+2, len(boards)-2)]),
                'reward': 1 if board.turn == winner else ( 0 if board.turn == None else -1 ),
                'action': action,
                'done': 1 if i==len(boards)-1 else 0,
                }
        replay_memory.append(transition)

    # 1エピソードに付き複数回学習
    for i in range(n_train_per_episode):
        transitions = replay_memory.sample(batch_size)
        y = model.predict([transitions['states'],transitions['turns']])
        new_q = model_target.predict([transitions['next_states'], transitions['next_turns']])
        y_ = transitions['rewards'] + (1 - transitions['dones'])*gamma*np.max(new_q, axis=1) # 次の手は相手なので、2手先で評価

        for i, (a, r) in enumerate(zip(transitions['actions'], y_)):
            if a is None:
                continue # TODO Passの時の学習
            y[i, a[0]*8+a[1]] = r

        history = model.fit([transitions['states'], transitions['turns']], y, epochs=1, verbose=0)

        n_frames += 1

        if eps > eps_end:
            eps -= tau

        if (n_frames + 1) % target_update_interval == 0:
            model_target = copy_weights(model, model_target)

    # 一定回数ごとにモデルの評価及び保存
    if (episode+1) % n_check == 0:
        print('Episode: %d, Eps: %.3f' % (episode+1, eps))
        model.save_weights('dqn_params_'+str(episode+1)+'.hdf5')
        print('model saved')

        roundRobin.load_model('dqn_params_'+str(episode+1)+'.hdf5')
        black_result, white_result = roundRobin.roundRobin(100)
        with open('win_rate_result.csv', 'a') as f:
            f.write(str(episode+1)+','+str(black_result[0][0])+','+str(white_result[0][0])+'\n')
