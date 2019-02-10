"""
Genetic Algorithmn Implementation
    see: http://www.obitko.com/tutorials/genetic-algorithms/ga-basic-description.php
         https://gist.github.com/bellbind/741853
"""

import random


class GeneticAlgorithm():
    def __init__(self, genetics):
        self.genetics = genetics

    def run(self):
        population = self.genetics.initial()
        while True:
            fits_pops = [(self.genetics.fitness(ch),  ch) for ch in population]
            self.genetics.generation += 1
            self.genetics.generation_info(fits_pops, 5)
            if self.genetics.check_stop():
                break
            population = self.next(fits_pops)
        return population

    def next(self, fits):
        parents_generator = self.genetics.parents(fits)
        size = len(fits)
        # print size
        nexts = []
        while len(nexts) < size:
            parents = next(parents_generator)  # ? father, mother
            # print parents
            # ? perform genetic operation to create new generation
            cross = random.random() < self.genetics.probability_crossover()
            children = self.genetics.crossover(parents) if cross else parents
            for ch in children:
                mutate = random.random() < self.genetics.probability_mutation()
                nexts.append(self.genetics.mutation(ch) if mutate else ch)
        return nexts[0:size]


class GeneticFunctions():
    def probability_crossover(self):
        """returns rate of occur crossover(0.0-1.0)"""
        return 1.0

    def probability_mutation(self):
        """returns rate of occur mutation(0.0-1.0)"""
        return 0.0

    def initial(self):
        """returns list of initial population"""
        return []

    def fitness(self, chromosome):
        """returns domain fitness value of chromosome"""
        return len(chromosome)

    def check_stop(self):
        """stop run if generation reach limit returns True"""
        return False

    def generation_info(self, fits_populations):
        """print info of current generation - fits_populations: list of (fitness_value, chromosome)"""
        return

    def parents(self, fits_populations):
        """generator of selected parents"""
        gen = iter(sorted(fits_populations))
        while True:
            f1, ch1 = next(gen)
            f2, ch2 = next(gen)
            yield (ch1, ch2)
            pass
        return

    def crossover(self, parents):
        """breed children"""
        return parents

    def mutation(self, chromosome):
        """mutate chromosome"""
        return chromosome


class CrackDigits():
    def __init__(self, targetDigits, maxGeneration=100, popSize=500, probXover=0.9, probMutation=0.2):
        self.target = self.number2digits(targetDigits)
        self.generation = 0

        self.maxGeneration = maxGeneration
        self.popSize = popSize
        self.probXover = probXover
        self.probMutation = probMutation
        pass

    #! overwrite genetic functions to our digits crack
    def probability_crossover(self):
        return self.probXover

    def probability_mutation(self):
        return self.probMutation

    def initial(self):
        # for i in range(self.popSize):
        #     print self.random_digits()
        return [self.random_digits() for i in range(self.popSize)]

    def fitness(self, chromosome):
        # ? find delta between each chromosome digit compare to target digit
        # result = 0
        # print zip(chromosome, self.target)
        # for c, t in zip(chromosome, self.target):
        #     result += abs(c - t)
        # print -result
        return -sum(abs(c - t) for c, t in zip(chromosome, self.target))

    def check_stop(self):
        return self.generation >= self.maxGeneration

    def generation_info(self, fits_populations, show_iter=10):
        if self.generation % show_iter == 0:
            best_match = list(sorted(fits_populations))[-1][1]
            fits = [f for f, ch in fits_populations]
            best = max(fits)
            worst = min(fits)
            ave = sum(fits) / len(fits)
            print(
                "[Gen %3d] fitness=(%4d, %4d, %4d): %r" %
                (self.generation, best, ave, worst,
                 self.digits2number(best_match)))
            pass

    def parents(self, fits_populations):
        while True:
            father = self.tournament(fits_populations)
            mother = self.tournament(fits_populations)
            yield (father, mother)
            pass
        pass

    def crossover(self, parents): #? cross value by swap index
        father, mother = parents
        index1 = random.randint(1, len(self.target) - 2)
        index2 = random.randint(1, len(self.target) - 2)
        if index1 > index2:
            index1, index2 = index2, index1
        child1 = father[:index1] + mother[index1:index2] + father[index2:]
        child2 = mother[:index1] + father[index1:index2] + mother[index2:]
        return (child1, child2)

    def mutation(self, chromosome):
        index = random.randint(0, len(self.target) - 1)
        # ? result can be the same value before mutated ??
        vary = random.randint(-5, 5)
        mutated = list(chromosome)
        mutated[index] += vary
        # ? eliminate out of range values
        mutated[index] = abs(mutated[index])
        if mutated[index] > 9:
            mutated[index] -= 9
        return mutated

    #! internal functions
    def tournament(self, fits_populations): #? random compare
        alicef, alice = self.select_random(fits_populations)
        bobf, bob = self.select_random(fits_populations)
        return alice if alicef > bobf else bob

    def select_random(self, fits_populations):
        return fits_populations[random.randint(0, len(fits_populations)-1)]

    def number2digits(self, number):
        return [int(d) for d in str(number)]

    def digits2number(self, digits):
        return "".join(str(digit) for digit in digits)

    def random_digits(self):
        return [random.randint(0, 9) for i in range(len(self.target))]


if __name__ == '__main__':
    # fits_pops = []

    # crack_function = CrackDigits(11223344556677889900)
    # pop = crack_function.initial()

    # for ch in pop:
    #     fits_pops.append((crack_function.fitness(ch), ch))
    # # fits_pops = [(crack_function.fitness(ch),  ch) for ch in pop]
    # print sorted(fits_pops)[-1][1]

    # print list(sorted(fits_pops))[-1][1]
    GeneticAlgorithm(CrackDigits('0813873280')).run()
