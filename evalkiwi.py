import numpy as np
import gautils
import pdb
#n, m, r, p are given as initial conditions

def evalFitness(genes,perfectPatterns,t, m, r):
	geneFitnessMap = []
	for individual in genes:
		initGene = individual[:m]
		caMap = np.empty((400,m,))
		caMap.fill(np.nan)
		caMap[0] = initGene
		done = False
		step = 1
		newRow = np.empty(m)
		#for step in range(1,t):
		while not done:
			for i in range(len(initGene)):
				neighbor = caMap[step-1].take(range(i-r,i+r+1),mode='wrap')
				#print range(i-r,i+r+1)
				s = ""
				for c in neighbor:
					s += str(int(c))
				s = int(s,2) #s is between 0 and 127
				#caMap[step][i] = individual[m+s]
				newRow[i] = individual[m+s]

			if (len(np.where(np.all(caMap == newRow, axis=1))[0]) > 0) and (step >= t):
				done = True
			elif (step >= 400):
				done = True
			else:
				caMap[step] = newRow
				step += 1

		matchScore = []
		best = np.empty((t,m))
		for i in range(0,1 + step-t):
			matchScore.append(1. - np.count_nonzero(perfectPatterns - caMap[i:i+t])/float(t*m))
			best = caMap[i:i+t]
		
		geneFitnessMap.append((individual,max(matchScore),caMap, best))

	return geneFitnessMap

			





