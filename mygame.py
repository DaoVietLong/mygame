import pygame
import random
import math
from pygame import mixer

# Name
GAME_NAME = "Space Invader"
# constants
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
NUM_OF_ENEMY = 5

# assets paths
PLAYER_IMAGE = "images/spaceship_resized.png"
ENEMY_IMAGE = "images/enemy_resized.png"
BULLET_IMAGE = "images/bullet_1_resized.png"
BACKGROUND_SOUND = "sounds/background.wav"
GAME_OVER_SOUND = "sounds/game_over.wav"
EXPLOSION_SOUND = "sounds/explosion.wav"
BULLET_SOUND = "sounds/laser.wav"
FONT = "freesansbold.ttf"

# initialize pygame
pygame.init()

# initialize pygame screen
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption(GAME_NAME)

# background music
mixer.music.load(BACKGROUND_SOUND)
mixer.music.play(-1)

# sounds
game_over_sound = mixer.Sound(GAME_OVER_SOUND)
explosion_sound = mixer.Sound(EXPLOSION_SOUND)
bullet_sound = mixer.Sound(BULLET_SOUND)

# player 
player_img = pygame.image.load(PLAYER_IMAGE)
player_x = 370
player_y = 480
player_x_change = 0
player_y_change = 0

# function to draw player
def player(x, y):
    screen.blit(player_img, (x, y))

# enemies
enemy_img = pygame.image.load(ENEMY_IMAGE)
enemy_x = []
enemy_y = []
enemy_x_change = []
enemy_y_change = []
game_over_font = pygame.font.Font(FONT, 64)

# function to initialize enemies
def initialize_enemies(num_of_enemy):
    for i in range(num_of_enemy):
        enemy_x.append(random.randint(0, SCREEN_WIDTH - 64))
        enemy_y.append(random.randint(50, 150))
        enemy_x_change.append(0.3)
        enemy_y_change.append(40)

initialize_enemies(NUM_OF_ENEMY)

# function to draw enemies
def enemies(x, y):
    screen.blit(enemy_img, (x, y))

# function to print game over text
def game_over_text():
    game_over = game_over_font.render("GAME OVER", True, (255, 0, 0))
    screen.blit(game_over, (200, 250))

# bullets
bullet_img = pygame.image.load(BULLET_IMAGE)
bullet_x = 0
bullet_y = 480
bullet_x_change = 0
bullet_y_change = 1
bullet_state = "ready"  # "ready" means you can fire, "fire" means bullet is moving

# function to fire bullet
def fire_bullet(x, y):
    global bullet_state
    bullet_state = "fire"
    screen.blit(bullet_img, (x + 16, y + 10))

# function to reload bullet
def reload(player_y):
    global bullet_state, bullet_y
    bullet_y = player_y
    bullet_state = "ready"

# stars 
stars = [{"x": random.randint(0, SCREEN_WIDTH), "y": random.randint(0, SCREEN_HEIGHT)} for _ in range(100)]
frame_count = 0

# function to draw stars
def draw_stars():
    for star in stars:
        pygame.draw.circle(screen, (255, 255, 255), (star["x"], star["y"]), 2)
# function to update stars
def update_stars():
    for star in stars:
        star["y"] += 1  # Move stars down slowly
        if star["y"] > SCREEN_HEIGHT:  # Reset star position if it moves out of the screen
            star["x"] = random.randint(0, SCREEN_WIDTH)
            star["y"] = 0

# function to check collision
def is_collision(enemy_x, enemy_y, object_x, object_y):
    distance = math.sqrt(math.pow(enemy_x - object_x, 2) + math.pow(enemy_y - object_y, 2))
    return distance <= 32
    
# score
my_score = 0
font = pygame.font.Font(FONT, 32)
text_x = 10
text_y = 10

# function to show score
def show_score(x, y):
    score = font.render("Enemy defeated: " + str(my_score), True, (255, 255, 255))
    screen.blit(score, (x, y))

# game loop
running = True
while running:
    # background
    screen.fill((0, 0, 64))

    # stars
    if frame_count % 5 == 0:
        update_stars()
    draw_stars()
    
    # game loop
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        # using keyboard to move
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                player_x_change = -0.5

            if event.key == pygame.K_RIGHT:
                player_x_change = 0.5

            if event.key == pygame.K_UP:
                player_y_change = -0.5

            if event.key == pygame.K_DOWN:
                player_y_change = 0.5

            if event.key == pygame.K_SPACE:
                if bullet_state == "ready":
                    bullet_sound.play()

                    # set bullet position to player position
                    bullet_x = player_x 
                    bullet_y = player_y  

                    # fire bullet
                    fire_bullet(bullet_x, bullet_y)

        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT or event.key == pygame.K_UP or event.key == pygame.K_DOWN:
                # remain position
                player_x_change = 0
                player_y_change = 0

    # changing player position
    player_x += player_x_change
    player_y += player_y_change

    # changing enemies position
    for enemy in range(NUM_OF_ENEMY):
        # game over
        crash = is_collision(enemy_x[enemy], enemy_y[enemy], player_x, player_y)

        # if enemy go to far
        if enemy_y[enemy] > 250:
            for enemy in range(NUM_OF_ENEMY):
                enemy_y[enemy] = 2000
            game_over_sound.play()
            game_over_text()
            break
            
        # ìf collide with enemy
        elif crash:
            for enemy in range(NUM_OF_ENEMY):
                enemy_y[enemy] = 2000
            explosion_sound.play()
            game_over_sound.play()
            game_over_text()
            break

        # changing enemies position
        enemy_x[enemy] += enemy_x_change[enemy]
        if enemy_x[enemy] <= 0:
            enemy_x_change[enemy] = 0.3
            enemy_y[enemy] += enemy_y_change[enemy]
        if enemy_x[enemy] >= SCREEN_WIDTH - 64:
            enemy_x_change[enemy] = -0.3
            enemy_y[enemy] += enemy_y_change[enemy]

        # kill
        kill = is_collision(enemy_x[enemy], enemy_y[enemy], bullet_x, bullet_y)
        if kill:
            explosion_sound.play()

            # reload
            reload(player_y)

            # count score
            my_score += 1

            # enemy respawn position
            enemy_x[enemy] = random.randint(0, SCREEN_WIDTH - 64)
            enemy_y[enemy] = random.randint(50, 150)

        # draw enemies
        enemies(enemy_x[enemy], enemy_y[enemy])

    # changing bullet position
    if bullet_y <= 0:
        reload(player_y)

    if bullet_state is "fire":
        fire_bullet(bullet_x, bullet_y)
        bullet_y -= bullet_y_change

    # adding boundaries
    if player_x <= 0:
        player_x = 0
    if player_x >= SCREEN_WIDTH - 64:
        player_x = SCREEN_WIDTH - 64 
    if player_y <= 0:
        player_y = 0
    if player_y >= SCREEN_HEIGHT - 64:
        player_y = SCREEN_HEIGHT - 64

    # draw player
    player(player_x, player_y)

    # show score
    show_score(text_x, text_y)

    # update display
    pygame.display.update()

pygame.quit()