# Main game file

# Imports
import time
import pygame
from sys import exit

import settings
from src import objects

# Variables
running = True
delta_speed = 0
game_speed = 10

interval = 1000
next_tick = pygame.time.get_ticks() + interval

last_time = time.time()

# Init pygame
pygame.init()

# Set attributes
org_screen = pygame.display.set_mode(settings.GAME_WINDOW_SIZE)
screen = org_screen.copy()
screen_rect = screen.get_rect()
GAME_FONT = pygame.font.Font("./assets/fonts/fonts.ttf", 50)
pygame.display.set_caption("Space Invaders")
clock = pygame.time.Clock()

# Declare objects
player = objects.Spaceship(10, settings.GAME_WINDOW_SIZE[1] - 120 - 10, 100, 120)
asteroidGenerator = objects.Generator(0, 5, 50, 2)
gameBackground = objects.Background('./assets/imgs/spacebackground2.png', [0, 0])

offset = (0, 0)
last_shake = time.time()

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
        
def shake(offset):
    shake_offset = 0
    
    if offset[0] >= 0:
        shake_offset = -2
    else:
        shake_offset = 2
        
    return (shake_offset, 0)
            
# Place threads here
try:
    pass
except Exception as error:
    print(error)
    quit()

pygame.display.update()

# sounds.space_music.play()

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
        org_screen.fill((0, 0, 0))
        screen.fill((255,255,255))
            
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
        
        # if time.time() - last_shake > 0.3:
        #     offset = shake(offset)
        
        # Display them here
        # org_screen.blit(gameBackground.image, gameBackground.rect)
        
        display_surfaces([
            (gameBackground.image, gameBackground.rect),
            (player.image, player.rect),
            (score_label[0], score_label[1])
        ])
        
        display_surfaces(player.bullets)
        display_surfaces(asteroidGenerator.asteroids)
        
        org_screen.blit(screen, offset)
        
        pygame.display.update()
        clock.tick(60)
        
except Exception as error:
    print(error)
    quit()