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

# bitarray codification of X1 and X2
# S III FFFFFFFFFF + S III FFFFFFFFFF = 28bits

INDIVIDUAL_LENGHT = 32 #number of bites to represent the individual.
POP_SIZE = 100 #number of individuals in the pop.
SELECTED = 0.2 #percentage of selected individuals.
RANDOM_IND = 0.05 #percentage of random individuals to include as parent. may have shit fitness.
MUTATE = 0.01 #percentage of individuals to mutate.

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
	shuffle(l)

	return ''.join(l)

#should receive a 32 bit string and returns a float number
def bin_to_float(binary):
	i = int(binary, 2)
	return struct.unpack('f', struct.pack('I', i))[0]

#receive a X bits string and a number indicate the size of the decimal part and return a pair of float (x1, x2) 
def get_x1_and_x2(binary):
	bin1 = binary[:(len(binary)/2)]
	bin2 = binary[(len(binary)/2):]

	x1 = float(int(bin1,2) - 32767.5)/10000
	x2 = float(int(bin2,2) - 32767.5)/10000

	pair = (x1,x2)
	return pair


#
# GA functions
def generate_population(population_size):
	return [ individual() for x in xrange(population_size) ]

def calculate_fitness(individual):
	xx = get_x1_and_x2(individual)
	x1 = xx[0]
	x2 = xx[1]

	ans = ((4 - (2.1 * (x1 ** 2)) + ((x1 ** 4)/3)) * (x1 ** 2)) + (x1 * x2) + ((-4 + (4*(x2 ** 2))) * x2)
	
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

	for x in xrange(1,5):
		p = evolve(p)
		print BEST_FITNESS

	'''

	control = 0
	tempFit = BEST_FITNESS

	while control < 6:

		p = evolve(p)

		if tempFit == BEST_FITNESS:
			control += 1
		else:
			control = 0

		print BEST_X

	'''











	




	

