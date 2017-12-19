import numpy as np
import scipy as sc
from scipy import spatial
import time
import csv


class Point:
	def __init__(self, name, dimension):
		self.dimension = dimension
		self.value = 0
		self.name = name
		self.distance = 0
		self.afterMutationCounter = 0
		self.afterCrossoverCounter = 0
		self.initialCounter = 0

	def addinitialCounter(self):
		self.initialCounter += 1

	def addAfterMutationCounter(self):
		self.afterMutationCounter += 1

	def addAfterCrossoverCounter(self):
		self.afterCrossoverCounter += 1

	def setDistance(self, dist):
		self.distance = dist

	def setValue(self, v):
		self.value = v

	def setRandomValueToPoint(self):
		"""assign a new value to a point in d dimension"""
		self.value = np.random.rand(1, self.dimension)[0][0]

	def copyObject(self, y):
		self.dimension = y.dimension
		self.value = y.value
		self.name = y.name
		self.distance = y.distance
		self.afterMutationCounter = y.afterMutationCounter
		self.afterCrossoverCounter = y.afterCrossoverCounter
		self.initialCounter = y.initialCounter

	def __repr__(self):
		return '%s --> distance: %s \n\t   counter: %s %s' % (self.name, self.distance, self.afterMutationCounter,self.afterCrossoverCounter)

	def __lt__(self, other):
		return self.distance < other.distance

	def __gt__(self, other):
		return self.distance > other.distance


def findDistance(x, y):
	"""find the distance between two points in D-dimension"""
	return sc.spatial.distance.euclidean(x.value, y.value)


def findMinimumDistancePoint(s, pointLst):
	"""find the point with the minimum distance"""
	dictionary = {}
	for x in pointLst:
		dictionary[x] = x.value
	#dictionary = {xa: xa.value, xb: xb.value, xc: xc.value, xm: xm.value, xp: xp.value}
	minimumValue = min(dictionary, key=dictionary.get)
	return minimumValue


def buildPoints(d):
	"""make the points"""

	s = Point('solution', d)
	xa = Point('xa',d)
	xb = Point('xb',d)
	xc = Point('xc',d)
	xm = Point('xm', d)
	xp = Point('xp', d)
	return s, xa, xb, xc, xm, xp


def buildTheCounters(d, f, cr):
	"""count the number of times each point has a minimum dist to the solution"""

	s, xa, xb, xc, xm, xp = buildPoints(d)

	for i in range(100000):
		xa.setRandomValueToPoint()
		xb.setRandomValueToPoint()
		xc.setRandomValueToPoint()
		xm.setValue(xa.value + f * (xb.value - xc.value))
		xp.setRandomValueToPoint()

		xa.setDistance(findDistance(s, xa))
		xb.setDistance(findDistance(s, xb))
		xc.setDistance(findDistance(s, xc))
		xm.setDistance(findDistance(s, xm))
		xp.setDistance(findDistance(s, xp))


		#------------------------------------------------------
		#initial points
		findMinimumDistancePoint(s, [xa, xb, xc, xp]).addinitialCounter()

		#------------------------------------------------------
		#mutation
		findMinimumDistancePoint(s, [xa, xb, xc, xm, xp]).addAfterMutationCounter()

		# ------------------------------------------------------
		#crossover
		if isCrossOver(cr):
			if xm.distance < xp.distance:
				xp.copyObject(xm)
				findMinimumDistancePoint(s, [xa, xb, xc, xp]).addAfterCrossoverCounter()
			else:
				findMinimumDistancePoint(s, [xa, xb, xc, xp]).addAfterCrossoverCounter()

	return s, xa, xb, xc, xm, xp


def probability(counter, total):
	return counter/total


def setXmValue(f, xa, xb, xc, xm):
	xm.setValue(xa.value + f*(xb.value - xc.value))


def isCrossOver(cr):
	cOver = np.random.random_sample()
	if cOver <= cr:
		return True
	else:
		return False

