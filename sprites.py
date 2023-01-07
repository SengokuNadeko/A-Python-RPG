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

        self.x_translation = 0 #stores the player's movement on the x axis
        self.y_translation = 0 #stores the player's movement on the y axis

        self.player_direction = "facing_down" #stores which direction the player object is facing. it will change depending on player's movement. the default state is facing_down

        self.image = pygame.Surface([self.width, self.height]) #creating the player sprite image. right now this is creating a rectangle.
        self.image.fill(RECT_COLOR) #filling the rectangle with a color. the color is determined in config.py

        self.rect = self.image.get_rect()
        self.rect.x = self.x
        self.rect.y = self.y

    def player_movement(self):
        keys = pygame.key.get_pressed()
        if(keys[pygame.K_a]):
            self.x_translation -= MOVEMENT_SPEED
            self.player_direction = "facing_left"

        if(keys[pygame.K_d]):
            self.x_translation += MOVEMENT_SPEED
            self.player_direction = "facing_right"

        if(keys[pygame.K_w]):
            self.y_translation -= MOVEMENT_SPEED
            self.player_direction = "facing_up"

        if(keys[pygame.K_s]):
            self.y_translation += MOVEMENT_SPEED
            self.player_direction = "facing_down"

    def update(self):
        #calling the player_movement variable. we call it in update to check each frame if the player is moving.
        self.player_movement()

        #changes the player's position on the map. we do this in the update method since it gets called each frame.
        self.rect.x += self.x_translation
        self.rect.y += self.y_translation

        #we set the translation variables to 0 again so that the player object does not move out of screen
        self.x_translation = 0
        self.y_translation = 0