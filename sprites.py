import pygame
from config import *
import math
import random

class Sprite_Sheet:
    def __init__(self, file):
        self.sprite_sheet = pygame.image.load(file).convert_alpha()

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
        self.image = self.game.character_sprite_sheet.get_sprite(0, 0, self.width, self.height)

        self.animation_loop = 0

        self.rect = self.image.get_rect()
        self.rect.x = self.x
        self.rect.y = self.y

    def player_movement(self):
        keys = pygame.key.get_pressed()
        if(keys[pygame.K_a]):
            self.x_translation -= PLAYER_MOVEMENT_SPEED #moves the player object left
            self.player_direction = "facing_left" #changes the player direction variable to the direction it's facing in.

        if(keys[pygame.K_d]):
            self.x_translation += PLAYER_MOVEMENT_SPEED #moves the player object right
            self.player_direction = "facing_right" #changes the player direction variable to the direction it's facing in.

        if(keys[pygame.K_w]):
            self.y_translation -= PLAYER_MOVEMENT_SPEED #moves the player object up
            self.player_direction = "facing_up" #changes the player direction variable to the direction it's facing in.

        if(keys[pygame.K_s]):
            self.y_translation += PLAYER_MOVEMENT_SPEED #moves the player object down
            self.player_direction = "facing_down" #changes the player direction variable to the direction it's facing in.

    #defining the collision_check function to detect collision when the player object hits something that is collidable 
    def wall_collision_check(self, direction):
        hits = pygame.sprite.spritecollide(self, self.game.block_sprites, False)
        if(direction == "x"):
            if(hits):
                if(self.x_translation > 0):
                    self.rect.x = hits[0].rect.left - self.rect.width #hits is a list. when we defined hits, we made sure it adds all the sprites in the block_sprites sprite group to the list. we use 0 in the index to indicate the wall spries in the sprite group because it is the first group of sprites that was added to the list.
                if(self.x_translation < 0):
                    self.rect.x = hits[0].rect.right

        if(direction == "y"):
            if(hits):
                if(self.y_translation > 0):
                    self.rect.y = hits[0].rect.top - self.rect.height
                if(self.y_translation < 0):
                    self.rect.y = hits[0].rect.bottom
    
    def enemy_collision_check(self, direction):
        hits = pygame.sprite.spritecollide(self, self.game.enemy_sprites, False)
        pass

    def player_animate(self):
        #defining arrays that store multiple sprites for player animation.

        #defining the walk_down_animation array and storing the sprites that contain the player moving downwards in the array
        walk_down_animation = [
            self.game.character_sprite_sheet.get_sprite(16, 0, self.width, self.height),
            self.game.character_sprite_sheet.get_sprite(32, 0, self.width, self.height),
            self.game.character_sprite_sheet.get_sprite(48, 0, self.width, self.height),
            self.game.character_sprite_sheet.get_sprite(64, 0, self.width, self.height)
        ]

        #defining the walk_up_animation array and storing the sprites that contain the player moving upwards in the array
        walk_up_animation = [
            self.game.character_sprite_sheet.get_sprite(16, 16, self.width, self.height),
            self.game.character_sprite_sheet.get_sprite(32, 16, self.width, self.height),
            self.game.character_sprite_sheet.get_sprite(48, 16, self.width, self.height),
            self.game.character_sprite_sheet.get_sprite(64, 16, self.width, self.height)
        ]

        #defining the walk_right_animation array and storing the sprites that contain the player moving right in the array
        walk_right_animation = [
            self.game.character_sprite_sheet.get_sprite(16, 32, self.width, self.height),
            self.game.character_sprite_sheet.get_sprite(32, 32, self.width, self.height),
            self.game.character_sprite_sheet.get_sprite(48, 32, self.width, self.height),
            self.game.character_sprite_sheet.get_sprite(64, 32, self.width, self.height)
        ]

        #defining the walk_left_animation array and storing the sprites that contain the player moving left in the array
        walk_left_animation = [
            self.game.character_sprite_sheet.get_sprite(16, 48, self.width, self.height),
            self.game.character_sprite_sheet.get_sprite(32, 48, self.width, self.height),
            self.game.character_sprite_sheet.get_sprite(48, 48, self.width, self.height),
            self.game.character_sprite_sheet.get_sprite(64, 48, self.width, self.height)
        ]

        if(self.player_direction == "facing_down"):
            if(self.y_translation == 0):
                self.image = self.game.character_sprite_sheet.get_sprite(0, 0, self.width, self.height) #getting the player sprite in the Arthax.png sprite sheet and storing it in the variable image. this is for the downward facing position.
            else:
                self.image = walk_down_animation[math.floor(self.animation_loop)] #math.floor() rounds down a number to the closest whole number. here, we use animation_loop as the index to get each sprite in the animation array.
                self.animation_loop += 0.1 #adds 0.1 to animation_loop every frame. this loops through the animation array above every time the player is, in this case, facing_down, moving, and the player_animate() function is called. 
                if(self.animation_loop >= 4):
                    self.animation_loop = 0 #if the animation_loop variable ends up being equal to or greater than 4, we reset it to 0. the reason we cap the maximum value at 4 is because the amount of sprites each animation array holds is 4, currently. and since the index of arrays starts at 0 instead of one, we want to cycle through 0-3 instead of 1-4. 
        
        if(self.player_direction == "facing_up"):
            if(self.y_translation == 0):
                self.image = self.game.character_sprite_sheet.get_sprite(0, 16, self.width, self.height) #getting the player sprite in the Arthax.png sprite sheet and storing it in the variable image. this is for the upward facing position.
            else:
                self.image = walk_up_animation[math.floor(self.animation_loop)] #math.floor() rounds down a number to the closest whole number. here, we use animation_loop as the index to get each sprite in the animation array.
                self.animation_loop += 0.1 #adds 0.1 to animation_loop every frame. this loops through the animation array above every time the player is, in this case, facing_up, moving, and the player_animate() function is called. 
                if(self.animation_loop >= 4):
                    self.animation_loop = 0 #if the animation_loop variable ends up being equal to or greater than 4, we reset it to 0. the reason we cap the maximum value at 4 is because the amount of sprites each animation array holds is 4, currently. and since the index of arrays starts at 0 instead of one, we want to cycle through 0-3 instead of 1-4. 
        
        if(self.player_direction == "facing_right"):
            if(self.x_translation == 0):
                self.image = self.game.character_sprite_sheet.get_sprite(0, 32, self.width, self.height) #getting the player sprite in the Arthax.png sprite sheet and storing it in the variable image. this is for the right facing position.
            else:
                self.image = walk_right_animation[math.floor(self.animation_loop)] #math.floor() rounds down a number to the closest whole number. here, we use animation_loop as the index to get each sprite in the animation array.
                self.animation_loop += 0.1 #adds 0.1 to animation_loop every frame. this loops through the animation array above every time the player is, in this case, facing_right, moving, and the player_animate() function is called. 
                if(self.animation_loop >= 4):
                    self.animation_loop = 0 #if the animation_loop variable ends up being equal to or greater than 4, we reset it to 0. the reason we cap the maximum value at 4 is because the amount of sprites each animation array holds is 4, currently. and since the index of arrays starts at 0 instead of one, we want to cycle through 0-3 instead of 1-4. 
        
        if(self.player_direction == "facing_left"):
            if(self.x_translation == 0):
                self.image = self.game.character_sprite_sheet.get_sprite(0, 48, self.width, self.height) #getting the player sprite in the Arthax.png sprite sheet and storing it in the variable image. this is for the left facing position.
            else:
                self.image = walk_left_animation[math.floor(self.animation_loop)] #math.floor() rounds down a number to the closest whole number. here, we use animation_loop as the index to get each sprite in the animation array.
                self.animation_loop += 0.1 #adds 0.1 to animation_loop every frame. this loops through the animation array above every time the player is, in this case, facing_left, moving, and the player_animate() function is called. 
                if(self.animation_loop >= 4):
                    self.animation_loop = 0 #if the animation_loop variable ends up being equal to or greater than 4, we reset it to 0. the reason we cap the maximum value at 4 is because the amount of sprites each animation array holds is 4, currently. and since the index of arrays starts at 0 instead of one, we want to cycle through 0-3 instead of 1-4. 

    def update(self):
        #calling the player_movement function. we call it in update to check each frame if the player is moving.
        self.player_movement()

        #calling the player_animate() function. we call it in update to animate the player object every frame.
        self.player_animate()

        #changes the player's position on the map. we do this in the update method since it gets called each frame.
        self.rect.x += self.x_translation
        self.wall_collision_check("x")

        self.rect.y += self.y_translation
        self.wall_collision_check("y")

        #we set the translation variables to 0 again so that the player object does not move out of screen
        self.x_translation = 0
        self.y_translation = 0


