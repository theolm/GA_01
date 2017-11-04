"""
Copyright (c) 2017 Theodoro L. Mota
"""

from random import randint, random, shuffle
from operator import add
from functools import reduce

#
# Global variables

INDIVIDUAL_LENGHT = 16 #number of bites to represent the individual.
POP_SIZE = 5000 #number of individuals in the pop.
SELECTED = 0.2 #percentage of selected individuals.
RANDOM_IND = 0.05 #percentage of random individuals to include as parent. may have shit fitness.
MUTATE = 0.01 #percentage of individuals to mutate.

BEST_X = 0
BEST_FITNESS = 0



#
# Helper functions

def individual():
    'Create a member of the population.'

    temp = ''

    for x in xrange(INDIVIDUAL_LENGHT):
    	temp += str(randint(0,1))

    return temp

def mutate_individual(individual):
	l = list(individual)
	shuffle(l)

	return ''.join(l)


#
# GA functions

def generate_population(population_size):
    return [ individual() for x in xrange(population_size) ]

def calculate_fitness(individual):
	return int(individual, 2) ** 2 # x^2 -> here goes the function to optimize 

def calculate_average_fitness(population):
	fitness_sum =  reduce(add, (calculate_fitness(x) for x in population), 0)
	return fitness_sum / (len(population) * 1.0)

def evolve(population):
	global BEST_FITNESS 
	global BEST_X

	graded = [ (calculate_fitness(x), x) for x in population]

	sorted_graded = sorted(graded)

	#always keeps traks of the best result to the fitness function.
	pop_leader = sorted_graded[-1]

	if pop_leader[0] > BEST_FITNESS:
		BEST_FITNESS = pop_leader[0]
		BEST_X = int(pop_leader[1], 2)



	graded = [ x[1] for x in sorted_graded]


	retain_length = int(len(graded)*SELECTED)
	parents = graded[-retain_length:] #pick X% of the best in the population

	#add shity individuals to escape max locals.
	for individual in graded[:-retain_length]:
		if RANDOM_IND > random():
			parents.append(individual)

	#mutate some the shit out of the parents
	for individual in xrange(len(parents)):
		if MUTATE > random():
			parents[individual] = mutate_individual(parents[individual])


	parents_length = len(parents)
	offspring_lenght = len(population) - parents_length
	offspings = []

	while len(offspings) < offspring_lenght:
		male = randint(0, parents_length-1)
		female = randint(0, parents_length-1)
		if male != female:
			male = parents[male]
			female = parents[female]
			child = male[:INDIVIDUAL_LENGHT] + female[INDIVIDUAL_LENGHT:]
			offspings.append(child)

	parents.extend(offspings)
	return parents

# functions to implement:
# average_fitness - determine the average fitness of the pop.


if __name__ == "__main__":
	p = generate_population(POP_SIZE)
	p = evolve(p)

	print BEST_X
	print BEST_FITNESS



	

