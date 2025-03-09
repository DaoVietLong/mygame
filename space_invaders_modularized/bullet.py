import pygame

class Bullet:
    def __init__(self, image_path, speed, magazine_size, reload_time):
        self.image = pygame.image.load(image_path)
        self.speed = speed
        self.magazine_size = magazine_size
        self.reload_time = reload_time
        self.magazine = [{"x": 0, "y": 0, "state": "ready"} for _ in range(magazine_size)]
        self.reloading = False
        self.reload_timer = 0

    def fire(self, x, y):
        """Fire the next available bullet in the magazine."""
        for bullet in self.magazine:
            if bullet["state"] == "ready":
                bullet["state"] = "fire"
                bullet["x"] = x
                bullet["y"] = y
                return

    def move(self):
        """Move all bullets currently in the 'fire' state."""
        for bullet in self.magazine:
            if bullet["state"] == "fire":
                bullet["y"] -= self.speed
                if bullet["y"] < 0:  # Change state to 'disappear' if it goes off-screen
                    bullet["state"] = "disappear"

    def reload(self):
        """Reload all bullets in the magazine."""
        for bullet in self.magazine:
            if bullet["state"] == "disappear":  # Only reload 'disappear' bullets
                bullet["state"] = "ready"

    def draw(self, screen):
        """Draw all bullets currently in the 'fire' state."""
        for bullet in self.magazine:
            if bullet["state"] == "fire":
                screen.blit(self.image, (bullet["x"] + 16, bullet["y"] + 10))
