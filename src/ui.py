import pygame
import os
from game.shakki import Shakki
from entities.piece import Piece

dirname = os.path.dirname(__file__)

class UI():
    def __init__(self):
        pygame.init()
        self.squaregrid =[[0,1,0,1,0,1,0,1],
                      [1,0,1,0,1,0,1,0],
                      [0,1,0,1,0,1,0,1],
                      [1,0,1,0,1,0,1,0],
                      [0,1,0,1,0,1,0,1],
                      [1,0,1,0,1,0,1,0],
                      [0,1,0,1,0,1,0,1],
                      [1,0,1,0,1,0,1,0]]
        self.peli = Shakki()

        self.chosen_piece = []
        self.chosen_piece_original_position = None

        self.load_tiles()

        self.height_and_width = len(self.peli.lauta)
        self.scale = self.tiles[0].get_width()
        self.screen = pygame.display.set_mode((self.height_and_width*self.scale, self.height_and_width*self.scale))
        self.black_pieces = pygame.sprite.Group()
        self.white_pieces = pygame.sprite.Group()
        self.all_sprites = pygame.sprite.LayeredUpdates()

        pygame.display.set_caption("Shakki")

        self.draw_board()
        self.set_board()
        self.main_loop()
    

    def main_loop(self):
        while True:
            self.check_events()
            self.draw_board()

    def check_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    pos_on_mbdown = pygame.mouse.get_pos()
                    self.chosen_piece = self.all_sprites.get_sprites_at(pos_on_mbdown)
                    if self.chosen_piece == []:
                        continue
                    if self.chosen_piece[0].color == "w" and self.peli.whitetomove:
                        self.chosen_piece_original_position = pos_on_mbdown
                    if self.chosen_piece[0].color == "b" and not self.peli.whitetomove:
                        self.chosen_piece_original_position = pos_on_mbdown

            if event.type == pygame.MOUSEBUTTONUP:
                if event.button == 1:
                    pos_on_mbup = pygame.mouse.get_pos()
                    if self.chosen_piece != []:
                            if self.chosen_piece_original_position != None:
                                y_np = self.downscale(pos_on_mbup[0])
                                x_np = self.downscale(pos_on_mbup[1])
                                y_op = (self.downscale(self.chosen_piece_original_position[0]))
                                x_op = (self.downscale(self.chosen_piece_original_position[1]))
                                dx = x_np-x_op
                                dy = y_np-y_op                               
                                self.peli.execute_move(x_op, y_op,dx,dy)
                            self.set_board()
                            self.chosen_piece_original_position = None
                            self.chosen_piece = []
    
    def draw_board(self):
        self.screen.fill((0,0,0))        
        for x in range(len(self.squaregrid)):
            for y in range(len(self.squaregrid)):
                square = self.squaregrid[x][y]
                self.screen.blit(self.tiles[square],(x*self.scale, y*self.scale))
        self.all_sprites.draw(self.screen)
        pygame.display.flip()  

    def load_tiles(self):
        self.tiles = []
        for name in ["sqrw","sqrb"]:
            self.tiles.append(pygame.image.load(
                os.path.join(dirname,"assets",name+".png")
            ))

    def set_board(self):
        self.all_sprites.remove_sprites_of_layer(0)
        for x in range(len(self.peli.lauta)):
            for y in range(len(self.peli.lauta)):
                scaled_x = x * self.scale
                scaled_y = y * self.scale
                if self.peli.choose_square(y,x) == -5:
                    self.all_sprites.add(Piece(scaled_x,scaled_y, "rook", "b", self.scale)) 
                if self.peli.choose_square(y,x) == -3:
                    self.all_sprites.add(Piece(scaled_x,scaled_y, "knight", "b", self.scale)) 
                if self.peli.choose_square(y,x) == -4:
                    self.all_sprites.add(Piece(scaled_x,scaled_y, "bishop", "b", self.scale))
                if self.peli.choose_square(y,x) == -6:
                    self.all_sprites.add(Piece(scaled_x,scaled_y, "queen", "b", self.scale))
                if self.peli.choose_square(y,x) == -7:
                    self.all_sprites.add(Piece(scaled_x,scaled_y, "king", "b", self.scale))
                if self.peli.choose_square(y,x) == 5:
                    self.all_sprites.add(Piece(scaled_x,scaled_y, "rook", "w", self.scale)) 
                if self.peli.choose_square(y,x) == 3:
                    self.all_sprites.add(Piece(scaled_x,scaled_y, "knight", "w", self.scale)) 
                if self.peli.choose_square(y,x) == 4:
                    self.all_sprites.add(Piece(scaled_x,scaled_y, "bishop", "w", self.scale))
                if self.peli.choose_square(y,x) == 6:
                    self.all_sprites.add(Piece(scaled_x,scaled_y, "queen", "w", self.scale))
                if self.peli.choose_square(y,x) == 7:
                    self.all_sprites.add(Piece(scaled_x,scaled_y, "king", "w", self.scale))
                if self.peli.choose_square(y,x) == -1:
                    self.all_sprites.add(Piece(scaled_x,scaled_y, "pawn", "b", self.scale))
                if self.peli.choose_square(y,x) == 1:
                    self.all_sprites.add(Piece(scaled_x,scaled_y, "pawn", "w", self.scale))

    def downscale(self, position):
        return position//self.scale