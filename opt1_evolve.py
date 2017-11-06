"""
Copyright (c) 2017 Theodoro L. Mota
"""

from random import randint, random, shuffle
from operator import add
from functools import reduce
import struct

#
# Global variables

INDIVIDUAL_LENGHT = 32 #number of bites to represent the individual.
POP_SIZE = 10000 #number of individuals in the pop.
SELECTED = 0.2 #percentage of selected individuals.
RANDOM_IND = 0.05 #percentage of random individuals to include as parent. may have shit fitness.
MUTATE = 0.01 #percentage of individuals to mutate.

BEST_X = 0
BEST_FITNESS = 0



#
# Helper functions

def individual():
	"Create a individual"
	
	temp = ''
	for x in xrange(INDIVIDUAL_LENGHT):
		temp += str(randint(0,1))
	
	return temp

def mutate_individual(individual):
	l = list(individual)
	shuffle(l)

	return ''.join(l)

#should receive a 32 bit string and returns a float number
def bin_to_float(binary):
	i = int(binary, 2)
	return struct.unpack('f', struct.pack('I', i))[0]

#receive a X bits string and a number indicate the size of the decimal part and return a pair of float (x1, x2) 
def get_x1_and_x2(binary, n_decimal):
	x1 = binary[:(len(binary)/2)]
	x1f = x1[-n_decimal:]
	x1 = x1[:-n_decimal]
	f1 = float(int(x1, 2)) + ((float(int(x1f, 2)))/10)

	x2 = binary[(len(binary)/2):]
	x2f = x2[-n_decimal:]
	x2 = x2[:-n_decimal]
	f2 = float(int(x2, 2)) + ((float(int(x2f, 2)))/10)

	return (f1, f2)


#
# GA functions

def generate_population(population_size):
	return [ individual() for x in xrange(population_size) ]

def calculate_fitness(individual):
	#x = int(individual, 2)
	x = bin_to_float(individual)
	return -(x ** 2) + (8 * x) + 7 # x^2 -> here goes the function to optimize 

#def calculate_average_fitness(population):
#	fitness_sum =  reduce(add, (calculate_fitness(x) for x in population), 0)
#	return (fitness_sum / (len(population) * 1.0))

def evolve(population):
	global BEST_FITNESS 
	global BEST_X

	graded = [ (calculate_fitness(x), x) for x in population]
	sorted_graded = sorted(graded)


	#always keeps traks of the best result to the fitness function.
	pop_leader = sorted_graded[-1]

	if pop_leader[0] > BEST_FITNESS: # change that if necessary
		BEST_FITNESS = pop_leader[0]
		BEST_X = bin_to_float(pop_leader[1])


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
	offsprings = []

	while len(offsprings) < offspring_lenght:
		male = randint(0, parents_length-1)
		female = randint(0, parents_length-1)
		if male != female:
			male = parents[male]
			female = parents[female]
			child = male[:INDIVIDUAL_LENGHT] + female[INDIVIDUAL_LENGHT:]
			offsprings.append(child)

	parents.extend(offsprings)
	return parents

# functions to implement:
# average_fitness - determine the average fitness of the pop.


if __name__ == "__main__":
	
	p = generate_population(POP_SIZE)
	print 'best x:' + str(BEST_X) + ' fitness: ' + str(BEST_FITNESS)

	for x in xrange(1,50):
		p = evolve(p)
		print 'best x:' + str(BEST_X) + ' fitness: ' + str(BEST_FITNESS)

	




	

