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
    
    def set_board(self, lauta):
        self.lauta = lauta

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
                if self.choose_square(x+dx,y+dy) <= 0 and not self.square_threatened(x+dx,y+dy):
                    return True
            return False
        else:
            if abs(dx) <= 1 and abs(dy) <= 1:
                if self.choose_square(x+dx,y+dy) >= 0 and not self.square_threatened(x+dx,y+dy):
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

    def square_threatened(self, x, y):
        n = len(self.lauta)
        if self.whitetomove:
            colormod = -1
            anticmod = 1
            #check for pawns
            if self.choose_square(x-1,y-1) == colormod*1 or self.choose_square(x-1,y+1) == colormod*1:
                return True
        else:
            colormod = 1
            anticmod = -1
            #check for pawns
            if self.choose_square(x+1,y-1) == colormod*1 or self.choose_square(x+1,y+1) == colormod*1:
                return True
        #check for knights
        if self.choose_square(x-2,y-1) == colormod*3 or self.choose_square(x-2,y+1) == colormod*3 \
        or  self.choose_square(x-1,y-2) == colormod*3 or self.choose_square(x-1,y+2) == colormod*3 \
        or self.choose_square(x+2,y-1) == colormod*3 or self.choose_square(x+2,y+1) == colormod*3 \
        or  self.choose_square(x+1,y-2) == colormod*3 or self.choose_square(x+1,y+2) == colormod*3:
            return True    
        unblockedfiles = [True,True,True,True]
        unblockeddiagonals = [True,True,True,True]
        for diff in range(1,n):
            #check for blocking pieces on file
            if self.whitetomove:
                if self.choose_square(x+diff,y) == None or self.choose_square(x+diff,y) == -1 or self.choose_square(x+diff,y) > 0:
                    unblockedfiles[0] = False
                if self.choose_square(x-diff,y) == None or self.choose_square(x+diff,y) == -1 or self.choose_square(x-diff,y) > 0 :
                    unblockedfiles[1] = False
                if self.choose_square(x,y+diff) == None  or self.choose_square(x+diff,y) == -1 or self.choose_square(x,y+diff) > 0:
                    unblockedfiles[2] = False
                if self.choose_square(x,y-diff) == None or self.choose_square(x+diff,y) == -1 or self.choose_square(x,y-diff) > 0:
                    unblockedfiles[3] = False
            else:
                if self.choose_square(x+diff,y) == None or self.choose_square(x+diff,y) == 1 or self.choose_square(x+diff,y) < 0:
                    unblockedfiles[0] = False
                if self.choose_square(x-diff,y) == None  or self.choose_square(x+diff,y) == 1 or self.choose_square(x-diff,y) < 0:
                    unblockedfiles[1] = False
                if self.choose_square(x,y+diff) == None or self.choose_square(x+diff,y) == 1 or self.choose_square(x,y+diff) < 0:
                    unblockedfiles[2] = False
                if self.choose_square(x,y-diff) == None or self.choose_square(x+diff,y) == 1 or self.choose_square(x,y-diff) < 0:
                    unblockedfiles[3] = False
            #check for queens or rooks
            if unblockedfiles[0]:
                if self.choose_square(x+diff,y) == colormod*5 or self.choose_square(x+diff,y) == colormod*6:
                    return True
            if unblockedfiles[1]:
                if self.choose_square(x-diff,y) == colormod*5 or self.choose_square(x-diff,y) == colormod*6:
                    return True
            if unblockedfiles[2]:
                if self.choose_square(x,y+diff) == colormod*5 or self.choose_square(x,y+diff) ==  colormod*6:
                    return True
            if unblockedfiles[3]:
                if self.choose_square(x,y-diff) == colormod*5 or self.choose_square(x,y-diff) == colormod*6:
                    return True
            #check for blocking pieces on diagonal
            if self.whitetomove:
                if self.choose_square(x+diff,y+diff) == None or self.choose_square(x+diff,y+diff) == -1 or self.choose_square(x+diff,y+diff) > 0:
                    unblockeddiagonals[0] = False
                if self.choose_square(x+diff,y-diff) == None or self.choose_square(x+diff,y-diff) == -1 or self.choose_square(x+diff,y-diff) > 0:
                    unblockeddiagonals[1] = False
                if self.choose_square(x-diff,y+diff) == None or self.choose_square(x-diff,y+diff) == -1 or self.choose_square(x-diff,y+diff) > 0:
                    unblockeddiagonals[2] = False
                if self.choose_square(x-diff,y-diff) == None or self.choose_square(x-diff+diff,y) == -1 or self.choose_square(x-diff,y-diff) > 0:
                    unblockeddiagonals[3] = False
            else:
                if self.choose_square(x+diff,y+diff) == None or self.choose_square(x+diff,y+diff) == 1 or self.choose_square(x+diff,y+diff) < 0:
                    unblockeddiagonals[0] = False
                if self.choose_square(x+diff,y-diff) == None or self.choose_square(x+diff,y-diff) == 1 or self.choose_square(x+diff,y-diff) < 0:
                    unblockeddiagonals[1] = False
                if self.choose_square(x-diff,y+diff) == None or self.choose_square(x-diff,y+diff) == 1 or self.choose_square(x-diff,y+diff) < 0:
                    unblockeddiagonals[2] = False
                if self.choose_square(x-diff,y-diff) == None or self.choose_square(x-diff+diff,y) == 1 or self.choose_square(x-diff,y-diff) < 0:
                    unblockeddiagonals[3] = False
            #check for queens or bishops
            if unblockeddiagonals[0]:
                if self.choose_square(x+diff,y+diff) == colormod*4 or self.choose_square(x+diff,y+diff) == colormod*6:
                    return True
            if unblockeddiagonals[1]:
                if self.choose_square(x+diff,y-diff) == colormod*4 or self.choose_square(x+diff,y-diff) == colormod*6:
                    return True
            if unblockeddiagonals[2]:
                if self.choose_square(x-diff,y+diff) == colormod*4 or self.choose_square(x-diff,y+diff) == colormod*6:
                    return True
            if unblockeddiagonals[3]:
                if self.choose_square(x-diff,y-diff) == colormod*4 or self.choose_square(x-diff,y-diff) == colormod*6:
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
        return self.square_threatened(kingx, kingy)


    def execute_move(self,x,y,dx,dy):
        if self.preview_move(x,y,dx,dy):
            self.lauta[x+dx][y+dy] = self.lauta[x][y]
            self.lauta[x][y] = 0
            self.change_mover()
        else:
            print("illegal move, try again")
    
    def preview_move(self,x,y,dx,dy):
        if self.check_move_legality(x,y,dx,dy):
            dupeboard = copy.deepcopy(self.lauta)
            dupeboard[x+dx][y+dy] = dupeboard[x][y]
            dupeboard[x][y] = 0
            print(dupeboard)
            if self.king_threatened(dupeboard):
                print("are we ever here")
                return False
            return True

        return False      

    def choose_square(self,x,y):
        if x < 0 or x >7 or y < 0 or y >7:
            return None
        return self.lauta[x][y]
    
    def change_mover(self):
        if self.whitetomove:
            self.whitetomove = False
        else:
            self.whitetomove = True
    
    def print_board(self):
        for row in self.lauta:
            for item in row:
                print(item, end='\t')
            print("\n")