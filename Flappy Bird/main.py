# Importing Libraries and Modules
import pygame
from pygame import *
import random

# Initializing Pygame
pygame.init()

# Width and Height of the Window
screen_width = 460
screen_height = 500

# Coding Window and Giving it the Caption 'Flappy Bird'
screen = pygame.display.set_mode((screen_width,screen_height))
pygame.display.set_caption('Flappy Bird')

# FPS Control
clock = pygame.time.Clock()
fps = 60

# Constant Game Variables
ground_scroll = 0
scroll_speed = 2
flying = False
game_over = False
pipe_gap = 100
pipe_frequency = 1500
last_pipe = pygame.time.get_ticks() - pipe_frequency
score = 0
pass_pipe = False

# Setting Font size and family
font = pygame.font.SysFont('Bauhaus 93',50)

# RGB Colors
white = (255, 255, 255)

# Loading Images needed for the Game to Variables
bg = pygame.image.load('Assets/bg.png')
bg = pygame.transform.scale(bg , (460, 420))
ground_img = pygame.image.load('Assets/ground.png')
ground_img = pygame.transform.scale(ground_img , (480, 80))
button_img = pygame.image.load('Assets/restart.png')

# Function to Draw Text on the Window
def draw_text(text, font, text_col, x, y):
    img = font.render(text, True, text_col)
    screen.blit(img, (x, y))

# Function to Restart the game
def reset_game():
    pipe_group.empty()
    flappy.rect.x = 100
    flappy.rect.y = int(screen_height / 2)
    score = 0 
    return score

# Class for the Object 'Bird' in the Game
class Bird(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.images = []
        self.index = 0
        self.counter = 0
        for num in range(1,4):
            img = pygame.image.load(f'Assets/bird{num}.png')
            img = pygame.transform.scale(img, (35, 25))
            self.images.append(img)
        self.image = self.images[self.index]
        self.rect = self.image.get_rect()
        self.rect.center = [x, y]
        self.vel = 0
        self.clicked = False

    def update(self):
        # Gravity
        if flying:
            self.vel += 0.2
            if self.vel > 30:
                self.vel = 0
            if self.rect.bottom < 420:
                self.rect.y += int(self.vel)

        if game_over == False:
            # Jump
            if pygame.mouse.get_pressed()[0] == 1 and self.clicked == False:
                self.clicked = True
                self.vel = -5
            if pygame.mouse.get_pressed()[0] == 0:
                self.clicked = False

            # Animation
            self.counter += 1
            flap_cooldown = 5

            if self.counter > flap_cooldown:
                self.counter = 0
                self.index += 1
                if self.index >= len(self.images):
                    self.index = 0

            self.image = self.images[self.index]

            # Rotation
            self.image = pygame.transform.rotate(self.images[self.index], self.vel * -2)
        else:
            self.image = pygame.transform.rotate(self.images[self.index], -90)


# Class for the Object 'Pipe' in the Game
class Pipe(pygame.sprite.Sprite):
    def __init__(self, x, y, position):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load('Assets/pipe.png')
        self.image = pygame.transform.scale(self.image, (35, 250))
        self.rect = self.image.get_rect()
        
        # Arranging the Gap Between Two Pipes
        if position == 1:
            self.image = pygame.transform.flip(self.image,False, True)
            self.rect.bottomleft = [x, y - int(pipe_gap /2)]
        elif position == -1:
            self.rect.topleft = [x, y + int(pipe_gap / 2)]

    def update(self):
        # Movement of Pipe
        self.rect.x -= scroll_speed
        if self.rect.right < 0:
            self.kill()

# Class for the Object 'Button' in the Game
class Button():
    def __init__(self, x, y, image):
        self.image = image
        self.rect = self.image.get_rect()
        self.rect.topleft = (x, y)

    def draw(self):
        # Drawing Button on the Window
        action = False
        pos = pygame.mouse.get_pos()
        if self.rect.collidepoint(pos):
            if pygame.mouse.get_pressed()[0] == 1:
                action = True
        screen.blit(self.image, (self.rect.x, self.rect.y))

        return action

# Making Objects Using Class for the Game
bird_group = pygame.sprite.Group()
flappy = Bird(100, int(screen_height/2))
bird_group.add(flappy)
pipe_group = pygame.sprite.Group()
button = Button(screen_width // 2 - 50, screen_height // 2 - 50, button_img)

# Mainloop For The Game, Which Trigger the Game Events
run = True
while run:
    # Setting FPS
    clock.tick(fps)

    # Drawing Background on the Window
    screen.blit(bg, (0, 0))

    # Drawing Moving Pipe on the Window
    pipe_group.draw(screen)

    # Drawing Ground on the Window
    screen.blit(ground_img, (ground_scroll, 420))
    
    # Starting the Game
    if game_over == False and flying == True:
        time_now = pygame.time.get_ticks()
        if time_now - last_pipe > pipe_frequency:
            pipe_height = random.randint(-50, 50)
            btm_pipe = Pipe(screen_width, int(screen_height/2) + pipe_height, -1)
            top_pipe = Pipe(screen_width, int(screen_height/2) + pipe_height, 1)
            pipe_group.add(btm_pipe)
            pipe_group.add(top_pipe)
            last_pipe = time_now

        pipe_group.update()

        # Scrolling the Ground
        ground_scroll -= scroll_speed
        if abs(ground_scroll) > 20:
            ground_scroll = 0

    # Changing the Score
    if len(pipe_group) > 0:
        if bird_group.sprites()[0].rect.left > pipe_group.sprites()[0].rect.left \
            and bird_group.sprites()[0].rect.left < pipe_group.sprites()[0].rect.right \
                and pass_pipe == False:
            pass_pipe = True

        if pass_pipe == True:
            if bird_group.sprites()[0].rect.left > pipe_group.sprites()[0].rect.right:
                score += 1
                pass_pipe = False
    
    # Updating the Score in the Windows By Drawing the Score to Window
    draw_text(str(score), font, white, int(screen_width / 2), 20)

    # Drawing Bird to the Window
    bird_group.draw(screen)
    bird_group.update()
    
    # Checking for Collision with Pipes
    if pygame.sprite.groupcollide(bird_group, pipe_group, False, False) or flappy.rect.top < 0:
        game_over = True

    # Checking for Collision with Ground
    if flappy.rect.bottom >= 420:
        game_over = True
        flying = False
    
    # Triggering the Restart Function on Game Over
    if game_over:
        if button.draw():
            game_over = False
            score = reset_game()

    # Loping Through all the Events in the Pygame for Needed Events
    for event in pygame.event.get():
        # Breaking the Mainloop to Quit the Program by 'pygame.QUIT' Event
        if event.type == pygame.QUIT:
            run = False
        # Avoiding Multiple Jumps for the Bird Per Click
        if event.type == pygame.MOUSEBUTTONDOWN and flying == False:
            flying = True

    # Updating the Screen of the Windows to See the Game
    pygame.display.update()

# To Quit the Program if Breaking from the Mainloop
pygame.quit()