import keras
import go 
import cnn_policy
import rl_player as pl
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
    nb_games: int,
    size: int=9,
    verbose: bool=False
    ) -> tuple:
    state = [go.GameState(size) for _ in range(nb_game)]    # list of current games
    moves = [[] for _ in range(nb_game)]                    # list of played moves
    games = [[] for _ in range(nb_game)]                    # list of game states
    id_won = []                                             # indices of won games
    ratio = 0
    conv = player.convertor
    start = time.time()
    # we play first move of each game
    for i in range(nb_games):
        move = opponent.get_move(state[i])                  # opponent with black stones starts
        state[i].do_move(move)
    # we play each move
    cur = player
    old = opponent
    end = 0
    round_ = 1
    while end < nb_games: 
        for i in range(nb_games):
                if not state[i].is_end_of_game:
                    move = cur.get_move(state[i])
                    state[i].do_move(move)
                    if cur == player: 
                        move[i].append(tools.one_hot_action(move, 19).flatten())    # we save the move
                        games[i].append(conv.state_to_tensor(state[i]))             # on the game state
                    if stae[i].is_end_of_game: 
                        end +=1
                        if state[i].get_winner() == -1:                             # -1 is for white
                            id_won.append(i)
                            ratio += 1
                    # display moves from last game
                    if i==1 and verbose==True:
                        round_ += 1
                        print("Move number {}".format(round_))
                        vis.vis_gs(state[i]) 
        old, cur = cur, old                     # switch players
    ratio /= float(nb_games)
    print("{} executed games in {} seconds".format(nb_games, time.time()-start))
    print("Victories ratio: {}".format(ratio))
    return moves, games, id_won, ratio

def r_learning(
    moves: list, 
    games: list, 
    id_won: list, 
    player: object, 
    name: str, 
    ratio: float, 
    nb_games: int, 
    epoch: int
    ) -> str:
    print('-'*15, 'Learning', '-'*15)
    total_nb_moves = 0
    for i in range(len(games)):
        print ('-'*10, 'Game {}'.format(i), '-'*10)
        moves[i] = np.array(moves[i])
        moves[i] = np.array(games[i])
        moves[i] = np.concatenate(games[i], axis=0)
        
        total_nb_moves += len(moves[i])
        if i in id_won:
        	optimizer.lr = np.absolute(optimizer.lr)
        else :
            optimizer.lr = np.absolute(optimizer.lr)*(-1)
        #player.policy.model.train_on_batch(np.concatenate(moves[i], axis=0), np.concatenate(moves[i],axis=0))
        loss = player.policy.model.train_on_batch(games[i], moves[i])
        print("loss = {}".format(loss))
        #player.policy.model.train_on_batch(np.concatenate(games[i], axis=0), moves[i])
    date = datetime.datetime.now()   
    filepath = ("%s/%s_R=%2f_N=%d_H=%s_%s_%sh%s.hdf5" %("RL", name, ratio, nb_games, date.day, date.month, date.hour, date.minute))
    tfilepath = ("%s/%s_R=%2f_N=%d_H=%s_%s_%sh%s.txt" %("RL", name, ratio, nb_games, date.day, date.month, date.hour, date.minute))
    player.policy.model.save(filepath)
    print('{} moves on {} learned games'.format(total_nb_moves, len(games)))
    tools.text_file(tfilepath, player.policy.model.model, total_nb_moves, epoch, date)
    return filepath 

def play_learn(
    player: object,
    opponent: object,
    nb_games: int,
    epoch: int,
    policy:,
    name: str,
    size: int=19,
    verbose: bool=False
    ) -> str:
	date = datetime.datetime.now()   
	preprocessor = player.convertor
    i = 1
	print("Learning started at {}".format(date))          
	print ('-'*15, 'Epoch {}'.format(i), '-'*15)
	moves, games, id_won, ratio_ = play_game(player, opponent, nb_games, 19, verbose)
	new_model = r_learning(moves, games, id_won, player, name, ratio_, nb_games, i)
	policy_pl = cnn_policy.CNN()
	policy_pl.load(new_model)
	policy_pl.model.compile(loss='categorical_crossentropy', optimizer=optimizer)
	del player
	player = pl.Player_pl(policy_pl, preprocessor) 
	
	while i < epoch+1:
		i+=1
		print ('-'*15, 'Epoch {}'.format(i), '-'*15)
		moves, games,id_won, ratio = play_game(player, opponent, nb_games, 19, False)
		new_model = r_learning(moves, games, id_won, player, name, ratio, nb_games, i)	
		del policy_pl
		policy_p = cnn_policy.CNN()
		policy_pl.load(new_model)
		policy_pl.model.compile(loss='categorical_crossentropy', optimizer=optimizer)
		del player
		player = pl.Player_pl(policy_pl, preprocessor)   
    
    date = datetime.datetime.now()   
	print("Learning finished at {}" %(date))
	print("Initial victories ratio: {}, last train victories ratio: {}" %(ratio_, ratio))
	return new_model        # returns the name of the last trained model
        
    

if __name__ == '__main__':

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
    FEATURES = [
    "stone_color_feature", 
    "ones", 
    "turns_since_move", 
    "liberties",
    "liberties_after"
    "capture_size",
    "atari_size",  
    "sensibleness", 
    "zeros"
    ]
    conv = ft.Preprocess(FEATURES)
    conv_ = ft.Preprocess(FEATURES_)
    learning_rate=0.001
    optimizer = SGD(lr=learning_rate)

    print("Creating players...")
    # SL model created by Mathias
    f_m = "models/supervised-learning/model_26_2_19h53.hdf5"
    policy_m = cnn_policy.CNN()
    policy_m.load(f_m)
    policy_m.model.compile(loss='categorical_crossentropy', optimizer=optimizer)
    player_m = pl.Player_pl(policy_m, conv)
    # SL model created by Evan
    f_e = "models/supervised-learning/model_temp.25.hdf5"
    policy_e = cnn_policy.CNN()
    policy_e.load(f_e)
    policy_e.model.compile(loss='categorical_crossentropy', optimizer=optimizer)
    player_e = pl.Player_pl(policy_e, conv_)
    # Adverserial player
    player_rd = pl.Player_rd(conv)
    opponent_rd = pl.Player_rd(conv)
    print ("-> Done")

    print ("Performances of the random adversarial player against itself...")
    play_game(player_rd, opponent_rd, 2, 19, False)

    nb_partie=100
    epoch=10
    verbose=False
    size=19

    print("Training of Adversarial against Mathias SL")
    policy = policy_m
    name= "M_random"
    play_learn(player_m, opponent_rd, nb_games, epoch, policy, name,  size, verbose)
    print('-> Done')

    print("Training of of Mathias SL against itself")
    name = "M_M"
    play_learn(player_m, opponent_m, nb_games, epoch, policy, name, size, verbose)
    print('-> Done')

    print("Training of Mathias SL against Evan SL")
    name = "M_E"
    play_learn(player_m, opponent_e,  nb_games, epoch, policy, name, size, verbose)
    print('-> Done')

    print("Training of Adversarial against Evan SL") 
    policy = policy_e
    name = "E_random"
    play_learn(player_e, opponent_rd, nb_games, epoch, policy_e, name, size, verbose)

    print("Training of Evan SL against itself")
    name = "E_E"
    play_learn(player_e, opponent_e, nb_partie, epoch, policy, name, size, verbose)

    print("Training of Evan SL against Mathias SL")
    name="E_M"
    play_learn(player_e, opponent_m, nb_games, epoch, policy, name, size, verbose)