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

        self.mapped_values = {1:100,3:320,4:330,5:500,6:900, 7:20000,-1:-100,-3:-320,-4:-330,-5:-500,-6:-900, -7:-20000, 0:0}

        self.white_king_pos = (7,4)
        self.black_king_pos = (0,4)

        self.movelist_white = []
        self.threatlist_white = []
        self.movelist_black = []
        self.threatlist_black = []
        self.piece_positions_all = []

        self.generate_supporting_lists()


        self.pawn_pos_table = [[0,   0,   0,   0,   0,   0, 0, 0],
                               [50, 50, 50, 50, 50, 50, 50, 50],
                                [10, 10, 20, 30, 30, 20, 10, 10],
                                [5,  5, 10, 25, 25, 10,  5,  5],
                                [0,  0,  0, 20, 20,  0,  0,  0],
                                [5, -5,-10,  0,  0,-10, -5,  5],
                                [5, 10, 10,-20,-20, 10, 10,  5],
                               [0,  0,  0,  0,  0,  0,  0,  0]]

        self.knight_pos_table = [[-50,-40,-30,-30,-30,-30,-40,-50,],
                                [-40,-20,  0,  0,  0,  0,-20,-40],
                                [-30,  0, 10, 15, 15, 10,  0,-30],
                                [-30,  5, 15, 20, 20, 15,  5,-30],
                                [-30,  0, 15, 20, 20, 15,  0,-30],
                                [-30,  5, 10, 15, 15, 10,  5,-30],
                                [-40,-20,  0,  5,  5,  0,-20,-40],
                                [-50,-40,-30,-30,-30,-30,-40,-50]]

        self.bishop_pos_table = [[-20,-10,-10,-10,-10,-10,-10,-20],
                                [-10,  0,  0,  0,  0,  0,  0,-10],
                                [-10,  0,  5, 10, 10,  5,  0,-10],
                                [-10,  5,  5, 10, 10,  5,  5,-10],
                                [-10,  0, 10, 10, 10, 10,  0,-10],
                                [-10, 10, 10, 10, 10, 10, 10,-10],
                                [-10,  5,  0,  0,  0,  0,  5,-10],
                                [-20,-10,-10,-10,-10,-10,-10,-20]]

        self.rook_pos_table = [[0,  0,  0,  0,  0,  0,  0,  0],
                                [5, 10, 10, 10, 10, 10, 10,  5],
                                [-5,  0,  0,  0,  0,  0,  0, -5],
                                [-5,  0,  0,  0,  0,  0,  0, -5],
                                [-5,  0,  0,  0,  0,  0,  0, -5],
                                [-5,  0,  0,  0,  0,  0,  0, -5],
                                [-5,  0,  0,  0,  0,  0,  0, -5],
                                [0,  0,  0,  5,  5,  0,  0,  0]]

        self.queen_pos_table = [[-20,-10,-10, -5, -5,-10,-10,-20],
                                [-10,  0,  0,  0,  0,  0,  0,-10],
                                [-10,  0,  5,  5,  5,  5,  0,-10],
                                [-5,  0,  5,  5,  5,  5,  0, -5],
                                [0,  0,  5,  5,  5,  5,  0, -5],
                                [-10,  5,  5,  5,  5,  5,  0,-10],
                                [-10,  0,  5,  0,  0,  0,  0,-10],
                                [-20,-10,-10, -5, -5,-10,-10,-20]]

        self.king_pos_table = [[-30,-40,-40,-50,-50,-40,-40,-30,],
                                [-30,-40,-40,-50,-50,-40,-40,-30,],
                                [-30,-40,-40,-50,-50,-40,-40,-30,],
                                [-30,-40,-40,-50,-50,-40,-40,-30,],
                                [-20,-30,-30,-40,-40,-30,-30,-20],
                                [-10,-20,-20,-20,-20,-20,-20,-10],
                                [ 20, 20,  0,  0,  0,  0, 20, 20],
                                [20, 30, 10,  0,  0, 10, 30, 20]]

    def make_move(self):
        self.generate_supporting_lists()
        dupeboard = self.peli.lauta[:]

        piece_eval = 0

        for i in range(8):
            for j in range(8):
                piece = dupeboard[i][j]
                if piece != 0:
                    piece_eval += self.mapped_values.get(piece)

        choice = self.alphabeta(dupeboard,self.depth,float("-inf"),float("inf"),self.peli.whitetomove,piece_eval,self.movelist_white,self.movelist_black,self.threatlist_white, self.threatlist_black)[1]
        
        #print("I chose:", self.move_as_UCI(choice))
        self.peli.execute_move(choice[1],choice[2],choice[3]-choice[1],choice[4]-choice[2])

    def move_as_UCI(self,movetuple):
        style_dict_UCI_row = { 0:"a",1:"b",2:"c",3: "d",4:"e",5:"f",6:"g",7:"h"}
        style_dict_UCI_file = { 0:"8",1:"7",2:"6",3: "5",4:"4",5:"3",6:"2",7:"1"}
        return style_dict_UCI_row[movetuple[2]] + style_dict_UCI_file[movetuple[1]] + style_dict_UCI_row[movetuple[4]] + style_dict_UCI_file[movetuple[3]]

    def alphabeta(self,lauta, depth,alpha,beta,maximizing_player,piece_eval,movelist_white, movelist_black, threatlist_white, threatlist_black):
        best_move = None
        
        if maximizing_player:
            mbyempty = movelist_white
        else:
            mbyempty = movelist_black

        if mbyempty == []:
            if maximizing_player:
                for item in threatlist_black:
                    if item[3] == self.white_king_pos[0] and item[4] == self.white_king_pos[1]:
                        return -100000-depth, best_move
                return 0, best_move
            else:
                for item in threatlist_white:
                    if item[3] == self.black_king_pos[0] and item[4] == self.black_king_pos[1]:
                        return 100000+depth, best_move
                return 0, best_move

        if depth == 0:
            return self.heuristic_function(self.piece_positions_all,piece_eval), best_move
        
        siirtolista = self.sort_movelist(mbyempty,maximizing_player)

        if maximizing_player:
            value = -1000000
            for siirto in siirtolista:
                copymovewhite = movelist_white[:]
                copymoveblack = movelist_black[:]
                copythreatwhite = threatlist_white[:]
                copythreatblack = threatlist_black[:]

                piece = siirto[0]
                x = siirto[1]
                y = siirto[2]
                dx = siirto[3]
                dy = siirto[4]
                target_sqr = lauta[dx][dy]

                self.manage_board(x,y,dx,dy,lauta)

                quadtuple = self.manage_list_states(piece,x,y,dx,dy,maximizing_player,lauta,copymovewhite, copymoveblack, copythreatwhite, copythreatblack)
                piece_eval -= self.mapped_values.get(target_sqr)

                #piece eval muutos jos promotion
                piece_eval -= self.mapped_values.get(piece)
                piece_eval += self.mapped_values.get(lauta[dx][dy])                

                value = max(value,self.alphabeta(lauta,depth-1,alpha,beta,False,piece_eval,quadtuple[0], quadtuple[1], quadtuple[2], quadtuple[3])[0])                

                piece_eval += self.mapped_values.get(target_sqr) 
                piece_eval += self.mapped_values.get(piece)
                piece_eval -= self.mapped_values.get(lauta[dx][dy])

                self.revert_board(x,y,dx,dy,target_sqr,piece,lauta)
                if value >= beta:
                    break
                if value > alpha:
                    best_move = siirto 
                    alpha = max(alpha,value)

            return value, best_move

        else:
            value = 1000000
            for siirto in siirtolista:
                copymovewhite = movelist_white[:]
                copymoveblack = movelist_black[:]
                copythreatwhite = threatlist_white[:]
                copythreatblack = threatlist_black[:]

                piece = siirto[0]
                x = siirto[1]
                y = siirto[2]
                dx = siirto[3]
                dy = siirto[4]
                target_sqr = lauta[dx][dy]
                self.manage_board(x,y,dx,dy,lauta)
               
                quadtuple = self.manage_list_states(piece,x,y,dx,dy,maximizing_player,lauta,copymovewhite, copymoveblack, copythreatwhite, copythreatblack)
                piece_eval -= self.mapped_values.get(target_sqr)

                #piece eval muutos jos promotion
                piece_eval -= self.mapped_values.get(piece)
                piece_eval += self.mapped_values.get(lauta[dx][dy])

                value = min(value,self.alphabeta(lauta,depth-1,alpha,beta,True,piece_eval,quadtuple[0], quadtuple[1], quadtuple[2], quadtuple[3])[0])  

                piece_eval += self.mapped_values.get(target_sqr) 
                piece_eval += self.mapped_values.get(piece)
                piece_eval -= self.mapped_values.get(lauta[dx][dy])

                self.revert_board(x,y,dx,dy,target_sqr,piece,lauta)

                if value <= alpha:
                    break
                if value < beta:
                    best_move = siirto
                    beta = min(beta, value)

            return value, best_move   

    def generate_supporting_lists(self,board=[]):
        if board == []:
            board = self.peli.lauta

        self.movelist_white = []
        self.threatlist_white = []
        self.movelist_black = []
        self.threatlist_black = []
        self.piece_positions_all = []

        for i in range(8):
            for j in range(8):
                piece = board[i][j]
                if piece != 0:
                    self.piece_positions_all.append((piece, i, j))

        for i in range(8):
            for j in range(8):
                piece = board[i][j]
                if piece > 0:
                    if piece == 7:
                        self.white_king_pos = (i,j)  
                    move_threat_tuple = self.generate_move_threat_all(i,j,abs(piece),True,board)
                    self.movelist_white.extend(move_threat_tuple[0])
                    self.threatlist_white.extend(move_threat_tuple[1])
                elif piece < 0:
                    if piece == -7:
                        self.black_king_pos = (i,j) 
                    move_threat_tuple = self.generate_move_threat_all(i,j,abs(piece),False,board)
                    self.movelist_black.extend(move_threat_tuple[0])
                    self.threatlist_black.extend( move_threat_tuple[1])   

    def generate_move_threat_all(self,x,y, piecenmbr, maximizing_player,board):
        movelist = []
        threatlist = []
        if piecenmbr == 1:
            move_threat_tuple = self.generate_move_threat_pawn(x,y,piecenmbr,maximizing_player,board)
            movelist.extend(move_threat_tuple[0])
            threatlist.extend(move_threat_tuple[1])
        elif piecenmbr == 3:
            move_threat_tuple = self.generate_move_threat_knight(x,y,piecenmbr,maximizing_player,board)
            movelist.extend(move_threat_tuple[0])
            threatlist.extend(move_threat_tuple[1])
        elif piecenmbr == 4:
            move_threat_tuple = self.generate_move_threat_bishop(x,y,piecenmbr,maximizing_player,board)
            movelist.extend(move_threat_tuple[0])
            threatlist.extend(move_threat_tuple[1])
        elif piecenmbr == 5:
            move_threat_tuple = self.generate_move_threat_rook(x,y,piecenmbr,maximizing_player,board)
            movelist.extend(move_threat_tuple[0])
            threatlist.extend(move_threat_tuple[1])
        elif piecenmbr == 6:
            move_threat_tuple = self.generate_move_threat_queen(x,y,piecenmbr,maximizing_player,board)
            movelist.extend(move_threat_tuple[0])
            threatlist.extend(move_threat_tuple[1])
        elif piecenmbr == 7:
            threat_king = self.generate_threat_king(x,y,piecenmbr,maximizing_player,board)
            threatlist.extend(threat_king)
            move_king = self.generate_move_king(x,y,piecenmbr,maximizing_player,board)
            movelist.extend(move_king)

        return movelist, threatlist    

    def generate_move_threat_pawn(self,x,y,piecenmbr, maximizing_player,board):  
        movelist = []
        threatlist = []

        if maximizing_player:
            cmod = 1
            if 0<= x-1 < 8:
                if board[x-1][y] == 0:
                    if self.king_not_checked_after_move(x,y,x-1,y,board,maximizing_player):
                        movelist.append((cmod*piecenmbr,x,y,x-1,y))
                if 0 <= y-1 <8:
                    if board[x-1][y-1] in {-1,-3,-4,-5,-6}:
                        if self.king_not_checked_after_move(x,y,x-1,y-1,board,maximizing_player):    
                            movelist.append((cmod*piecenmbr,x,y,x-1,y-1))
                    threatlist.append((cmod*piecenmbr,x,y,x-1,y-1))
                if 0 <= y+1 <8:
                    if board[x-1][y+1] in {-1,-3,-4,-5,-6}:
                        if self.king_not_checked_after_move(x,y,x-1,y+1,board,maximizing_player):
                            movelist.append((cmod*piecenmbr,x,y,x-1,y+1))
                    threatlist.append((cmod*piecenmbr,x,y,x-1,y+1))
            if x == 6:
                if board[x-1][y] == 0 and board[x-2][y] == 0:
                    if self.king_not_checked_after_move(x,y,x-2,y,board,maximizing_player):
                        movelist.append((cmod*piecenmbr,x,y,x-2,y)) 
        else:       
            cmod = -1

            if 0<= x+1 < 8:
                if board[x+1][y] == 0:
                    if self.king_not_checked_after_move(x,y,x+1,y,board,maximizing_player):
                        movelist.append((cmod*piecenmbr,x,y,x+1,y))
                if 0 <= y-1 <8:
                    if board[x+1][y-1] in {1,3,4,5,6}:
                        if self.king_not_checked_after_move(x,y,x+1,y-1,board,maximizing_player):
                            movelist.append((cmod*piecenmbr,x,y,x+1,y-1))
                    threatlist.append((cmod*piecenmbr,x,y,x+1,y-1))
                if 0 <= y+1 <8:
                    if board[x+1][y+1] in {1,3,4,5,6}:
                        if self.king_not_checked_after_move(x,y,x+1,y+1,board,maximizing_player):
                            movelist.append((cmod*piecenmbr,x,y,x+1,y+1))
                    threatlist.append((cmod*piecenmbr,x,y,x+1,y+1))
            if x == 1:
                if board[x+1][y] == 0 and board[x+2][y] == 0:
                    if self.king_not_checked_after_move(x,y,x+2,y,board,maximizing_player):
                        movelist.append((cmod*piecenmbr,x,y,x+2,y))
        return movelist , threatlist
    
    def generate_move_threat_knight(self,x,y,piecenmbr, maximizing_player,board):  
        movelist = []
        threatlist = []
        cmod = -1
        if maximizing_player:
            cmod = 1
        if 0<= x-2 < 8 and 0 <= y-1 <8:
            threatlist.append((cmod*piecenmbr,x,y,x-2,y-1))
            if board[x-2][y-1] not in {cmod*1,cmod*3,cmod*4,cmod*5,cmod*6,cmod*7}:
                if self.king_not_checked_after_move(x,y,x-2,y-1,board,maximizing_player):
                    movelist.append((cmod*piecenmbr,x,y,x-2,y-1))
        if 0<= x-2 < 8 and 0 <= y+1 <8:
            threatlist.append((cmod*piecenmbr,x,y,x-2,y+1))
            if board[x-2][y+1] not in {cmod*1,cmod*3,cmod*4,cmod*5,cmod*6,cmod*7}:
                if self.king_not_checked_after_move(x,y,x-2,y+1,board,maximizing_player):
                    movelist.append((cmod*piecenmbr,x,y,x-2,y+1))
        if 0<= x-1 < 8 and 0 <= y-2 <8:
            threatlist.append((cmod*piecenmbr,x,y,x-1,y-2))
            if board[x-1][y-2] not in {cmod*1,cmod*3,cmod*4,cmod*5,cmod*6,cmod*7}:
                if self.king_not_checked_after_move(x,y,x-1,y-2,board,maximizing_player):
                    movelist.append((cmod*piecenmbr,x,y,x-1,y-2))
        if 0<= x-1 < 8 and 0 <= y+2 <8:
            threatlist.append((cmod*piecenmbr,x,y,x-1,y+2))
            if board[x-1][y+2] not in {cmod*1,cmod*3,cmod*4,cmod*5,cmod*6,cmod*7}:
                if self.king_not_checked_after_move(x,y,x-1,y+2,board,maximizing_player):
                    movelist.append((cmod*piecenmbr,x,y,x-1,y+2))
        if 0<= x+2 < 8 and 0 <= y+1 <8:
            threatlist.append((cmod*piecenmbr,x,y,x+2,y+1))
            if board[x+2][y+1] not in {cmod*1,cmod*3,cmod*4,cmod*5,cmod*6,cmod*7}:
                if self.king_not_checked_after_move(x,y,x+2,y+1,board,maximizing_player):
                    movelist.append((cmod*piecenmbr,x,y,x+2,y+1))
        if 0<= x+2 < 8 and 0 <= y-1 <8:
            threatlist.append((cmod*piecenmbr,x,y,x+2,y-1))
            if board[x+2][y-1] not in {cmod*1,cmod*3,cmod*4,cmod*5,cmod*6,cmod*7}:
                if self.king_not_checked_after_move(x,y,x+2,y-1,board,maximizing_player):
                    movelist.append((cmod*piecenmbr,x,y,x+2,y-1))
        if 0<= x+1 < 8 and 0 <= y-2 <8:
            threatlist.append((cmod*piecenmbr,x,y,x+1,y-2))
            if board[x+1][y-2] not in {cmod*1,cmod*3,cmod*4,cmod*5,cmod*6,cmod*7}:
                if self.king_not_checked_after_move(x,y,x+1,y-2,board,maximizing_player):
                    movelist.append((cmod*piecenmbr,x,y,x+1,y-2))
        if 0<= x+1 < 8 and 0 <= y+2 <8:
            threatlist.append((cmod*piecenmbr,x,y,x+1,y+2))
            if board[x+1][y+2] not in {cmod*1,cmod*3,cmod*4,cmod*5,cmod*6,cmod*7}:
                if self.king_not_checked_after_move(x,y,x+1,y+2,board,maximizing_player):
                    movelist.append((cmod*piecenmbr,x,y,x+1,y+2))
        return movelist , threatlist
    
    def generate_move_threat_bishop(self,x,y,piecenmbr,maximizing_player, board):
        movelist = []
        threatlist = []
        n = 8
        cmod = -1
        if maximizing_player:
            cmod = 1
        blocked_diagonals = [True,True,True,True]
        for dz in range(1,n):
            if blocked_diagonals[0]:
                if 0<= x+dz <8 and 0<= y+dz <8:
                    threatlist.append((cmod*piecenmbr,x,y,x+dz,y+dz))  
                    if board[x+dz][y+dz] not in {cmod*1,cmod*3,cmod*4,cmod*5,cmod*6,cmod*7,-cmod*7}:
                        if self.king_not_checked_after_move(x,y,x+dz,y+dz,board,maximizing_player):
                            movelist.append((cmod*piecenmbr,x,y,x+dz,y+dz))  
                            if board[x+dz][y+dz] in {-cmod*1,-cmod*3,-cmod*4,-cmod*5,-cmod*6}:
                                blocked_diagonals[0] = False
                    else:
                        blocked_diagonals[0] = False
                else:
                    blocked_diagonals[0] = False
            if blocked_diagonals[1]:        
                if 0<= x+dz <8 and 0<= y-dz <8:
                    threatlist.append((cmod*piecenmbr,x,y,x+dz,y-dz))  
                    if board[x+dz][y-dz] not in {cmod*1,cmod*3,cmod*4,cmod*5,cmod*6,cmod*7,-cmod*7}:
                        if self.king_not_checked_after_move(x,y,x+dz,y-dz,board,maximizing_player):
                            movelist.append((cmod*piecenmbr,x,y,x+dz,y-dz))
                            if board[x+dz][y-dz] in {-cmod*1,-cmod*3,-cmod*4,-cmod*5,-cmod*6}:
                                blocked_diagonals[1] = False
                    else:
                        blocked_diagonals[1] = False
                else:
                    blocked_diagonals[1] = False
            if blocked_diagonals[2]:   
                if 0<= x-dz <8 and 0<= y+dz <8:
                    threatlist.append((cmod*piecenmbr,x,y,x-dz,y+dz))  
                    if board[x-dz][y+dz] not in {cmod*1,cmod*3,cmod*4,cmod*5,cmod*6,cmod*7,-cmod*7}:
                        if self.king_not_checked_after_move(x,y,x-dz,y+dz,board,maximizing_player):
                            movelist.append((cmod*piecenmbr,x,y,x-dz,y+dz)) 
                            if board[x-dz][y+dz] in {-cmod*1,-cmod*3,-cmod*4,-cmod*5,-cmod*6}:
                                blocked_diagonals[2] = False
                    else:
                        blocked_diagonals[2] = False
                else:
                    blocked_diagonals[2] = False
            if blocked_diagonals[3]:
                if 0<= x-dz <8 and 0<= y-dz <8:
                    threatlist.append((cmod*piecenmbr,x,y,x-dz,y-dz))  
                    if board[x-dz][y-dz] not in {cmod*1,cmod*3,cmod*4,cmod*5,cmod*6,cmod*7,-cmod*7}:
                        if self.king_not_checked_after_move(x,y,x-dz,y-dz,board,maximizing_player):
                            movelist.append((cmod*piecenmbr,x,y,x-dz,y-dz))
                            if board[x-dz][y-dz] in {-cmod*1,-cmod*3,-cmod*4,-cmod*5,-cmod*6}:
                                blocked_diagonals[3] = False
                    else:
                        blocked_diagonals[3] = False
                else:
                    blocked_diagonals[3] = False
            if True not in blocked_diagonals:
                break
        return movelist,threatlist  

    def generate_move_threat_rook(self,x,y,piecenmbr,maximizing_player, board): 
        movelist = []
        threatlist = []
        n = 8
        cmod = -1
        if maximizing_player:
            cmod = 1
        blocked_files = [True,True,True,True]
        for dz in range(1,n):
            if blocked_files[0]:
                if 0<= x+dz <8:
                    threatlist.append((cmod*piecenmbr,x,y,x+dz,y))  
                    if board[x+dz][y] not in {cmod*1,cmod*3,cmod*4,cmod*5,cmod*6,cmod*7,-cmod*7}:
                        if self.king_not_checked_after_move(x,y,x+dz,y,board,maximizing_player):
                            movelist.append((cmod*piecenmbr,x,y,x+dz,y))  
                            if board[x+dz][y] in {-cmod*1,-cmod*3,-cmod*4,-cmod*5,-cmod*6}:
                                blocked_files[0] = False
                    else:
                        blocked_files[0] = False
                else:
                    blocked_files[0] = False
            if blocked_files[1]:        
                if 0<= x-dz <8:
                    threatlist.append((cmod*piecenmbr,x,y,x-dz,y))  
                    if board[x-dz][y] not in {cmod*1,cmod*3,cmod*4,cmod*5,cmod*6,cmod*7,-cmod*7}:
                        if self.king_not_checked_after_move(x,y,x-dz,y,board,maximizing_player):
                            movelist.append((cmod*piecenmbr,x,y,x-dz,y))
                            if board[x-dz][y] in {-cmod*1,-cmod*3,-cmod*4,-cmod*5,-cmod*6}:
                                blocked_files[1] = False
                    else:
                        blocked_files[1] = False
                else:
                    blocked_files[1] = False
            if blocked_files[2]:   
                if 0<= y+dz <8:
                    threatlist.append((cmod*piecenmbr,x,y,x,y+dz))  
                    if board[x][y+dz] not in {cmod*1,cmod*3,cmod*4,cmod*5,cmod*6,cmod*7,-cmod*7}:
                        if self.king_not_checked_after_move(x,y,x,y+dz,board,maximizing_player):
                            movelist.append((cmod*piecenmbr,x,y,x,y+dz)) 
                            if board[x][y+dz] in {-cmod*1,-cmod*3,-cmod*4,-cmod*5,-cmod*6}:
                                blocked_files[2] = False
                    else:
                        blocked_files[2] = False
                else:
                    blocked_files[2] = False
            if blocked_files[3]:
                if 0<= y-dz <8:
                    threatlist.append((cmod*piecenmbr,x,y,x,y-dz))  
                    if board[x][y-dz] not in {cmod*1,cmod*3,cmod*4,cmod*5,cmod*6,cmod*7,-cmod*7}:
                        if self.king_not_checked_after_move(x,y,x,y-dz,board,maximizing_player):
                            movelist.append((cmod*piecenmbr,x,y,x,y-dz))
                            if board[x][y-dz] in {-cmod*1,-cmod*3,-cmod*4,-cmod*5,-cmod*6}:
                                blocked_files[3] = False
                    else:
                        blocked_files[3] = False
                else:
                    blocked_files[3] = False
            if True not in blocked_files:
                break    
        return movelist , threatlist
    
    def generate_move_threat_queen(self,x,y,piecenmbr,maximizing_player, board):
        movelist = []
        threatlist = []
        n = 8
        cmod = -1
        if maximizing_player:
            cmod = 1
        blocked_diagonals = [True,True,True,True]
        blocked_files = [True,True,True,True]
        for dz in range(1,n):
            if blocked_files[0]:
                if 0<= x+dz <8:
                    threatlist.append((cmod*piecenmbr,x,y,x+dz,y))  
                    if board[x+dz][y] not in {cmod*1,cmod*3,cmod*4,cmod*5,cmod*6,cmod*7,-cmod*7}:
                        if self.king_not_checked_after_move(x,y,x+dz,y,board,maximizing_player):
                            movelist.append((cmod*piecenmbr,x,y,x+dz,y))  
                            if board[x+dz][y] in {-cmod*1,-cmod*3,-cmod*4,-cmod*5,-cmod*6}:
                                blocked_files[0] = False
                    else:
                        blocked_files[0] = False
                else:
                    blocked_files[0] = False
            if blocked_files[1]:        
                if 0<= x-dz <8:
                    threatlist.append((cmod*piecenmbr,x,y,x-dz,y))  
                    if board[x-dz][y] not in {cmod*1,cmod*3,cmod*4,cmod*5,cmod*6,cmod*7,-cmod*7}:
                        if self.king_not_checked_after_move(x,y,x-dz,y,board,maximizing_player):
                            movelist.append((cmod*piecenmbr,x,y,x-dz,y))
                            if board[x-dz][y] in {-cmod*1,-cmod*3,-cmod*4,-cmod*5,-cmod*6}:
                                blocked_files[1] = False
                    else:
                        blocked_files[1] = False
                else:
                    blocked_files[1] = False
            if blocked_files[2]:   
                if 0<= y+dz <8:
                    threatlist.append((cmod*piecenmbr,x,y,x,y+dz))  
                    if board[x][y+dz] not in {cmod*1,cmod*3,cmod*4,cmod*5,cmod*6,cmod*7,-cmod*7}:
                        if self.king_not_checked_after_move(x,y,x,y+dz,board,maximizing_player):
                            movelist.append((cmod*piecenmbr,x,y,x,y+dz))
                            if board[x][y+dz] in {-cmod*1,-cmod*3,-cmod*4,-cmod*5,-cmod*6}:
                                blocked_files[2] = False
                    else:
                        blocked_files[2] = False
                else:
                    blocked_files[2] = False
            if blocked_files[3]:
                if 0<= y-dz <8:
                    threatlist.append((cmod*piecenmbr,x,y,x,y-dz))  
                    if board[x][y-dz] not in {cmod*1,cmod*3,cmod*4,cmod*5,cmod*6,cmod*7,-cmod*7}:
                        if self.king_not_checked_after_move(x,y,x,y-dz,board,maximizing_player):
                            movelist.append((cmod*piecenmbr,x,y,x,y-dz))
                            if board[x][y-dz] in {-cmod*1,-cmod*3,-cmod*4,-cmod*5,-cmod*6}:
                                blocked_files[3] = False
                    else:
                        blocked_files[3] = False
                else:
                    blocked_files[3] = False
            if blocked_diagonals[0]:
                if 0<= x+dz <8 and 0<= y+dz <8:
                    threatlist.append((cmod*piecenmbr,x,y,x+dz,y+dz))  
                    if board[x+dz][y+dz] not in {cmod*1,cmod*3,cmod*4,cmod*5,cmod*6,cmod*7,-cmod*7}:
                        if self.king_not_checked_after_move(x,y,x+dz,y+dz,board,maximizing_player):
                            movelist.append((cmod*piecenmbr,x,y,x+dz,y+dz))  
                            if board[x+dz][y+dz] in {-cmod*1,-cmod*3,-cmod*4,-cmod*5,-cmod*6}:
                                blocked_diagonals[0] = False
                    else:
                        blocked_diagonals[0] = False
                else:
                    blocked_diagonals[0] = False
            if blocked_diagonals[1]:        
                if 0<= x+dz <8 and 0<= y-dz <8:
                    threatlist.append((cmod*piecenmbr,x,y,x+dz,y-dz))  
                    if board[x+dz][y-dz] not in {cmod*1,cmod*3,cmod*4,cmod*5,cmod*6,cmod*7,-cmod*7}:
                        if self.king_not_checked_after_move(x,y,x+dz,y-dz,board,maximizing_player):
                            movelist.append((cmod*piecenmbr,x,y,x+dz,y-dz))
                            if board[x+dz][y-dz] in {-cmod*1,-cmod*3,-cmod*4,-cmod*5,-cmod*6}:
                                blocked_diagonals[1] = False
                    else:
                        blocked_diagonals[1] = False
                else:
                    blocked_diagonals[1] = False
            if blocked_diagonals[2]:   
                if 0<= x-dz <8 and 0<= y+dz <8:
                    threatlist.append((cmod*piecenmbr,x,y,x-dz,y+dz))  
                    if board[x-dz][y+dz] not in {cmod*1,cmod*3,cmod*4,cmod*5,cmod*6,cmod*7,-cmod*7}:
                        if self.king_not_checked_after_move(x,y,x-dz,y+dz,board,maximizing_player):
                            movelist.append((cmod*piecenmbr,x,y,x-dz,y+dz)) 
                            if board[x-dz][y+dz] in {-cmod*1,-cmod*3,-cmod*4,-cmod*5,-cmod*6}:
                                blocked_diagonals[2] = False
                    else:
                        blocked_diagonals[2] = False
                else:
                    blocked_diagonals[2] = False
            if blocked_diagonals[3]:
                if 0<= x-dz <8 and 0<= y-dz <8:
                    threatlist.append((cmod*piecenmbr,x,y,x-dz,y-dz))  
                    if board[x-dz][y-dz] not in {cmod*1,cmod*3,cmod*4,cmod*5,cmod*6,cmod*7,-cmod*7}:
                        if self.king_not_checked_after_move(x,y,x-dz,y-dz,board,maximizing_player):
                            movelist.append((cmod*piecenmbr,x,y,x-dz,y-dz))
                            if board[x-dz][y-dz] in {-cmod*1,-cmod*3,-cmod*4,-cmod*5,-cmod*6}:
                                blocked_diagonals[3] = False
                    else:
                        blocked_diagonals[3] = False
                else:
                    blocked_diagonals[3] = False
            if True not in blocked_diagonals and True not in blocked_files:
                break
        return movelist, threatlist

    def generate_threatlists(self,board):
        threatlist_white = []
        threatlist_black = []
        for i in range(8):
            for j in range(8):
                piece = board[i][j]
                if piece > 0:
                    threatlist_white.extend(self.generate_threat_all(i,j,abs(piece),True,board))
                elif piece < 0:
                    threatlist_black.extend(self.generate_threat_all(i,j,abs(piece),False,board))
        
        return threatlist_white, threatlist_black
    
    def generate_threat_all(self,x,y, piecenmbr, maximizing_player,board):
        threatlist = []
        if piecenmbr == 1:
            threatlist.extend(self.generate_threat_pawn(x,y,piecenmbr,maximizing_player,board))
        elif piecenmbr == 3:
            threatlist.extend(self.generate_threat_knight(x,y,piecenmbr,maximizing_player,board))
        elif piecenmbr == 4:
            threatlist.extend(self.generate_threat_bishop(x,y,piecenmbr,maximizing_player,board))
        elif piecenmbr == 5:
           threatlist.extend(self.generate_threat_rook(x,y,piecenmbr,maximizing_player,board))
        elif piecenmbr == 6:
            threatlist.extend(self.generate_threat_queen(x,y,piecenmbr,maximizing_player,board))
        elif piecenmbr == 7:
            threatlist.extend(self.generate_threat_king(x,y,piecenmbr,maximizing_player,board))

        return threatlist    

    def generate_threat_pawn(self,x,y,piecenmbr, maximizing_player,board):  
        threatlist = []

        if maximizing_player:
            cmod = 1

            if 0<= x-1 < 8:
                if 0 <= y-1 <8:
                    threatlist.append((cmod*piecenmbr,x,y,x-1,y-1))
                if 0 <= y+1 <8:
                    threatlist.append((cmod*piecenmbr,x,y,x-1,y+1))
        else:       
            cmod = -1

            if 0<= x+1 < 8:
                if 0 <= y-1 <8:
                    threatlist.append((cmod*piecenmbr,x,y,x+1,y-1))
                if 0 <= y+1 <8:
                    threatlist.append((cmod*piecenmbr,x,y,x+1,y+1))

        return threatlist
    
    def generate_threat_knight(self,x,y,piecenmbr, maximizing_player,board):  
        threatlist = []
        cmod = -1
        if maximizing_player:
            cmod = 1
        if 0<= x-2 < 8 and 0 <= y-1 <8:
            threatlist.append((cmod*piecenmbr,x,y,x-2,y-1))
        if 0<= x-2 < 8 and 0 <= y+1 <8:
            threatlist.append((cmod*piecenmbr,x,y,x-2,y+1))
        if 0<= x-1 < 8 and 0 <= y-2 <8:
            threatlist.append((cmod*piecenmbr,x,y,x-1,y-2))
        if 0<= x-1 < 8 and 0 <= y+2 <8:
            threatlist.append((cmod*piecenmbr,x,y,x-1,y+2))
        if 0<= x+2 < 8 and 0 <= y+1 <8:
            threatlist.append((cmod*piecenmbr,x,y,x+2,y+1))
        if 0<= x+2 < 8 and 0 <= y-1 <8:
            threatlist.append((cmod*piecenmbr,x,y,x+2,y-1))
        if 0<= x+1 < 8 and 0 <= y-2 <8:
            threatlist.append((cmod*piecenmbr,x,y,x+1,y-2))
        if 0<= x+1 < 8 and 0 <= y+2 <8:
            threatlist.append((cmod*piecenmbr,x,y,x+1,y+2))

        return threatlist
    
    def generate_threat_bishop(self,x,y,piecenmbr,maximizing_player, board):
        threatlist = []
        n = 8
        cmod = -1
        if maximizing_player:
            cmod = 1
        blocked_diagonals = [True,True,True,True]
        for dz in range(1,n):
            if blocked_diagonals[0]:
                if 0<= x+dz <8 and 0<= y+dz <8:
                    threatlist.append((cmod*piecenmbr,x,y,x+dz,y+dz))  
                    if board[x+dz][y+dz] in {cmod*1,cmod*3,cmod*4,cmod*5,cmod*6,cmod*7,-cmod*1,-cmod*3,-cmod*4,-cmod*5,-cmod*6}:
                        blocked_diagonals[0] = False
                else:
                    blocked_diagonals[0] = False
            if blocked_diagonals[1]:        
                if 0<= x+dz <8 and 0<= y-dz <8:
                    threatlist.append((cmod*piecenmbr,x,y,x+dz,y-dz))  
                    if board[x+dz][y-dz] in {cmod*1,cmod*3,cmod*4,cmod*5,cmod*6,cmod*7,-cmod*1,-cmod*3,-cmod*4,-cmod*5,-cmod*6}:
                        blocked_diagonals[1] = False
                else:
                    blocked_diagonals[1] = False
            if blocked_diagonals[2]:   
                if 0<= x-dz <8 and 0<= y+dz <8:
                    threatlist.append((cmod*piecenmbr,x,y,x-dz,y+dz))  
                    if board[x-dz][y+dz] in {cmod*1,cmod*3,cmod*4,cmod*5,cmod*6,cmod*7,-cmod*1,-cmod*3,-cmod*4,-cmod*5,-cmod*6}:
                        blocked_diagonals[2] = False
                else:
                    blocked_diagonals[2] = False
            if blocked_diagonals[3]:
                if 0<= x-dz <8 and 0<= y-dz <8:
                    threatlist.append((cmod*piecenmbr,x,y,x-dz,y-dz))  
                    if board[x-dz][y-dz] in {cmod*1,cmod*3,cmod*4,cmod*5,cmod*6,cmod*7,-cmod*1,-cmod*3,-cmod*4,-cmod*5,-cmod*6}:
                        blocked_diagonals[3] = False
                else:
                    blocked_diagonals[3] = False
            if True not in blocked_diagonals:
                break
        return threatlist  

    def generate_threat_rook(self,x,y,piecenmbr,maximizing_player, board): 
        threatlist = []
        n = 8
        cmod = -1
        if maximizing_player:
            cmod = 1
        blocked_files = [True,True,True,True]
        for dz in range(1,n):
            if blocked_files[0]:
                if 0<= x+dz <8:
                    threatlist.append((cmod*piecenmbr,x,y,x+dz,y))  
                    if board[x+dz][y] in {cmod*1,cmod*3,cmod*4,cmod*5,cmod*6,cmod*7,-cmod*1,-cmod*3,-cmod*4,-cmod*5,-cmod*6}:
                        blocked_files[0] = False
                else:
                    blocked_files[0] = False
            if blocked_files[1]:        
                if 0<= x-dz <8:
                    threatlist.append((cmod*piecenmbr,x,y,x-dz,y))  
                    if board[x-dz][y] in {cmod*1,cmod*3,cmod*4,cmod*5,cmod*6,cmod*7,-cmod*1,-cmod*3,-cmod*4,-cmod*5,-cmod*6}:
                        blocked_files[1] = False
                else:
                    blocked_files[1] = False
            if blocked_files[2]:   
                if 0<= y+dz <8:
                    threatlist.append((cmod*piecenmbr,x,y,x,y+dz))  
                    if board[x][y+dz] in {cmod*1,cmod*3,cmod*4,cmod*5,cmod*6,cmod*7,-cmod*1,-cmod*3,-cmod*4,-cmod*5,-cmod*6}:
                        blocked_files[2] = False
                else:
                    blocked_files[2] = False
            if blocked_files[3]:
                if 0<= y-dz <8:
                    threatlist.append((cmod*piecenmbr,x,y,x,y-dz))  
                    if board[x][y-dz] in {cmod*1,cmod*3,cmod*4,cmod*5,cmod*6,cmod*7,-cmod*1,-cmod*3,-cmod*4,-cmod*5,-cmod*6}:
                        blocked_files[3] = False
                else:
                    blocked_files[3] = False
            if True not in blocked_files:
                break    
        return threatlist
    
    def generate_threat_queen(self,x,y,piecenmbr,maximizing_player, board):
        threatlist = []
        n = 8
        cmod = -1
        if maximizing_player:
            cmod = 1
        blocked_diagonals = [True,True,True,True]
        blocked_files = [True,True,True,True]
        for dz in range(1,n):
            if blocked_files[0]:
                if 0<= x+dz <8:
                    threatlist.append((cmod*piecenmbr,x,y,x+dz,y))  
                    if board[x+dz][y] in {cmod*1,cmod*3,cmod*4,cmod*5,cmod*6,cmod*7,-cmod*1,-cmod*3,-cmod*4,-cmod*5,-cmod*6}:
                        blocked_files[0] = False
                else:
                    blocked_files[0] = False
            if blocked_files[1]:        
                if 0<= x-dz <8:
                    threatlist.append((cmod*piecenmbr,x,y,x-dz,y))  
                    if board[x-dz][y] in {cmod*1,cmod*3,cmod*4,cmod*5,cmod*6,cmod*7,-cmod*1,-cmod*3,-cmod*4,-cmod*5,-cmod*6}:
                        blocked_files[1] = False
                else:
                    blocked_files[1] = False
            if blocked_files[2]:   
                if 0<= y+dz <8:
                    threatlist.append((cmod*piecenmbr,x,y,x,y+dz))  
                    if board[x][y+dz] in {cmod*1,cmod*3,cmod*4,cmod*5,cmod*6,cmod*7,-cmod*1,-cmod*3,-cmod*4,-cmod*5,-cmod*6}:
                        blocked_files[2] = False
                else:
                    blocked_files[2] = False
            if blocked_files[3]:
                if 0<= y-dz <8:
                    threatlist.append((cmod*piecenmbr,x,y,x,y-dz))  
                    if board[x][y-dz] in {cmod*1,cmod*3,cmod*4,cmod*5,cmod*6,cmod*7,-cmod*1,-cmod*3,-cmod*4,-cmod*5,-cmod*6}:
                        blocked_files[3] = False
                else:
                    blocked_files[3] = False
            if blocked_diagonals[0]:
                if 0<= x+dz <8 and 0<= y+dz <8:
                    threatlist.append((cmod*piecenmbr,x,y,x+dz,y+dz))  
                    if board[x+dz][y+dz] in {cmod*1,cmod*3,cmod*4,cmod*5,cmod*6,cmod*7,-cmod*1,-cmod*3,-cmod*4,-cmod*5,-cmod*6}:
                        blocked_diagonals[0] = False
                else:
                    blocked_diagonals[0] = False
            if blocked_diagonals[1]:        
                if 0<= x+dz <8 and 0<= y-dz <8:
                    threatlist.append((cmod*piecenmbr,x,y,x+dz,y-dz))  
                    if board[x+dz][y-dz] in {cmod*1,cmod*3,cmod*4,cmod*5,cmod*6,cmod*7,-cmod*1,-cmod*3,-cmod*4,-cmod*5,-cmod*6}:
                        blocked_diagonals[1] = False
                else:
                    blocked_diagonals[1] = False
            if blocked_diagonals[2]:   
                if 0<= x-dz <8 and 0<= y+dz <8:
                    threatlist.append((cmod*piecenmbr,x,y,x-dz,y+dz))  
                    if board[x-dz][y+dz] in {cmod*1,cmod*3,cmod*4,cmod*5,cmod*6,cmod*7,-cmod*1,-cmod*3,-cmod*4,-cmod*5,-cmod*6}:
                        blocked_diagonals[2] = False
                else:
                    blocked_diagonals[2] = False
            if blocked_diagonals[3]:
                if 0<= x-dz <8 and 0<= y-dz <8:
                    threatlist.append((cmod*piecenmbr,x,y,x-dz,y-dz))  
                    if board[x-dz][y-dz] in {cmod*1,cmod*3,cmod*4,cmod*5,cmod*6,cmod*7,-cmod*1,-cmod*3,-cmod*4,-cmod*5,-cmod*6}:
                        blocked_diagonals[3] = False
                else:
                    blocked_diagonals[3] = False
            if True not in blocked_diagonals and True not in blocked_files:
                break
        return threatlist
    
    def generate_threat_king(self,x,y,piecenmbr,maximizing_player,board):
        threatlist = []
        cmod = -1
        if maximizing_player:
            cmod = 1
        if 0<= x+1 <8:
            threatlist.append((cmod*piecenmbr,x,y,x+1,y))
        if 0<= x+1 <8 and 0<= y-1 <8:
            threatlist.append((cmod*piecenmbr,x,y,x+1,y-1))
        if 0<= x+1 <8 and 0<= y+1 <8:
            threatlist.append((cmod*piecenmbr,x,y,x+1,y+1))
        if 0<= y+1 <8:
            threatlist.append((cmod*piecenmbr,x,y,x,y+1))
        if 0<= y-1 <8:
            threatlist.append((cmod*piecenmbr,x,y,x,y-1))
        if 0<= x-1 <8:
            threatlist.append((cmod*piecenmbr,x,y,x-1,y))
        if 0<= x-1 <8 and 0<= y-1 <8:
            threatlist.append((cmod*piecenmbr,x,y,x-1,y-1))
        if 0<= x-1 <8 and 0<= y+1 <8:
            threatlist.append((cmod*piecenmbr,x,y,x-1,y+1))

        return threatlist    

    def generate_move_king(self,x,y,piecenmbr,maximizing_player, board):
        movelist = []
        cmod = -1
        if maximizing_player:
            cmod = 1
        if 0<= x+1 <8:
            if board[x+1][y] not in {cmod*1,cmod*3,cmod*4,cmod*5,cmod*6,cmod*7}:
                if self.king_not_checked_after_move(x,y,x+1,y,board,maximizing_player):
                    movelist.append((cmod*piecenmbr,x,y,x+1,y))
        if 0<= x+1 <8 and 0<= y-1 <8:
            if board[x+1][y-1] not in {cmod*1,cmod*3,cmod*4,cmod*5,cmod*6,cmod*7}:
                if self.king_not_checked_after_move(x,y,x+1,y-1,board,maximizing_player):
                    movelist.append((cmod*piecenmbr,x,y,x+1,y-1))
        if 0<= x+1 <8 and 0<= y+1 <8:
            if board[x+1][y+1] not in {cmod*1,cmod*3,cmod*4,cmod*5,cmod*6,cmod*7}:
                if self.king_not_checked_after_move(x,y,x+1,y+1,board,maximizing_player):
                    movelist.append((cmod*piecenmbr,x,y,x+1,y+1))
        if 0<= y+1 <8:
            if board[x][y+1] not in {cmod*1,cmod*3,cmod*4,cmod*5,cmod*6,cmod*7}:
                if self.king_not_checked_after_move(x,y,x,y+1,board,maximizing_player):
                    movelist.append((cmod*piecenmbr,x,y,x,y+1))
        if 0<= y-1 <8:
            if board[x][y-1] not in {cmod*1,cmod*3,cmod*4,cmod*5,cmod*6,cmod*7}:
                if self.king_not_checked_after_move(x,y,x,y-1,board,maximizing_player):
                    movelist.append((cmod*piecenmbr,x,y,x,y-1))
        if 0<= x-1 <8:
            if board[x-1][y] not in {cmod*1,cmod*3,cmod*4,cmod*5,cmod*6,cmod*7}:
                if self.king_not_checked_after_move(x,y,x-1,y,board,maximizing_player):
                    movelist.append((cmod*piecenmbr,x,y,x-1,y))
        if 0<= x-1 <8 and 0<= y-1 <8:
            if board[x-1][y-1] not in {cmod*1,cmod*3,cmod*4,cmod*5,cmod*6,cmod*7}:
                if self.king_not_checked_after_move(x,y,x-1,y-1,board,maximizing_player):
                    movelist.append((cmod*piecenmbr,x,y,x-1,y-1))
        if 0<= x-1 <8 and 0<= y+1 <8:
            if board[x-1][y+1] not in {cmod*1,cmod*3,cmod*4,cmod*5,cmod*6,cmod*7}:
                if self.king_not_checked_after_move(x,y,x-1,y+1,board,maximizing_player):
                    movelist.append((cmod*piecenmbr,x,y,x-1,y+1))
        return movelist 

    def square_threatened(self,x,y,maximizing_player, threatlist_white, threatlist_black):
        if maximizing_player:
            for item in threatlist_black:
                if item[3] == x and item[4] == y:
                    return True
            return False
        else:
            for item in threatlist_white:
                if item[3] == x and item[4] == y:
                    return True
            return False

    def manage_board(self,x,y,dx,dy,board):
        piece = board[x][y]
        self.piece_positions_all.remove((piece,x,y))
        try:
            self.piece_positions_all.remove((board[dx][dy],dx,dy))
        except:
            if board[dx][dy] != 0:
                print("board[dx][dy]",board[dx][dy],piece,self.piece_positions_all)
        if piece == 1:
            if dx == 0:
                board[dx][dy] = 6
            else:
                board[dx][dy] = piece
        elif piece == -1:
            if dx == 7:
                board[dx][dy] = -6
            else:
                board[dx][dy] = piece
        else:
            if piece == 7:
                self.white_king_pos = (dx,dy)
            elif piece == -7:
                self.black_king_pos = (dx,dy)
            board[dx][dy] = piece

        self.piece_positions_all.append((board[dx][dy],dx,dy))

        board[x][y] = 0
    
    def revert_board(self,x,y,dx,dy,target_sqr, piece ,board):
        self.piece_positions_all.remove((board[dx][dy],dx,dy))
        self.piece_positions_all.append((piece,x,y))
        if target_sqr != 0:
            self.piece_positions_all.append((target_sqr,dx,dy))
        board[x][y] = piece
        board[dx][dy] = target_sqr 
        if piece == 7:
            self.white_king_pos = (x,y)
        elif piece == -7:
            self.black_king_pos = (x,y)
    
    def king_not_checked_after_move(self,x,y,dx,dy,board, maximizing_player):

        piece = board[x][y]
        target_sqr = board[dx][dy]

        self.manage_board(x,y,dx,dy,board)

        king_position = self.black_king_pos

        if maximizing_player:
            king_position = self.white_king_pos

        threat_tuple = self.generate_threatlists(board)        

        if self.square_threatened(king_position[0],king_position[1],maximizing_player,threat_tuple[0],threat_tuple[1]):
            self.revert_board(x,y,dx,dy,target_sqr,piece,board)
            return False

        self.revert_board(x,y,dx,dy,target_sqr,piece,board)
        return True
    

    def manage_list_states(self,piecenmbr, x,y,dx,dy,maximizing_player,board,copymovewhite, copymoveblack, copythreatwhite, copythreatblack):  

        if maximizing_player:

            mv_white_indices = []

            for i in range(len(copymovewhite)):
                if copymovewhite[i][1] == x and copymovewhite[i][2] == y:
                    mv_white_indices.append(i)

            mv_white_indices.sort(reverse=True)

            for index in mv_white_indices:
                copymovewhite.pop(index)

            thrt_white_indices = []

            for i in range(len(copythreatwhite)):
                if copythreatwhite[i][1] == x and copythreatwhite[i][2] == y:             
                    thrt_white_indices.append(i)

            thrt_white_indices.sort(reverse=True)

            for index in thrt_white_indices:
                copythreatwhite.pop(index)
            
            move_threat_tuple = self.generate_move_threat_all(dx,dy,abs(piecenmbr),True,board)
            copymovewhite.extend(move_threat_tuple[0])
            copythreatwhite.extend(move_threat_tuple[1])

            copythreatblack = []
            copymoveblack = []

            copyallpos = self.piece_positions_all[:]
            for item in copyallpos:  
                if item[0] < 0:                    
                    move_threat_tuple = self.generate_move_threat_all(item[1],item[2],abs(item[0]),False,board)
                    copymoveblack.extend(move_threat_tuple[0])
                    copythreatblack.extend(move_threat_tuple[1])  
        else:
            mv_black_indices = []

            for i in range(len(copymoveblack)):
                if copymoveblack[i][1] == x and copymoveblack[i][2] == y:
                    mv_black_indices.append(i)

            mv_black_indices.sort(reverse=True)

            for index in mv_black_indices:
                copymoveblack.pop(index)

            thrt_black_indices = []

            for i in range(len(copythreatblack)):
                if copythreatblack[i][1] == x and copythreatblack[i][2] == y:             
                    thrt_black_indices.append(i)

            thrt_black_indices.sort(reverse=True)

            for index in thrt_black_indices:
                copythreatblack.pop(index)
            
            move_threat_tuple = self.generate_move_threat_all(dx,dy,abs(piecenmbr),False,board)
            copymoveblack.extend(move_threat_tuple[0])
            copythreatblack.extend(move_threat_tuple[1])

            copythreatwhite = []
            copymovewhite = []
            
            copyallpos = self.piece_positions_all[:]
            for item in copyallpos:                 
                if item[0] > 0:
                    move_threat_tuple = self.generate_move_threat_all(item[1],item[2],abs(item[0]),True,board)
                    copymovewhite.extend(move_threat_tuple[0])
                    copythreatwhite.extend(move_threat_tuple[1])       

        return copymovewhite, copymoveblack, copythreatwhite, copythreatblack
        
    def heuristic_function(self, poslist, piece_eval):
        summa = 0
        for item in poslist:
            piece = item[0]
            i = item[1]
            j = item[2]
            if piece == 1:
                summa += self.pawn_pos_table[i][j]
            elif piece == 3:
                summa += self.knight_pos_table[i][j]
            elif piece == 4:
                summa += self.bishop_pos_table[i][j]
            elif piece == 5:
                summa += self.rook_pos_table[i][j]
            elif piece == 6:
                summa += self.queen_pos_table[i][j]
            elif piece == 7:
                summa += self.king_pos_table[i][j]
            elif piece == -1:
                summa += -self.pawn_pos_table[-(i+1)][-(j+1)]
            elif piece == -3:
                summa += -self.knight_pos_table[-(i+1)][-(j+1)]    
            elif piece == -4:
                summa += -self.bishop_pos_table[-(i+1)][-(j+1)]
            elif piece == -5:
                summa  += -self.rook_pos_table[-(i+1)][-(j+1)]
            elif piece == -6:
                summa += -self.queen_pos_table[-(i+1)][-(j+1)]
            elif piece == -7:
                summa += -self.king_pos_table[-(i+1)][-(j+1)]

        return summa+piece_eval
    
    def sort_movelist(self, movelist, maximizing_player):
        returning_list = []
        indices = []

        if maximizing_player:
            for i in range(len(movelist)):            
                for pos in self.piece_positions_all:
                    if pos[0] < 0 and movelist[i][3] == pos[1] and movelist[i][4] == pos[2]:
                        returning_list.append(movelist[i])
                        indices.append(i)

            indices.sort(reverse=True)

            for index in indices:
                movelist.pop(index)
            returning_list.sort()
            movelist.sort(reverse=True)
            returning_list.extend(movelist)
        else:
            for i in range(len(movelist)):
                for pos in self.piece_positions_all:
                    if pos[0] > 0 and movelist[i][3] == pos[1] and movelist[i][4] == pos[2]:
                        returning_list.append(movelist[i])
                        indices.append(i)

            indices.sort(reverse=True)

            for index in indices:
                movelist.pop(index)
            returning_list.sort(reverse=True)
            movelist.sort()
            returning_list.extend(movelist)
        return returning_list