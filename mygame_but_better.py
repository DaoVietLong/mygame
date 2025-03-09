import pygame
import random
import math
from pygame import mixer

# Game Constants
GAME_NAME = "Space Invader"
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
NUM_OF_ENEMY = 5
MAGAZINE_SIZE = 3
RELOAD_TIME = 500
RELOAD_COMPLETE_TIME = 300
GAME_OVER_TIME = 4000

# Asset Paths
PLAYER_IMAGE = "images/spaceship_resized.png"
ENEMY_IMAGE = "images/enemy_resized.png"
BULLET_IMAGE = "images/bullet_1_resized.png"
BACKGROUND_SOUND = "sounds/background.wav"
GAME_OVER_SOUND = "sounds/game_over.wav"
EXPLOSION_SOUND = "sounds/explosion.wav"
BULLET_SOUND = "sounds/laser.wav"
FONT = "freesansbold.ttf"

# Initialize pygame
pygame.init()
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption(GAME_NAME)

# Sounds
mixer.music.load(BACKGROUND_SOUND)
mixer.music.play(-1)
game_over_sound = mixer.Sound(GAME_OVER_SOUND)
explosion_sound = mixer.Sound(EXPLOSION_SOUND)
bullet_sound = mixer.Sound(BULLET_SOUND)

# Player
player_img = pygame.image.load(PLAYER_IMAGE)
player_x = 370
player_y = 480
player_x_change = 0
player_y_change = 0

def draw_player(x, y):
    screen.blit(player_img, (x, y))

# Enemies
enemy_img = pygame.image.load(ENEMY_IMAGE)
enemy_x = []
enemy_y = []
enemy_x_change = []
enemy_y_change = []
for _ in range(NUM_OF_ENEMY):
    enemy_x.append(random.randint(0, SCREEN_WIDTH - 64))
    enemy_y.append(random.randint(50, 150))
    enemy_x_change.append(0.3)
    enemy_y_change.append(40)

def draw_enemy(x, y):
    screen.blit(enemy_img, (x, y))

# Bullets (Magazine)
bullet_img = pygame.image.load(BULLET_IMAGE)
magazine = [{"x": 0, "y": 0, "state": "ready"} for _ in range(MAGAZINE_SIZE)]
reloading = False
reload_timer = 0
reload_complete_timer = 0
flicker_counter = 0  # Counter to manage text flickering

def fire_bullet(index, x, y):
    magazine[index]["state"] = "fire"
    magazine[index]["x"] = x
    magazine[index]["y"] = y
    screen.blit(bullet_img, (x + 16, y + 10))

def reload_magazine():
    global reloading, reload_timer, reload_complete_timer
    reloading = True
    reload_timer = RELOAD_TIME
    reload_complete_timer = 0 
    print("Reloading...")

# Collision Detection
def is_collision(enemy_x, enemy_y, object_x, object_y):
    distance = math.sqrt(math.pow(enemy_x - object_x, 2) + math.pow(enemy_y - object_y, 2))
    return distance <= 32

# Stars for Background
stars = [{"x": random.randint(0, SCREEN_WIDTH), "y": random.randint(0, SCREEN_HEIGHT)} for _ in range(100)]

def draw_stars():
    for star in stars:
        pygame.draw.circle(screen, (255, 255, 255), (star["x"], star["y"]), 2)

def update_stars():
    for star in stars:
        star["y"] += 1
        if star["y"] > SCREEN_HEIGHT:
            star["x"] = random.randint(0, SCREEN_WIDTH)
            star["y"] = 0

# Score and Bullets Text
score_value = 0
font = pygame.font.Font(FONT, 32)


def show_score(x, y):
    score = font.render(f"Score: {score_value}", True, (255, 255, 255))
    screen.blit(score, (x, y))

def show_magazine(x, y):
    bullets_left = sum(1 for bullet in magazine if bullet["state"] == "ready")
    magazine_text = font.render(f"Bullets: {bullets_left}/{MAGAZINE_SIZE}", True, (255, 255, 255))
    screen.blit(magazine_text, (x, y))

def show_reload_prompt():
    global flicker_counter
    if flicker_counter // 300 % 2 == 0:  # Flicker every 30 frames
        reload_text = font.render("Magazine empty! Press R to reload.", True, (255, 255, 255))
        screen.blit(reload_text, (200, 300))

