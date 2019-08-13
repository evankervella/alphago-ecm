import CNN_policy
import numpy as np
import go
import features as ft
import visualisation as vis
import sys

def conv_mat(position: tuple, size: int) -> int:   
    """Converts matrix indices [x][y] into liste[x*size+y] indices
    """
    (x, y) = position
    return x * size + y

def conv_lis(position: int, size :int) -> tuple:
    """Oposite of conv_mat
    """
    y = position % size
    x = (position-y) / size
    #print(x)
    #print(y)
    return (x.astype(int),y.astype(int))

class Player_rd(object):
    """A random player
    """
    def __init__(self, convertor):
        # so we can execute `play_game`
        self.convertor = convertor
        return
    
    def get_move(self, state: object) -> int:
        if len(state.history) > 100 and state.history[-3] == go.PASS_MOVE:
        	return go.PASS_MOVE
        # list with sensible moves
        sensible_moves = [move for move in state.get_legal_moves(include_eyes=False)]        
        if len(sensible_moves) > 0:
            a=np.random.randint(0,len(sensible_moves),1) #on prend un coup au hasard
            return(sensible_moves[a[0]])
        return go.PASS_MOVE


class Player_pl(object): 
    """Plays the most probable move after the policy
    """
    def __init__(self, policy_function, convertor) -> None:
        self.policy = policy_function
        self.convertor=convertor
       
    def eval_state(self, state: tuple, moves: list=None): -> list
        """Outputs the probability to play each move after the policy
        """
        if len(moves) == 0:
            return []
        tensor = self.convertor.state_to_tensor(state) 
        network_output = self.policy.pred(tensor)  
        move_indices = [conv_mat(m, state.size) for m in moves] 

        # TODO: get network activations at legal move locations
        distribution = network_output[0][move_indices] 
        return distribution
    
    def get_move(self, state: object) -> int:
        # list with sensible moves
        sensible_moves = [move for move in state.get_legal_moves(include_eyes=False)]
             
        if len(state.history) > 100 and state.history[-3] == go.PASS_MOVE:
        	return go.PASS_MOVE

        # Read the possible moves and outputs the best after the policy
        if len(sensible_moves) > 0:
            move_probs = self.eval_state(state, sensible_moves)
        else:
            return go.PASS_MOVE

        move_ = (-1,-1) # init
        while state.is_legal(move_) != True: # if the `move_` is illegal we pass
            max_prob = np.argmax(move_probs) # takes the most probable `move`
            move_ = conv_lis(max_prob, state.size)               
            move_probs= np.delete(move_probs, max_prob)
            if len(move_probs)==0:
                sensible_moves = [move for move in state.get_legal_moves(include_eyes=False)]        
                if len(sensible_moves) > 0:
                    random_move = np.random.randint(0,len(sensible_moves), 1)
                    return(sensible_moves[random_move[0]])
                return go.PASS_MOVE

        return move_       


class Player_human(object):
    def __init__(self, convertor):
        # so we can execute `play_game`
        self.convertor = convertor
        return
    
    def get_move(self, state: object) -> tuple:
        # list with sensible moves
        move_ = (-1,-1)
        while state.is_legal(move_) != True:
            move_ = eval(raw_input("Enter coordinates:"))
            if move_ == 0:
                return go.PASS_MOVE 
            if state.is_legal(move_) != True:
                print("Illegal move, try something else!")
        return move_