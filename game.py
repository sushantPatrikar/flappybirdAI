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
        ''' Main game loop. Iterates until the game ends
        Updates the window continuously and adds birds at the
        start of each iteration'''
        gameExit = False

        # Game loop which runs the game by setting up the window and performing
        # actions on the birds
        while not gameExit:         
            gameExit = eventsListen()
            updateWindow()

            for bird in self.birds:
                birdAdd(bird)
                birdCheckCollision(bird)
            
            self.counter += 1
            pygame.display.update()
            self.clock.tick(30)

        pygame.quit()
        quit()

    def showBestBird(self):
        ''' Shows the path of the current best/smartest brain. "Restarts"
        the game and changes score message to display the best birds score '''
        self.pipes = []
        bestCounter = 0
        bird = Bird(self)
        bird.brain = pickle.loads(self.bestBird)
        gameExit = False


        while not gameExit:
            gameExit = eventsListen()
            addPipes()
            birdAdd(bird)
            bestBirdCollision(bird)

        bestBirdMessages()
        pygame.quit()
        quit()

    def addPipes():
        ''' Appends new pipes to list and displays them '''
        if self.counter % 50 == 0:
            from pipe import Pipe
            self.pipes.append(Pipe())
        for pipe in self.pipes:
            pipe.showPipe()
            pipe.x -= 10
            if pipe.x <= -75:
                self.pipes = self.pipes[1:]

    def birdAdd(bird):
        ''' Adds a bird model and sets up its brain '''
        bird.showBird()
        bird.think()
        bird.predict()
        bird.distance += 1
        bird.y += bird.y_vel
        bird.y_vel += bird.gravity

    def bestBirdMessages():
        ''' Changes the game messages to show the score for the best bird '''
        msg2 = self.font.render('Score: ' + str(bird.score), True, (0, 0, 0))
        self.gameDisplay.blit(msg2, [1050, 10])
        bestCounter += 1
        pygame.display.update()
        self.clock.tick(30)

    def birdCheckCollision(bird):
        ''' Handles collision for the birds and updates game messages '''
        if (bird.x + bird.radius) > (self.pipes[0].x + 75) and self.pipes[0].z == 0:
            bird.score += 1

            # Handles the case in which a new high score is set
            if bird.score > self.highscore:
                self.bestBirdBrain = bird.brain
                self.foundBestBird = True
                self.highscore = bird.score
                self.pipes[0].z = 1
            
            # Handles wall or pipe collision by adding and removing birds from the lists
            if bird.collidingWall() or bird.collidingPipe():
                self.savedBirds.append(bird)
                self.birds.remove(bird)

                # Handles the death of the last bird
                if len(self.birds) == 0:
                    self.gameDisplay.blit(self.image, [0, 0])
                    self.pipes = []
                    self.counter = 0
                    ga = GA(self)
                    ga.nextGeneration()
                    self.generation += 1
                    self.gameLoop()

    def bestBirdCollision(bird):
        ''' Handles collision for the best bird and updates score '''
        if (bird.x + bird.radius) > (self.pipes[0].x + 75) and self.pipes[0].z == 0:
            bird.score += 1
            self.pipes[0].z = 1
        if bird.collidingWall() or bird.collidingPipe():
            return

    def eventsListen():
        ''' Sets up pygame events to listen to game exit and the key S to show the best bird'''
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                gameExit = True
            if event.type == pygame.KEYDOWN and event.key == pygame.K_s:
                self.bestBird = pickle.dumps(self.bestBirdBrain)
                self.showBestBird()
        return False

    def updateWindow():
        ''' Sets up important visual game assets (pipe, text messages) and key events'''
        self.gameDisplay.blit(self.image, [0, 0])
        addPipes()
        birdMessages()

    def birdMessages()
        ''' Updates game messages regarding generation and score during normal bird run'''
        msg = f'Gen : {str(self.generation)}'
        screen_text = self.font.render(msg, True, (0, 0, 0))
        self.gameDisplay.blit(screen_text, [10, 10])
        msg2 = self.font.render(f'Best Score: {str(self.highscore)}', True, (0, 0, 0))
        self.gameDisplay.blit(msg2, [1050, 10])

if __name__ == '__main__':
    game = Game()