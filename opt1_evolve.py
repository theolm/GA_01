"""
Copyright (c) 2017 Theodoro L. Mota
"""

from random import randint, random
from operator import add

#
# Global variables

INDIVIDUAL_LENGHT = 8 #number of bites to represent the individual
POP_INDIVIDUAL_SIZE = 500 #number of individuals in the pop.


#
# Helper functions

def individual():
    'Create a member of the population.'

    temp = ''

    for x in xrange(INDIVIDUAL_LENGHT):
    	temp += str(randint(0,1))

    return temp

def population():
    return [ individual() for x in xrange(POP_INDIVIDUAL_SIZE) ]


#
# GA functions

if __name__ == "__main__":
	pop = population()

	for n in range(len(pop)):
		print pop[n]

