import pygame
import os

dirname = os.path.dirname(__file__)

class Piece(pygame.sprite.Sprite):
    def __init__(self,x=0,y=0, name = "pawn", color = "w", scale =128):
        self.name = name
        self.color = color
        self.scale = scale
        super().__init__()

        self.image = pygame.transform.scale(pygame.image.load(
            os.path.join(dirname, "..", "assets", name + color+".png")
        ),(self.scale, self.scale))

        self.rect = self.image.get_rect()

        self.rect.x = x
        self.rect.y = y