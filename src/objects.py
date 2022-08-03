# Imports
import time
import pygame
from random import randrange
from time import sleep

import settings

# Settings
asteroid_spawn_y = 20

# Functions
def find_place_in_list(nums, lost):
    last_num = 0
    
    for num in nums:
        if lost >= last_num and lost < num:
            return last_num
        
        last_num = num

# Classes
class Generator:
    
    def __init__(self, spawn_y, start_point_x, default_size, spawnrate):
        
        # Class variables
        self.spawn_y = spawn_y
        self.start_point_x = start_point_x
        self.default_size = default_size
        self.spawnRate = spawnrate
        
        self.asteroids = pygame.sprite.Group()
        self.shouldRun = False
        self.last_generation = time.time()
        self.creation_rate = 2
        self.score = 0
        self.difficulty = 0
        
        self.size_to_hp = {
            10: 1,
            30: 1,
            50: 2,
            70: 3,
            5000: 3 # Set an impossible number as the max
        }
    
    def create_asteroid(self):
        pos_variance = randrange(-10, 20)
        size_variance = randrange(-20, 50)
        
        size = self.default_size + size_variance
        speed = 5
        
        spawn_x = randrange(self.start_point_x + size + 10, settings.GAME_WINDOW_SIZE[0] - size - 10)

        newAsteroid = Asteroid(spawn_x, self.spawn_y + pos_variance, size , size, speed, 1)
        
        hp = self.size_to_hp[find_place_in_list(self.size_to_hp, size)]
        
        hp_increase = 0
        
        if self.difficulty <= 2:
            hp_increase = self.difficulty
        
        newAsteroid.health = hp + hp_increase
        
        print(newAsteroid)
        return newAsteroid
    
    def update(self):
        
        if time.time() - self.last_generation > self.creation_rate:
            if self.difficulty == 0:
                asteroidAmount = 1
            else:
                asteroidAmount = self.difficulty
            
            for i in range(0, asteroidAmount):
                self.generate_asteroid()
            
            print(self.asteroids)
            
    def generate_asteroid(self):
        if self.score >= 10:
            if self.difficulty < 3:
                print("Increase asteroid spawn amount")
                self.difficulty += 1
            
            if self.creation_rate > 1.4:
                print("Decrease asteroid spawn rate")
                self.creation_rate -= 0.2
                
            self.score = 0
        
        asteroid = self.create_asteroid()
        self.asteroids.add(asteroid)
        
        self.last_generation = time.time()
        self.score += 1
            
    def stop(self):
        self.shouldRun = False

class Spaceship(pygame.sprite.Sprite):
    def __init__(self, dx, dy, sx, sy):
        super().__init__()
        self.image = pygame.image.load("./assets/imgs/Spaceship.png").convert_alpha()
        
        self.rect = self.image.get_rect()
        self.rect.x = dx
        self.rect.y = dy
        
        # Change the size of the spaceship
        self.image = pygame.transform.scale(self.image, (sx, sy))
        self.size_x = sx
        self.size_y = sy
        
        # Class variables
        self.vel_x = 0
        self.max_vel_x = 5
        self.vel_y = 0
        self.max_vel_y = 5
        
        self.bullets = pygame.sprite.Group()
        
        self.friction = 1
        self.firerate = 0.2
        
        self.shouldShoot = False
        self.gameRun = True
        self.last_shoot = None
        
    def move_x(self, x, delta):
        if x < 0: # Some rounding corrections
            x += 1
            
        self.rect.x += x * delta
            
    def move_y(self, y, delta):
        self.rect.y += y * delta
        
    def shoot(self):
        newBullet = Bullet(self.rect.x, self.rect.y, 10, 30, 10)
        newBullet2 = Bullet(self.rect.x + self.size_x - 20, self.rect.y, 10, 30, 10)
        self.bullets.add(newBullet)
        self.bullets.add(newBullet2)
        
        self.last_shoot = time.time()
            
    def update(self):
        if self.rect.left < 0:
            self.rect.left = 0
        elif self.rect.right > settings.GAME_WINDOW_SIZE[0] - 50:
            self.rect.right = settings.GAME_WINDOW_SIZE[0] - 50

        if self.rect.top < 0:
            self.rect.top = 0
        elif self.rect.bottom > settings.GAME_WINDOW_SIZE[1]:
            self.rect.bottom = settings.GAME_WINDOW_SIZE[1]
            
        if self.shouldShoot:
            if time.time() - self.last_shoot > self.firerate:
                self.shouldShoot = False
                

class Asteroid(pygame.sprite.Sprite):
    
    def __init__(self, dx, dy, sx, sy, speed, hp):
        super().__init__()
        
        self.image = pygame.image.load("./assets/imgs/asteroid.png")
        
        # Change the size of the asteroid
        self.image = pygame.transform.scale(self.image, (sx, sy))
        self.size_x = sx
        self.size_y = sy
        
        self.rect = self.image.get_rect()
        self.rect.x = dx
        self.rect.y = dy
        
        # Class variables
        self.health = hp
        self.speed = speed
        self.point = 1
        
    def update(self, delta):
        if self.rect.y < settings.GAME_WINDOW_SIZE[1]:
            self.rect.y += self.speed * delta
        else:
            self.kill()
            
        if self.rect.left < 0:
            self.kill()
        elif self.rect.right > settings.GAME_WINDOW_SIZE[0]:
            self.kill()
            
            
class Bullet(pygame.sprite.Sprite):
    
    def __init__(self, dx, dy, sx, sy, speed):
        super().__init__()
        
        self.image = pygame.image.load("./assets/imgs/bullets.png").convert_alpha()
        
        self.rect = self.image.get_rect()
        self.rect.x = dx
        self.rect.y = dy
        
        # Change the size of the bullet
        self.image = pygame.transform.scale(self.image, (sx, sy))
        self.size_x = sx
        self.size_y = sy
        
        # Class variables
        self.speed = speed
        self.damage = 1
        
    def update(self, delta):
        if self.rect.y > 0:
            self.rect.y -= self.speed * delta
        else:
            self.kill()
            
            
class Background(pygame.sprite.Sprite):
    def __init__(self, image_file, location):
        pygame.sprite.Sprite.__init__(self)  #call Sprite initializer
        self.image = pygame.image.load(image_file)
        self.image = pygame.transform.scale(self.image, (settings.GAME_WINDOW_SIZE[0], settings.GAME_WINDOW_SIZE[1]))
        
        self.rect = self.image.get_rect()
        self.rect.left, self.rect.top = location