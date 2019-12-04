import numpy as np
import pandas as pd
import os
import sys

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.append(BASE_DIR)
sys.path.append(os.path.join(BASE_DIR, 'models'))
sys.path.append(os.path.join(BASE_DIR, 'utils'))
import provider
import tf_util
NUM_POINT = 32


def augment(i, cur_data, cur_label, cur_meta, points, labels, meta):
    # rotated_data = provider.rotate_point_cloud(np.expand_dims(cur_data[i], axis=0))
    jittered_data = provider.jitter_point_cloud(np.expand_dims(cur_data[i], axis=0))
    translated_data = provider.translate_point_cloud(jittered_data)
    points.append(np.squeeze(translated_data))
    labels.append(cur_label[i])
    meta.append(cur_meta[i])
    return points, labels, meta


def main():
    current_data = np.load('data/points/points{}.npy'.format(NUM_POINT))
    current_label = pd.read_csv('data/labels/labels{}.csv'.format(NUM_POINT), header=None).values
    current_meta = pd.read_csv('data/metadata/metadata{}.csv'.format(NUM_POINT), header=None).values
    # train = pd.read_csv('data/split/train32.csv', header=None).values

    # provider.load_csvs(NUM_POINT)
    # current_data, current_label = provider.train_split()
    print(current_data.shape)
    print(current_label.shape)
    print(current_meta.shape)
    # current_data, current_label, _ = provider.shuffle_data(current_data, np.squeeze(current_label))
    current_label = np.squeeze(current_label)
    print(current_label.shape)
    points = list(current_data)
    labels = list(current_label)
    meta = list(current_meta)

    # current_data = np.take(train)
    # current_label = np.take(train)

    for i, val in enumerate(current_data):
        print(len(current_label))

        if current_label[i] == 0:
            points, labels, meta = augment(i, current_data, current_label, current_meta, points, labels, meta)

        elif current_label[i] == 3:
            for j in range(0, 2):
                points, labels, meta = augment(i, current_data, current_label, current_meta, points, labels, meta)

        elif current_label[i] == 2:
            for j in range(0, 8):
                points, labels, meta = augment(i, current_data, current_label, current_meta, points, labels, meta)

        else:
            for j in range(0, 40):
                points, labels, meta = augment(i, current_data, current_label, current_meta, points, labels, meta)

    print(len(points))

    np.save('data/points/augment{}.npy'.format(NUM_POINT), np.reshape(points, (-1, NUM_POINT, 3)))
    pd.DataFrame(labels).to_csv('data/labels/augment{}.csv'.format(NUM_POINT), header=None, index=None)
    pd.DataFrame(meta).to_csv('data/metadata/augment{}.csv'.format(NUM_POINT), header=None, index=None)


if __name__ == '__main__':
    main()
