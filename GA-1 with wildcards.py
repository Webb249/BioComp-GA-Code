from random import randrange, random
import csv

POPULATION_SIZE = 10
DATA_TWO_POPULATION_SIZE = 32
DATA_TWO_CLASS_LOCATION = 6
DATA_TWO_GENE_SIZE = 5
RULE_LENGTH = 10
GENE_SIZE = 60


# Store rules and data from dataset
class DataClass:
    def __init__(self, gene, class_number):
        self.gene = gene
        self.class_number = class_number

# Store rules and corresponding fitness
class DataClassSet:
    def __init__(self, data_class, fitness):
        self.data_class = data_class
        self.fitness = fitness

# Store best, worst and average fitness to be stored in a file at exit
class Average:
    def __init__(self, best, worst, average):
        self.best = best
        self.worst = worst
        self.average = average


# Read each line in the file
def get_list_of_file_lines(file_name):
    file = open(file_name, 'r')
    line_list = []
    first_line = True

    for line in file:
        if first_line is True:
            first_line = False
        else:
            line_list.append(line)

    return line_list


# Calculate fitness of the solution given
def fitness_function(solution, data_set):
    fitness = 0

    for data in data_set:
        for i in range(10):
            if matcher(solution[i].gene, [int(numeric_string) for numeric_string in data.gene]):
                if int(data.class_number) == solution[i].class_number:
                    fitness += 1
                break



    return fitness

# Test if arrays match
def matcher(l1, l2):
    for i in range(5):
        if l1[i] != l2[i] and l1[i] != 2:
            return False

    return True


# Get data from the dataset file
def create_rules(pop_size, class_location, gene_size):
    data_lines = get_list_of_file_lines('data1.txt')
    population_list = [DataClass(None, None) for _ in range(pop_size)]
    j = 0
    for i in data_lines[:]:
        gene = list(i)
        population_list[j].class_number = gene[class_location]
        population_list[j].gene = gene[:gene_size]
        j = j + 1

    return population_list


# Generate population
def produce_population():
    population_list = [DataClassSet(None, 0) for _ in range(POPULATION_SIZE)]

    for i in range(POPULATION_SIZE):
        for j in range(RULE_LENGTH):
            population_list[i].data_class = create_individual()

    return population_list


# Create individual for generating population
def create_individual():
    population_list = [DataClass(None, None) for _ in range(RULE_LENGTH)]

    for i in range(RULE_LENGTH):
        gene = [None] * DATA_TWO_GENE_SIZE
        for j in range(DATA_TWO_GENE_SIZE):
            gene[j] = randrange(3)
        population_list[i].gene = gene
        population_list[i].class_number = randrange(2)

    return population_list


# Convert solution to a long array
def convert_solution_single_array(population_list):
    temp_population = [None] * GENE_SIZE
    x = 0

    for i in range(RULE_LENGTH):
        for j in range(DATA_TWO_GENE_SIZE):
            temp_population[x] = population_list[i].gene[j]
            x += 1
        temp_population[x] = population_list[i].class_number
        x += 1

    return temp_population


# Convert long array back to objects
def convert_single_array_solution(individual):
    population_list = [DataClass(None, None) for _ in range(POPULATION_SIZE)]
    j = 1

    for i in range(RULE_LENGTH):
        temp_gene = individual[i * 6:j * 6]
        population_list[i].gene = temp_gene[:5]
        population_list[i].class_number = temp_gene[5]
        j += 1

    return population_list


# Select best fitness out of randomly selected parents
def selection(population_list):
    offspring = [DataClassSet(None, None) for _ in range(RULE_LENGTH)]

    for i in range(RULE_LENGTH):
        parent1 = randrange(RULE_LENGTH)
        parent2 = randrange(RULE_LENGTH)

        if population_list[parent1].fitness >= population_list[parent2].fitness:
            offspring[i] = population_list[parent1]
        else:
            offspring[i] = population_list[parent2]

    return offspring


# Bit wise muation to randomly change a gene
def bit_wise_mutation(population_list):
    population_list_array = [None] * RULE_LENGTH
    offspring_sets = [DataClassSet(None, 0) for _ in range(RULE_LENGTH)]

    for i in range(RULE_LENGTH):
        population_list_array[i] = convert_solution_single_array(population_list[i].data_class)

    for i in range(RULE_LENGTH):
        for j in range(GENE_SIZE):
            if 0.1 < random() < 0.103:
                if (j + 1) % 6 == 0:
                    if population_list_array[i][j] == 0:
                        population_list_array[i][j] = 1
                    else:
                        population_list_array[i][j] = 0
                else:
                    if population_list_array[i][j] == 0:
                        population_list_array[i][j] = randrange(1, 3)
                    elif population_list_array[i][j] == 1:
                        population_list_array[i][j] = randrange(3)
                        while population_list_array[i][j] == 1:
                            population_list_array[i][j] = randrange(3)
                    else:
                        population_list_array[i][j] = randrange(2)

    for i in range(RULE_LENGTH):
        offspring_sets[i].data_class = convert_single_array_solution(population_list_array[i])

    return offspring_sets


