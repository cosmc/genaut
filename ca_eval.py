import numpy as np
import gautils
import pdb

def evalFitness(genes,perfectPatterns,t, m, r):
# Create Cellular Automata for each individual based on the input genes, and 
# 		evaluate the fitness of all possible subwindows of the CA against perfectPatterns. 
# Inputs: evalfunc -- the function used to evaluate the fitness
#		  genes -- 2D numpy array where each row is genome of an individual with 2^(2r+1)+m elements.
#         perfectPatterns -- t by m 2D numpy array of binary numbers generated from
#								actual data. (an output of generatePerfectPattern())
#         t -- The number of steps in CA
#         m -- The width of the configuration space.
#         r -- The radius of the transition rule.
#
# Output: A list of tuples (genome, fitness score, CA map, best subwindow) 
#			in which fitness score is the score calculated from the best matching subwindow of the CA. 
#			The last two are the entire CA map and the map of its best performing subwindow (saved for plot).

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
		# best = np.empty((t,m))
		for i in range(0,1 + step-t):
			matchScore.append(Hamming(perfectPatterns,caMap[i:i+t]) )/float(t*m))
			# best = caMap[i:i+t]
		best_i = matchScore.index(max(matchScore))
		best = caMap[best_i:best_i+t]
		geneFitnessMap.append((individual,max(matchScore),caMap, best))

	return geneFitnessMap

			
def Hamming(map1,map2):
	# Return the hamming distance (# of exact matches) between the two grid maps
	return 1. - np.count_nonzero(map1 - map2)

def Gaussian(map1,map2):
	# Apply Gaussian filtering and compare the resulting maps
	return

def Prior(map1,map2):
	# Use the prior info about perfectPatterns: weight the matches depending on its importance
	return

def GroupMatch(map1,map2):
	# A more scientific and general approach than the prior.
	# Detect the groups/clusters of 0s and 1s, and measure the match between those groups.
	return


