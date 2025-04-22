import os
import sys
import copy
from game.shakki import Shakki


sys.setrecursionlimit(10**6)

dirname = os.path.dirname(__file__)

class Engine:
    def __init__(self,depth = 2, shakki=Shakki()):
        self.peli = shakki
        self.depth = depth
        self.weightboard = [[1,1,1,1,1,1,1,1],
                            [1,2,2,2,2,2,2,1],
                            [1,2,3,3,3,3,2,1],
                            [1,2,3,4,4,3,2,1],
                            [1,2,3,4,4,3,2,1],
                            [1,2,3,3,3,3,2,1],
                            [1,2,2,2,2,2,2,1],
                            [1,1,1,1,1,1,1,1]]

    def make_move(self):
        dupeboard = copy.deepcopy(self.peli.lauta)
        choice_as_uci = self.alphabeta(dupeboard,self.depth,float("-inf"),float("inf"),self.peli.whitetomove)[1]
        choice = self.move_as_grid_coordinates(choice_as_uci)
        self.peli.execute_move(choice[0],choice[1],choice[2],choice[3])

    def move_as_grid_coordinates(self, uci_move:str):
        quad = [0,0,0,0]
        if uci_move == None:
            return quad
        reverse_style_dict_UCI = {"a":0,"b":1,"c":2,"d":3,"e":4,"f":5,"g":6,"h":7,"8":0,"7":1,"6":2,"5":3,"4":4,"3":5,"2":6,"1":7}
        quad[1] = reverse_style_dict_UCI[uci_move[0]]
        quad[0] = reverse_style_dict_UCI[uci_move[1]]
        quad[3] = reverse_style_dict_UCI[uci_move[2]]-quad[1]
        quad[2] = reverse_style_dict_UCI[uci_move[3]]-quad[0]
        return quad
    
    def alphabeta(self,lauta, depth,alpha,beta,maximizing_player):
        best_move = None

        siirtolista = self.generate_movelist(lauta,maximizing_player)   

        if depth == 0:
            return self.dumb_heuristic(lauta,maximizing_player,siirtolista), best_move
        
        else:
            if siirtolista == []:
                if maximizing_player:
                    if self.peli.king_threatened(lauta,maximizing_player):
                        return float("-inf"), best_move
                    return 0, best_move
                else:
                    if self.peli.king_threatened(lauta,maximizing_player):
                        return float("inf"), best_move
                    return 0, best_move
            
        if maximizing_player:
            value = float("-inf")
            for siirto in siirtolista:
                siirtodata = self.move_as_grid_coordinates(siirto)
                x = siirtodata[0]
                y = siirtodata[1]
                dx = siirtodata[2]
                dy = siirtodata[3]
                piece = lauta[x][y]
                target_sqr = lauta[x+dx][y+dy]
                newboard = self.generate_board(x,y,dx,dy,lauta)
                value = max(value,self.alphabeta(newboard,depth-1,alpha,beta,False)[0])
                self.revert_board(x,y,dx,dy,target_sqr,piece,lauta)
                if value >= beta:
                    break
                if value > alpha:
                    alpha = value
                    best_move = siirto    
            if best_move == None:
                best_move = siirtolista[0]
            return value, best_move
        else:
            value = float("inf")
            for siirto in siirtolista:
                siirtodata = self.move_as_grid_coordinates(siirto)
                x = siirtodata[0]
                y = siirtodata[1]
                dx = siirtodata[2]
                dy = siirtodata[3]
                piece = lauta[x][y]
                target_sqr = lauta[x+dx][y+dy]
                newboard = self.generate_board(x,y,dx,dy,lauta)
                value = min(value,self.alphabeta(newboard,depth-1,alpha,beta,True)[0])
                self.revert_board(x,y,dx,dy,target_sqr,piece,lauta)
                if value <= alpha:
                    break
                if value < beta:
                    beta = value 
                    best_move = siirto
            if best_move == None:
                best_move = siirtolista[0]
            return value, best_move       

    def generate_movelist(self,board, maxplayer):
        sortedlist = self.peli.return_move_list(board,maxplayer)
        sortedlist.sort(key=len, reverse = True)

        return sortedlist
    
    def generate_board(self,x,y,dx,dy,board):
        piece = board[x][y]
        if piece == 1:
            if x+dx == 7:
                board[x+dx][y+dy] == 6
        elif piece == -1:
            if x+dx == 0:
                board[x+dx][y+dy] == -6
        else:
            board[x+dx][y+dy] = piece
        board[x][y] = 0

        return board
    
    def revert_board(self,x,y,dx,dy,target_sqr, piece ,board):
        board[x][y] = piece
        board[x+dx][y+dy] = target_sqr
        return board

    def return_board_repetitions(self,board):
        rval = self.peli.draw_by_repetition.get(self.peli.get_board_as_FEN(board))
        if rval == None:
            return 0
        return rval
        
    def crude_control_heuristic(self,lauta):
        white_control = self.peli.return_control_list(lauta,True)
        black_control = self.peli.return_control_list(lauta,False)
        sum = 0
        n_white = len(white_control)
        n_black = len(black_control)
        for i in range(max(n_white,n_black)):
            if i < n_white:
                sum += self.weightboard[white_control[i][0]][white_control[i][1]]
            if i < n_black:
                sum -= self.weightboard[black_control[i][0]][black_control[i][1]]
        return sum
    
    def material_difference(self,lauta):
        sum = 0
        for i in range(len(lauta)):
            for j in range(len(lauta)):
                sum += lauta[i][j]
        return sum
    
    def dumb_heuristic(self, lauta, maximizing_player, siirtolista):
        if siirtolista == []:
            if maximizing_player:
                if self.peli.king_threatened(lauta,maximizing_player):
                    return float("-inf")
                return 0
            else:
                if self.peli.king_threatened(lauta,maximizing_player):
                    return float("inf")
                return 0

        mat_diff = self.material_difference(lauta)
        pch = self.crude_control_heuristic(lauta)

        if mat_diff == 0:
            return pch/100
        
        return mat_diff+pch/100  
                  