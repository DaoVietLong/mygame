import pygame
import random

class Background:
    def __init__(self, num_stars, screen_width, screen_height):
        self.stars = [{"x": random.randint(0, screen_width), "y": random.randint(0, screen_height)} for _ in range(num_stars)]
        self.screen_width = screen_width
        self.screen_height = screen_height

    def update(self):
        for star in self.stars:
            star["y"] += 1
            if star["y"] > self.screen_height:
                star["x"] = random.randint(0, self.screen_width)
                star["y"] = 0

    def draw(self, screen):
        for star in self.stars:
            pygame.draw.circle(screen, (255, 255, 255), (star["x"], star["y"]), 2)
