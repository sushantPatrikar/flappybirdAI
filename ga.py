import random

from bird import Bird

class GA:
    def __init__(self, game):
        self.game = game

    def nextGeneration(self):
        self.calculateFitness()
        if (self.game.foundBestBird):
            child = Bird(self.game)
            child.brain = self.game.bestBirdBrain
            self.game.birds.append(child)
        else:
            self.game.birds.append(self.game.savedBirds[random.randrange(self.game.population)])
        for i in range(self.game.population - 1):
            self.game.birds.append(self.pickOne())
        self.game.savedBirds = []

    def calculateFitness(self):
        summ = 0
        for bird in self.game.savedBirds:
            bird.calculateFitness()
            summ += bird.fitness
        for bird in self.game.savedBirds:
            bird.fitness /= summ

    def pickOne(self):
        r1 = random.uniform(0, 1)
        index = 0
        while r1 > 0:
            r1 -= self.game.savedBirds[index].fitness
            index += 1
        index -= 1

        bird1 = self.game.savedBirds[index]

        r2 = random.uniform(0, 1)
        index_2 = 0

        while r2 > 0:
            r2 -= self.game.savedBirds[index_2].fitness
            index_2 += 1
        index_2 -= 1

        bird2 = self.game.savedBirds[index_2]

        child = Bird(self.game)

        child.brain.in_hidden1_weights = bird1.brain.crossover(bird1.brain.in_hidden1_weights,
                                                               bird2.brain.in_hidden1_weights)
        child.brain.in_hidden1_biases = bird1.brain.crossover(bird1.brain.in_hidden1_biases,
                                                              bird2.brain.in_hidden1_biases)
        child.brain.hidden1_output_weights = bird1.brain.crossover(bird1.brain.hidden1_output_weights,
                                                                   bird2.brain.hidden1_output_weights)
        child.brain.hidden1_output_biases = bird1.brain.crossover(bird1.brain.hidden1_output_biases,
                                                                  bird2.brain.hidden1_output_biases)

        child.brain.mutate(child.brain.in_hidden1_weights, 0.3)
        child.brain.mutate(child.brain.in_hidden1_biases, 0.3)
        child.brain.mutate(child.brain.hidden1_output_weights, 0.3)
        child.brain.mutate(child.brain.hidden1_output_biases, 0.3)
        return child
