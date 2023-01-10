import pygame
from config import *
import math
import random

class Sprite_Sheet:
    def __init__(self, file):
        self.sprite_sheet = pygame.image.load(file).convert()
    
    def get_sprite(self, x, y, width, height):
        sprite = pygame.Surface([width, height])
        sprite.blit(self.sprite_sheet, (0,0), (x, y, width, height))
        sprite.set_colorkey(BLACK)
        return sprite

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

        self.image = self.game.character_sprite_sheet.get_sprite(0, 0, self.width, self.height) #getting the player sprite in the Arthax.png sprite sheet and storing it in the variable image.

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

    #defining the collision_check function to detect collision when the player object hits something that is collidable 
    def collision_check(self, direction):
        if(direction == "x"):
            hits = pygame.sprite.spritecollide(self, self.game.block_sprites, False)
            if(hits):
                if(self.x_translation > 0):
                    self.rect.x = hits[0].rect.left - self.rect.width #hits is a list. when we defined hits, we made sure it adds all the sprites in the block_sprites sprite group to the list. we use 0 in the index to indicate the wall spries in the sprite group because it is the first group of sprites that was added to the list.
                if(self.x_translation < 0):
                    self.rect.x = hits[0].rect.right

        if(direction == "y"):
            hits = pygame.sprite.spritecollide(self, self.game.block_sprites, False)
            if(hits):
                if(self.y_translation > 0):
                    self.rect.y = hits[0].rect.top - self.rect.height
                if(self.y_translation < 0):
                    self.rect.y = hits[0].rect.bottom

    def update(self):
        #calling the player_movement variable. we call it in update to check each frame if the player is moving.
        self.player_movement()

        #changes the player's position on the map. we do this in the update method since it gets called each frame.
        self.rect.x += self.x_translation
        self.collision_check("x")

        self.rect.y += self.y_translation
        self.collision_check("y")

        #we set the translation variables to 0 again so that the player object does not move out of screen
        self.x_translation = 0
        self.y_translation = 0


class Walls(pygame.sprite.Sprite):
    def __init__(self, game, x, y):
        self.game = game
        self._layer = LAYER_WALLS #handles the sprite layer for the wall class. the underscore at the beginning of the variable is just to show that it's supposed to be used internally for this class. it has no built in function
        self.sprite_groups = self.game.all_sprites, self.game.block_sprites
        pygame.sprite.Sprite.__init__(self, self.sprite_groups)

        self.x = x * MAP_TILE_SIZE
        self.y = y * MAP_TILE_SIZE
        self.width = MAP_TILE_SIZE 
        self.height = MAP_TILE_SIZE 
        
        self.image = self.game.wall_sprite_sheet.get_sprite(0, 0, self.width, self.height) #getting the "wall" sprite in the Signs.png sprite sheet and storing it in the variable image.

        self.rect = self.image.get_rect()
        self.rect.x = self.x
        self.rect.y = self.y

class Ground(pygame.sprite.Sprite):
    def __init__(self, game, x, y):
        self.game = game
        self._layer = LAYER_GROUND #handles the sprite layer for the ground class. the underscore at the beginning of the variable is just to show that it's supposed to be used internally for this class. it has no built in function
        self.sprite_groups = self.game.all_sprites
        pygame.sprite.Sprite.__init__(self, self.sprite_groups)

        self.x = x * MAP_TILE_SIZE
        self.y = y * MAP_TILE_SIZE
        self.width = MAP_TILE_SIZE 
        self.height = MAP_TILE_SIZE 
        
        self.image = self.game.tile_sprite_sheet.get_sprite(0, 0, self.width, self.height) #getting the ground sprite in the TexturedGrass.png sprite sheet and storing it in the variable image.

        self.rect = self.image.get_rect()
        self.rect.x = self.x
        self.rect.y = self.y
