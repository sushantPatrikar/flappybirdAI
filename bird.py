import math

import pygame

import numpy as np

from NeuralNetwork import NeuralNetwork


class Bird:
    def __init__(self, game):
        self.x = 50
        self.radius = 15
        from game import Game
        self.y = Game.height // 2
        self.y_vel = 0
        self.gravity = 1
        self.score = 0
        self.fitness = 0
        self.distance = 0
        self.brain = NeuralNetwork(8, 5, 2)
        self.game = game
        self.inputs = 8 * [0]

    def showBird(self):
        from game import Game
        pygame.draw.circle(Game.gameDisplay, Game.black, (self.x, self.y), self.radius)

    def collidingWall(self):
        from game import Game
        if (self.y + self.radius) >= Game.height or (self.y - self.radius) <= 0:
            return True

    def collidingPipe(self):
        from game import Game
        if (self.x + self.radius) in range(self.game.pipes[0].x, self.game.pipes[0].x + 76):
            if (self.y + self.radius) in range(self.game.pipes[0].y, Game.height + 1):
                return True
            elif (self.y - self.radius) in range(0, (self.game.pipes[0].y - self.game.pipes[0].gap) + 1):
                return True
        return False

    def moveUp(self):
        self.y_vel = -(self.gravity + 8)

    def findClosestPipe(self):
        for pipe in self.game.pipes:
            distance = (pipe.x + 75) - (self.x + self.radius)
            if distance >= 0:
                return pipe

    def calculateFitness(self):
        self.fitness = math.pow(2, self.score) + (self.distance ** 2)

    def think(self):
        # Inputs to neural network
        # 1. horizontal distance from the start of pipe
        # 2. horizontal distance from the end of pipe
        # 3. vertical distance from the upper pipe
        # 4. verical distance from the lower pipe
        # 5. y position of bird
        # 6. y velocity of bird
        # 7. vertical distance from upper wall
        # 8. vertical distance from ground

        pipe = self.findClosestPipe()

        # 1. horizontal distance from the start of pipe

        dis_1 = pipe.x - (self.x + self.radius)
        dis_1 /= self.game.width
        self.inputs[0] = dis_1

        # 2. horizontal distance from the end of pipe

        dis_2 = (pipe.x + 75) - (self.x + self.radius)
        dis_2 /= self.game.width
        self.inputs[1] = dis_2

        # 3. vertical distance from the upper pipe

        dis_3 = (self.y - self.radius) - (pipe.y - pipe.gap)
        dis_3 /= self.game.height
        self.inputs[2] = dis_3

        # 4. verical distance from the lower pipe

        dis_4 = (self.y + self.radius) - (pipe.y)
        dis_4 /= self.game.height
        self.inputs[3] = dis_4

        # 5. y position of bird

        y_pos = self.y
        y_pos /= self.game.height
        self.inputs[4] = y_pos

        # 6. y velocity of bird

        y_vel = self.y_vel
        y_vel /= self.game.height
        self.inputs[5] = y_vel

        # 7. vertical distance from upper wall

        ver_dis_1 = (self.y - self.radius)
        ver_dis_1 /= self.game.height
        self.inputs[6] = ver_dis_1

        # 8. vertical distance from ground

        ver_dis_2 = (self.y + self.radius) - self.game.height
        ver_dis_2 /= self.game.height
        self.inputs[7] = ver_dis_2

    def predict(self):
        self.inputs = np.reshape(self.inputs, (8, 1))
        output = self.brain.feedforward(self.inputs)
        output = np.argmax(output)

        if output == 0:
            self.moveUp()
        elif output == 1:
            pass
