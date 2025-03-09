import pygame
from pygame import mixer
from player import Player
from enemy import Enemy
from bullet import Bullet
from background import Background
from constants import *

class Game:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption(GAME_NAME)

        mixer.music.load(BACKGROUND_SOUND)
        mixer.music.play(-1)

        self.lost_point_y = LOST_POINT  # Threshold for the lost point
        self.warning_active = False
        self.warning_timer = 0

        self.clock = pygame.time.Clock()
        self.running = True
        self.game_over = False
        self.game_over_timer = GAME_OVER_TIME

        # Player, enemies, and bullets
        self.player = Player(PLAYER_IMAGE, 370, 480)
        self.enemies = [Enemy(ENEMY_IMAGE, SCREEN_WIDTH, SCREEN_HEIGHT) for _ in range(NUM_OF_ENEMY)]
        self.bullets = [
            Bullet("images/bullet_1_resized.png", speed=BULLET_1_SPEED, magazine_size=MAGAZINE_1_SIZE, reload_time=RELOAD_TIME_1),
            Bullet("images/bullet_2_resized.png", speed=BULLET_2_SPEED, magazine_size=MAGAZINE_2_SIZE, reload_time=RELOAD_TIME_2),
            Bullet("images/bullet_3_resized.png", speed=BULLET_3_SPEED, magazine_size=MAGAZINE_3_SIZE, reload_time=RELOAD_TIME_3),
        ]
        self.current_bullet = 0
        self.reload_timer = 0

        self.background = Background(100, SCREEN_WIDTH, SCREEN_HEIGHT)
        self.score = 0

        self.reloading = False
        self.reload_complete_timer = 0

    def is_collision(self, x1, y1, x2, y2):
        return ((x2 - x1) ** 2 + (y2 - y1) ** 2) ** 0.5 < 32

    def reload_current_bullet(self):
        """Reload the magazine of the current bullet type."""
        if not self.reloading:
            self.reloading = True
            self.reload_timer = self.bullets[self.current_bullet].reload_time
            print(f"Reloading bullet type {self.current_bullet + 1}...")

    def handle_reloading(self):
        """Handles the reload timer and reload completion."""
        if self.reloading:
            self.reload_timer -= 1
            if self.reload_timer <= 0:
                self.reloading = False
                self.bullets[self.current_bullet].reload()
                self.reload_complete_timer = RELOAD_COMPLETE_TIME
                print(f"Reload complete for bullet type {self.current_bullet + 1}.")

    def show_magazine(self, x, y):
        """Display the magazine status for the current bullet."""
        font = pygame.font.Font(FONT, 32)
        current_bullet = self.bullets[self.current_bullet]
        text = font.render(
            f"Bullet {self.current_bullet + 1}: {len([b for b in current_bullet.magazine if b['state'] == 'ready'])}/{current_bullet.magazine_size}",
            True,
            (255, 255, 255),
        )
        self.screen.blit(text, (x, y))

    def show_reloading_message(self):
        """Display the reloading message."""
        font = pygame.font.Font(FONT, 32)
        text = font.render(f"Reloading Bullet {self.current_bullet + 1}...", True, (255, 255, 0))
        self.screen.blit(text, (200, 300))

    def show_reload_complete_message(self):
        """Display the reload complete message."""
        font = pygame.font.Font(FONT, 32)
        text = font.render("Reload complete!", True, (0, 255, 0))
        self.screen.blit(text, (200, 300))

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False

            if not self.game_over:
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_LEFT:
                        self.player.x_change = -5
                    if event.key == pygame.K_RIGHT:
                        self.player.x_change = 5
                    if event.key == pygame.K_UP:
                        self.player.y_change = -5
                    if event.key == pygame.K_DOWN:
                        self.player.y_change = 5
                    if event.key == pygame.K_SPACE:
                        self.bullets[self.current_bullet].fire(self.player.x, self.player.y)
                        mixer.Sound(BULLET_SOUND).play()
                    if event.key == pygame.K_r:
                        self.reload_current_bullet()
                    if event.key == pygame.K_e:
                        self.current_bullet = (self.current_bullet + 1) % len(self.bullets)

                if event.type == pygame.KEYUP:
                    if event.key in [pygame.K_LEFT, pygame.K_RIGHT, pygame.K_UP, pygame.K_DOWN]:
                        self.player.x_change = 0
                        self.player.y_change = 0

    def check_enemy_lost_point(self):
        """Check if any enemy is near the lost point."""
        self.warning_active = False
        for enemy in self.enemies:
            if enemy.y >= self.lost_point_y:  # Enemy near the lost point
                self.warning_active = True
                self.warning_timer = 60  # Warning lasts for 1 second
                return

    def show_warning(self):
        """Display a warning message on the screen."""
        if self.warning_active or self.warning_timer > 0:
            font = pygame.font.Font(FONT, 32)
            warning_text = font.render("Warning! Enemy Near Lost Point!", True, (255, 0, 0))
            self.screen.blit(warning_text, (SCREEN_WIDTH // 2 - 200, SCREEN_HEIGHT - 50))
            self.warning_timer -= 1

    def update(self):
        if not self.game_over:
            self.player.move(SCREEN_WIDTH, SCREEN_HEIGHT)

            for enemy in self.enemies:
                enemy.move(SCREEN_WIDTH)

            for bullet in self.bullets:
                bullet.move()

            # Check for collisions
            for enemy in self.enemies:
                for bullet in self.bullets:
                    for b in bullet.magazine:
                        if b["state"] == "fire" and self.is_collision(enemy.x, enemy.y, b["x"], b["y"]):
                            self.score += 1
                            b["state"] = "disappear"
                            enemy.reset_position(SCREEN_WIDTH, SCREEN_HEIGHT)

                # Check if enemy reaches the player or lost point
                if self.is_collision(enemy.x, enemy.y, self.player.x, self.player.y):
                    self.game_over = True
                    mixer.Sound(GAME_OVER_SOUND).play()

                if enemy.y >= self.lost_point_y + 64:
                    self.game_over = True
                    mixer.Sound(GAME_OVER_SOUND).play()

            # Check for enemies near the lost point
            self.check_enemy_lost_point()

        self.handle_reloading()

    def draw(self):
        self.screen.fill((0, 0, 64))
        self.background.draw(self.screen)
        self.player.draw(self.screen)
        for enemy in self.enemies:
            enemy.draw(self.screen)
        for bullet in self.bullets:
            bullet.draw(self.screen)

        self.show_score(10, 10)
        self.show_magazine(10, 50)

        # Show warning if active
        self.show_warning()

        if self.reloading:
            self.show_reloading_message()
        if self.reload_complete_timer > 0:
            self.reload_complete_timer -= 1
            self.show_reload_complete_message()

        if self.game_over:
            self.show_game_over()

        pygame.display.update()

    def show_score(self, x, y):
        font = pygame.font.Font(FONT, 32)
        score_text = font.render(f"Score: {self.score}", True, (255, 255, 255))
        self.screen.blit(score_text, (x, y))

    def show_game_over(self):
        font = pygame.font.Font(FONT, 64)
        game_over_text = font.render("GAME OVER", True, (255, 0, 0))
        self.screen.blit(game_over_text, (200, 250))
        self.game_over_timer -= 1
        if self.game_over_timer <= 0:
            self.running = False

    def run(self):
        while self.running:
            self.handle_events()
            if not self.game_over or self.game_over_timer > 0:
                self.update()
            self.draw()
            self.clock.tick(60)
        pygame.quit()