# def main():
#
# 	# run for 100'000 times
#
# 	# build solution and points
#
# 	# ----------------------------------------------
# 	# Calculate the probability before crossover
#
#
# 	#----------------------------------------------
# 	# Do the crossover
#
# 	#----------------------------------------------
# 	# Calculate the probability after crossover
#
#
# 	return


def main():
	start_time = time.time()
	#fitness = [0.4, 0.8, 1]

	#file 1
	csvFile1 = open('outputinitialPoints.csv', 'w')
	writer1 = csv.writer(csvFile1, delimiter=',')
	writer1.writerow(['dimension', 'mutation rate', 'cross over rate', 'pxa', 'pxb', 'pxc', 'pxp'])

	#file 2
	csvFile2 = open('outputAfterMutation.csv', 'w')
	writer2 = csv.writer(csvFile2, delimiter=',')
	writer2.writerow(['dimension', 'cross over rate', 'mutation rate', 'pxa', 'pxb', 'pxc', 'pxp', 'pxm'])

	#file 3
	csvFile3 = open('outputAfterCrossover.csv', 'w')
	writer3 = csv.writer(csvFile3, delimiter=',')
	writer3.writerow(['dimension', 'cross over rate', 'mutation rate', 'pxa', 'pxb', 'pxc', 'pxp'])


	crossOver = [float(("{0:.1f}".format(i))) for i in np.arange(0.1, 1, 0.1)]
	fitness = [float(("{0:.1f}".format(i))) for i in np.arange(0.2, 1.1, 0.1)]
	# crossOver = [float(("{0:.1f}".format(i))) for i in np.arange(0.1, 1, 0.3)]
	# fitness = [float(("{0:.1f}".format(i))) for i in np.arange(0.2, 1.1, 0.4)]
	dimension = [i for i in range(1, 101)]

	for d in dimension:  # dimension interval
		print ("dimension", d)
		for cr in crossOver:
			print ("cr", cr)
			for f in fitness:  # to check different fitness values
				s, xa, xb, xc, xm, xp = buildTheCounters(d, f, cr)

				#probabilities of initial points
				pxa3 = probability(xa.initialCounter, 100000)
				pxb3 = probability(xb.initialCounter, 100000)
				pxc3 = probability(xc.initialCounter, 100000)
				pxp3 = probability(xp.initialCounter, 100000)

				#probabilities after mutation
				pxa1 = probability(xa.afterMutationCounter, 100000)
				pxb1 = probability(xb.afterMutationCounter, 100000)
				pxc1 = probability(xc.afterMutationCounter, 100000)
				pxp1 = probability(xp.afterMutationCounter, 100000)
				pxm1 = probability(xm.afterMutationCounter, 100000)

				#probabilities after crossover
				pxa2 = probability(xa.afterCrossoverCounter, 100000)
				pxb2 = probability(xb.afterCrossoverCounter, 100000)
				pxc2 = probability(xc.afterCrossoverCounter, 100000)
				pxp2 = probability(xp.afterCrossoverCounter, 100000)
				#pxm2 = probability(xp.afterCrossoverCounter, 100000)


				#initial point file writing
				sentenceInitialPoints = [d, cr, f, pxa3, pxb3, pxc3, pxp3]
				writer1.writerow(sentenceInitialPoints)

				#after mutation file writing
				sentenceAfterMutation = [d, cr, f, pxa1, pxb1, pxc1, pxp1, pxm1]
				writer2.writerow(sentenceAfterMutation)
				#print("--- %s seconds for the first file---" % (time.time() - start_time))


				#after crossover file writing
				sentenceAfterCrossover = [d, cr, f, pxa2, pxb2, pxc2, pxp2]
				writer3.writerow(sentenceAfterCrossover)

	csvFile1.close()
	csvFile2.close()
	csvFile3.close()

	print("--- %s seconds ---" % (time.time() - start_time))

main()

