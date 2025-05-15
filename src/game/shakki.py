import copy


class Shakki:
    """Luokka, joka sisältää shakkipelin toiminnallisuuden.

    Attributes:
        lauta: pitää kirjaa pelin nappuloiden sijoittumisesta laudalla
        whitetomove: pitää kirjaa pelaajien siirtovuoroista
        gamestatus: pitää kirjaa pelin tilanteesta
        draw_by_repetition: pitää kirjaa toistuneista asemista
    """

    def __init__(self):
        """Luokan konstruktori, joka luo uuden pelin ja alustaa luokan attribuutit
        """

        self.lauta = [[-5, -3, -4, -6, -7, -4, -3, -5],
                      [-1, -1, -1, -1, -1, -1, -1, -1],
                      [0, 0, 0, 0, 0, 0, 0, 0],
                      [0, 0, 0, 0, 0, 0, 0, 0],
                      [0, 0, 0, 0, 0, 0, 0, 0],
                      [0, 0, 0, 0, 0, 0, 0, 0],
                      [1, 1, 1, 1, 1, 1, 1, 1],
                      [5, 3, 4, 6, 7, 4, 3, 5]]
        self.whitetomove = True
        self.gamestatus = "WHITE TO MOVE"
        self.draw_by_repetition = {
            "rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w": 1}

    def move_like_pawn(self, x, y, dx, dy, board, mover=None):
        """Funktio, joka tutkii siirron laillisuutta, kun liikutettavaksi valittu nappula on moukka.

            Args:
                x: nappulan sijainnin x-koordinaatti
                y: nappulan sijainnin y-koordinaatti
                dx: nappulan x-koordinaatin muutos
                dy: nappulan y-koordinaatin muutos
                board: laudan tilanne liikkeen hetkellä
                mover: siirtovuorossa oleva pelaaja

            Returns:
                True: jos siirto on shakkipelin sääntöjen mukainen
                False: jos siirto on laiton
        """

        if mover == None:
            mover = self.whitetomove
        if mover:
            if dx == -1:
                if dy == -1 or dy == 1:
                    if self.choose_square(x+dx, y+dy, board) < 0:
                        return True
                    else:
                        return False
                if dy == 0 and self.choose_square(x+dx, y+dy, board) == 0:
                    return True
                return False
            if dx == -2:
                if dy != 0 or x != 6:
                    return False
                if self.choose_square(x-1, y+dy, board) == 0 and self.choose_square(x+dx, y+dy, board) == 0:
                    return True
            return False
        else:
            if dx == 1:
                if dy == -1 or dy == 1:
                    if self.choose_square(x+dx, y+dy, board) > 0:
                        return True
                    else:
                        return False
                if dy == 0 and self.choose_square(x+dx, y+dy, board) == 0:
                    return True
                return False
            if dx == 2:
                if dy != 0 or x != 1:
                    return False
                if self.choose_square(x+1, y+dy, board) == 0 and self.choose_square(x+dx, y+dy, board) == 0:
                    return True
            return False

    def move_like_knight(self, x, y, dx, dy, board, mover=None):
        """Funktio, joka tutkii siirron laillisuutta, kun liikutettavaksi valittu nappula on ratsu.

            Args:
                x: nappulan sijainnin x-koordinaatti
                y: nappulan sijainnin y-koordinaatti
                dx: nappulan x-koordinaatin muutos
                dy: nappulan y-koordinaatin muutos
                board: laudan tilanne liikkeen hetkellä
                mover: siirtovuorossa oleva pelaaja

            Returns:
                True: jos siirto on shakkipelin sääntöjen mukainen
                False: jos siirto on laiton
        """

        if mover == None:
            mover = self.whitetomove
        if ((abs(dy) == 2 and abs(dx) == 1) or (abs(dy) == 1 and abs(dx) == 2)):
            if mover:
                if self.choose_square(x+dx, y+dy, board) <= 0:
                    return True
                return False
            else:
                if self.choose_square(x+dx, y+dy, board) >= 0:
                    return True
                return False
        return False

    def move_like_bishop(self, x, y, dx, dy, board, mover=None):
        """Funktio, joka tutkii siirron laillisuutta, kun liikutettavaksi valittu nappula on lähetti.

            Args:
                x: nappulan sijainnin x-koordinaatti
                y: nappulan sijainnin y-koordinaatti
                dx: nappulan x-koordinaatin muutos
                dy: nappulan y-koordinaatin muutos
                board: laudan tilanne liikkeen hetkellä
                mover: siirtovuorossa oleva pelaaja

            Returns:
                True: jos siirto on shakkipelin sääntöjen mukainen
                False: jos siirto on laiton
        """

        if mover == None:
            mover = self.whitetomove
        if abs(dx) != abs(dy):
            return False
        xstep = -1
        ymod = -1
        if dy * dx > 0:
            ymod = 1
        if dx < 0:
            xstep = 1
        if mover:
            for i in range(dx, 0, xstep):
                if i == dx:
                    if self.choose_square(x+i, y+i*ymod, board) > 0:
                        return False
                    continue
                else:
                    if self.choose_square(x+i, y+i*ymod, board) != 0:
                        return False
            return True
        else:
            for i in range(dx, 0, xstep):
                if i == dx:
                    if self.choose_square(x+i, y+i*ymod, board) < 0:
                        return False
                    continue
                else:
                    if self.choose_square(x+i, y+i*ymod, board) != 0:
                        return False
            return True

    def move_like_rook(self, x, y, dx, dy, board, mover=None):
        """Funktio, joka tutkii siirron laillisuutta, kun liikutettavaksi valittu nappula on torni.

            Args:
                x: nappulan sijainnin x-koordinaatti
                y: nappulan sijainnin y-koordinaatti
                dx: nappulan x-koordinaatin muutos
                dy: nappulan y-koordinaatin muutos
                board: laudan tilanne liikkeen hetkellä
                mover: siirtovuorossa oleva pelaaja

            Returns:
                True: jos siirto on shakkipelin sääntöjen mukainen
                False: jos siirto on laiton
        """

        if mover == None:
            mover = self.whitetomove
        if mover:
            if ((dy == 0 and dx != 0) or (dx == 0 and dy != 0)) and self.choose_square(x+dx, y+dy, board) <= 0:
                negcorrector = 1
                if dy == 0:
                    if dx < 0:
                        negcorrector = -1
                    for i in range(x+negcorrector, x+dx, negcorrector):
                        if self.choose_square(i, y, board) != 0:
                            return False
                    return True
                elif dx == 0:
                    if dy < 0:
                        negcorrector = -1
                    for i in range(y+negcorrector, y+dy, negcorrector):
                        if self.choose_square(x, i, board) != 0:
                            return False
                    return True
        else:
            if ((dy == 0 and dx != 0) or (dx == 0 and dy != 0)) and self.choose_square(x+dx, y+dy, board) >= 0:
                negcorrector = 1
                if dy == 0:
                    if dx < 0:
                        negcorrector = -1
                    for i in range(x+negcorrector, x+dx, negcorrector):
                        if self.choose_square(i, y, board) != 0:
                            return False
                    return True
                elif dx == 0:
                    if dy < 0:
                        negcorrector = -1
                    for i in range(y+negcorrector, y+dy, negcorrector):
                        if self.choose_square(x, i, board) != 0:
                            return False
                    return True
        return False

    def move_like_queen(self, x, y, dx, dy, board, mover):
        """Funktio, joka tutkii siirron laillisuutta, kun liikutettavaksi valittu nappula on kuningatar.

            Args:
                x: nappulan sijainnin x-koordinaatti
                y: nappulan sijainnin y-koordinaatti
                dx: nappulan x-koordinaatin muutos
                dy: nappulan y-koordinaatin muutos
                board: laudan tilanne liikkeen hetkellä
                mover: siirtovuorossa oleva pelaaja

            Returns:
                True: jos siirto on shakkipelin sääntöjen mukainen
                False: jos siirto on laiton
        """

        if mover == None:
            mover = self.whitetomove
        if self.move_like_rook(x, y, dx, dy, board, mover) or self.move_like_bishop(x, y, dx, dy, board, mover):
            return True
        return False

    def move_like_king(self, x, y, dx, dy, board, mover=None):
        """Funktio, joka tutkii siirron laillisuutta, kun liikutettavaksi valittu nappula on kuningas.

            Args:
                x: nappulan sijainnin x-koordinaatti
                y: nappulan sijainnin y-koordinaatti
                dx: nappulan x-koordinaatin muutos
                dy: nappulan y-koordinaatin muutos
                board: laudan tilanne liikkeen hetkellä
                mover: siirtovuorossa oleva pelaaja

            Returns:
                True: jos siirto on shakkipelin sääntöjen mukainen
                False: jos siirto on laiton
        """

        if mover == None:
            mover = self.whitetomove
        if mover:
            if abs(dx) <= 1 and abs(dy) <= 1:
                if self.choose_square(x+dx, y+dy, board) <= 0:
                    return True
            return False
        else:
            if abs(dx) <= 1 and abs(dy) <= 1:
                if self.choose_square(x+dx, y+dy, board) >= 0:
                    return True
            return False

    def check_move_legality(self, x, y, dx, dy, board=[], mover=None):
        """Funktio, joka tutkii siirron laillisuutta.

            Args:
                x: nappulan sijainnin x-koordinaatti
                y: nappulan sijainnin y-koordinaatti
                dx: nappulan x-koordinaatin muutos
                dy: nappulan y-koordinaatin muutos
                board: laudan tilanne liikkeen hetkellä
                mover: siirtovuorossa oleva pelaaja

            Returns:
                True: jos siirto on shakkipelin sääntöjen mukainen
                False: jos siirto on laiton
        """

        if mover == None:
            mover = self.whitetomove
        if board == []:
            board = self.lauta
        if dx == dy == 0:
            return False
        if 0 <= x+dx <= 7 and 0 <= y+dy <= 7:
            if self.choose_square(x, y, board) == 0:
                return False
            if abs(self.choose_square(x, y, board)) == 1:
                return self.move_like_pawn(x, y, dx, dy, board, mover)
            if abs(self.choose_square(x, y, board)) == 3:
                return self.move_like_knight(x, y, dx, dy, board, mover)
            if abs(self.choose_square(x, y, board)) == 4:
                return self.move_like_bishop(x, y, dx, dy, board, mover)
            if abs(self.choose_square(x, y, board)) == 5:
                return self.move_like_rook(x, y, dx, dy, board, mover)
            if abs(self.choose_square(x, y, board)) == 6:
                return self.move_like_queen(x, y, dx, dy, board, mover)
            if abs(self.choose_square(x, y, board)) == 7:
                return self.move_like_king(x, y, dx, dy, board, mover)
        return False

    def square_threatened(self, x, y, board=[], mover=None):
        """Funktio, joka tutkii, uhkaako jokin vastustajan nappuloista laudan ruutua koordinaateissa (x,y).

            Args:
                x: nappulan sijainnin x-koordinaatti
                y: nappulan sijainnin y-koordinaatti
                board: laudan tilanne liikkeen hetkellä
                mover: siirtovuorossa oleva pelaaja

            Returns:
                True: jos ruutu on uhattu
                False: jos ruutu ei ole uhattu
        """

        if board == []:
            board = self.lauta
        n = len(board)
        if mover == None:
            mover = self.whitetomove
        if x == None or y == None:
            return False
        if mover:
            colormod = -1
            if self.square_is_in_bounds(x-1, y-1, board):
                if self.choose_square(x-1, y-1, board) == colormod*1:
                    return True
            if self.square_is_in_bounds(x-1, y+1, board):
                if self.choose_square(x-1, y+1, board) == colormod*1:
                    return True
        else:
            colormod = 1
            if self.square_is_in_bounds(x+1, y-1, board):
                if self.choose_square(x+1, y-1, board) == colormod*1:
                    return True
            if self.square_is_in_bounds(x+1, y+1, board):
                if self.choose_square(x+1, y+1, board) == colormod*1:
                    return True
        if self.square_is_in_bounds(x-2, y-1, board):
            if self.choose_square(x-2, y-1, board) == colormod*3:
                return True
        if self.square_is_in_bounds(x-2, y+1, board):
            if self.choose_square(x-2, y+1, board) == colormod*3:
                return True
        if self.square_is_in_bounds(x-1, y-2, board):
            if self.choose_square(x-1, y-2, board) == colormod*3:
                return True
        if self.square_is_in_bounds(x-1, y+2, board):
            if self.choose_square(x-1, y+2, board) == colormod*3:
                return True
        if self.square_is_in_bounds(x+2, y-1, board):
            if self.choose_square(x+2, y-1, board) == colormod*3:
                return True
        if self.square_is_in_bounds(x+2, y+1, board):
            if self.choose_square(x+2, y+1, board) == colormod*3:
                return True
        if self.square_is_in_bounds(x+1, y-2, board):
            if self.choose_square(x+1, y-2, board) == colormod*3:
                return True
        if self.square_is_in_bounds(x+1, y+2, board):
            if self.choose_square(x+1, y+2, board) == colormod*3:
                return True
        unblockedfiles = [True, True, True, True]
        unblockeddiagonals = [True, True, True, True]
        for diff in range(1, n):
            if mover:
                if self.choose_square(x+diff, y, board) == None or self.choose_square(x+diff, y, board) in {-1, -3, -4, -7} or self.choose_square(x+diff, y, board) > 0:
                    unblockedfiles[0] = False
                if self.choose_square(x-diff, y, board) == None or self.choose_square(x-diff, y, board) in {-1, -3, -4, -7} or self.choose_square(x-diff, y, board) > 0:
                    unblockedfiles[1] = False
                if self.choose_square(x, y+diff, board) == None or self.choose_square(x, y+diff, board) in {-1, -3, -4, -7} or self.choose_square(x, y+diff, board) > 0:
                    unblockedfiles[2] = False
                if self.choose_square(x, y-diff, board) == None or self.choose_square(x, y-diff, board) in {-1, -3, -4, -7} or self.choose_square(x, y-diff, board) > 0:
                    unblockedfiles[3] = False
            else:
                if self.choose_square(x+diff, y, board) == None or self.choose_square(x+diff, y, board) in {1, 3, 4, 7} or self.choose_square(x+diff, y, board) < 0:
                    unblockedfiles[0] = False
                if self.choose_square(x-diff, y, board) == None or self.choose_square(x-diff, y, board) in {1, 3, 4, 7} or self.choose_square(x-diff, y, board) < 0:
                    unblockedfiles[1] = False
                if self.choose_square(x, y+diff, board) == None or self.choose_square(x, y+diff, board) in {1, 3, 4, 7} or self.choose_square(x, y+diff, board) < 0:
                    unblockedfiles[2] = False
                if self.choose_square(x, y-diff, board) == None or self.choose_square(x, y-diff, board) in {1, 3, 4, 7} or self.choose_square(x, y-diff, board) < 0:
                    unblockedfiles[3] = False
            if unblockedfiles[0]:
                if self.choose_square(x+diff, y, board) == colormod*5 or self.choose_square(x+diff, y, board) == colormod*6:
                    return True
            if unblockedfiles[1]:
                if self.choose_square(x-diff, y, board) == colormod*5 or self.choose_square(x-diff, y, board) == colormod*6:
                    return True
            if unblockedfiles[2]:
                if self.choose_square(x, y+diff, board) == colormod*5 or self.choose_square(x, y+diff, board) == colormod*6:
                    return True
            if unblockedfiles[3]:
                if self.choose_square(x, y-diff, board) == colormod*5 or self.choose_square(x, y-diff, board) == colormod*6:
                    return True
            if mover:
                if self.choose_square(x+diff, y+diff, board) == None or self.choose_square(x+diff, y+diff, board) in {-1, -3, -5, -7} or self.choose_square(x+diff, y+diff, board) > 0:
                    unblockeddiagonals[0] = False
                if self.choose_square(x+diff, y-diff, board) == None or self.choose_square(x+diff, y-diff, board) in {-1, -3, -5, -7} or self.choose_square(x+diff, y-diff, board) > 0:
                    unblockeddiagonals[1] = False
                if self.choose_square(x-diff, y+diff, board) == None or self.choose_square(x-diff, y+diff, board) in {-1, -3, -5, -7} or self.choose_square(x-diff, y+diff, board) > 0:
                    unblockeddiagonals[2] = False
                if self.choose_square(x-diff, y-diff, board) == None or self.choose_square(x-diff, y-diff, board) in {-1, -3, -5, -7} or self.choose_square(x-diff, y-diff, board) > 0:
                    unblockeddiagonals[3] = False
            else:
                if self.choose_square(x+diff, y+diff, board) == None or self.choose_square(x+diff, y+diff, board) in {1, 3, 5, 7} or self.choose_square(x+diff, y+diff, board) < 0:
                    unblockeddiagonals[0] = False
                if self.choose_square(x+diff, y-diff, board) == None or self.choose_square(x+diff, y-diff, board) in {1, 3, 5, 7} or self.choose_square(x+diff, y-diff, board) < 0:
                    unblockeddiagonals[1] = False
                if self.choose_square(x-diff, y+diff, board) == None or self.choose_square(x-diff, y+diff, board) in {1, 3, 5, 7} or self.choose_square(x-diff, y+diff, board) < 0:
                    unblockeddiagonals[2] = False
                if self.choose_square(x-diff, y-diff, board) == None or self.choose_square(x-diff, y-diff, board) in {1, 3, 5, 7} or self.choose_square(x-diff, y-diff, board) < 0:
                    unblockeddiagonals[3] = False
            if unblockeddiagonals[0]:
                if self.choose_square(x+diff, y+diff, board) == colormod*4 or self.choose_square(x+diff, y+diff, board) == colormod*6:
                    return True
            if unblockeddiagonals[1]:
                if self.choose_square(x+diff, y-diff, board) == colormod*4 or self.choose_square(x+diff, y-diff, board) == colormod*6:
                    return True
            if unblockeddiagonals[2]:
                if self.choose_square(x-diff, y+diff, board) == colormod*4 or self.choose_square(x-diff, y+diff, board) == colormod*6:
                    return True
            if unblockeddiagonals[3]:
                if self.choose_square(x-diff, y-diff, board) == colormod*4 or self.choose_square(x-diff, y-diff, board) == colormod*6:
                    return True
        if self.choose_square(x+1, y, board) == colormod*7:
            return True
        if self.choose_square(x+1, y-1, board) == colormod*7:
            return True
        if self.choose_square(x+1, y+1, board) == colormod*7:
            return True
        if self.choose_square(x, y+1, board) == colormod*7:
            return True
        if self.choose_square(x, y-1, board) == colormod*7:
            return True
        if self.choose_square(x-1, y, board) == colormod*7:
            return True
        if self.choose_square(x-1, y-1, board) == colormod*7:
            return True
        if self.choose_square(x-1, y+1, board) == colormod*7:
            return True
        return False

    def king_threatened(self, board=[], mover=None):
        """Funktio, joka löytää oman kuninkaan laudalta, ja tutkii onko se ruudulla, jota vastustaja uhkaa.

            Args:
                board: laudan tilanne liikkeen hetkellä
                mover: siirtovuorossa oleva pelaaja

            Returns:
                True: jos oma kuningas on uhattu
                False: jos oma kuningas ei ole uhattu
        """

        if board == []:
            board = self.lauta
        n = len(board)
        colormod = -1
        if mover == None:
            mover = self.whitetomove
        if mover:
            colormod = 1
        kingx = None
        kingy = None
        for i in range(n):
            for j in range(n):
                if board[i][j] == colormod*7:
                    kingx = i
                    kingy = j
                    break
        return self.square_threatened(kingx, kingy, board, mover)

    def execute_move(self, x, y, dx, dy):
        """Funktio, joka päivittää luokan konstruktorissa alustetut attribuutit saadessaan laillisen siirron parametrit, tai ilmoittaa jos siirto oli laiton.
        Funktio myös tarkistaa, onko peli ohi tehdyn siirron jälkeen.

            Args:
                x: nappulan sijainnin x-koordinaatti
                y: nappulan sijainnin y-koordinaatti
                dx: nappulan x-koordinaatin muutos
                dy: nappulan y-koordinaatin muutos                
        """

        if self.preview_move(x, y, dx, dy):
            if abs(self.choose_square(x, y)) == 1:
                self.draw_by_repetition = {}
            self.lauta[x+dx][y+dy] = self.lauta[x][y]
            self.lauta[x][y] = 0
            self.promote_pawns()
            self.change_mover()
            fenboard = self.get_board_as_FEN()
            if self.draw_by_repetition.setdefault(fenboard, 0) != None:
                self.draw_by_repetition[fenboard] += 1
                if self.draw_by_repetition[fenboard] == 3:
                    self.gamestatus = "DRAW BY REPETITION"
            if self.king_threatened(self.lauta):
                self.gamestatus = "CHECK! " + self.gamestatus
            if self.check_for_having_no_moves():
                if self.king_threatened(self.lauta):
                    self.gamestatus = "CHECKMATE"
                else:
                    self.gamestatus = "STALEMATE"
        else:
            print("illegal move, try again")
            pass

    def promote_pawns(self, board=[]):
        """Funktio, joka korottaa moukat kuningattariksi, jos ne ovat päässeet laudan loppuun.

            Args:
                board: lauta, jolle korotukset tehdään
        """

        if board == []:
            board = self.lauta
        n = len(board)
        for i in range(n):
            if self.choose_square(0, i, board) == 1:
                board[0][i] = 6
            if self.choose_square(7, i, board) == -1:
                board[7][i] = -6

    def preview_move(self, x, y, dx, dy, board=[], mover=None):
        """Funktio, joka tekee siirron kopioidulle laudalle, ja palauttaa siirron laillisuuden.

            Args:
                x: nappulan sijainnin x-koordinaatti
                y: nappulan sijainnin y-koordinaatti
                dx: nappulan x-koordinaatin muutos
                dy: nappulan y-koordinaatin muutos
                board: laudan tilanne liikkeen hetkellä
                mover: siirtovuorossa oleva pelaaja

            Returns:
                True: jos siirto on shakkipelin sääntöjen mukainen
                False: jos siirto on laiton
        """

        if mover == None:
            mover = self.whitetomove
        if board == []:
            board = self.lauta
        if self.check_move_legality(x, y, dx, dy, board, mover):
            dupeboard = copy.deepcopy(board)
            dupeboard[x+dx][y+dy] = dupeboard[x][y]
            dupeboard[x][y] = 0
            if self.king_threatened(dupeboard, mover):
                return False
            return True
        return False

    def check_for_having_no_moves(self):
        """Funktio, joka tutkii onko pelaajalla laillisia siirtoja jäljellä.

            Returns:
                True: jos pelaajalla ei ole laillisia siirtoja
                False: jos pelaajalla on laillisia siirtoja jäljellä
        """

        movelist = self.return_move_list()
        if movelist == []:
            return True
        return False

    def choose_square(self, x, y, board=[]):
        """Funktio, joka palauttaa laudan esityksen ruudun sisällöstä, jos koordinaatit on määritelty oikein.

            Args:
                x: nappulan sijainnin x-koordinaatti
                y: nappulan sijainnin y-koordinaatti
                board: laudan tilanne liikkeen hetkellä

            Returns:
                None: jos koordinaatit veisivät laudan ulkopuolelle
                laudan esitys ruudun sisällöstä koordinaatissa (x,y) muuten.
        """

        if board == []:
            board = self.lauta
        if x < 0 or x > 7 or y < 0 or y > 7:
            return None
        return board[x][y]

    def change_mover(self):
        """Funktio, joka vaihtaa siirtovuoron toiselle pelaajalle ja päivittää pelin statuksen.
        """

        if self.whitetomove:
            self.whitetomove = False
            self.gamestatus = "BLACK TO MOVE"
        else:
            self.whitetomove = True
            self.gamestatus = "WHITE TO MOVE"

    def set_board(self, lauta, mover=None):
        """Funktio, joka asettaa nappulat laudalle parametrilla määritellyllä tavalla. Siirtovuorossa olevan pelaajan voi myös määritellä parametrina.

            Args:
                lauta: haluttu nappuloiden konfiguraatio
                mover: mahdollisuus määritellä siirtovuoro
        """

        if mover != None:
            self.whitetomove = mover
        self.lauta = lauta

    def print_board(self):
        """Funktio, joka tulostaa laudan tilanteen käyttäjälle helppolukuisena. Lähinnä käytetty kehityksen aikana varmistamaan laudan tilanteen muuttuvan oikein.
        """

        for row in self.lauta:
            for item in row:
                print(item, end='\t')
            print("\n")

    def get_board_as_FEN(self, board=[], mover=None):
        """Funktio, joka tulostaa laudan tilanteen merkkijonona jokseenkin FEN-muotoisena(Forsyth-Edwards Notation). Vain tälle projektille tarpeellinen informaatio on sisällytetty merkkijonoon.
            Funktiota käytetään vain toistuvan aseman tasapelitarkasteluun.

            Args:
                board: pelilauta
                mover: liikkumisvuorossa oleva pelaaja

            Returns:
                palauttaa pelitilanteen merkkijonona
        """

        if mover == None:
            mover = self.whitetomove
        if board == []:
            board = self.lauta
        rval = ""
        style_dict_FEN = {1: "P", 3: "N", 4: "B", 5: "R", 6: "Q",
                          7: "K", -1: "p", -3: "n", -4: "b", -5: "r", -6: "q", -7: "k"}
        n = len(board)
        for i in range(n):
            counter = 0
            for j in range(n):
                if board[i][j] != 0:
                    if counter != 0:
                        rval += str(counter)
                        counter = 0
                    rval += style_dict_FEN[board[i][j]]
                else:
                    counter += 1
            if counter != 0:
                rval += str(counter)
            if i != 7:
                rval += "/"
        if mover:
            rval += " w"
        else:
            rval += " b"

        return rval

    def return_move_list(self, board=[], mover=None):
        """Funktio, joka etsii kaikki lailliset siirrot pelaajalle, ja palautta ne listana.

            Args:
                board: pelilauta
                mover: liikuntavuorossa oleva pelaaja

            Returns:
                palauttaa kaikki lailliset siirrot listana
        """

        allmovelist = []
        if mover == None:
            mover = self.whitetomove
        if board == []:
            board = self.lauta
        n = len(board)
        for x in range(n):
            for y in range(n):
                piecenmbr = self.choose_square(x, y, board)
                if mover:
                    if piecenmbr > 0:
                        temp = self.get_movelist_for_piece(
                            x, y, piecenmbr, board, mover)
                        if temp != []:
                            allmovelist.extend(temp)
                else:
                    if piecenmbr < 0:
                        temp = self.get_movelist_for_piece(
                            x, y, piecenmbr, board, mover)
                        if temp != []:
                            allmovelist.extend(temp)
        return allmovelist

    def get_movelist_for_piece(self, x, y, piecenmbr, board, mover):
        """Funktio, joka etsii kaikki lailliset siirrot nappulalle.

            Args:
                x: nappulan x-koordinaatti laudalla
                y: nappulan y-koordinaatti laudalla
                piecenmbr: nappula
                board: lauta
                mover: siirtovuorossa oleva pelaaja

            Returns:
                palauttaa nappulan lailliset siirrot
        """

        mvlist = []
        if abs(piecenmbr) == 1:
            mvlist.extend(self.can_pawn_movelist(
                x, y, piecenmbr, board, mover))
        elif abs(piecenmbr) == 3:
            mvlist.extend(self.can_knight_movelist(x, y, board, mover))
        elif abs(piecenmbr) == 4:
            mvlist.extend(self.can_bishop_movelist(x, y, board, mover))
        elif abs(piecenmbr) == 5:
            mvlist.extend(self.can_rook_movelist(x, y, board, mover))
        elif abs(piecenmbr) == 6:
            mvlist.extend(self.can_queen_movelist(x, y, board, mover))
        elif abs(piecenmbr) == 7:
            mvlist.extend(self.can_king_movelist(x, y, board, mover))
        return mvlist

    def can_pawn_movelist(self, x, y, piecenmbr, board, mover):
        """Funktio, joka etsii kaikki lailliset siirrot moukalle.

            Args:
                x: nappulan x-koordinaatti laudalla
                y: nappulan y-koordinaatti laudalla
                piecenmbr: nappula
                board: lauta
                mover: siirtovuorossa oleva pelaaja

            Returns:
                palauttaa nappulan lailliset siirrot
        """

        movelist = []
        if piecenmbr == 1:
            if self.preview_move(x, y, -1, 1, board, mover):
                movelist.append((self.move_as_UCI(x, y, -1, 1)))
            if self.preview_move(x, y, -1, -1, board, mover):
                movelist.append((self.move_as_UCI(x, y, -1, -1)))
            if self.preview_move(x, y, -1, 0, board, mover):
                movelist.append((self.move_as_UCI(x, y, -1, 0)))
            if self.preview_move(x, y, -2, 0, board, mover):
                movelist.append((self.move_as_UCI(x, y, -2, 0)))
        if piecenmbr == -1:
            if self.preview_move(x, y, 1, 1, board, mover):
                movelist.append((self.move_as_UCI(x, y, 1, 1)))
            if self.preview_move(x, y, 1, -1, board, mover):
                movelist.append((self.move_as_UCI(x, y, 1, -1)))
            if self.preview_move(x, y, 1, 0, board, mover):
                movelist.append((self.move_as_UCI(x, y, 1, 0)))
            if self.preview_move(x, y, 2, 0, board, mover):
                movelist.append((self.move_as_UCI(x, y, 2, 0)))

        return movelist

    def can_knight_movelist(self, x, y, board, mover):
        """Funktio, joka etsii kaikki lailliset siirrot ratsulle.

            Args:
                x: nappulan x-koordinaatti laudalla
                y: nappulan y-koordinaatti laudalla
                piecenmbr: nappula
                board: lauta
                mover: siirtovuorossa oleva pelaaja

            Returns:
                palauttaa nappulan lailliset siirrot
        """

        movelist = []
        if self.preview_move(x, y, -2, -1, board, mover):
            movelist.append(self.move_as_UCI(x, y, -2, -1))
        if self.preview_move(x, y, -2, 1, board, mover):
            movelist.append(self.move_as_UCI(x, y, -2, 1))
        if self.preview_move(x, y, -1, -2, board, mover):
            movelist.append(self.move_as_UCI(x, y, -1, -2))
        if self.preview_move(x, y, -1, 2, board, mover):
            movelist.append(self.move_as_UCI(x, y, -1, 2))
        if self.preview_move(x, y, 2, 1, board, mover):
            movelist.append(self.move_as_UCI(x, y, 2, 1))
        if self.preview_move(x, y, 2, -1, board, mover):
            movelist.append(self.move_as_UCI(x, y, 2, -1))
        if self.preview_move(x, y, 1, -2, board, mover):
            movelist.append(self.move_as_UCI(x, y, 1, -2))
        if self.preview_move(x, y, 1, 2, board, mover):
            movelist.append(self.move_as_UCI(x, y, 1, 2))
        return movelist

    def can_bishop_movelist(self, x, y, board, mover):
        """Funktio, joka etsii kaikki lailliset siirrot lähetille.

            Args:
                x: nappulan x-koordinaatti laudalla
                y: nappulan y-koordinaatti laudalla
                piecenmbr: nappula
                board: lauta
                mover: siirtovuorossa oleva pelaaja

            Returns:
                palauttaa nappulan lailliset siirrot
        """

        movelist = []
        n = len(board)
        for dz in range(1, n):
            if self.preview_move(x, y, dz, dz, board, mover):
                movelist.append(self.move_as_UCI(x, y, dz, dz))
            if self.preview_move(x, y, dz, -dz, board, mover):
                movelist.append(self.move_as_UCI(x, y, dz, -dz))
            if self.preview_move(x, y, -dz, dz, board, mover):
                movelist.append(self.move_as_UCI(x, y, -dz, dz))
            if self.preview_move(x, y, -dz, -dz, board, mover):
                movelist.append(self.move_as_UCI(x, y, -dz, -dz))
        return movelist

    def can_rook_movelist(self, x, y, board, mover):
        """Funktio, joka etsii kaikki lailliset siirrot tornille.

            Args:
                x: nappulan x-koordinaatti laudalla
                y: nappulan y-koordinaatti laudalla
                piecenmbr: nappula
                board: lauta
                mover: siirtovuorossa oleva pelaaja

            Returns:
                palauttaa nappulan lailliset siirrot
        """

        movelist = []
        n = len(board)
        for diff in range(1, n):
            if self.preview_move(x, y, diff, 0, board, mover):
                movelist.append(self.move_as_UCI(x, y, diff, 0))
            if self.preview_move(x, y, 0, -diff, board, mover):
                movelist.append(self.move_as_UCI(x, y, 0, -diff))
            if self.preview_move(x, y, -diff, 0, board, mover):
                movelist.append(self.move_as_UCI(x, y, -diff, 0))
            if self.preview_move(x, y, 0, diff, board, mover):
                movelist.append(self.move_as_UCI(x, y, 0, diff))
        return movelist

    def can_queen_movelist(self, x, y, board, mover):
        """Funktio, joka etsii kaikki lailliset siirrot kuningattarelle.

            Args:
                x: nappulan x-koordinaatti laudalla
                y: nappulan y-koordinaatti laudalla
                piecenmbr: nappula
                board: lauta
                mover: siirtovuorossa oleva pelaaja

            Returns:
                palauttaa nappulan lailliset siirrot
        """

        movelist = []
        movelist.extend(self.can_rook_movelist(x, y, board, mover))
        movelist.extend(self.can_bishop_movelist(x, y, board, mover))
        return movelist

    def can_king_movelist(self, x, y, board, mover):
        """Funktio, joka etsii kaikki lailliset siirrot kuninkaalle.

            Args:
                x: nappulan x-koordinaatti laudalla
                y: nappulan y-koordinaatti laudalla
                piecenmbr: nappula
                board: lauta
                mover: siirtovuorossa oleva pelaaja

            Returns:
                palauttaa nappulan lailliset siirrot
        """

        movelist = []
        if self.preview_move(x, y, 1, 0, board, mover):
            movelist.append(self.move_as_UCI(x, y, 1, 0))
        if self.preview_move(x, y, 1, -1, board, mover):
            movelist.append(self.move_as_UCI(x, y, 1, -1))
        if self.preview_move(x, y, 1, 1, board, mover):
            movelist.append(self.move_as_UCI(x, y, 1, 1))
        if self.preview_move(x, y, 0, 1, board, mover):
            movelist.append(self.move_as_UCI(x, y, 0, 1))
        if self.preview_move(x, y, 0, -1, board, mover):
            movelist.append(self.move_as_UCI(x, y, 0, -1))
        if self.preview_move(x, y, -1, 0, board, mover):
            movelist.append(self.move_as_UCI(x, y, -1, 0))
        if self.preview_move(x, y, -1, -1, board, mover):
            movelist.append(self.move_as_UCI(x, y, -1, -1))
        if self.preview_move(x, y, -1, 1, board, mover):
            movelist.append(self.move_as_UCI(x, y, -1, 1))
        return movelist

    def square_is_in_bounds(self, x, y, board=[]):
        """Funktio, joka tutkii, ovatko koordinaatit laudalla.

            Args:
                x: x-koordinaatti
                y: y-koordinaatti
                board: lauta

            Returns:
                True: jos sijainti (x,y) on laudalla
                False: muuten
        """

        if board == []:
            board = self.lauta
        if x >= 0 and x < 8 and y >= 0 and y < 8:
            return True
        return False

    def move_as_UCI(self, x, y, dx, dy):
        """Funktio, joka palauttaa siirron merkkijonona UCI-muotoisena(Universal Chess Interface).

            Args:
                x: x-koordinaatti
                y: y-koordinaatti
                dx: x-koordinaatin muutos
                dy: y-koordinaatin muutos
                board: lauta

            Returns:
                palauttaa siirron merkkijonoesityksen
        """

        style_dict_UCI_row = {0: "a", 1: "b", 2: "c",
                              3: "d", 4: "e", 5: "f", 6: "g", 7: "h"}
        style_dict_UCI_file = {0: "8", 1: "7", 2: "6",
                               3: "5", 4: "4", 5: "3", 6: "2", 7: "1"}
        return style_dict_UCI_row[y] + style_dict_UCI_file[x] + style_dict_UCI_row[y+dy] + style_dict_UCI_file[x+dx]
