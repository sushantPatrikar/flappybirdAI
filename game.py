import pygame
import pickle
from GA import GA
from bird import Bird


class Game:
    pygame.init()
    clock = pygame.time.Clock()
    green = (0, 200, 0)
    black = (0, 0, 0)
    width = 1200
    height = 600
    gameDisplay = pygame.display.set_mode((width, height))
    pygame.display.set_caption('flappybirdAI')
    pipes = []
    birds = []
    savedBirds = []
    population = 300
    counter = 0
    generation = 1
    highscore = 0
    bestBirdBrain = None
    foundBestBird = False
    bestBird = None

    def __init__(self):

        for _ in range(self.population):
            self.birds.append(Bird(self))
        self.gameLoop()

    def gameLoop(self):
        gameExit = False
        font = pygame.font.SysFont(None, 25)
        image = pygame.image.load('background.png').convert_alpha()
        while not gameExit:
            self.gameDisplay.blit(image, [0, 0])
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    gameExit = True
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_s:
                        self.bestBird = pickle.dumps(self.bestBirdBrain)
                        self.showBest()

            if self.counter % 50 == 0:
                from pipe import Pipe
                self.pipes.append(Pipe())

            for pipe in self.pipes:
                pipe.showPipe()
                pipe.x -= 10
                if pipe.x <= -75:
                    self.pipes = self.pipes[1:]
            msg = 'Gen : ' + str(self.generation)
            screen_text = font.render(msg, True, (0, 0, 0))
            self.gameDisplay.blit(screen_text, [10, 10])
            msg2 = font.render('Best Score: ' + str(self.highscore), True, (0, 0, 0))
            self.gameDisplay.blit(msg2, [1050, 10])
            for bird in self.birds:
                bird.showBird()
                bird.think()
                bird.predict()
                bird.distance += 1
                bird.y += bird.y_vel
                bird.y_vel += bird.gravity
                if (bird.x + bird.radius) > (self.pipes[0].x + 75) and self.pipes[0].z == 0:
                    bird.score += 1
                    if bird.score > self.highscore:
                        self.bestBirdBrain = bird.brain
                        self.foundBestBird = True
                        self.highscore = bird.score
                    self.pipes[0].z = 1
                if bird.collidingWall() or bird.collidingPipe():
                    self.savedBirds.append(bird)
                    self.birds.remove(bird)
                    if len(self.birds) == 0:
                        self.gameDisplay.blit(image, [0, 0])
                        self.pipes = []
                        self.counter = 0
                        ga = GA(self)
                        ga.nextGenration()
                        self.generation += 1
                        self.gameLoop()
            self.counter += 1
            pygame.display.update()
            self.clock.tick(30)
        pygame.quit()
        quit()

    def showBest(self):
        self.pipes = []
        bestCounter = 0
        bird = Bird(self)
        bird.brain = pickle.loads(self.bestBird)
        gameExit = False
        font = pygame.font.SysFont(None, 25)
        image = pygame.image.load('background.png').convert_alpha()
        while not gameExit:
            self.gameDisplay.blit(image, [0, 0])
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    gameExit = True

            if bestCounter % 50 == 0:
                from pipe import Pipe
                self.pipes.append(Pipe())

            for pipe in self.pipes:
                pipe.showPipe()
                pipe.x -= 10
                if pipe.x <= -75:
                    self.pipes = self.pipes[1:]
            msg2 = font.render('Score: ' + str(bird.score), True, (0, 0, 0))
            self.gameDisplay.blit(msg2, [1050, 10])
            bird.showBird()
            bird.think()
            bird.predict()
            bird.distance += 1
            bird.y += bird.y_vel
            bird.y_vel += bird.gravity
            if (bird.x + bird.radius) > (self.pipes[0].x + 75) and self.pipes[0].z == 0:
                bird.score += 1
                self.pipes[0].z = 1
            if bird.collidingWall() or bird.collidingPipe():
                return
            bestCounter += 1
            pygame.display.update()
            self.clock.tick(30)
        pygame.quit()
        quit()



if __name__ == '__main__':
    game = Game()
