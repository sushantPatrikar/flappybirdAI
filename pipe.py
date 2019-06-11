import random

import pygame

from game import Game


class Pipe:
    gap = 100

    # pipes = []
    def __init__(self):
        self.x = Game.width
        self.y = random.randrange(self.gap, Game.height)
        self.z = 0

    def showPipe(self):
        pygame.draw.rect(Game.gameDisplay, Game.green, [self.x, self.y, 75, (Game.height - self.y)])
        pygame.draw.rect(Game.gameDisplay, Game.green, [self.x, 0, 75, (self.y - self.gap)])
