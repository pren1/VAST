import os
import numpy as np
import pdb

def files_in_target_folder(path, extension=".opus"):
	# obtain all file paths in the target folder
	res_files=[]
	for file in os.listdir(path):
		if file.endswith(extension):
			res_files.append(file)
	return res_files

def get_all_sub_folders(path):
	first_level_folders = [x[0] for x in os.walk(path)]
	for first in first_level_folders:
		second_level_folders = [f"{first}/" + x[0] for x in os.walk(first)]
	return second_level_folders

def stereoToMono(audiodata):
	'turn 2d array to 1d'
	return np.array(audiodata[:, 0] / 2 + audiodata[:, 1] / 2)

def interval_to_info(interval_seq):
	res = []
	start = 0
	in_interval = False
	for (index, label) in zip(range(len(interval_seq)), interval_seq):
		if label >= 1 and not in_interval:
			res.append(np.asarray([start, index]))
			in_interval = True
		if label == 0 and in_interval:
			start = index
			in_interval = False
	if not in_interval:
		res.append(np.asarray([start, len(interval_seq)]))
	return np.asarray(res), Dur_info(np.asarray(res), len(interval_seq))

def Dur_info(current_interval_info, whole_length):
	during_turn_interval = []
	for index in range(len(current_interval_info)):
		if index == 0:
			continue
		if current_interval_info[index][0] == current_interval_info[index][1]:
			continue
		during_turn_interval.append(np.asarray([current_interval_info[index-1][1], current_interval_info[index][0]]))
	if current_interval_info[-1][1] != whole_length:
		'In case it ends with an interval'
		during_turn_interval.append(np.asarray([current_interval_info[-1][1], whole_length]))
	return during_turn_interval

def rolling_window(array, window):
	'Obtain the stddev of the array'
	half_window_size = window//2
	res = []
	for index in range(len(array)):
		current_slice = array[max(index - half_window_size, 0):min(index + half_window_size, len(array))]
		res.append(np.std(current_slice))
	return np.asarray(res)

def front_clip(array, threshold):
	'clip std array from front'
	for i in range(len(array)):
		if array[i] < threshold:
			pass
		else:
			return True, i
	return False, -1

def end_clip(array, threshold):
	'clip std array from end'
	for i in range(len(array)):
		if array[~i] < threshold:
			pass
		else:
			return True, i
	return False, -1

def create_folders(directory):
	if not os.path.exists(directory):
		os.makedirs(directory)

def save_data_array_as_npy(input_array, file_name):
	np.save(file_name, input_array)

def load_data_array_from_npy(file_name):
	return np.load(file_name, allow_pickle=True)

def return_download_dict(read_in_name = "file_name_dict.npy"):
	return load_data_array_from_npy(read_in_name)