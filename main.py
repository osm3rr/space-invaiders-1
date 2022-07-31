from turtle import distance
from numpy import math
import pygame
from random import randint
import math

# initialize the pygame
pygame.init()

# screen size
screen_width = 800
screen_height = 600

size = ( screen_width, screen_height )

# display the screen
screen = pygame.display.set_mode( size )

# background
background = pygame.image.load( 'space-bg.png' )

# windows title
pygame.display.set_caption( "Space invaders - osm3rr" )

# icon
icon = pygame.image.load( 'ufo.png' )
pygame.display.set_icon( icon )

# player definitions
player_img = pygame.image.load('player3.png')
player_x = 370
player_y = 480
player_x_change = 0

# enemy definitions
enemy_img = pygame.image.load('enemy.png')
enemy_x = randint( 0, 735 )
enemy_y = randint( 50, 150 )
enemy_x_change = 4
enemy_y_change = 40

# bullet definitions
bullet_img = pygame.image.load('bullet.png')
bullet_x = 0
bullet_y = 480
bullet_x_change = 0
bullet_y_change = 10
bullet_state = "ready"

# score
score = 0


# player function
def player(x, y):
    screen.blit( player_img, ( x, y ) )

# enemy function
def enemy(x, y):
    screen.blit( enemy_img, ( x, y ) )
    
# bullet function
def fire_bullet( x, y ):
    global bullet_state
    bullet_state = "fire"
    screen.blit( bullet_img, ( x + 16, y + 10 ) )
    
# Function for detect the collision between the enemy and the bullet
def is_collision( enemy_x, enemy_y, bullet_x, bullet_y ):
    distance_enemy_bullet = math.sqrt( ( enemy_x - bullet_x )**2 + ( enemy_y - bullet_y )**2 )
    
    if distance_enemy_bullet < 27:
        return True
    else:
        return False

# game loop
running = True
while running:
    # RGB: Red - Gree - Blue
    rgb = (0, 0, 0)
    screen.fill( rgb )
    
    # background
    screen.blit( background, (0, 0) )
          
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        
        # if keystroke is pressed check wheter its right or left
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                player_x_change = -5 
                
            if event.key == pygame.K_RIGHT:
                player_x_change = 5
                
            if event.key == pygame.K_SPACE:
                if bullet_state == "ready":
                    # get the current x cordinate of the spaceship
                    bullet_x = player_x
                    fire_bullet( bullet_x, bullet_y )
            
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                player_x_change = 0
                             
    # player boundaries
    player_x += player_x_change
    
    if player_x <= 0:
        player_x = 0
        
    elif player_x >= 736:
        player_x = 736
        
    # enemy movement
    enemy_x += enemy_x_change
    
    if enemy_x <= 0:
        enemy_x_change = 4
        enemy_y += enemy_y_change 
        
    elif enemy_x >= 736:
        enemy_x_change = -4
        enemy_y += enemy_y_change
    
    # bullet movement
    if bullet_y <= 0:
        bullet_y = 480
        bullet_state = "ready"
    
    if bullet_state == "fire":
        fire_bullet( bullet_x, bullet_y )
        bullet_y -= bullet_y_change
        
    # collision 
    collision =  is_collision( enemy_x, enemy_y, bullet_x, bullet_y)
    
    if collision:
        bullet_y = 480
        bullet_state = "ready"
        score += 1
        print( score )
        enemy_x = randint( 0, 735 )
        enemy_y = randint( 50, 150 )
    
    player( player_x, player_y )
    enemy( enemy_x, enemy_y )
    pygame.display.update()    