def single_point_crossover(population_list):
    population_list_array = [None] * RULE_LENGTH
    offspring_sets = [DataClassSet(None, 0) for _ in range(POPULATION_SIZE)]

    for i in range(RULE_LENGTH):
        population_list_array[i] = convert_solution_single_array(population_list[i].data_class)

    for i in range(RULE_LENGTH):
        parent1 = randrange(RULE_LENGTH)
        parent2 = randrange(RULE_LENGTH)
        cross_over_point = randrange(GENE_SIZE)

        for j in range(GENE_SIZE):
            if j > cross_over_point:
                population_list_array[parent1][j] = population_list_array[parent2][j]
                population_list_array[parent2][j] = population_list_array[parent1][j]
            else:
                population_list_array[parent2][j] = population_list_array[parent1][j]
                population_list_array[parent1][j] = population_list_array[parent2][j]

        for x in range(RULE_LENGTH):
            offspring_sets[i].data_class = convert_single_array_solution(population_list_array[i])

    return offspring_sets


def send_to_file(all):
    path = 'C:/Users/HP USER/Worksheet1.txt'
    with open(path,'w') as csvfile:
        fieldnames = ['Best', 'Worst', 'Average']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

        writer.writeheader()
        for i in range(len(all.best)):
            writer.writerow({'Best': all.best[i], 'Worst': all.worst[i], 'Average': all.average[i]})


def calculate_best_worst_and_average(population_list, all):
    highest = population_list[0].fitness
    lowest = population_list[0].fitness
    all_fitness = 0

    for i in range(len(population_list)):
        if population_list[i].fitness > highest:
            highest = population_list[i].fitness

        if population_list[i].fitness < lowest:
            lowest = population_list[i].fitness

        all_fitness += population_list[i].fitness

    all.best.append(highest)
    all.worst.append(lowest)
    all.average.append(all_fitness / len(population_list))

    return all


def send_to_file(all):
    path = 'C:/Users/HP USER/Worksheet1.txt'
    with open(path,'w') as csvfile:
        fieldnames = ['Best', 'Worst', 'Average']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

        writer.writeheader()
        for i in range(len(all.best)):
            writer.writerow({'Best': all.best[i], 'Worst': all.worst[i], 'Average': all.average[i]})


def calculate_best_worst_and_average(population_list, all):
    highest = population_list[0].fitness
    lowest = population_list[0].fitness
    all_fitness = 0

    for i in range(len(population_list)):
        if population_list[i].fitness > highest:
            highest = population_list[i].fitness

        if population_list[i].fitness < lowest:
            lowest = population_list[i].fitness

        all_fitness += population_list[i].fitness

    all.best.append(highest)
    all.worst.append(lowest)
    all.average.append(all_fitness / len(population_list))

    return all


def main():
    generation_count = 0
    max_fitness_found = True
    all = Average([0.0], [0.0], [0.0])


    data_set = create_rules(DATA_TWO_POPULATION_SIZE, DATA_TWO_CLASS_LOCATION, DATA_TWO_GENE_SIZE)
    population_list = produce_population()
    for i in range(RULE_LENGTH):
        population_list[i].fitness = fitness_function(population_list[i].data_class, data_set)

    for _ in range(3000):
        all = calculate_best_worst_and_average(population_list, all)

        #for a in range(10):
        #    for b in range(10):
        #        print("{0}[{1}]  {2}".format(population_list[a].data_class[b].gene, population_list[a].data_class[b].class_number, population_list[a].fitness))

        generation_count += 1
        population_list = selection(population_list)
        #population_list = roulette_selection(population_list)
        population_list = single_point_crossover(population_list)
        population_list = bit_wise_mutation(population_list)
        for i in range(RULE_LENGTH):
            population_list[i].fitness = fitness_function(population_list[i].data_class, data_set)
            #if population_list[i].fitness == DATA_TWO_POPULATION_SIZE:
            #    max_fitness_found = False
            #    print("Generation: {}".format(generation_count))
            #    print("Fitness: {}".format(population_list[i].fitness))
            #    for a in range(10):
            #        print("Final gene: {}{}".format(population_list[i].data_class[a].gene, population_list[i].data_class[a].class_number))

    send_to_file(all)

if __name__ == '__main__':
    main()
