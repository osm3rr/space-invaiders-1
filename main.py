from turtle import distance
from numpy import math
import pygame
from random import randint
import math
from pygame import mixer

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

# background sound
mixer.music.load( 'gamemusic.wav' )
mixer.music.play( -1 )

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
enemy_img = []
enemy_x = []
enemy_y = []
enemy_x_change = []
enemy_y_change = []
num_of_enemies = 6

# enemy loop
for e in range( num_of_enemies ):
    enemy_img.append( pygame.image.load('enemy.png') )
    enemy_x.append( randint( 0, 735 ) )
    enemy_y.append( randint( 50, 150 ) )
    enemy_x_change.append( 4 )
    enemy_y_change.append( 40 )

# bullet definitions
bullet_img = pygame.image.load('bullet.png')
bullet_x = 0
bullet_y = 480
bullet_x_change = 0
bullet_y_change = 10
bullet_state = "ready"

# score
score_value = 0

font = pygame.font.Font('freesansbold.ttf', 32)
#font = pygame.font.Font('stocky.ttf', 32)


text_x = 10
text_y = 10

def show_score(x, y):
    # define the score text
    score = font.render( "Score: " + str( score_value ), True, (255, 255, 255) )
    screen.blit( score, ( x, y ) )

# player function
def player(x, y):
    screen.blit( player_img, ( x, y ) )

# enemy function
def create_enemy(x, y, e):
    screen.blit( enemy_img[e], ( x, y ) )
    
# bullet function
def fire_bullet( x, y ):
    global bullet_state
    bullet_state = "fire"
    screen.blit( bullet_img, ( x + 16, y + 10 ) ) # for a better bullet ubication
    
# Function for detect the collision between the enemy and the bullet
def is_collision( enemy_x, enemy_y, bullet_x, bullet_y ):
    
    distance_enemy_bullet = math.sqrt( ( enemy_x - bullet_x )**2 + ( enemy_y - bullet_y )**2 )
        
    if distance_enemy_bullet < 27: # review why this value
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
                    bullet_sound = mixer.Sound( 'shotgun-firing.wav' )
                    bullet_sound.play()
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
    for enemy in range( num_of_enemies ):
        enemy_x[enemy] += enemy_x_change[enemy]
        
        if enemy_x[enemy] <= 0:
            enemy_x_change[enemy] = 4
            enemy_y[enemy] += enemy_y_change[enemy] 
            
        elif enemy_x[enemy] >= 736:
            enemy_x_change[enemy] = -4
            enemy_y[enemy] += enemy_y_change[enemy]
        
        # collision 
        collision =  is_collision( enemy_x[enemy], enemy_y[enemy], bullet_x, bullet_y)
    
        if collision:
            explosion_sound = mixer.Sound( 'hq-explosion.wav' )
            explosion_sound.play()
            
            bullet_y = 480
            bullet_state = "ready"
            score_value += 1
            # print for tests. We delete this sentence for add the score in the screen
            # print( score )
            enemy_x[enemy] = randint( 0, 735 )
            enemy_y[enemy] = randint( 50, 150 )
        
        create_enemy( enemy_x[enemy], enemy_y[enemy], enemy )
    
    # bullet movement
    if bullet_y <= 0:
        bullet_y = 480
        bullet_state = "ready"
    
    if bullet_state == "fire":
        fire_bullet( bullet_x, bullet_y )
        bullet_y -= bullet_y_change
        
    player( player_x, player_y )
    show_score( text_x, text_y )
    pygame.display.update()    