def show_reloading_message():
    reload_text = font.render("Reloading...", True, (255, 255, 0))
    screen.blit(reload_text, (200, 300))

def show_reload_complete_message():
    reload_complete_text = font.render("Reload complete!", True, (0, 255, 0))
    screen.blit(reload_complete_text, (200, 300))

# Game Over
game_over_font = pygame.font.Font(FONT, 64)

def game_over_text():
    game_over = game_over_font.render("GAME OVER", True, (255, 0, 0))
    screen.blit(game_over, (200, 250))

# Game Loop
running = True
reload_timer = 0
while running:
    screen.fill((0, 0, 64))
    draw_stars()
    update_stars()

    flicker_counter += 1

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        # Movement
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
                for i, bullet in enumerate(magazine):
                    if bullet["state"] == "ready":
                        bullet_sound.play()
                        fire_bullet(i, player_x, player_y)
                        break
                else:
                    print("Magazine empty! Press R to reload.")
            if event.key == pygame.K_r:
                if not reloading:
                    reload_magazine()

        if event.type == pygame.KEYUP:
            if event.key in [pygame.K_LEFT, pygame.K_RIGHT, pygame.K_UP, pygame.K_DOWN]:
                player_x_change = 0
                player_y_change = 0

    # Update Player Position
    player_x += player_x_change
    player_y += player_y_change
    player_x = max(0, min(player_x, SCREEN_WIDTH - 64))
    player_y = max(0, min(player_y, SCREEN_HEIGHT - 64))

    # Update Bullets
    for bullet in magazine:
        if bullet["state"] == "fire":
            screen.blit(bullet_img, (bullet["x"] + 16, bullet["y"] + 10))
            bullet["y"] -= 2
            if bullet["y"] <= 0:
                bullet["state"] = "disappear"

    # Handle Reloading
    if reloading:
        reload_timer -= 1
        show_reloading_message()
        if reload_timer <= 0:
            for bullet in magazine:
                if bullet["state"] == "disappear":
                    bullet["state"] = "ready"
            reloading = False
            reload_complete_timer = RELOAD_COMPLETE_TIME
            print("Reload complete!")

    if reload_complete_timer > 0:
        reload_complete_timer -= 1
        show_reload_complete_message()

    # Handle Enemies
    for i in range(NUM_OF_ENEMY):

        enemy_x[i] += enemy_x_change[i]
        if enemy_x[i] <= 0:
            enemy_x_change[i] = 0.3
            enemy_y[i] += enemy_y_change[i]
        elif enemy_x[i] >= SCREEN_WIDTH - 64:
            enemy_x_change[i] = -0.3
            enemy_y[i] += enemy_y_change[i]

        # Collision
        for bullet in magazine:
            if bullet["state"] == "fire" and is_collision(enemy_x[i], enemy_y[i], bullet["x"], bullet["y"]):
                explosion_sound.play()
                score_value += 1
                bullet["state"] = "disappear"
                enemy_x[i] = random.randint(0, SCREEN_WIDTH - 64)
                enemy_y[i] = random.randint(50, 150)

        draw_enemy(enemy_x[i], enemy_y[i])

    bullets_left = sum(1 for bullet in magazine if bullet["state"] == "ready")
    if bullets_left == 0 and not reloading:
        show_reload_prompt()

    # Handle game over
    for i in range(NUM_OF_ENEMY):
        if enemy_y[i] > 250:
            for j in range(NUM_OF_ENEMY):
                enemy_y[j] = 2000
            game_over_sound.play()
            game_over_text()
            if GAME_OVER_TIME is not None:
                GAME_OVER_TIME -= 1
                if GAME_OVER_TIME <= 0:
                    running = False
            break

        crash = is_collision(enemy_x[i], enemy_y[i], player_x, player_y)
        if crash:
            for j in range(NUM_OF_ENEMY):
                enemy_y[j] = 2000
            game_over_sound.play()
            game_over_text()
            if GAME_OVER_TIME is not None:
                GAME_OVER_TIME -= 1
                if GAME_OVER_TIME <= 0:
                    running = False
            break

    draw_player(player_x, player_y)
    show_score(10, 10)
    show_magazine(10, 50)
    pygame.display.update()
