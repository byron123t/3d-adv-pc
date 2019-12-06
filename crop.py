import sys, cv2, time, os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.append(BASE_DIR)
KITTI_PATH = os.path.join(BASE_DIR, 'data/kitti_dataset/extracts')
LABEL_PATH = os.path.join(BASE_DIR, 'data/txt')
CROPS_PATH = os.path.join(BASE_DIR, 'data/crop')


def crop(path, image, x, y, w, h, file):
	val = 1
	delta = 5
	img = cv2.imread(image)

	if (img is not None) and (os.path.isfile(image)):
		height, width, c = img.shape
		x1 = int((x * width) - (w * width / 2))
		x2 = int((x * width) + (w * width / 2))
		y1 = int((y * height) - (h * height / 2))
		y2 = int((y * height) + (h * height / 2))
		crop_img = img[y1:y2, x1:x2,:]

		if crop_img is not None:
			print(y1, y2 + delta, x1, x2 + delta)
			print(crop_img.shape)
			crop_img2 = cv2.resize(crop_img, (32, 32))
			cv2.imwrite(os.path.join(path, file), crop_img2)

	else:
		print(image + ' is empty')


def main():
	if not os.path.exists(KITTI_PATH):
		print('Please run download_kitti.py to download the KITTI dataset first.')
		return
	if not os.path.exists(CROPS_PATH):
		os.mkdir(CROPS_PATH)

	for file in os.listdir(LABEL_PATH):
		if file.endswith('.txt'):
			# Path processing and splitting
			split = file.split('sync_')
			text1 = split[0]
			text2 = split[1]
			date = file.split('_drive_')[0]
			drive = text1 + 'sync'
			frame = text2.replace('txt', 'png').zfill(14)
			num = text2.replace('txt', 'png')

			with open(os.path.join(LABEL_PATH, file), 'r') as infile:
				# Extracting each sign's shape label and bounding box
				lines = infile.readlines()
				count = 0

				for line in lines:
					line = line.strip('\n')
					split1 = line.split(' ')
					x = float(split1[1])
					y = float(split1[2])
					w = float(split1[3])
					h = float(split1[4])

					if count >= 1:
						file_name = drive + '_' + str(count) + '_' + num
						crop(CROPS_PATH, os.path.join(KITTI_PATH, date, drive, 'image_02/data', frame), x, y, w, h, file_name)
					else:
						file_name = file.replace('txt', 'png')
						crop(CROPS_PATH, os.path.join(KITTI_PATH, date, drive, 'image_02/data', frame), x, y, w, h, file_name)
						
					count += 1


if __name__ == '__main__':
	main()
