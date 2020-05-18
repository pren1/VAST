import csv
import numpy as np
import pdb
from util import save_data_array_as_npy


def read_target_csv(path_to_csv):
	# read in target csv, and return azimuth data and original labels in azimuth files
	if not path_to_csv.endswith('.csv'):
		assert(1==0), path_to_csv + " extension is not csv"
	with open(path_to_csv, "r") as csvfile:
		reader = csv.reader(csvfile)
		#[1] azimuth angle here, we discard the time since we know the frequency is 25 HZ
		dataset = [row[0] for row in reader]
	return np.asarray(dataset)

output_dict = {'宝鐘マリン': [],
               '白上フブキ': [],
               '天音かなた': [],
               '夏色まつり': []}

# output_dict = {'白上フブキ': []}

root_path = 'Name_CSV/'

for key in output_dict:
	path = root_path + key + ".csv"
	result = read_target_csv(path)
	output_dict[key] = result

save_data_array_as_npy(output_dict, "file_name_dict")

