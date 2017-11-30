from random import random, choice, uniform, randrange
from operator import add, sub
from copy import deepcopy
import csv

POPULATION_SIZE = 100
RULES = 10
MUTATION_RATE = 0.150

# Store the value of best, worst and average fitness to be stored in a file after completion
class Average:
    def __init__(self, best, worst, average):
        self.best = best
        self.worst = worst
        self.average = average

# Store the data conditions
class DataSet(object):
    def __init__(self):
        self.condition = [0.0, 0.0, 0.0, 0.0, 0.0, 0.0]
        self.out = None

# Store an individual gene
class IndividualGene(object):
    def __init__(self):
        self.ruleSet = [RuleSet() for _ in range(10)]
        self.fitness = 0

    def send_to_array(self):
        return_array = []
        for rule_set in self.ruleSet[:]:
            for rule in rule_set.rules[:]:
                return_array.append(rule.lower)
                return_array.append(rule.higher)
            return_array.append(rule_set.out)
        return return_array

    def get_from_array(self, array):
        count = 0
        for ruleset in self.ruleSet[:]:
            for rule in ruleset.rules[:]:
                rule.lower = array[count]
                count += 1
                rule.higher = array[count]
                count += 1
            ruleset.out = array[count]
            count += 1


# Store the rules
class RuleSet(object):
    def __init__(self):
        self.rules = [Rules() for _ in range(6)]
        self.out = None


# store the higher and lower of each gene
class Rules(object):
    def __init__(self):
        self.lower = 0.0
        self.higher = 0.0

    def generate_number(self):
        self.lower = generate_random_number()
        self.higher = generate_random_number()

    def low(self):
        return float(self.lower) if float(self.lower) < float(self.higher) else float(self.higher)

    def high(self):
        return float(self.lower) if float(self.lower) > float(self.higher) else float(self.higher)


RULESET = [IndividualGene() for _ in range(POPULATION_SIZE)]
TRAINING_DATA = [DataSet() for _ in range(1000)]
TEST_DATA = [DataSet() for _ in range(1000)]
BESTINDIVIDUAL = IndividualGene()


# Random starting number for the genes
def generate_random_number():
    return "%.6f" % uniform(0, 1)

# Set amount the gene could change by
def random_mutation_amount():
    return "%.6f" % uniform(0, 0.1)

# Get the dataset from the file
def read_file():
    lines = []
    file_open = open("./data3.txt", "r").read().splitlines()
    for line in file_open:
        lines.append(line)
    lines.pop(0)

    return lines

# Generate the population of rules
def generate_population():
    for rule_object in RULESET[:]:
        for ruleset in rule_object.ruleSet[:]:
            for rule in ruleset.rules[:]:
                rule.generate_number()
            ruleset.out = randrange(2)
        fitness_function(rule_object, TRAINING_DATA)


# Roulette selection better for dataset 3
def roulette_selection():
    return_offspring = [None, None]
    max_value = 0

    for rule in RULESET[:]:
        max_value += int(rule.fitness)

    for children in range(len(return_offspring)):
        pick = randrange(0, max_value)
        current = 0
        for individual in RULESET[:]:
            current += int(individual.fitness)
            if current > pick:
                return_offspring[children] = deepcopy(individual)
                break

    return return_offspring


# Single point crossover
def crossover(parents):
    parent1 = parents[0].send_to_array()
    parent2 = parents[1].send_to_array()

    ran_num = randrange(1, len(parent1) - 1)

    parents[0].get_from_array((parent1[:ran_num] + parent2[ran_num:]))
    parents[1].get_from_array((parent2[:ran_num] + parent1[ran_num:]))

    return parents


# Mutate gene randomly by random amount
def mutate(parents):
    ops = [add, sub]

    for number, parent in enumerate(parents[:]):
        parent1 = parent.send_to_array()
        for c, i in enumerate(parent1[:]):
            if isinstance(i, int):
                if random() < MUTATION_RATE:
                    parent1[c] = 1 - int(i)
            else:
                if random() < MUTATION_RATE:
                    done1 = True
                    while done1:
                        operation = choice(ops)
                        new_number = operation(float(i), float(random_mutation_amount()))
                        if 0.0 < new_number < 1.0:
                            parent1[c] = str(new_number)
                            done1 = False

        parents[number].get_from_array(parent1)

    return parents


