import pygame

# Paddle Class #
class Paddle:
    def __init__(self, position, size, color):
        # Sets variables to access from outside the class #
        self.position = pygame.Vector2()
        self.position.xy = position[0], position[1]

        self.size = pygame.Vector2()
        self.size.xy = size[0], size[1]

        self.color = color

    def is_touching(self, ball):
        touching = False

        # X Check #
        if int(ball.position.x + ball.size / 2) >= int(self.position.x) and int(ball.position.x + ball.size / 2) <= int(self.position.x) + int(self.size.x):
            # Y Check #
            if int(ball.position.y) + int(ball.size) >= int(self.position.y) and int(ball.position.y) - int(ball.size) <= int(self.position.y) + int(self.size.y):
                touching = True

        return touching