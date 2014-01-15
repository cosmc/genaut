from gautils import *
from evalkiwi import *

population = init_pop(1,10,3, 0.3)

perf = np.array([[1 if random() < 0.3 else 0 for i in xrange(10)] for j in xrange(200)])
print perf

print evalFitness(population, perf, 200, 10, 3)
