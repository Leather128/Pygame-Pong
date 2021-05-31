import pygame

# Pong Ball Class #
class PongBall:
    def __init__(self, position, size, color):
        # Sets variables to access from outside the class #
        self.position = pygame.Vector2()
        self.position.xy = position[0], position[1]

        self.size = size
        self.color = color

        self.velocity = pygame.Vector2()