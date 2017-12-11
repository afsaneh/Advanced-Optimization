from mpl_toolkits.mplot3d import Axes3D
from matplotlib import cm
import matplotlib.pyplot as plt
import numpy as np
import scipy.interpolate as interp
from mpl_toolkits.mplot3d import Axes3D


import csv


def importCSV():
	with open('output2.csv', 'rU') as infile:
		reader = csv.DictReader(infile)
		next(reader, None)
		data = {}
		for row in reader:
			for header, value in row.items():
				try:
					value = float(value)
					data[header].append(value)
				except KeyError:
					data[header] = [value]

		dimensions = data['dimension']
		fitness = data['fitness value']
		pxm = data['pxm']
		return dimensions, fitness, pxm

def plot(x, y , z):
	# fig = plt.figure()
	# ax = fig.gca(projection='3d')
	# ax.plot_trisurf(x, y, z, linewidth=0.2)
	# plt.show()

	plotx, ploty = np.meshgrid(np.linspace(np.min(x), np.max(x), 10), np.linspace(np.min(y), np.max(y), 10))
	plotz = interp.griddata((x, y), z, (plotx, ploty), method='linear')

	fig = plt.figure()
	ax = fig.add_subplot(111, projection='3d')
	ax.plot_surface(plotx, ploty, plotz, cstride=1, rstride=1, cmap='viridis')
	ax.set_xlabel('\n' + 'dimension', linespacing=1, labelpad=10)
	ax.set_zlabel('\n' + 'pxm', linespacing=0.2, labelpad=10)
	ax.set_ylabel('\n' + 'fitness value', linespacing=1, labelpad=10)
	plt.show()

# dimesions = data['dimension']
# fitness = data['fitness value']
# pxm = data['pxm']
d, f, p = importCSV()
plot(d, f, p)
#plot(fitness, dimesions,pxm)
#print (fitness)
