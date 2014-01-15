import numpy as np
import gautils
import pdb
#n, m, r, p are given as initial conditions

def evalFitness(genes,perfectPatterns,t, m, r):
	geneFitnessMap = []
	for individual in genes:
		initGene = individual[:m]
		caMap = np.empty((t,m,))
		caMap.fill(np.nan)
		caMap[0] = initGene
		for step in range(1,t):
			for i in range(len(initGene)):
				neighbor = initGene.take(range(i-r,i+r+1),mode='wrap')
				s = ""
				for c in neighbor:
					s += str(c)
				s = int(s,2) #s is between 0 and 127
				caMap[step][i] = individual[m+s]
		matchScore = 1. - np.count_nonzero(perfectPatterns - caMap)/float(t*m)
		geneFitnessMap.append((individual,matchScore))

	return geneFitnessMap

			





