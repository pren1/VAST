import csv
import numpy as np
import pdb
from util import save_data_array_as_npy
import pandas as pd

def read_target_csv(path_to_csv):
	# read in target csv, and return azimuth data and original labels in azimuth files
	if not path_to_csv.endswith('.csv'):
		assert(1==0), path_to_csv + " extension is not csv"
	with open(path_to_csv, "r") as csvfile:
		reader = csv.reader(csvfile)
		#[1] azimuth angle here, we discard the time since we know the frequency is 25 HZ
		dataset = [row[0] for row in reader]
	return np.asarray(dataset)

target_path = "target_link.csv"
df = pd.read_csv(target_path, header=None)

aug_df = pd.read_csv("aug_target_link.csv", header=None)
aug_output_dict = {}

output_dict = {}
for index in range(len(df)):
	line = df.loc[index]
	output_dict[line[0]] = line[1:].tolist()

	aug_line = aug_df.loc[index]
	if index == 0:
		aug_output_dict[line[0]] = aug_line[1:].tolist()
	else:
		aug_output_dict[line[0]] = aug_line[1:-1].tolist()

save_data_array_as_npy(aug_output_dict, "aug_multiple_name_dict")

# output_dict = {'宝鐘マリン': [],
#                '白上フブキ': [],
#                '天音かなた': [],
#                '夏色まつり': []}
#
# output_dict = {'白上フブキ': [],
#                '夏色まつり': []}
#
# root_path = 'Name_CSV/'
#
# for key in output_dict:
# 	path = root_path + key + ".csv"
# 	result = read_target_csv(path)
# 	output_dict[key] = result
#
# save_data_array_as_npy(output_dict, "file_name_dict")

