# Main game file

# Imports
import time
import pygame
from sys import exit
import threading

import settings
from src import objects

# Variables
running = True
delta_speed = 0
game_speed = 10

interval = 1000
next_tick = pygame.time.get_ticks() + interval

last_time = time.time()

# Set attributes
pygame.init()
screen = pygame.display.set_mode(settings.GAME_WINDOW_SIZE)
GAME_FONT = pygame.font.Font("./assets/fonts/fonts.ttf", 50)
pygame.display.set_caption("Space Invaders")
clock = pygame.time.Clock()

# Declare objects
player = objects.Spaceship(10, 700 - 100 - 10, 100, 100)
asteroidGenerator = objects.Generator(0, 5, 50, 2)
gameBackground = objects.Background('./assets/imgs/spacebackground2.png', [0, 0])

score = 0
score_label = GAME_FONT.render(str(score), True, (255, 255, 255))
    
label_rect = score_label.get_rect()
label_rect.x = settings.GAME_WINDOW_SIZE[0] / 2
label_rect.y = 20

score_label = (score_label, label_rect)

# Functions
def quit():
    print("The game is quiting!")
    running = False
    player.gameRun = False
    asteroidGenerator.stop()
    pygame.quit()
    exit()
    
def display_surfaces(surfaces):
    
    # Refresh surfaces
    for surface in surfaces:
        if type(surface) == tuple:
            position = surface[1]
            surface = surface[0]
            
            if type(surface) != pygame.Surface:
                surface = surface.image
            
            screen.blit(surface, position)
        else:
            screen.blit(surface.image, surface.rect)
            
# Place threads here
try:
    pass
except Exception as error:
    print(error)
    quit()

pygame.display.update()

# The game loop
try:
    while running:
        
        delta = time.time() - last_time
        delta *= 60
        last_time = time.time()
        
        for event in pygame.event.get():
            
            if event.type == pygame.QUIT:
                quit()
                
        # Fill the background
        screen.fill((0, 0, 0))
            
        keys = pygame.key.get_pressed()  
        speed = 5
        
        if keys[pygame.K_RIGHT]:
            player.move_x(speed, delta)
        if keys[pygame.K_LEFT]:
            player.move_x(-speed, delta)
        if keys[pygame.K_SPACE] and player.shouldShoot == False:
            player.shouldShoot = True
            player.shoot()
                
        # Game logic
        player.update()
        asteroidGenerator.update()
        
        for bullet in player.bullets:
            bullet.update(delta)
                
        for asteroid in asteroidGenerator.asteroids:
            asteroid.update(delta)
            
            bullets = player.bullets
            
            for bullet in bullets:
                if asteroid.rect.colliderect(bullet.rect):
                    asteroid.health -= bullet.damage
                    
                    if asteroid.health == 0:
                        asteroid.kill()
                        score += asteroid.point
                        score_label = (GAME_FONT.render(str(score), True, (255, 255, 255)), score_label[1])
                    
                    # Destroy the bullet
                    bullet.kill()
        
        # Display them here
        display_surfaces([
            (gameBackground.image, gameBackground.rect),
            (player.image, player.rect),
            (score_label[0], score_label[1])
        ])
        
        display_surfaces(player.bullets)
        display_surfaces(asteroidGenerator.asteroids)
        
        # Game time management
        
        pygame.display.update()
        clock.tick(60)
        
except Exception as error:
    print(error)
    quit()