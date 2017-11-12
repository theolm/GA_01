"""
Copyright (c) 2017 Theodoro L. Mota
"""

from random import randint, random, shuffle
from math import sin
from scipy.integrate import quad
from operator import add
from functools import reduce
import struct


#Six-hump camel back function
# -3 < x1 < 3 && -2 < x2 < 2
# x1 = 6 * 10**4 -> 60000 -> 16 bits (int 65535)
# x2 = 4 * 10**4 -> 40000 -> 16 bits (int 65535)


#
# Global variables

INDIVIDUAL_LENGHT = 30 #number of bites to represent the individual.
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


#receive a X bits string and a number indicate the size of the decimal part and return a pair of float (x1, x2) 
def convert_to_x1_and_x2(binary):

	ind_size = INDIVIDUAL_LENGHT/2

	x1_decimal = int(binary[:ind_size], 2)
	x2_decimal = int(binary[ind_size:], 2)

	divider = (2**ind_size) - 1
	

	x1 = -3.0 + x1_decimal * (6.0/divider)
	x2 = -2.0 + x2_decimal * (4.0/divider)

	return (x1,x2)


#
# GA functions
def generate_population(population_size):
	return [ individual() for x in xrange(population_size) ]

def calculate_fitness(individual):
	xx = convert_to_x1_and_x2(individual)
	x1 = xx[0]
	x2 = xx[1]

	ans = (4 - 2.1*(x1*x1) + (x1*x1*x1*x1)/3.0)*(x1*x1) + x1*x2 + (-4 + 4*(x2*x2))*(x2*x2)

	return ans


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

	#add shity individuals to escape max locals.
	for individual in graded[retain_length:]:
		if RANDOM_IND > random():
			parents.append(individual)

	#mutate the parents
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
			half = len(male) / 2
			child = male[:half] + female[half:]
			offsprings.append(child)
			#print 'male: ' + male + ' female: ' + female + ' child: ' + child

	parents.extend(offsprings)
	return parents

# functions to implement:
# average_fitness - determine the average fitness of the pop.


if __name__ == "__main__":

		
	p = generate_population(POP_SIZE)
	p = evolve(p)

	temp_best = BEST_FITNESS
	count = 0
	while (count < 200):
		p = evolve(p)
		if BEST_FITNESS != temp_best:
			temp_best = BEST_FITNESS
			count = 0
		count +=1
		print count


	print convert_to_x1_and_x2(BEST_X)
	print BEST_FITNESS






	

