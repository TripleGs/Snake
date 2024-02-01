import pygame
import random

class Player:

    '''Holds all of the player data'''

    def __init__ (self, window):

        self.segments = [(30,30)]
        self.speed = 15
        self.x_speed = self.speed
        self.y_speed = 0
        self.green = (50,250,50)
        self.color = self.green
        self.obj = pygame.draw.rect(window, self.color, [(self.segments[0][0], self.segments[0][1]), (15,15)])
        self.moving_right = True
        self.moving_left = False
        self.moving_up = False
        self.moving_down = False

    #Turns key presses into player movements
    def move(self, window):
        key_presses = pygame.key.get_pressed()
        if key_presses[pygame.K_LEFT] and self.moving_right == False:
            self.x_speed = -self.speed
            self.y_speed = 0
            self.moving_right = False
            self.moving_left = True
            self.moving_up = False
            self.moving_down = False
        if key_presses[pygame.K_RIGHT] and self.moving_left == False:
            self.x_speed = self.speed
            self.y_speed = 0
            self.moving_right = True
            self.moving_left = False
            self.moving_up = False
            self.moving_down = False
        if key_presses[pygame.K_DOWN] and self.moving_up == False:
            self.x_speed = 0
            self.y_speed = self.speed
            self.moving_right = False
            self.moving_left = False
            self.moving_up = False
            self.moving_down = True
        if key_presses[pygame.K_UP] and self.moving_down == False:
            self.x_speed = 0
            self.y_speed = -self.speed
            self.moving_right = False
            self.moving_left = False
            self.moving_up = True
            self.moving_down = False

        self.segments.insert(0, (self.segments[0][0] + self.x_speed, self.segments[0][1] + self.y_speed))
        self.segments.pop(-1)
        self.obj = pygame.draw.rect(window, (50,250,50), [(self.segments[0][0], self.segments[0][1]), (15,15)])

        for segment in self.segments:
            pygame.draw.rect(window, (50,250,50), [segment, (15,15)])
        
class Game:

    '''Function that manages the operations of the snake game'''

    #Initializes game objects
    def __init__ (self, window_name = 'Snake Game', window_size = (600,600)):

        #Defines the window
        pygame.init()
        pygame.display.set_caption(window_name)
        self.window = pygame.display.set_mode(window_size)

        #Manages FPS
        self.clock = pygame.time.Clock()
        self.fps = 10

        #Manages game objects
        self.obj_size = 30
        self.apple_eaten = True
        self.player = Player(self.window)

        #Tracks if the game is running
        self.running = True

        #Tracks the start menu buttons
        self.settings_button = None
        self.start_button = None
        self.back_button = None

        #Creates the starting position of the apple
        self.apple_cords = [(random.randint(1,19)*30, random.randint(1,19)*30), (15,15)]
        while self.apple_cords == self.player.segments:
            self.apple_cords = [(random.randint(1,19)*30, random.randint(1,19)*30), (15,15)]
        self.apple = pygame.draw.rect(self.window, (200,50,50), self.apple_cords)


    #Checks to see if the window was closed
    def check_if_window_closed(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False

    #Draws the apples
    def draw_apples(self):
        if self.apple_eaten:
            self.apple_eaten = False
            self.apple_cords = [(random.randint(1,19)*30, random.randint(1,19)*30), (15,15)]
            while self.apple_cords in self.player.segments:
                self.apple_cords = [(random.randint(1,19)*30, random.randint(1,19)*30), (15,15)]
        else:
            self.apple = pygame.draw.rect(self.window, (200,50,50), self.apple_cords)

    #Draws the player
    def draw_player(self):

        #If the player eats an apple
        if self.player.obj.colliderect(self.apple):
            self.apple_eaten = True
            self.player.segments.append([self.player.segments[-1][0] - self.player.speed, self.player.segments[-1][1]])

        #Checks if the body of the snake hits the head of the snake
        for segment in self.player.segments:
            num = self.player.segments.count(segment)
            if num >= 2:
                self.running = False

        #Checks if the snake goes off screen
        if self.player.obj.x <0:
            self.running = False
        if self.player.obj.x >= 600:
            self.running = False
        if self.player.obj.y < 0:
            self.running = False
        if self.player.obj.y >= 600:
            self.running = False

        #Moves the player
        self.player.move(self.window)
        
    #Draws the items on the screen
    def draw_screen(self):
        self.window.fill((0,0,0))
        self.draw_apples()
        self.draw_player()
        pygame.display.flip()

    #Manages the game events 
    def run(self):
        while self.running:
            self.check_if_window_closed()
            self.draw_screen()
            self.clock.tick(self.fps)
        pygame.quit()

    #Draws the start button
    def draw_start_button(self):
        self.start_button = pygame.draw.rect(self.window, (50,200,50), [(200, 400), (200, 50)])
        my_font = pygame.font.SysFont('Courier New', 30)
        text_surface = my_font.render('START', False, (0, 0, 0))
        self.window.blit(text_surface, (252, 410))

    #Draws the settings button
    def draw_settings_button(self):
        self.settings_button = pygame.draw.rect(self.window, (50,200,50), [(200, 330), (200, 50)])
        my_font = pygame.font.SysFont('Courier New', 30)
        text_surface = my_font.render('SETTINGS', False, (0, 0, 0))
        self.window.blit(text_surface, (228, 340))

    #Manages button events
    def check_button_events(self):
        left, middle, right = pygame.mouse.get_pressed()
        if left:
            if self.start_button.collidepoint(pygame.mouse.get_pos()):
                self.run()

    #Manages start menu events
    def start(self):
        while self.running:
            self.window.fill((0,0,0))
            self.check_if_window_closed()
            self.draw_start_button()
            self.check_button_events()
            
            #Updates screen and error traps game error
            if self.running:
                pygame.display.flip()
        pygame.quit()

game = Game()
game.start()
