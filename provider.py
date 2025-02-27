import os
import sys
import csv
import numpy as np
import h5py
import pandas as pd
import random
from sklearn.model_selection import train_test_split

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.append(BASE_DIR)

# Download dataset for point cloud classification
DATA_DIR = os.path.join(BASE_DIR, 'data')
SPLIT_DIR = os.path.join(DATA_DIR, 'split')
POINT_DIR = os.path.join(DATA_DIR, 'points')
if not os.path.exists(DATA_DIR):
    os.mkdir(DATA_DIR)
# if not os.path.exists(os.path.join(DATA_DIR, 'modelnet40_ply_hdf5_2048')):
#     www = 'https://shapenet.cs.stanford.edu/media/modelnet40_ply_hdf5_2048.zip'
#     zipfile = os.path.basename(www)
#     os.system('wget %s; unzip %s' % (www, zipfile))
#     os.system('mv %s %s' % (zipfile[:-4], DATA_DIR))
#     os.system('rm %s' % (zipfile))


def shuffle_data(data, labels):
    """ Shuffle data and labels.
        Input:
          data: B,N,... numpy array
          label: B,... numpy array
        Return:
          shuffled data, label and shuffle indices
    """
    idx = np.arange(len(labels))
    np.random.shuffle(idx)
    return data[idx, ...], labels[idx], idx


def rotate_point_cloud(batch_data):
    """ Randomly rotate the point clouds to augument the dataset
        rotation is per shape based along up direction
        Input:
          BxNx3 array, original batch of point clouds
        Return:
          BxNx3 array, rotated batch of point clouds
    """
    rotated_data = np.zeros(batch_data.shape, dtype=np.float32)
    for k in range(batch_data.shape[0]):
        rotation_angle = np.random.uniform() * 2 * np.pi
        cosval = np.cos(rotation_angle)
        sinval = np.sin(rotation_angle)
        rotation_matrix = np.array([[cosval, 0, sinval],
                                    [0, 1, 0],
                                    [-sinval, 0, cosval]])
        shape_pc = batch_data[k, ...]
        rotated_data[k, ...] = np.dot(shape_pc.reshape((-1, 3)), rotation_matrix)
    return rotated_data


def translate_point_cloud(batch_data):
    """ Randomly rotate the point clouds to augument the dataset
        rotation is per shape based along up direction
        Input:
          BxNx3 array, original batch of point clouds
        Return:
          BxNx3 array, rotated batch of point clouds
    """
    negative = random.random()
    neg = 1
    if negative > 0.5:
        neg = -1
    translation = random.random() * random.randint(1, 5) * neg
    batch_data += translation

    return batch_data
    


def rotate_point_cloud_by_angle(batch_data, rotation_angle):
    """ Rotate the point cloud along up direction with certain angle.
        Input:
          BxNx3 array, original batch of point clouds
        Return:
          BxNx3 array, rotated batch of point clouds
    """
    rotated_data = np.zeros(batch_data.shape, dtype=np.float32)
    for k in range(batch_data.shape[0]):
        #rotation_angle = np.random.uniform() * 2 * np.pi
        cosval = np.cos(rotation_angle)
        sinval = np.sin(rotation_angle)
        rotation_matrix = np.array([[cosval, 0, sinval],
                                    [0, 1, 0],
                                    [-sinval, 0, cosval]])
        shape_pc = batch_data[k, ...]
        rotated_data[k, ...] = np.dot(shape_pc.reshape((-1, 3)), rotation_matrix)
    return rotated_data


def jitter_point_cloud(batch_data, sigma=0.01, clip=0.05):
    """ Randomly jitter points. jittering is per point.
        Input:
          BxNx3 array, original batch of point clouds
        Return:
          BxNx3 array, jittered batch of point clouds
    """
    B, N, C = batch_data.shape
    assert(clip > 0)
    jittered_data = np.clip(sigma * np.random.randn(B, N, C), -1*clip, clip)
    jittered_data += batch_data
    return jittered_data

def getDataFiles(list_filename):
    return [line.rstrip() for line in open(list_filename)]

def load_h5(h5_filename):
    f = h5py.File(h5_filename)
    data = f['data'][:]
    label = f['label'][:]
    return (data, label)

def loadDataFile(filename):
    return load_h5(filename)

def load_h5_data_label_seg(h5_filename):
    f = h5py.File(h5_filename)
    data = f['data'][:]
    label = f['label'][:]
    seg = f['pid'][:]
    return (data, label, seg)


def loadDataFile_with_seg(filename):
    return load_h5_data_label_seg(filename)


def load_csvs(num_points, augment):
    if not os.path.exists(POINT_DIR):
        print('Please run pc_crop.py to crop point clouds first.')
        return
    if not os.path.exists(SPLIT_DIR):
        print('Please run split.py to split into training and testing set first.')
        return

    global X_TRAIN
    global X_TEST
    global Y_TRAIN
    global Y_TEST

    train = []
    test = []

    if augment:
        x = np.load(os.path.join(POINT_DIR, 'augment.npy'))
        y = pd.read_csv(os.path.join(POINT_DIR, 'augment.csv'), header=None).values
        raw_train = pd.read_csv(os.path.join(SPLIT_DIR, 'train_augment.csv'), header=None).values
        raw_test = pd.read_csv(os.path.join(SPLIT_DIR, 'test_augment.csv'), header=None).values
    else:
        x = np.load(os.path.join(POINT_DIR, 'points_crop.npy'))
        y = pd.read_csv(os.path.join(POINT_DIR, 'labels_crop.csv'), header=None).values
        raw_train = pd.read_csv(os.path.join(SPLIT_DIR, 'train_points.csv'), header=None).values
        raw_test = pd.read_csv(os.path.join(SPLIT_DIR, 'test_points.csv'), header=None).values

    for i, val in enumerate(raw_train):
        train.append(val[0])

    for i, val in enumerate(raw_test):
        test.append(val[0])

    X_TRAIN = np.take(x, train, axis=0)
    X_TEST = np.take(x, test, axis=0)
    Y_TRAIN = np.take(y, train, axis=0)
    Y_TEST = np.take(y, test, axis=0)


def train_split():
    return X_TRAIN, Y_TRAIN


def test_split():
    return X_TEST, Y_TEST
