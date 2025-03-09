import pygame
import random

class Enemy:
    def __init__(self, image_path, screen_width, screen_height):
        self.image = pygame.image.load(image_path)
        self.x = random.randint(0, screen_width - 64)
        self.y = random.randint(50, 150)
        self.x_change = 3
        self.y_change = 40

    def move(self, screen_width):
        self.x += self.x_change
        if self.x <= 0 or self.x >= screen_width - 64:
            self.x_change *= -1
            self.y += self.y_change

    def draw(self, screen):
        screen.blit(self.image, (self.x, self.y))

    def reset_position(self, screen_width, screen_height):
        """Resets the enemy's position to a random spot."""
        self.x = random.randint(0, screen_width - 64)
        self.y = random.randint(50, 150)
