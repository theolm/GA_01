"""
Copyright (c) 2017 Theodoro L. Mota
"""
import matplotlib.pyplot as plt
from random import randint, random, shuffle
from math import sin
from scipy.integrate import quad
from operator import add
from functools import reduce
import struct

#
# Global variables

INDIVIDUAL_LENGHT = 15 #number of bites to represent the individual.
POP_SIZE = 100 #number of individuals in the pop.
SELECTED = 0.2 #percentage of selected individuals.
RANDOM_IND = 0.05 #percentage of random individuals to include as parent. may have shit fitness.
MUTATE = 0.01 #percentage of individuals to mutate.
MUTATE_FACTOR = 0.6 #chance to change a bit in the mutation

PI = 3.141592 # Pi

BEST_X = None
BEST_FITNESS = None



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

	for x in xrange(len(l)):
		if random() < MUTATE_FACTOR:
			if l[x] == '0':
				l[x] = '1'
			else:
				l[x] = '0'


	return ''.join(l)

#should receive a 32 bit string and returns a float number
def bin_to_float(binary):
	i = int(binary, 2)
	return struct.unpack('f', struct.pack('I', i))[0]

#receive a X bits string and a number indicate the size of the decimal part and return a pair of float (x1, x2)
def convert_to_x(binary):
	x_decimal = int(binary, 2)
	x = x_decimal * (PI/(2**len(binary) - 1))
	return x

#
# GA functions
def generate_population(population_size):
	return [ individual() for x in xrange(population_size) ]

def calculate_fitness(individual):
	x = convert_to_x(individual)
	m = 10
	ans = 0

	for i in xrange(1,6):
		ans = ans + ((sin(x) * (sin((i*(x ** 2))/ PI) ** (2 * m))) * -1)

	return ans

#def calculate_average_fitness(population):
#	fitness_sum =  reduce(add, (calculate_fitness(x) for x in population), 0)
#	return (fitness_sum / (len(population) * 1.0))

def evolve(population):
	global BEST_FITNESS
	global BEST_X

	graded = [ (calculate_fitness(x), x) for x in population]
	sorted_graded = sorted(graded)

	#always keeps traks of the best result to the fitness function. in this case the lower fitness
	pop_leader = sorted_graded[0]

	if BEST_X is None:
		BEST_FITNESS = pop_leader[0]

		BEST_X = pop_leader[1]

	if pop_leader[0] < BEST_FITNESS: # change that if necessary
		BEST_FITNESS = pop_leader[0]

		BEST_X = pop_leader[1]


	graded = [ x[1] for x in sorted_graded]

	retain_length = int(len(graded)*SELECTED)
	parents = graded[:retain_length] #pick X% of the best in the population

	#add shitty individuals to escape max locals.
	for individual in graded[retain_length:]:
		if RANDOM_IND > random():
			parents.append(individual)

	#mutate some the shit out of the parents
	#for individual in xrange(len(parents)):
	#	if MUTATE > random():
	#		parents[individual] = mutate_individual(parents[individual])


	parents_length = len(parents)
	offspring_lenght = len(population) - parents_length
	offsprings = []

	while len(offsprings) < offspring_lenght:
		male = randint(0, parents_length-1)
		female = randint(0, parents_length-1)
		if male != female:
			male = parents[male]
			female = parents[female]
			half = len(male) / 2
			child = male[:half] + female[half:]
			offsprings.append(child)

	parents.extend(offsprings)

	p = []

	#mutate 1% of the new gen
	for individual in xrange(len(parents)):
		mut = parents[individual]
		if 0.01 > random():
			mut = mutate_individual(mut)

		p.append(mut)

	return p

# functions to implement:
# average_fitness - determine the average fitness of the pop.


if __name__ == "__main__":

	p = generate_population(POP_SIZE)

	lst_best_x = []

 	lst_best_fitness = []


	print 'best x:' + str(BEST_X) + ' fitness: ' + str(BEST_FITNESS)

	for x in xrange(1,6000):
		p = evolve(p)
		lst_best_x.append(convert_to_x(BEST_X))
		lst_best_fitness.append(BEST_FITNESS)
		print 'best x:' + str(convert_to_x(BEST_X)) + ' fitness: ' + str(BEST_FITNESS)



	plt.plot(lst_best_x)
	sup_limit = max(lst_best_x)
	inf_limit = min(lst_best_x)
	plt.axis([0,6000,inf_limit - 0.0001,sup_limit + 0.0001])
	plt.show()

	plt.plot(lst_best_fitness)
	sup_limitf= max(lst_best_fitness)
	inf_limitf = min(lst_best_fitness)
	plt.axis([0,6000,inf_limitf - 0.01,sup_limitf + 0.01])
	plt.show()
