import pygame
from sprites import *
from config import *
import sys #imports system libraries

class Main_Game:
    def __init__(self):
        pygame.init() #this initializes pygame so that we could use the pygame library.
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT)) #creates the window for the game
        self.clock = pygame.time.Clock() #sets the game's framerate
        #self.font = pygame.font.Font('Arial', 32)
        self.is_running = True

    def new(self):
        self.is_playing = True #this and is_running are booleans that will determine if the game is running or not for various reasons.
        self.all_sprites = pygame.sprite.LayeredUpdates() #LayeredUpdates creates a sprite group that handles layers and draws sprites in the game for sprites in this group.
        self.block_sprites = pygame.sprite.LayeredUpdates() 
        self.enemy_sprites = pygame.sprite.LayeredUpdates()
        self.attack_sprites = pygame.sprite.LayeredUpdates()

        self.player = Player(self, 1, 1)

    def events(self):
        for event in pygame.event.get(): #gets all events in pygame and iterates through them
            if event.type == pygame.QUIT: #if the player closes the window or any quit button this will trigger the QUIT event in pygame
                #if triggered, the game will close
                self.is_playing = False
                self.is_running = False

    def update(self):
        self.all_sprites.update() #this will find the update method in all objects in the sprite group and run them.

    def draw(self):
        self.screen.fill(BG_COLOR) #fills the screen with the color defined in BG_COLOR in config.py
        self.all_sprites.draw(self.screen) #draws all the sprites in the sprite group on the screen
        self.clock.tick(FRAME_RATE) #this ticks through a certain framerate defined in FRAME_RATE in config.py
        pygame.display.update()  #this updates the display

    def main(self):
        #defining the main game loop
        while(self.is_playing):
            self.events()
            self.update()
            self.draw()

        self.is_running = False

    def game_over_screen(self):
        pass

    def intro_screen(self):
        pass

mg_game = Main_Game() #creating on object of the Main_Game class. 
mg_game.intro_screen() #this plays the intro screen, currently does nothing
mg_game.new()


while(mg_game.is_running):
    mg_game.main()
    mg_game.game_over_screen()

pygame.quit()
sys.exit()