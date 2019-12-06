import pykitti
import sys
import os
import csv
import imagesize
import h5py
import random
import numpy as np
import pandas as pd
from scipy.spatial.distance import euclidean
from sklearn.cluster import KMeans

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.append(BASE_DIR)
BASEPATH = os.path.join(BASE_DIR, 'data/kitti_dataset/extracts')
OUT_PATH = os.path.join(BASE_DIR, 'data/points')


def prepare_velo_points(pts3d_raw):
	"""
	Replaces the reflectance value by 1, and tranposes the array, so
	points can be directly multiplied by the camera projection matrix
	"""

	pts3d = pts3d_raw
	# Reflectance > 0
	pts3d = pts3d[pts3d[:, 3] > 0 ,:]
	pts3d[:,3] = 1
	return pts3d.transpose()


def project_velo_points_in_img(pts3d, T_cam_velo, Rrect, Prect):
	"""
	Project 3D points into 2D image. Expects pts3d as a 4xN
	numpy array. Returns the 2D projection of the points that
	are in front of the camera only an the corresponding 3D points.
	"""

	# 3D points in camera reference frame.
	pts3d_cam = Rrect.dot(T_cam_velo.dot(pts3d))

	# Before projecting, keep only points with z>0 
	# (points that are in fronto of the camera).
	idx = (pts3d_cam[2,:]>=0)
	pts2d_cam = Prect.dot(pts3d_cam[:,idx])

	return pts3d[:, idx], pts2d_cam/pts2d_cam[2,:]


def crop_2d(pts2d, Prect, bounds):
	"""
	Expects 2D coordinate points and a dict of bounds of traffic signs
	"""

	min_x = bounds['x'] - bounds['w']
	max_x = bounds['x'] + bounds['w']
	min_y = bounds['y'] - bounds['h']
	max_y = bounds['y'] + bounds['h']
	# print(min_x)
	# print(max_x)
	# print(min_y)
	# print(max_y)

	points = []
	for i, x in enumerate(pts2d[0]):
		y = pts2d[1][i]
		if min_x < x < max_x and min_y < y < max_y:
			points.append(i)

	return points


def load_data(basedir):
	"""
	Loads strings and bounds from KITTI dataset
	"""

	dates = []
	drives = []
	frames = []
	bounds = []
	labels = []

	for date in os.listdir(basedir):
		if date.startswith('2011_'):
			for i in os.listdir(os.path.join(basedir, date)):

				if i.startswith('2011_'):
					drive = i.split('drive_')[1].replace('_sync', '')

					for j in os.listdir(os.path.join(basedir, date, i, 'txt')):
						frame = int(j.replace('.txt', ''))

						with open(os.path.join(basedir, date, i, 'txt', j), 'r') as infile:
							width, height= imagesize.get(os.path.join(basedir, date, i, 'image_02/data', j.replace('.txt', '.png')))

							for line in infile:
								split = line.split()
								x = float(float(split[1]) * width)
								w = float(float(split[3]) * width / 2)
								y = float(float(split[2]) * height)
								h = float(float(split[4]) * height / 2)

								dates.append(date)
								drives.append(drive)
								frames.append(frame)
								bounds.append({'x': x, 'w': w, 'y': y, 'h': h})
								labels.append(split[0])

	return dates, drives, frames, bounds, labels


def add_limit(xcrop, indices, limit):
	for j, val in enumerate(xcrop):
		if val <= limit:
			indices.append(j)

	return indices


def check_limit(xcrop):
	indices = []
	if len(xcrop) >= 32:
		limit = min(xcrop) + 2
		indices = add_limit(xcrop, indices, limit)

		if len(indices) < 32:
			limit += 1
			indices = add_limit(xcrop, indices, limit)

			if len(indices) < 32:
				limit += 1
				indices = add_limit(xcrop, indices, limit)

	return indices


def cluster(point_cloud,):
	closest = []
	k = KMeans(n_clusters=32, random_state=0).fit(point_cloud)
	c = k.cluster_centers_

	for j, center in enumerate(c):
		min_dist = 100000000
		min_index = 0

		for k, val in enumerate(point_cloud):
			temp = euclidean(val, center)
			if temp < min_dist:
				min_dist = temp
				min_index = k
		closest.append(min_index)

	return closest


def main():
	if not os.path.exists(BASEPATH):
		print('Please run download_kitti.py to download the KITTI dataset first.')
		return
	if not os.path.exists(OUT_PATH):
		os.mkdir(OUT_PATH)

	dates, drives, frames, bounds, labels = load_data(BASEPATH)

	cloud0 = []
	label0 = []
	meta0 = []

	cloud_full = []
	label_full = []
	meta_full = []

	for i, date in enumerate(dates):
		data = pykitti.raw(BASEPATH, dates[i], drives[i], frames=[frames[i]])
		velo1 = data.get_velo(0)
		velos = project_velo_points_in_img(prepare_velo_points(velo1), data.calib.T_cam0_velo, data.calib.R_rect_00, data.calib.P_rect_00)
		cropped = crop_2d(velos[1], data.calib.P_rect_00, bounds[i])

		x = np.take(velos[0][0], cropped)
		y = np.take(velos[0][1], cropped)
		z = np.take(velos[0][2], cropped)
		r = np.take(velos[0][3], cropped)

		x_full = velos[0][0]
		y_full = velos[0][1]
		z_full = velos[0][2]
		r_full = velos[0][3]

		indices = check_limit(x)
		zcrop = []

		if len(indices) >= 32:
			xcrop = np.take(x, indices)
			ycrop = np.take(y, indices)
			zcrop = np.take(z, indices)

			point_cloud_full = np.stack((x_full, y_full, z_full), axis=1)
			point_cloud = np.stack((xcrop, ycrop, zcrop), axis=1)

			print(point_cloud.shape)
			print(point_cloud_full.shape)

			closest = cluster(point_cloud)

			xcrop0 = np.take(xcrop, closest)
			ycrop0 = np.take(ycrop, closest)
			zcrop0 = np.take(zcrop, closest)

			cluster_cloud = np.stack((xcrop0, ycrop0, zcrop0), axis=1)
			print(cluster_cloud.shape)

			cloud0.append(cluster_cloud)
			if labels[i] == '3':
				label0.append('2')
			elif labels[i] == '4':
				label0.append('3')
			else:
				label0.append(labels[i])
			meta0.append(np.array([dates[i], drives[i], frames[i]]))

			cloud_full.append(point_cloud_full)
			label_full.append(labels[i])
			meta_full.append(np.array([dates[i], drives[i], frames[i]]))

		print(data.data_path)
		print(data.frames)

		print('Total points - {}'.format(len(z)))
		print('Crop points - {}\n'.format(len(zcrop)))

	print('FINISHED')
	print(len(cloud0))

	np.save(os.path.join(OUT_PATH, 'points_full.npy'), np.asarray(cloud_full))
	np.save(os.path.join(OUT_PATH, 'points_crop.npy'), np.asarray(cloud0))

	pd.DataFrame(label_full).to_csv(os.path.join(OUT_PATH, 'labels_full.csv'), header=None, index=None)
	pd.DataFrame(meta_full).to_csv(os.path.join(OUT_PATH, 'metadata_full.csv'), header=None, index=None)

	pd.DataFrame(label0).to_csv(os.path.join(OUT_PATH, 'labels_crop.csv'), header=None, index=None)
	pd.DataFrame(meta0).to_csv(os.path.join(OUT_PATH, 'metadata_crop.csv'), header=None, index=None)


if __name__ == '__main__':
	main()