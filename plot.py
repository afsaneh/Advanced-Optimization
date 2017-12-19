from mpl_toolkits.mplot3d import Axes3D
from matplotlib import cm
import matplotlib.pyplot as plt
import numpy as np
import scipy.interpolate as interp
from mpl_toolkits.mplot3d import Axes3D


import csv


def importCSV():
	with open('outputAfterMutation.csv', 'rU') as infile:
		reader = csv.DictReader(infile)
		next(reader, None)
		data = {}
		for row in reader:
			for header, value in row.items():
				if not value:
					continue
				try:
					value = float(value)
					data[header].append(value)
				except KeyError:
					data[header] = [value]

		cr = data['cross over rate']
		dimensions = data['dimension']
		mutationRate = data['mutation rate']
		pxp = data['pxp']
		return cr, dimensions, mutationRate, pxp
#
def plot(x, y , z):
	# fig = plt.figure()
	# ax = fig.gca(projection='3d')
	# ax.plot_trisurf(x, y, z, linewidth=0.2)
	# plt.show()

	plotx, ploty = np.meshgrid(np.linspace(np.min(x), np.max(x), 10), np.linspace(np.min(y), np.max(y), 10))
	plotz = interp.griddata((x, y), z, (plotx, ploty), method='linear')

	fig = plt.figure()
	ax = fig.add_subplot(111, projection='3d')
	ax.plot_surface(plotx, ploty, plotz, cstride=1, rstride=1, linewidth=0, antialiased=False)
	ax.set_xlabel('\n' + 'f', linespacing=1, labelpad=10)
	ax.set_zlabel('\n' + 'p', linespacing=0.2, labelpad=10)
	ax.set_ylabel('\n' + 'cr', linespacing=1, labelpad=10)
	plt.show()

# dimesions = data['dimension']
# fitness = data['fitness value']
# pxm = data['pxm']
cr, dimensions, mutationRate, pxp = importCSV()
plot(mutationRate, cr, pxp)
#plot(fitness, dimesions,pxm)
#print (fitness)
#
#
import matplotlib
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import numpy as np

# def plot (x,y,z, d):
# 	# # domains
# 	# x = np.logspace(-1.,np.log10(5),50) # [0.1, 5]
# 	# y = np.linspace(6,9,50)             # [6, 9]
# 	# z = np.linspace(-1,1,50)            # [-1, 1]
#
# 	x1 = np.array(x)
# 	y1 = np.array(y)
# 	z1 = np.array(z)
# 	#convert to 2d matrices
# 	Z = np.outer(z1.T, z1)        # 50x50
# 	X, Y = np.meshgrid(x1, y1)    # 50x50
#
# 	# fourth dimention - colormap
# 	# create colormap according to x-value (can use any 50x50 array)
# 	color_dimension = d # change to desired fourth dimension
# 	minn, maxx = min(color_dimension), max(color_dimension)
# 	norm = matplotlib.colors.Normalize(minn, maxx)
# 	m = plt.cm.ScalarMappable(norm=norm, cmap='jet')
# 	m.set_array([])
# 	fcolors = m.to_rgba(color_dimension)
#
# 	# plot
# 	fig = plt.figure()
# 	ax = fig.gca(projection='3d')
# 	X, Y = np.meshgrid(x, y)
# 	ax.plot_surface(X,Y,Z, rstride=1, cstride=1, facecolors=fcolors, vmin=minn, vmax=maxx, shade=False)
# 	ax.set_xlabel('x')
# 	ax.set_ylabel('y')
# 	ax.set_zlabel('z')
# 	fig.canvas.show()
#
# cr, dimensions, mutationRate, pxp = importCSV()
# plot(cr, pxp,mutationRate, dimensions)