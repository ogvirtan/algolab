import copy

class Shakki:
    def __init__(self):
        self.lauta = [[-5,-3,-4,-6,-7,-4,-3,-5],
                      [-1,-1,-1,-1,-1,-1,-1,-1],
                      [0,0,0,0,0,0,0,0],
                      [0,0,0,0,0,0,0,0],
                      [0,0,0,0,0,0,0,0],
                      [0,0,0,0,0,0,0,0],
                      [1,1,1,1,1,1,1,1],
                      [5,3,4,6,7,4,3,5]]
        self.whitetomove = True
        self.gamestatus = "WHITE TO MOVE"

    def move_like_pawn(self, x,y,dx,dy):
        if self.whitetomove:
            if dx == -1:
                if dy == -1 or dy == 1:
                    if self.choose_square(x+dx,y+dy) < 0:
                        return True
                    else:
                        return False
                if dy==0 and self.choose_square(x+dx,y+dy) == 0:
                    return True
                return False             
            if dx == -2:
                if dy != 0 or x != 6:
                    return False
                if self.choose_square(x-1,y+dy) == 0 and self.choose_square(x+dx,y+dy) == 0:
                    return True
            return False
        else:
            if dx == 1:
                if dy == -1 or dy == 1:
                    if self.choose_square(x+dx,y+dy) > 0:
                        return True
                    else:
                        return False
                if dy==0 and self.choose_square(x+dx,y+dy) == 0:
                    return True
                return False              
            if dx == 2:
                if dy != 0 or x != 1:
                    return False
                if self.choose_square(x+1,y+dy) == 0 and self.choose_square(x+dx,y+dy) == 0:
                    return True
            return False

    def move_like_knight(self, x,y,dx,dy):
        if ((abs(dy) == 2 and abs(dx) == 1) or (abs(dy) == 1 and abs(dx) == 2)):
            if self.whitetomove:
                if self.choose_square(x+dx,y+dy) <= 0:
                    return True
                return False
            else:
                if self.choose_square(x+dx,y+dy) >= 0:
                    return True
                return False
        return False

    def move_like_bishop(self, x,y,dx,dy):
        if abs(dx) != abs(dy):
            return False
        xstep = -1
        ymod = -1
        if dy * dx > 0:
            ymod = 1
        if dx < 0:
            xstep = 1
        if self.whitetomove:
            for i in range(dx,0,xstep):
                if i == dx:
                    if self.choose_square(x+i,y+i*ymod) > 0:
                        return False
                    continue
                else:
                    if self.choose_square(x+i,y+i*ymod) != 0:
                        return False
            return True
        else:
            for i in range(dx,0,xstep):
                if i == dx:
                    if self.choose_square(x+i,y+i*ymod) < 0:
                        return False
                    continue
                else:
                    if self.choose_square(x+i,y+i*ymod) != 0:
                        return False
            return True



    def move_like_rook(self, x,y,dx,dy):
        if self.whitetomove:
            if ((dy == 0 and dx != 0) or (dx == 0 and dy != 0)) and self.choose_square(x+dx,y+dy) <= 0:
                negcorrector = 1
                if dy == 0:
                    if dx < 0:
                        negcorrector = -1
                    for i in range(x+negcorrector, x+dx, negcorrector):
                        if self.choose_square(i,y) != 0:
                            return False
                    return True
                elif dx == 0:
                    if dy < 0:
                        negcorrector = -1
                    for i in range(y+negcorrector, y+dy, negcorrector):
                        if self.choose_square(x,i) != 0:
                            return False   
                    return True
        else:
            if ((dy == 0 and dx != 0) or (dx == 0 and dy != 0)) and self.choose_square(x+dx,y+dy) >= 0:
                negcorrector = 1
                if dy == 0:
                    if dx < 0:
                        negcorrector = -1
                    for i in range(x+negcorrector, x+dx, negcorrector):
                        if self.choose_square(i,y) != 0:
                            return False
                    return True
                elif dx == 0:
                    if dy < 0:
                        negcorrector = -1
                    for i in range(y+negcorrector, y+dy, negcorrector):
                        if self.choose_square(x,i) != 0:
                            return False   
                    return True

    def move_like_queen(self,x,y,dx,dy):
        if self.move_like_rook(x,y,dx,dy) or self.move_like_bishop(x,y,dx,dy):
            return True
        return False

    def move_like_king(self, x,y,dx,dy):
        if self.whitetomove:
            if abs(dx) <= 1 and abs(dy) <= 1:
                if self.choose_square(x+dx,y+dy) <= 0:
                    return True
            return False
        else:
            if abs(dx) <= 1 and abs(dy) <= 1:
                if self.choose_square(x+dx,y+dy) >= 0:
                    return True
            return False

    def check_move_legality(self, x,y,dx,dy):
        if dx == dy == 0:
            return False
        if 0<= x+dx <=7 and 0<= y+dy <=7:
            if self.choose_square(x,y) == 0:
                return False
            #pawn
            if abs(self.choose_square(x,y)) == 1:
                return self.move_like_pawn(x,y,dx,dy)
            #knight
            if abs(self.choose_square(x,y)) == 3:
                return self.move_like_knight(x,y,dx,dy)
            #bishop
            if abs(self.choose_square(x,y)) == 4:
                return self.move_like_bishop(x,y,dx,dy)
            #rook        
            if abs(self.choose_square(x,y)) == 5:
                return self.move_like_rook(x,y,dx,dy)
            #queen
            if  abs(self.choose_square(x,y)) == 6:
                return self.move_like_queen(x,y,dx,dy)
            #king
            if abs(self.choose_square(x,y)) == 7:
                return self.move_like_king(x,y,dx,dy)
        return False

    def square_threatened(self, x, y, board):
        n = len(self.lauta)
        if self.whitetomove:
            colormod = -1
            anticmod = 1
            #check for pawns
            if self.choose_square_diff_board(x-1,y-1,board) == colormod*1 or self.choose_square_diff_board(x-1,y+1,board) == colormod*1:
                return True
        else:
            colormod = 1
            anticmod = -1
            #check for pawns
            if self.choose_square_diff_board(x+1,y-1,board) == colormod*1 or self.choose_square_diff_board(x+1,y+1,board) == colormod*1:
                return True
        #check for knights
        if self.choose_square_diff_board(x-2,y-1,board) == colormod*3 or self.choose_square_diff_board(x-2,y+1,board) == colormod*3 \
        or  self.choose_square_diff_board(x-1,y-2,board) == colormod*3 or self.choose_square_diff_board(x-1,y+2,board) == colormod*3 \
        or self.choose_square_diff_board(x+2,y-1,board) == colormod*3 or self.choose_square_diff_board(x+2,y+1,board) == colormod*3 \
        or  self.choose_square_diff_board(x+1,y-2,board) == colormod*3 or self.choose_square_diff_board(x+1,y+2,board) == colormod*3:
            return True    
        unblockedfiles = [True,True,True,True]
        unblockeddiagonals = [True,True,True,True]
        for diff in range(1,n):
            #check for blocking pieces on file
            if self.whitetomove:
                if self.choose_square_diff_board(x+diff,y,board) == None or self.choose_square_diff_board(x+diff,y,board) == -1 or self.choose_square_diff_board(x+diff,y,board) > 0:
                    unblockedfiles[0] = False
                if self.choose_square_diff_board(x-diff,y,board) == None or self.choose_square_diff_board(x-diff,y,board) == -1 or self.choose_square_diff_board(x-diff,y,board) > 0 :
                    unblockedfiles[1] = False
                if self.choose_square_diff_board(x,y+diff,board) == None or self.choose_square_diff_board(x,y+diff,board) == -1 or self.choose_square_diff_board(x,y+diff,board) > 0:
                    unblockedfiles[2] = False
                if self.choose_square_diff_board(x,y-diff,board) == None or self.choose_square_diff_board(x,y-diff,board) == -1 or self.choose_square_diff_board(x,y-diff,board) > 0:
                    unblockedfiles[3] = False
            else:
                if self.choose_square_diff_board(x+diff,y,board) == None or self.choose_square_diff_board(x+diff,y,board) == 1 or self.choose_square_diff_board(x+diff,y,board) < 0:
                    unblockedfiles[0] = False
                if self.choose_square_diff_board(x-diff,y,board) == None or self.choose_square_diff_board(x-diff,y,board) == 1 or self.choose_square_diff_board(x-diff,y,board) < 0:
                    unblockedfiles[1] = False
                if self.choose_square_diff_board(x,y+diff,board) == None or self.choose_square_diff_board(x,y+diff,board) == 1 or self.choose_square_diff_board(x,y+diff,board) < 0:
                    unblockedfiles[2] = False
                if self.choose_square_diff_board(x,y-diff,board) == None or self.choose_square_diff_board(x,y-diff,board) == 1 or self.choose_square_diff_board(x,y-diff,board) < 0:
                    unblockedfiles[3] = False
            #check for queens or rooks
            if unblockedfiles[0]:
                if self.choose_square_diff_board(x+diff,y,board) == colormod*5 or self.choose_square_diff_board(x+diff,y,board) == colormod*6:
                    return True
            if unblockedfiles[1]:
                if self.choose_square_diff_board(x-diff,y,board) == colormod*5 or self.choose_square_diff_board(x-diff,y,board) == colormod*6:
                    return True
            if unblockedfiles[2]:
                if self.choose_square_diff_board(x,y+diff,board) == colormod*5 or self.choose_square_diff_board(x,y+diff,board) ==  colormod*6:
                    return True
            if unblockedfiles[3]:
                if self.choose_square_diff_board(x,y-diff,board) == colormod*5 or self.choose_square_diff_board(x,y-diff,board) == colormod*6:
                    return True
            #check for blocking pieces on diagonal
            if self.whitetomove:
                if self.choose_square_diff_board(x+diff,y+diff,board) == None or self.choose_square_diff_board(x+diff,y+diff,board) == -1 or self.choose_square_diff_board(x+diff,y+diff,board) > 0:
                    unblockeddiagonals[0] = False
                if self.choose_square_diff_board(x+diff,y-diff,board) == None or self.choose_square_diff_board(x+diff,y-diff,board) == -1 or self.choose_square_diff_board(x+diff,y-diff,board) > 0:
                    unblockeddiagonals[1] = False
                if self.choose_square_diff_board(x-diff,y+diff,board) == None or self.choose_square_diff_board(x-diff,y+diff,board) == -1 or self.choose_square_diff_board(x-diff,y+diff,board) > 0:
                    unblockeddiagonals[2] = False
                if self.choose_square_diff_board(x-diff,y-diff,board) == None or self.choose_square_diff_board(x-diff,y-diff,board) == -1 or self.choose_square_diff_board(x-diff,y-diff,board) > 0:
                    unblockeddiagonals[3] = False
            else:
                if self.choose_square_diff_board(x+diff,y+diff,board) == None or self.choose_square_diff_board(x+diff,y+diff,board) == 1 or self.choose_square_diff_board(x+diff,y+diff,board) < 0:
                    unblockeddiagonals[0] = False
                if self.choose_square_diff_board(x+diff,y-diff,board) == None or self.choose_square_diff_board(x+diff,y-diff,board) == 1 or self.choose_square_diff_board(x+diff,y-diff,board) < 0:
                    unblockeddiagonals[1] = False
                if self.choose_square_diff_board(x-diff,y+diff,board) == None or self.choose_square_diff_board(x-diff,y+diff,board) == 1 or self.choose_square_diff_board(x-diff,y+diff,board) < 0:
                    unblockeddiagonals[2] = False
                if self.choose_square_diff_board(x-diff,y-diff,board) == None or self.choose_square_diff_board(x-diff,y-diff,board) == 1 or self.choose_square_diff_board(x-diff,y-diff,board) < 0:
                    unblockeddiagonals[3] = False
            #check for queens or bishops
            if unblockeddiagonals[0]:
                if self.choose_square_diff_board(x+diff,y+diff,board) == colormod*4 or self.choose_square_diff_board(x+diff,y+diff,board) == colormod*6:
                    return True
            if unblockeddiagonals[1]:
                if self.choose_square_diff_board(x+diff,y-diff,board) == colormod*4 or self.choose_square_diff_board(x+diff,y-diff,board) == colormod*6:
                    return True
            if unblockeddiagonals[2]:
                if self.choose_square_diff_board(x-diff,y+diff,board) == colormod*4 or self.choose_square_diff_board(x-diff,y+diff,board) == colormod*6:
                    return True
            if unblockeddiagonals[3]:
                if self.choose_square_diff_board(x-diff,y-diff,board) == colormod*4 or self.choose_square_diff_board(x-diff,y-diff,board) == colormod*6:
                    return True
            #check for kings
            if self.choose_square_diff_board(x+1,y,board) == colormod*7:
                return True
            if self.choose_square_diff_board(x+1,y-1,board) == colormod*7:
                return True
            if self.choose_square_diff_board(x+1,y+1,board) == colormod*7:
                return True
            if self.choose_square_diff_board(x,y+1,board) == colormod*7:
                return True
            if self.choose_square_diff_board(x,y-1,board) == colormod*7:
                return True
            if self.choose_square_diff_board(x-1,y,board) == colormod*7:
                return True
            if self.choose_square_diff_board(x-1,y-1,board) == colormod*7:
                return True
            if self.choose_square_diff_board(x-1,y+1,board) == colormod*7:
                return True
        return False
        
    def king_threatened(self, board):
        n = len(board)
        colormod = -1
        if self.whitetomove:
            colormod = 1
        kingx = None
        kingy = None
        for i in range(n):
            for j in range(n):
                if board[i][j] == colormod*7:
                    kingx = i
                    kingy = j
                    break
        return self.square_threatened(kingx, kingy, board)


    def execute_move(self,x,y,dx,dy):
        if self.preview_move(x,y,dx,dy):
            self.lauta[x+dx][y+dy] = self.lauta[x][y]
            self.lauta[x][y] = 0
            self.change_mover()
            if self.king_threatened(self.lauta):
                self.gamestatus = "CHECK! " + self.gamestatus
            if self.check_for_having_no_moves():
                if self.king_threatened(self.lauta):
                    self.gamestatus = "CHECKMATE"
                else:
                    self.gamestatus = "STALEMATE"
        else:
            print("illegal move, try again")
    
    def preview_move(self,x,y,dx,dy):
        if self.check_move_legality(x,y,dx,dy):
            dupeboard = copy.deepcopy(self.lauta)
            dupeboard[x+dx][y+dy] = dupeboard[x][y]
            dupeboard[x][y] = 0
            if self.king_threatened(dupeboard):
                return False
            return True
        return False
    
    def check_for_having_no_moves(self):
        n = len(self.lauta)
        rval = True
        for x in range(n):
            for y in range(n):
                piecenmbr = self.choose_square(x,y)
                if self.whitetomove:               
                    if piecenmbr > 0:
                        if self.get_moves_for_piece(x,y, piecenmbr):
                            rval = False
                else:
                    if piecenmbr < 0:
                        if self.get_moves_for_piece(x,y, piecenmbr):
                            rval = False
        return rval

    def get_moves_for_piece(self, x, y, piecenmbr):
        if abs(piecenmbr) == 1:
            return self.can_pawn_move(x,y,piecenmbr)
        elif abs(piecenmbr) == 3:
            return self.can_knight_move(x,y)
        elif abs(piecenmbr) == 4:
            return self.can_bishop_move(x,y)
        elif abs(piecenmbr) == 5:
            return self.can_rook_move(x,y) 
        elif abs(piecenmbr) == 6:
            return self.can_queen_move(x,y) 
        elif abs(piecenmbr) == 7:
            return self.can_king_move(x,y)
        return False

    def can_pawn_move(self,x,y,piecenmbr):
        if piecenmbr == 1:
            if self.preview_move(x,y,-1,1) or self.preview_move(x,y,-1,-1) or self.preview_move(x,y,-1,0) or self.preview_move(x,y,-2,0):
                return True
        if piecenmbr == -1:
            if self.preview_move(x,y,1,1) or self.preview_move(x,y,1,-1) or self.preview_move(x,y,1,0) or self.preview_move(x,y,2,0):
                return True
        return False

    def can_knight_move(self,x,y):
        if self.preview_move(x,y,-2,-1) or self.preview_move(x,y,-2,1) \
        or  self.preview_move(x,y,-1,-2) or self.preview_move(x,y,-1,2)\
        or self.preview_move(x,y,2,-1) or self.preview_move(x,y,2,1)\
        or  self.preview_move(x,y,1,2) or self.preview_move(x,y,1,-2):
            return True
        return False

    def can_bishop_move(self,x,y):
        n = len(self.lauta)
        unblockeddiagonals = [True,True,True,True]
        for dz in range(1,n):
            if unblockeddiagonals[0]:
                if self.preview_move(x,y,dz,dz):
                    return True             
                else:
                    unblockeddiagonals[0] = False
            if unblockeddiagonals[1]:
                if self.preview_move(x,y,dz,-dz):
                    return True   
                else:
                    unblockeddiagonals[1] = False
            if unblockeddiagonals[2]:
                if self.preview_move(x,y,-dz,dz):
                    return True
                else:
                    unblockeddiagonals[2] = False
            if unblockeddiagonals[3]:
                if self.preview_move(x,y,-dz,-dz):
                    return True
                else:      
                    unblockeddiagonals[3] = False
            else:
                break
        return False

    def can_rook_move(self,x,y):
        n = len(self.lauta)
        for diff in range(1,n):
            if self.preview_move(x,y,diff,0) or self.preview_move(x,y,0,-diff) \
            or self.preview_move(x,y,-diff,0) or self.preview_move(x,y,0,diff):
                return True  
        return False

    def can_queen_move(self,x,y):
        if self.can_bishop_move(x,y):
            return True
        elif self.can_rook_move(x,y):
            return True
        return False
    
    def can_king_move(self,x,y):
        if self.preview_move(x,y,1,0) or self.preview_move(x,y,1,-1) or self.preview_move(x,y,1,1) \
        or self.preview_move(x,y,0,1) or self.preview_move(x,y,0,-1) \
        or self.preview_move(x,y,-1,0) or self.preview_move(x,y,-1,-1) or self.preview_move(x,y,-1,1):
            return True
        return False 

    def choose_square(self,x,y):
        if x < 0 or x >7 or y < 0 or y >7:
            return None
        return self.lauta[x][y]

    def choose_square_diff_board(self,x,y, board):
        if x < 0 or x >7 or y < 0 or y >7:
            return None
        return board[x][y]
    
    def change_mover(self):
        if self.whitetomove:
            self.whitetomove = False
            self.gamestatus = "BLACK TO MOVE"
        else:
            self.whitetomove = True
            self.gamestatus = "WHITE TO MOVE"
    
    def set_board(self, lauta):
        self.lauta = lauta
    
    def set_board_FEN(self, fenstring:str):
        reverse_style_dict_FEN = {"P":1,"N":3,"B":4,"R":5,"Q":6,"K":7,"p":-1,"n":-3,"b":-4,"r":-5,"q":-6,"k":-7}
        unpacked = []
        temp = []
        for item in fenstring:
            if item not in reverse_style_dict_FEN.keys():
                if item == "/":
                    continue
                for i in range(int(item)):
                    temp.append(0)
            else:
                temp.append(reverse_style_dict_FEN[item])
            if len(temp) == 8:
                unpacked.append(temp)
                temp = []
        self.lauta = unpacked
    
    def print_board(self):
        for row in self.lauta:
            for item in row:
                print(item, end='\t')
            print("\n")
    
    def get_board_as_SAN(self):
        style_dict_SAN = { 0:".",1:"P",3:"N",4:"B",5:"R",6:"Q",7:"K",-1:"p",-3:"n",-4:"b",-5:"r",-6:"q",-7:"k"}
        rval = ""
        for row in self.lauta:
            for item in row:
                rval += style_dict_SAN[item] + " "
            rval += "\n"
        return rval
    
    def get_board_as_FEN(self):
        rval = ""
        style_dict_FEN = {1:"P",3:"N",4:"B",5:"R",6:"Q",7:"K",-1:"p",-3:"n",-4:"b",-5:"r",-6:"q",-7:"k"}
        n = len(self.lauta)
        for i in range(n):
            counter = 0
            for j in range(n):
                if  self.lauta[i][j] != 0:
                    rval += style_dict_FEN[self.lauta[i][j]]
                    if counter != 0:
                        rval += str(counter)
                        counter = 0
                else:
                    counter += 1
            if counter != 0:
                rval += str(counter)
            if i != 7:
                rval += "/"
        if self.whitetomove:
            rval += " w - - 0 0" 
        else:
            rval += " b - - 0 0"
        
        return rval

    def return_move_list(self):
        allmovelist = []
        n = len(self.lauta)
        for x in range(n):
            for y in range(n):
                piecenmbr = self.choose_square(x,y)
                if self.whitetomove:               
                    if piecenmbr > 0:
                        temp = self.get_movelist_for_piece(x,y, piecenmbr)
                        if temp != []:
                            allmovelist.extend(temp)
                else:
                    if piecenmbr < 0:
                        temp = self.get_movelist_for_piece(x,y, piecenmbr)
                        if temp != []:
                            allmovelist.extend(temp)
        return allmovelist

    def get_movelist_for_piece(self, x, y, piecenmbr):
        mvlist = []
        if abs(piecenmbr) == 1:
            mvlist.extend(self.can_pawn_movelist(x,y,piecenmbr))
        elif abs(piecenmbr) == 3:
            mvlist.extend(self.can_knight_movelist(x,y))
        elif abs(piecenmbr) == 4:
            mvlist.extend(self.can_bishop_movelist(x,y))
        elif abs(piecenmbr) == 5:
            mvlist.extend(self.can_rook_movelist(x,y))
        elif abs(piecenmbr) == 6:
            mvlist.extend(self.can_queen_movelist(x,y))
        elif abs(piecenmbr) == 7:
            mvlist.extend(self.can_king_movelist(x,y))
        return mvlist

    def can_pawn_movelist(self,x,y,piecenmbr):
        movelist = []
        if piecenmbr == 1:
            if self.preview_move(x,y,-1,1):
                movelist.append((self.move_as_UCI(x,y,-1,1)))
            if self.preview_move(x,y,-1,-1):
                movelist.append((self.move_as_UCI(x,y,-1,-1)))
            if self.preview_move(x,y,-1,0):
                movelist.append((self.move_as_UCI(x,y,-1,0)))
            if self.preview_move(x,y,-2,0):
                movelist.append((self.move_as_UCI(x,y,-2,0)))
                
        if piecenmbr == -1:
            if self.preview_move(x,y,1,1):
                movelist.append((self.move_as_UCI(x,y,1,1)))
            if self.preview_move(x,y,1,-1):
                movelist.append((self.move_as_UCI(x,y,1,-1)))
            if self.preview_move(x,y,1,0):
                movelist.append((self.move_as_UCI(x,y,1,0)))
            if self.preview_move(x,y,2,0):
                movelist.append((self.move_as_UCI(x,y,2,0)))

        return movelist

    def can_knight_movelist(self,x,y):
        movelist = []
        if self.preview_move(x,y,-2,-1):
            movelist.append(self.move_as_UCI(x,y,-2,-1))
        if self.preview_move(x,y,-2,1):
            movelist.append(self.move_as_UCI(x,y,-2,1))
        if self.preview_move(x,y,-1,-2):
            movelist.append(self.move_as_UCI(x,y,-1,-2))
        if self.preview_move(x,y,-1,2):
            movelist.append(self.move_as_UCI(x,y,-1,2))
        if self.preview_move(x,y,2,1):
            movelist.append(self.move_as_UCI(x,y,2,1))
        if self.preview_move(x,y,2,-1):
            movelist.append(self.move_as_UCI(x,y,2,-1))
        if  self.preview_move(x,y,1,-2):
            movelist.append(self.move_as_UCI(x,y,1,-2))
        if self.preview_move(x,y,1,2):
            movelist.append(self.move_as_UCI(x,y,1,2))
        return movelist

    def can_bishop_movelist(self,x,y):
        movelist = []
        n = len(self.lauta)
        unblockeddiagonals = [True,True,True,True]
        for dz in range(1,n):
            if unblockeddiagonals[0]:
                if self.preview_move(x,y,dz,dz):
                    movelist.append(self.move_as_UCI(x,y,dz,dz))             
                else:
                    unblockeddiagonals[0] = False
            if unblockeddiagonals[1]:
                if self.preview_move(x,y,dz,-dz):
                    movelist.append(self.move_as_UCI(x,y,dz,-dz))
                else:
                    unblockeddiagonals[1] = False
            if unblockeddiagonals[2]:
                if self.preview_move(x,y,-dz,dz):
                    movelist.append(self.move_as_UCI(x,y,-dz,dz)) 
                else:
                    unblockeddiagonals[2] = False
            if unblockeddiagonals[3]:
                if self.preview_move(x,y,-dz,-dz):
                    movelist.append(self.move_as_UCI(x,y,-dz,-dz))
                else:      
                    unblockeddiagonals[3] = False
            else:
                break
        return movelist

    def can_rook_movelist(self,x,y):
        movelist = []
        n = len(self.lauta)
        for diff in range(1,n):
            if self.preview_move(x,y,diff,0):
                movelist.append(self.move_as_UCI(x,y,diff,0)) 
            if self.preview_move(x,y,0,-diff):
                movelist.append(self.move_as_UCI(x,y,0,-diff)) 
            if self.preview_move(x,y,-diff,0):
                movelist.append(self.move_as_UCI(x,y,-diff,0)) 
            if self.preview_move(x,y,0,diff):
                movelist.append(self.move_as_UCI(x,y,0,diff))  
        return movelist

    def can_queen_movelist(self,x,y):
        movelist = []
        movelist.extend(self.can_bishop_movelist(x,y))
        movelist.extend(self.can_rook_movelist(x,y))
        return movelist
    
    def can_king_movelist(self,x,y):
        movelist = []
        if self.preview_move(x,y,1,0):
            movelist.append(self.move_as_UCI(x,y,1,0))
        if self.preview_move(x,y,1,-1):
            movelist.append(self.move_as_UCI(x,y,1,-1))
        if self.preview_move(x,y,1,1):
            movelist.append(self.move_as_UCI(x,y,1,1))
        if self.preview_move(x,y,0,1):
            movelist.append(self.move_as_UCI(x,y,0,1))
        if self.preview_move(x,y,0,-1):
            movelist.append(self.move_as_UCI(x,y,0,-1))
        if self.preview_move(x,y,-1,0):
            movelist.append(self.move_as_UCI(x,y,-1,0))
        if self.preview_move(x,y,-1,-1):
            movelist.append(self.move_as_UCI(x,y,-1,-1))
        if self.preview_move(x,y,-1,1):
            movelist.append(self.move_as_UCI(x,y,-1,1))
        return movelist
    
    def move_as_UCI(self,x,y,dx,dy):
        style_dict_UCI_row = { 0:"a",1:"b",2:"c",3: "d",4:"e",5:"f",6:"g",7:"h"}
        style_dict_UCI_file = { 0:"8",1:"7",2:"6",3: "5",4:"4",5:"3",6:"2",7:"1"}
        return style_dict_UCI_row[y] + style_dict_UCI_file[x] + style_dict_UCI_row[y+dy] + style_dict_UCI_file[x+dx]