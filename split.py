import numpy as np
import pandas as pd
from math import ceil


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
	# x = np.load('data/points/points32.npy')
	# y = pd.read_csv('data/labels/labels32.csv', header=None).values
	# train_test_split(x, y, 0.2, 'data/split/train32.csv', 'data/split/test32.csv')

	# x = np.load('data/points/points64.npy')
	# y = pd.read_csv('data/labels/labels64.csv', header=None).values
	# train_test_split(x, y, 0.2, 'data/split/train64.csv', 'data/split/test64.csv')

	# x = np.load('data/points/points128.npy')
	# y = pd.read_csv('data/labels/labels128.csv', header=None).values
	# train_test_split(x, y, 0.2, 'data/split/train128.csv', 'data/split/test128.csv')

	# x = np.load('data/points/points256.npy')
	# y = pd.read_csv('data/labels/labels256.csv', header=None).values
	# train_test_split(x, y, 0.2, 'data/split/train256.csv', 'data/split/test256.csv')

#	x = np.load('data/points/points0.npy')
#	y = pd.read_csv('data/labels/labels0.csv', header=None).values
#	train_test_split(x, y, 0.2, 'data/split/train0.csv', 'data/split/test0.csv')

	x = np.load('data/points/augment32.npy')
	y = pd.read_csv('data/labels/augment32.csv', header=None).values
	train_test_split(x, y, 0.2, 'data/split/train_augment32.csv', 'data/split/test_augment32.csv')	

if __name__ == '__main__':
	main()
