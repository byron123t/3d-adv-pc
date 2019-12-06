import os, wget, zipfile, sys

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.append(BASE_DIR)
DATA_PATH = os.path.join(BASE_DIR, 'data')
PATH = os.path.join(DATA_PATH, 'kitti_dataset')
EXTRACTS = os.path.join(PATH, 'extracts')
TEMP = os.path.join(PATH, 'temp_downloads')
BASE = 'https://s3.eu-central-1.amazonaws.com/avg-kitti/raw_data/'


# A download script for the KITTI dataset. Not all drives are included in the files array.
def download(files):
	for i in files:
		will_download = True
		will_extract = True
		file_path = os.path.join(TEMP, i + '_sync.zip')

		for j in os.listdir(TEMP):
			if i in j:
				will_download = False
				break

		for j in os.listdir(EXTRACTS):
			for k in os.listdir(os.path.join(EXTRACTS, j)):
				if i in k:
					will_extract = False
					break

		if will_download:
			url = BASE + i + '/' + i + '_sync.zip'
			print('Downloading: {}'.format(url))
			wget.download(url, file_path)
		else:
			print('{} already downloaded'.format(file_path))

		if will_extract:
			print('\nExtracting: {}'.format(file_path))
			zip_ref = zipfile.ZipFile(file_path)
			zip_ref.extractall(EXTRACTS)
			zip_ref.close()
		else:
			print('{} already extracted'.format(file_path))


def main():
	if not os.path.exists(DATA_PATH):
		os.mkdir(DATA_PATH)
	if not os.path.exists(PATH):
		os.mkdir(PATH)
	if not os.path.exists(EXTRACTS):
		os.mkdir(EXTRACTS)
	if not os.path.exists(TEMP):
		os.mkdir(TEMP)

	files = ['2011_09_26_drive_0019','2011_09_26_drive_0020','2011_09_26_drive_0022',
	'2011_09_26_drive_0023','2011_09_26_drive_0035','2011_09_26_drive_0036','2011_09_26_drive_0039',
	'2011_09_26_drive_0046','2011_09_26_drive_0061','2011_09_26_drive_0064','2011_09_26_drive_0079',
	'2011_09_26_drive_0086','2011_09_26_drive_0087','2011_09_30_drive_0018','2011_09_30_drive_0020',
	'2011_09_30_drive_0027','2011_09_30_drive_0028','2011_09_30_drive_0033','2011_09_30_drive_0034',
	'2011_10_03_drive_0027','2011_10_03_drive_0034','2011_09_26_drive_0015','2011_09_26_drive_0027',
	'2011_09_26_drive_0028','2011_09_26_drive_0029','2011_09_26_drive_0032','2011_09_26_drive_0052',
	'2011_09_26_drive_0070','2011_09_26_drive_0101','2011_09_29_drive_0004','2011_09_30_drive_0016',
	'2011_10_03_drive_0042','2011_10_03_drive_0047','2011_09_28_drive_0016','2011_09_28_drive_0021',
	'2011_09_28_drive_0034','2011_09_28_drive_0035','2011_09_28_drive_0037','2011_09_28_drive_0038',
	'2011_09_28_drive_0043','2011_09_28_drive_0045','2011_09_28_drive_0047']

	download(files)


if __name__ == '__main__':
	main()
