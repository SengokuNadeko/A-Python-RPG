import pygame
from config import *
import math
import random

class Player(pygame.sprite.Sprite):
    def __init__(self, game, x, y): #the game parameter is for the player object to access everything in the Main_Game class. the x and y parameters are for the player object's position in the game map.
        self.game = game
        self._layer = LAYER_PLAYER #handles the sprite layer for the player class. the underscore at the beginning of the variable is just to show that it's supposed to be used internally for this class. it has no built in function
        self.sprite_groups = self.game.all_sprites
        pygame.sprite.Sprite.__init__(self, self.sprite_groups)

        self.x = x * MAP_TILE_SIZE #setting x position of the player object
        self.y = y * MAP_TILE_SIZE #setting y position of the player object
        self.width = MAP_TILE_SIZE #setting the width of the player object
        self.height = MAP_TILE_SIZE #setting the height of the player object

        self.image = pygame.Surface([self.width, self.height]) #creating the player sprite image. right now this is creating a rectangle.
        self.image.fill(RECT_COLOR) #filling the rectangle with a color. the color is determined in config.py

        self.rect = self.image.get_rect()
        self.rect.x = self.x
        self.rect.y = self.y

    def update(self):
        pass