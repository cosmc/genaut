import numpy as np
from random import random, randint, randrange

def init_pop(n,m,r,p):
# Initializes a population, represented by a numpy array of genomes.
# Inputs: n -- The number of individuals.
#         m -- The width of the configuration space.
#         r -- The radius of the transition rule.
#         p -- The frequency of 1s in the genomes.
# Returns: An n by 2^(2r+m) numpy array, where each row is the genome of an individual.
  
  return np.array([[1 if random() < p else 0 for i in range(m + pow(2, 2*r+1))] for j in range(n)])


def breed(fitpop, p_elite, p_survive, p_mut):
# Breeds the current population based on fitness to generate the next population.
# Inputs: fitpop    -- A list of tuples (genome, fitness) representing he current population.
#         p_elite   -- The fraction of the population to breed from, rounded down.
#         p_survive -- The fraction of the population to be retained in the next iteration, rounded down.
#         p_mut     -- The probability of mutation.
# Returns: The new population as a 2D numpy array.

  sortpop = sorted(fitpop, key=lambda x: x[1])
  n = len(sortpop)
  n_elite = int(p_elite * n)
  n_survive = int(p_survive * n)

  elite = [sortpop[i][0] for i in range(n_elite)]
  survivors = [sortpop[i][0] for i in range(n_survive)]

  newpop = elite

  # ACTIVATE THE RECOMBINATRON
  for i in range(n - n_elite):
    mom, dad = elite[randint(0, n_elite-1)], elite[randint(0, n_elite-1)]
    cxPoint = randrange(0,len(mom))
    baby = np.concatenate((mom[:cxPoint],dad[cxPoint:]))
    newpop.append(baby)

  # ACTIVATE THE MUTAGENATRIX
  for i in range(len(newpop)):
    for j in range(len(newpop[i])):
      if random() < p_mut:
          newpop[i][j] += 1
          newpop[i][j] %= 2

  return newpop
