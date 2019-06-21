import pygame
import pickle

from ga import GA
from bird import Bird

class Game:
    # Module and clock initialisation
    pygame.init()
    clock = pygame.time.Clock()
    
    # Setting up the pipe and bird colors respectively 
    pipeColour = (0, 200, 0)
    birdColour = (255, 200, 50) # Birds are yellow

    # Setting up the game window dimensions
    width = 1200
    height = 600
    gameDisplay = pygame.display.set_mode((width, height))
    pygame.display.set_caption('Flappy Bird AI')
    font = pygame.font.SysFont(None, 25)
    image = pygame.image.load('background.png').convert_alpha()

    # Lists containing the respective pipe, and bird objects
    pipes = []
    birds = []

    # TODO: figure out what this list is for
    savedBirds = []

    # Bird population
    population = 300

    # Game information/control variables
    counter = 0
    generation = 1
    highscore = 0
    bestBirdBrain = None
    foundBestBird = False
    bestBird = None

    def __init__(self):
        ''' Appends the population of birds to the array self.birds, 
        then initialises the game by calling self.gameLoop()'''
        for _ in range(self.population):
            self.birds.append(Bird(self))
        self.gameLoop()

    def gameLoop(self):
        ''' Main game loop. Iterates until the game ends and executes operations on each bird '''
        gameExit = False

        while not gameExit:
            self.updateWindow()
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
                        self.gameDisplay.blit(self.image, [0, 0])
                        self.pipes = []
                        self.counter = 0
                        ga = GA(self)
                        ga.nextGeneration()
                        self.generation += 1
                        self.gameLoop()
            self.counter += 1
            pygame.display.update()
            self.clock.tick(30)
        pygame.quit()
        quit()

    def updateWindow(self):
        ''' Sets up important visual game assets (pipe, text messages) and key events'''
        self.gameDisplay.blit(self.image, [0, 0])
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                gameExit = True
            if event.type == pygame.KEYDOWN and event.key == pygame.K_s:
                    self.bestBird = pickle.dumps(self.bestBirdBrain)
                    self.showBestBird()

        # Appends new pipes to list and displays them
        if self.counter % 50 == 0:
            from pipe import Pipe
            self.pipes.append(Pipe())
        for pipe in self.pipes:
            pipe.showPipe()
            pipe.x -= 10
            if pipe.x <= -75:
                self.pipes = self.pipes[1:]

        # Updates game messages
        msg = f'Gen : {str(self.generation)}'
        screen_text = self.font.render(msg, True, (0, 0, 0))
        self.gameDisplay.blit(screen_text, [10, 10])
        msg2 = self.font.render(f'Best Score: {str(self.highscore)}', True, (0, 0, 0))
        self.gameDisplay.blit(msg2, [1050, 10])

    def showBestBird(self):
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
