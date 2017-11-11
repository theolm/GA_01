"""
Copyright (c) 2017 Theodoro L. Mota
					& Vilmar Neto
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

INDIVIDUAL_LENGHT = 32 #number of bites to represent the individual.
POP_SIZE = 500 #number of individuals in the pop.
SELECTED = 0.2 #percentage of selected individuals.
RANDOM_IND = 0.05 #percentage of random individuals to include as parent. may have shit fitness.
MUTATE = 0.01 #percentage of individuals to mutate.

PI = 3.141592 # Pi

BEST_X = None
BEST_FITNESS = None

BITS32 = 2 ** 32
BITS16 = 2 ** 16

#
# Helper functions
"""
change_bit: individual -> string of bits
 			i -> random position of the string of bits

change_bit: receives an individual and a index of a random position
			then change that respective random bit.
"""
def change_bit(individual,i):
	if individual[i] == '1':
		individual[i] = '0'
	elif individual[i] == '0':
		individual[i] = '1'
	return individual
"""
individual -> string with 0's & 1's (bits)

individual: creates a individual, composed by 0's & 1's.
"""
def individual():


	temp = ''
	for x in xrange(INDIVIDUAL_LENGHT):
		temp += str(randint(0,1))

	return temp
"""
mutate_individual -> individual

mutate_individual: receive an individual then change a random bit
				   in its content.
"""
def mutate_individual(individual):
	l = list(individual)

	random_position = randint(0,len(l)-1)
	#shuffle(l)
	l = change_bit(l,random_position)


	return ''.join(l)

#should receive a 32 bit string and returns a float number
def bin_to_float(binary):
	i = int(binary, 2)
	return struct.unpack('f', struct.pack('I', i))[0]

#receive a X bits string and a number indicate the size of the decimal part and return a pair of float (x1, x2)
def get_x1_and_x2(binary):
	bin1 = binary[:(len(binary)/2)]
	bin2 = binary[(len(binary)/2):]

	x1 = float(int(bin1,2) -1 - 32767)/10000
	x2 = float(int(bin2,2) -1 - 32767)/10000

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

	for x in xrange(1,10):
		p = evolve(p)
	print get_x1_and_x2(BEST_X)
	print BEST_FITNESS
