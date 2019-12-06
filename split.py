import os, sys
import numpy as np
import pandas as pd
from math import ceil

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.append(BASE_DIR)
POINTS_PATH = os.path.join(BASE_DIR, 'data/points')
SPLIT_PATH = os.path.join(BASE_DIR, 'data/split')


def train_test_split(x, y, test_size, train_file, test_file):
	labels = {}
	test = []
	train = []

	print(x.shape)
	print(y.shape)

	for i, val in enumerate(x):
		if y[i][0] in labels:
			labels[y[i][0]].append(i)
		else:
			labels[y[i][0]] = [i]

	for key, val in labels.items():
		length = ceil(len(val) * test_size)
		np.random.shuffle(val)
		for i in range(length):
			test.append(val[i])
		for i in range(length, len(val)):
			train.append(val[i])

	pd.DataFrame(train).to_csv(train_file, header=None, index=None)
	pd.DataFrame(test).to_csv(test_file, header=None, index=None)


def main():
	if not os.path.exists(POINTS_PATH):
		print('Please run augment.py to augment the point clouds first.')
		return
	if not os.path.exists(SPLIT_PATH):
		os.mkdir(SPLIT_PATH)

	x = np.load(os.path.join(POINTS_PATH, 'points_crop.npy'))
	y = pd.read_csv(os.path.join(POINTS_PATH, 'labels_crop.csv'), header=None).values
	train_test_split(x, y, 0.2, os.path.join(SPLIT_PATH, 'train_points.csv'), os.path.join(SPLIT_PATH, 'test_points.csv'))	

	x = np.load(os.path.join(POINTS_PATH, 'augment.npy'))
	y = pd.read_csv(os.path.join(POINTS_PATH, 'augment.csv'), header=None).values
	train_test_split(x, y, 0.2, os.path.join(SPLIT_PATH, 'train_augment.csv'), os.path.join(SPLIT_PATH, 'test_augment.csv'))

if __name__ == '__main__':
	main()
