import numpy as np
import pandas as pd
import open3d
import random
import os


def load(num_points):
	y = pd.read_csv('data/labels/labels{}.csv'.format(num_points), header=None).values
	z = pd.read_csv('data/metadata/metadata{}.csv'.format(num_points)).values
	x = np.load('data/points/points{}.npy'.format(num_points))
	return x, y, z


def load_augment(num_points):
	y = pd.read_csv('data/labels/augment{}.csv'.format(num_points), header=None).values
	z = []
	x = np.load('data/points/augment{}.npy'.format(num_points))
	return x, y, z


def load_adversarial(filename):
	x = np.load('perturbation/{}'.format(filename))
	y = []
	z = []
	return x, y, z


def visualize(index, x, y, z):
	if len(y) != 0:
		print(y[index])
	if len(z) != 0:
		print(z[index])
	cloud = open3d.geometry.PointCloud()
	cloud.points = open3d.utility.Vector3dVector(x[index])
	open3d.visualization.draw_geometries([cloud])


def vis(x, y, z):
	cloud = open3d.geometry.PointCloud()
	cloud.points = open3d.utility.Vector3dVector(x[0])
	open3d.visualization.draw_geometries([cloud])


def main():
	points = ['0_1_0_adv.npy', '0_1_0_orig.npy', '0_2_0_adv.npy', '0_2_0_orig.npy', '0_3_0_adv.npy', '0_3_0_orig.npy',
		'1_0_0_adv.npy', '1_0_0_orig.npy', '1_2_0_adv.npy', '1_2_0_orig.npy', '1_3_0_adv.npy', '1_3_0_orig.npy',
		'2_0_0_adv.npy', '2_0_0_orig.npy', '2_1_0_adv.npy', '2_1_0_orig.npy', '2_3_0_adv.npy', '2_3_0_orig.npy',
		'3_0_0_adv.npy', '3_0_0_orig.npy', '3_1_0_adv.npy', '3_1_0_orig.npy', '3_2_0_adv.npy', '3_2_0_orig.npy']

#	points = ['0_1_0_orig.npy', '0_2_0_orig.npy', '0_3_0_orig.npy',
#                '1_0_0_orig.npy', '1_2_0_orig.npy', '1_3_0_orig.npy',
#                '2_0_0_orig.npy', '2_1_0_orig.npy', '2_3_0_orig.npy',
#                '3_0_0_orig.npy', '3_1_0_orig.npy', '3_2_0_orig.npy']

	# x, y, z = load('_crop')
	# x_f, y_f, z_f = load('_full')
	# x, y, z = load('32')
#	for i in os.listdir('perturbation/'):
	for i in points:
		x, y, z = load_adversarial(i)
		print(i)
		vis(x, y, z)
		#LENGTH = len(x)
		#rand = []
		#for i in range(LENGTH):
		#	rand.append(i)
		#random.shuffle(rand)
		#for i in rand:
			#visualize(i, x_f, y_f, z_f)
			#print(x[i].shape)
			#z_axis = []
			#for j in x[i]:
			#	z_axis.append(j[0])
			#z_axis.sort()
			#print(z_axis)
		#	visualize(i, x, y, z)


if __name__ == '__main__':
	main()
