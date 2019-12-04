import os, wget, zipfile


PATH = './data/kitti_dataset/'
EXTRACTS = os.path.join(path, 'extracts/')
TEMP = os.path.join(path, 'temp_downloads/')
BASE = 'https://s3.eu-central-1.amazonaws.com/avg-kitti/raw_data/'



# A download script for the KITTI dataset. Not all drives are included in the files array.
def download(files):
	for i in files:
		will_download = True
		will_extract = True

		for j in os.listdir(TEMP):
			if i in j:
				will_download = False
				file = os.path.join(TEMP, j)
				break

		for j in os.listdir(EXTRACTS):
			for k in os.listdir(os.path.join(EXTRACTS, j)):
				if i in k:
					will_extract = False
					file = os.path.join(TEMP, j)
					break

		if will_download:
			url = BASE + i + '/' + i + '_sync.zip'
			print('Downloading: {}'.format(url))
			file = wget.download(url, os.path.join(TEMP, i, '_sync.zip'))
		else:
			print('{} already downloaded'.format(os.path.join(TEMP, i, '_sync.zip')))
			file = os.path.join(TEMP, i, '_sync.zip')

		if will_extract:
			print('Extracting: {}'.format(file))
			zip_ref = zipfile.ZipFile(file)
			zip_ref.extractall(EXTRACTS)
			zip_ref.close()
		else:
			print('{} already extracted'.format(file))


def main():
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
