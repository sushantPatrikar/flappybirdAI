import random
import pygame

from game import Game

class Pipe:
    # gap is the number of units of space between the upper and lower pipes
    gap = 100

    def __init__(self):
        self.x = Game.width
        self.y = random.randrange(self.gap, Game.height)
        self.z = 0

    def showPipe(self):
        ''' Show the upper then the lower pipe. 75 is the width of the pipe '''
        pygame.draw.rect(Game.gameDisplay, Game.pipeColour, [self.x, self.y, 75, (Game.height - self.y)])
        pygame.draw.rect(Game.gameDisplay, Game.pipeColour, [self.x, 0, 75, (self.y - self.gap)])
