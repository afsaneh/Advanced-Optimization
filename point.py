import numpy as np
import scipy as sc
from scipy import spatial
import time
import csv
from matplotlib import pyplot


class Point:
	def __init__(self, name, dimension):
		self.dimension = dimension
		self.value = 0
		self.name = name
		self.distance = 0
		self.counter = 0

	def addCounter(self):
		self.counter += 1

	def setDistance(self, dist):
		self.distance = dist

	def setValue(self, v):
		self.value = v

	def setRandomValueToPoint(self):
		"""assign a new value to a point in d dimension"""
		self.value = np.random.rand(1, self.dimension)[0][0]

	def __repr__(self):
		return '%s --> distance: %s \n\t   counter: %s' % (self.name, self.distance, self.counter)

	def __lt__(self, other):
		return self.distance < other.distance

	def __gt__(self, other):
		return self.distance > other.distance


def findDistance(x, y):
	"""find the distance between two points in D-dimension"""
	return sc.spatial.distance.euclidean(x.value, y.value)


def findMinimumDistancePoint(s, xa, xb, xc, xm):
	'''find the point with the minimum distance'''

	dictionary = {xa: xa.value, xb: xb.value, xc: xc.value, xm: xm.value}
	minimumValue = min(dictionary, key=dictionary.get)
	return minimumValue


def buildPoints(d):
	"""make the points"""

	s = Point('solution', d)
	xa = Point('xa',d)
	xb = Point('xb',d)
	xc = Point('xc',d)
	xm = Point('xm', d)
	return s, xa, xb, xc, xm


def buildTheCounters(d, f):
	'''count the number of times each point has a minimum dist to the solution'''
	s, xa, xb, xc, xm = buildPoints(d)
	for i in range(1, 100001):
		xa.setRandomValueToPoint()
		xb.setRandomValueToPoint()
		xc.setRandomValueToPoint()
		xm.setValue(xa.value + f * (xb.value - xc.value))

		xa.setDistance(findDistance(s, xa))
		xb.setDistance(findDistance(s, xb))
		xc.setDistance(findDistance(s, xc))
		xm.setDistance(findDistance(s, xm))


		# print(findMinimumDistancePoint(s, xa, xb, xc, xm))
		findMinimumDistancePoint(s, xa, xb, xc, xm).addCounter()
		# print(xa.counter, xb.counter, xc.counter)
		# print(xa.value, xb.value, xc.value)
	return s, xa, xb,xc, xm


def probability(counter, total):
	return counter/total


def pointProbability(x, total):
	return probability(x.counter, total)


def setXmValue(f, xa, xb, xc, xm):
	xm.setValue(xa.value + f*(xb.value - xc.value))


def isCrossOver(cr):
	cOver = np.random.random_sample()
	if cOver <= cr:
		return True
	else:
		return False


def test():
	start_time = time.time()
	fitness = [0.4, 0.8, 1]
	csvFile = open('output.csv', 'a')
	rowWriter = csv.writer(csvFile, delimiter=',')
	rowWriter.writerow(['dimension', 'fitness value', 'pxa', 'pxb', 'pxc', 'pxm'])

	for f in fitness:  # to check different fitness values
		for d in range(1, 100):  # dimension interval
			s, xa, xb, xc, xm = buildTheCounters(d, f)

			pxa = pointProbability(xa, 100000)
			pxb = pointProbability(xb, 100000)
			pxc = pointProbability(xc, 100000)
			pxm = pointProbability(xm, 100000)

			sentence = [d, f, pxa, pxb, pxc, pxm]
			rowWriter.writerow(sentence)
	csvFile.close()

	print("--- %s seconds ---" % (time.time() - start_time))

test()