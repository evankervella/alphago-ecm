import sgf_to_gs
import features as ft

# visualization of a GameState
def vis_gs(gs: object) -> None:
    x = 0
    size = len(gs.board)
    while x < size:
        y = 0
        string = ""
        while y < size:
            cell = gs.board[y, x] #v you have to intervert x and y here
            if  cell == -1:
                string += "W"
            if  cell == 0:
                string += "."
            if  cell == 1: 
                string += "B"
            string += " "
            y += 1
        print(string) 
        x += 1
    if gs.current_player == 1:
        print("current_player = Black")
    if gs.current_player ==- 1:
        print("current_player = White")

#visualization of a layer
def vis_layer(layer, num_layer: int) -> None:
    x = 0
    size = len(layer[num_layer,:,:])
    while x < size:
        string = ""
        y = 0
        while y < size:
            if layer[num_layer,y,x] == 1:  # you have to intervert x and y here
                string = string + " 1"    
            else:
                string = string + " ."
            y += 1
        print(string)
        x += 1
        
# visualization of a layer and associated GameState
def vis_gs_layer(gs: object, layer: int, num_layer: int) -> None:
    x = 0
    size = len(gs.board)
    while x < size:
        string = ""
        y = 0
        string = ""
        # display the GameState
        while y < size:
            cell = gs.board[y,x] # you have to intervert x and y here
            if  cell == -1:
                string += "W"
            if  cell == 0:
                string += "."
            if  cell == 1: 
                string += "B"
            string += " "
            y += 1
        # display the layer
        string += "          "
        y = 0
        while y < size:
            if layer[num_layer,y,x]==1: # you have to intervert x and y here
                string = string + " 1"    
            else:
                string = string + " ."
            y += 1
        print(string) 
        x += 1