from gautils import *
from evalkiwi import *
from spect import *
import matplotlib.pyplot as plt

width = 129
timesteps = 47
numGens = 1000

population = init_pop(100,width,3, 0.3)

perf = getPerfectPattern('./ploink.wav', timesteps, width, 1.0)
plt.matshow(perf, cmap=cm.gist_heat_r)
plt.savefig('plots/perf.png')
plt.close

for gen in xrange(numGens):

	fitpop = evalFitness(population, perf, timesteps, width, 3)

	#top fitness score
	best = max(fitpop, key=lambda x: x[1])
	print gen ,":", best[1]
	fname = "plots/" + str(gen) + ".png"
	plt.matshow(best[2], cmap=cm.gist_heat_r)
	plt.savefig(fname)
	plt.close()

	population = breed(fitpop, 0.80, 0.2, 0.002)
