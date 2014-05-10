#!/usr/local/bin/python

from gautils import *
from ca_eval import *
from spect import *
import matplotlib.pyplot as plt
import os, sys
from datetime import datetime
import pdb
import random
import multiprocessing
from subprocess import Popen, PIPE


debug = True

##----------------------------##
##    Important parameters    ##
##----------------------------##

# number of processors to use in multiprocessing
num_proc = 10 

# grid size parameter
width = 129
timesteps = 47

# number of generation GA runs
numGens = 2000

# GA initial population parameter; 
init_numpop = 10
p_init_ones = 0.7

# GA breed parameter
p_elite = 0.2
p_survive = 0.0
p_mut = 0.05

#-----------------------------#
paramDir = 'Hamming/size%i_%iinit%gp%g_%g_%g/'%(width,timesteps,p_init_ones,p_elite, p_survive, p_mut)


def checkLastJob():
    if os.path.isfile(paramDir+"pid_file.txt"):
        f = open(paramDir+"pid_file.txt",'r')
        l = f.readline()
        sub_proc = Popen(['ps', 'aux'], shell=False, stdout=PIPE)
        for line in sub_proc.stdout:
            if str(l) in line:
                print "Another instance of the submission script is running ... exiting"
                print "check pid: ",line
                exit(0)
        print "removing stale lock file"
        os.system("rm -f "+paramDir+"pid_file.txt")


def runCAGA(id,width,timesteps,numGens,init_numpop,p_init_ones,p_elite, p_survive, p_mut):
	random.seed(id)
	time = datetime.now().strftime('%Y%m%d_%H%M')
	paramDir = 'Hamming/size%i_%iinit%gp%g_%g_%g/'%(width,timesteps,p_init_ones,p_elite, p_survive, p_mut)
	plotDir = paramDir + str(id) + '_' + time +'/'

	if not os.path.exists(paramDir + 'log/'):
		os.makedirs(paramDir + 'log/')
	if not os.path.exists(plotDir):
		os.makedirs(plotDir)

	# Record the pid for each instance
	with open(paramDir+"pid_file.txt",'a') as f:
	    f.write('%i \n' % os.getpid())

	# Begin logging the stdout
	old_stdout = sys.stdout
	log_file = open(paramDir+'log/'+str(id)+'_'+time+".log","w")
	sys.stdout = log_file

	population = init_pop(init_numpop, width, 3, p_init_ones)
	# pdb.set_trace();
	perf = getPerfectPattern('./ploink.wav', timesteps, width, 1.0)
	plt.matshow(perf, cmap=cm.gist_heat_r)
	plt.savefig(plotDir+'perf.png')
	plt.close

	print "p_elite, p_survive, p_mut: %g, %g, %g"%(p_elite, p_survive, p_mut)
	print "gen iteration start time: ", datetime.now().strftime('%Y-%m-%d %H:%M:%S')
	previousBest = 0
	for gen in xrange(numGens):
		fitpop = evalFitness(population, perf, timesteps, width, 3)
		# top fitness score among all individuals in this generation
		best = max(fitpop, key=lambda x: x[1])	
		if best[1] != previousBest:
			print gen ,":", best[1]
			fname = plotDir + str(gen) + ".png"
			fname_sub = plotDir + str(gen) + "_sub.png"
			plt.matshow(best[2], cmap=cm.gist_heat_r)
			plt.savefig(fname)
			plt.close()
			plt.matshow(best[3], cmap=cm.gist_heat_r)
			plt.savefig(fname_sub)
			plt.close()

			previousBest = best[1]
		population = breed(fitpop, p_elite, p_survive, p_mut)

	sys.stdout = old_stdout
	log_file.close()



# ------------------Execute multiprocessing------------------ #


if __name__ == "__main__":
	checkLastJob()
	if debug:
		numGens = 20
		runCAGA(0,width,timesteps,numGens,init_numpop,p_init_ones,p_elite, p_survive, p_mut)
	else:
		jobs = []
		for i in xrange(num_proc):
			for i in range(0, num_proc):
				out_list = list()
				process = multiprocessing.Process(target=runCAGA, 
					        	args=(i,width,timesteps,numGens,init_numpop,p_init_ones,p_elite, p_survive, p_mut))
				jobs.append(process)

			# Start the processes (i.e. calculate the random number lists)		
			print "starting the multiprocessing jobs"
			for j in jobs:
				j.start()

			# Ensure all of the processes have finished
			for j in jobs:
				j.join()



