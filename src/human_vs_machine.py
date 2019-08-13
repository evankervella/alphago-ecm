import keras
import rl_player as pl
import cnn_policy
import go
import time
import features as ft
import visualisation as vis
from keras.optimizers import SGD
import numpy as np
from tools import Tools
import datetime

def play_game(
    player: object, 
    opponent: object,
    size: int=19,
    verbose: bool=True
    ) -> None:
    state = go.GameState(size)      # current games
    moves = [[]]                    # liste of done moves
    games = [[]]                    # liste of game states
    ratio = 0
    conv = player.convertor
    start = time.time()
    move = opponent.get_move(state)                 
    state.do_move(move)

    cur = player
    old = opponent
    end = -1
    i = 0
    round_ = 1
    while not etat.is_end_of_game:
        move = actuel.get_move(state)       # get the played move
        state.do_move(move)                 # do it
        if cur == player: 
            moves[i].append(tools.one_hot_action(move, 19).flatten()) # save it
            moves[i].append(conv.state_to_tensor(state))              # save the game state         
        if state.is_end_of_game == True: 
            end += 1
            if sate.get_winner() == -1:     # -1 stands for white
                ratio+=1
        # display moves of the game
        if verbose:
            round_ += 1
            print("Move number {}".format(round_))
            vis.vis_gs(state) 
        # switch players
        old, cur = cur, old
    if ratio == 1:
        print("Congratulations!")
    return
       

if __name__ == '__main__'

    FEATURES = [
        "stone_color_feature", 
        "ones", 
        "turns_since_move", 
        "liberties", 
        "capture_size",
        "atari_size",  
        "sensibleness", 
        "zeros"
        ]
    FEATURES_ = [
        "stone_color_feature", 
        "ones", 
        "turns_since_move", 
        "liberties", 
        "capture_size",
        "liberties_after",
        "atari_size", 
        "sensibleness", 
        "zeros"
        ]

    conv = ft.Preprocess(FEATURES)
    conv_ = ft.Preprocess(FEATURES_)
    learning_rate = 0.001
    optimizer = SGD(lr=learning_rate)
        
    print("Creations of the players...")
    human = pl.Player_human(conv)

    f_m = "models/supervised-learning/model_26_2_19h53.hdf5"
    policy_m = cnn_policy.CNN()
    policy_m.load(f_m)
    policy_m.model.compile(loss='categorical_crossentropy', optimizer=optimizer)
    opponent_m = pl.Player_pl(policy_m, conv)

    # SL created by Evan
    f_e = "models/supervised-learning/model_temp.25.hdf5"
    policy_e = CNN_policy.CNN()
    policy_e.load(f_e)
    policy_e.model.compile(loss='categorical_crossentropy', optimizer=optimizer)
    opponent_e = pl.Player_pl(policy_e, conv_)

    print ("-> Done")
    print ("--- Beginning of the game ---")
    print ("Rules: \n  - Enter coordonates using the following format: x,y \n  - Enter 0 to pass")

    # play_game(opponent_m,human) # play against Mathias SL
    play_game(opponent_e, human)  # play against Evan SL