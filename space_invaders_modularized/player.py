import pygame

class Player:
    def __init__(self, image_path, x, y):
        self.image = pygame.image.load(image_path)
        self.x = x
        self.y = y
        self.x_change = 0
        self.y_change = 0

    def move(self, screen_width, screen_height):
        self.x += self.x_change
        self.y += self.y_change
        self.x = max(0, min(self.x, screen_width - 64))
        self.y = max(0, min(self.y, screen_height - 64))

    def draw(self, screen):
        screen.blit(self.image, (self.x, self.y))