# Calcualte fitness of the individual solution
def fitness_function(individual_solution, data):
    global BESTINDIVIDUAL, TRAINING_DATA

    fitness = 0

    for td in data[:]:
        for i in individual_solution.ruleSet[:]:
            correct = 0
            for condition_count, c in enumerate(td.condition[:]):
                if float(c) >= i.rules[condition_count].low() and float(c) <= i.rules[condition_count].high():
                    correct += 1
                    continue

            if correct == 6:
                if str(td.out) == str(i.out):
                    fitness += 1
                break

    individual_solution.fitness = int(fitness)

    if individual_solution.fitness > BESTINDIVIDUAL.fitness:
        BESTINDIVIDUAL = deepcopy(individual_solution)


# After max fitness found store results in file
def send_to_file(all, path):
    with open(path,'w') as csvfile:
        fieldnames = ['Best', 'Worst', 'Average']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

        writer.writeheader()
        for i in range(len(all.best)):
            writer.writerow({'Best': all.best[i], 'Worst': all.worst[i], 'Average': all.average[i]})


# Calculate results to be stored in file when finished
def calculate_best_worst_and_average(rule_set, all):
    highest = rule_set[0].fitness
    lowest = rule_set[0].fitness
    all_fitness = 0

    for i in rule_set[:]:
        if i.fitness > highest:
            highest = i.fitness

        if i.fitness < lowest:
            lowest = i.fitness

        all_fitness += i.fitness

    all.best.append(highest)
    all.worst.append(lowest)
    all.average.append(all_fitness / len(rule_set))

    return all


def main():
    global RULESET
    all = Average([0.0], [0.0], [0.0])
    test_all = Average([0.0], [0.0], [0.0])


    load_dataset = read_file()
    pointer = 0

    # get training data
    for i in TRAINING_DATA[:]:
        split = load_dataset[pointer].split(" ")
        i.condition[0] = split[0]
        i.condition[1] = split[1]
        i.condition[2] = split[2]
        i.condition[3] = split[3]
        i.condition[4] = split[4]
        i.condition[5] = split[5]
        i.out = split[6]
        pointer += 1

    # get testing data
    for i in TEST_DATA[:]:
        split = load_dataset[pointer].split(" ")
        i.condition[0] = split[0]
        i.condition[1] = split[1]
        i.condition[2] = split[2]
        i.condition[3] = split[3]
        i.condition[4] = split[4]
        i.condition[5] = split[5]
        i.out = split[6]
        pointer += 1

    generate_population()

    generations = 1
    while generations < 800:
        if generations % 10 == 0:
            print("Test Data: {}".format(BESTINDIVIDUAL.fitness))
            test_all = calculate_best_worst_and_average(RULESET, test_all)
        else:
            all = calculate_best_worst_and_average(RULESET, all)

        child_population = []

        while len(child_population) < POPULATION_SIZE:
            parent = roulette_selection()
            children = crossover(parent)
            children = mutate(children)

            if generations % 10 == 0:
                fitness_function(children[0], TEST_DATA)
                fitness_function(children[1], TEST_DATA)
            else:
                fitness_function(children[0], TRAINING_DATA)
                fitness_function(children[1], TRAINING_DATA)

            child_population.append(children[0])
            child_population.append(children[1])

        RULESET += child_population
        RULESET.sort(key=lambda x: x.fitness, reverse=True)

        for i in range(POPULATION_SIZE):
            RULESET.pop()

        print("Best Fitness: {}  Generation: {}".format(BESTINDIVIDUAL.fitness, generations))
        generations += 1

    send_to_file(all, 'C:/Users/HP USER/Worksheet1.txt')
    send_to_file(test_all, 'C:/Users/HP USER/Worksheet1_test_data.txt')


if __name__ == '__main__':
    main()