class Enemies(pygame.sprite.Sprite):
    def __init__(self, game, x, y):
        self.game = game
        self._layer = LAYER_ENEMY
        self.sprite_groups = self.game.all_sprites, self.game.enemy_sprites
        pygame.sprite.Sprite.__init__(self, self.sprite_groups)

        self.x = x * MAP_TILE_SIZE
        self.y = y * MAP_TILE_SIZE
        self.width = MAP_TILE_SIZE 
        self.height = MAP_TILE_SIZE 
        
        self.x_translation = 0
        self.y_translation = 0

        self.enemy_direction = random.choice(["facing_left", "facing_right"])
        self.animation_loop = 0
        self.movement_loop = 0
        self.max_travel = random.randint(6, 100)

        self.image = self.game.enemy_sprite_sheet.get_sprite(0, 0, self.width, self.height) #getting the enemy sprite in the Slime.png sprite sheet and storing it in the variable image.

        self.rect = self.image.get_rect()
        self.rect.x = self.x
        self.rect.y = self.y

    def update(self):
        self.enemy_movement()
        self.enemy_animate()

        self.rect.x += self.x_translation
        self.wall_collision_check("x")

        self.rect.y += self.y_translation
        self.wall_collision_check("y")

        self.x_translation = 0
        self.y_translation = 0

    def enemy_movement(self):
        if(self.enemy_direction == "facing_left"):
            self.x_translation -= ENEMY_MOVEMENT_SPEED
            self.movement_loop -= 1
            if(self.movement_loop <= -self.max_travel):
                self.enemy_direction = "facing_right"

        if(self.enemy_direction == "facing_right"):
            self.x_translation += ENEMY_MOVEMENT_SPEED
            self.movement_loop += 1
            if(self.movement_loop >= self.max_travel):
                self.enemy_direction = "facing_left"
    
    def enemy_animate(self):
        walk_left_animation = [
            self.game.enemy_sprite_sheet.get_sprite(16, 16, self.width, self.height),
            self.game.enemy_sprite_sheet.get_sprite(32, 16, self.width, self.height),
            self.game.enemy_sprite_sheet.get_sprite(48, 16, self.width, self.height),
            self.game.enemy_sprite_sheet.get_sprite(64, 16, self.width, self.height),
            self.game.enemy_sprite_sheet.get_sprite(80, 16, self.width, self.height)
        ]

        walk_right_animation = [
            self.game.enemy_sprite_sheet.get_sprite(16, 32, self.width, self.height),
            self.game.enemy_sprite_sheet.get_sprite(32, 32, self.width, self.height),
            self.game.enemy_sprite_sheet.get_sprite(48, 32, self.width, self.height),
            self.game.enemy_sprite_sheet.get_sprite(64, 32, self.width, self.height),
            self.game.enemy_sprite_sheet.get_sprite(80, 32, self.width, self.height)
        ]

        if(self.enemy_direction == "facing_right"):
            if(self.x_translation == 0):
                self.image = self.game.enemy_sprite_sheet.get_sprite(16, 32, self.width, self.height) #getting the enemy sprite in the Slime.png sprite sheet and storing it in the variable image. this is for the right facing position.
            else:
                self.image = walk_right_animation[math.floor(self.animation_loop)] #math.floor() rounds down a number to the closest whole number. here, we use animation_loop as the index to get each sprite in the animation array.
                self.animation_loop += 0.1 #adds 0.1 to animation_loop every frame. this loops through the animation array above every time the enemy is, in this case, facing_right, moving, and the enemy_animate() function is called. 
                if(self.animation_loop >= 5):
                    self.animation_loop = 0 #if the animation_loop variable ends up being equal to or greater than 5, we reset it to 0. the reason we cap the maximum value at 5 is because the amount of sprites each animation array holds is 5, currently. and since the index of arrays starts at 0 instead of one, we want to cycle through 0-4 instead of 1-5. 
        
        if(self.enemy_direction == "facing_left"):
            if(self.x_translation == 0):
                self.image = self.game.character_sprite_sheet.get_sprite(16, 16, self.width, self.height) #getting the enemy sprite in the Slime.png sprite sheet and storing it in the variable image. this is for the left facing position.
            else:
                self.image = walk_left_animation[math.floor(self.animation_loop)] #math.floor() rounds down a number to the closest whole number. here, we use animation_loop as the index to get each sprite in the animation array.
                self.animation_loop += 0.1 #adds 0.1 to animation_loop every frame. this loops through the animation array above every time the enemy is, in this case, facing_left, moving, and the enemy_animate() function is called. 
                if(self.animation_loop >= 5):
                    self.animation_loop = 0 #if the animation_loop variable ends up being equal to or greater than 5, we reset it to 0. the reason we cap the maximum value at 5 is because the amount of sprites each animation array holds is 5, currently. and since the index of arrays starts at 0 instead of one, we want to cycle through 0-4 instead of 1-5. 
    
    def wall_collision_check(self, direction):
        hits = pygame.sprite.spritecollide(self, self.game.block_sprites, False)
        if(direction == "x"):
            if(hits):
                if(self.x_translation > 0):
                    self.rect.x = hits[0].rect.left - self.rect.width #hits is a list. when we defined hits, we made sure it adds all the sprites in the block_sprites sprite group to the list. we use 0 in the index to indicate the wall spries in the sprite group because it is the first group of sprites that was added to the list.
                if(self.x_translation < 0):
                    self.rect.x = hits[0].rect.right

        if(direction == "y"):
            if(hits):
                if(self.y_translation > 0):
                    self.rect.y = hits[0].rect.top - self.rect.height
                if(self.y_translation < 0):
                    self.rect.y = hits[0].rect.bottom

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
