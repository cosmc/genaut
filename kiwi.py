from gautils import *
from evalkiwi import *
from spect import *
import matplotlib.pyplot as plt

width = 129
timesteps = 47
numGens = 500

population = init_pop(100,width,3, 0.3)

perf = getPerfectPattern('./ploink.wav', timesteps, width, 1.0)

for gen in xrange(numGens):

  fitpop = evalFitness(population, perf, timesteps, width, 3)

  #top fitness score
  best = max(fitpop, key=lambda x: x[1])
  print gen ,":", best[1]
  fname = "plots/" + str(gen) + ".png"
  plt.matshow(best[2])
  plt.savefig(fname)
  plt.close()

  population = breed(fitpop, 0.9, 0.1, 0.05)
