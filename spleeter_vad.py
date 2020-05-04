from spleeter.separator import Separator
# Use audio loader explicitly for loading audio waveform :
from spleeter.audio.adapter import get_default_audio_adapter
import pdb
from tqdm import tqdm
import matplotlib.pyplot as plt
import sounddevice as sd
import numpy as np
from pyvad import vad, split

audio_path = 'audio/test.m4a'
# Using embedded configuration.
separator = Separator('spleeter:2stems')
audio_loader = get_default_audio_adapter()
sample_rate = 48000
window_size = 48000 * 1
padding_length = 48000

waveform, _ = audio_loader.load(audio_path, sample_rate=sample_rate)

def stereoToMono(audiodata):
	return np.array(audiodata[:, 0] / 2 + audiodata[:, 1] / 2)

def visualize_results(accompaniment, padding_length):
	plt.plot(accompaniment, color='c', label='data with padding')
	plt.plot(np.arange(padding_length, len(accompaniment) - padding_length),
	         accompaniment[padding_length:-padding_length], color='r', label='clipped data')
	plt.legend()
	plt.show()

vocal_res = []
accompan_res = []

for split_waveform_index in tqdm(range(0, window_size*60, window_size)):
	# Perform the separation :
	print(f"{split_waveform_index}/{len(waveform)}")
	print(waveform[split_waveform_index:min(split_waveform_index + window_size, len(waveform))].shape)
	clipped_waveform = waveform[split_waveform_index:min(split_waveform_index + window_size, len(waveform))]
	'add padding zeros to each waveform'
	zero_padded_waveform = np.zeros((clipped_waveform.shape[0] + padding_length*2, clipped_waveform.shape[1]))
	zero_padded_waveform[padding_length:-padding_length] = clipped_waveform
	'we may also use the extra data'
	if split_waveform_index-padding_length >= 0 and split_waveform_index + window_size + padding_length < len(waveform):
		zero_padded_waveform[:padding_length] = waveform[split_waveform_index-padding_length:split_waveform_index]
		zero_padded_waveform[-padding_length:] = waveform[split_waveform_index + window_size: split_waveform_index + window_size + padding_length]

	'sperate using spleeter'
	prediction = separator.separate(zero_padded_waveform)
	'clip padded part, throw them away'
	prediction['vocals'] = prediction['vocals'][padding_length: -padding_length]
	prediction['accompaniment'] = prediction['accompaniment'][padding_length: -padding_length]
	'merge results together'
	vocal_res.extend(prediction['vocals'])
	accompan_res.extend(prediction['accompaniment'])

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

from spleeter_test import sep
dur_info = sep(np.asarray(vocal_res))
dur_info = [[x[0] * 48, x[1] * 48] for x in dur_info]

vocal_res = stereoToMono(np.asarray(vocal_res))
result_interval = np.zeros((int(len(vocal_res))))

for result in dur_info:
	result_interval[result[0]: result[1]] = 1

plt.plot(result_interval)
plt.plot(vocal_res)
plt.show()

#
# mode_3 = vad(vocal_res, fs=48000, fs_vad=48000, hop_length=10, vad_mode=3)
# bet_info, dur_info = interval_to_info(mode_3)

for single_info in dur_info:
	splitted_voice = vocal_res[single_info[0]:single_info[1]]
	sd.play(splitted_voice)
	plt.plot(splitted_voice, color = 'c', label='Has vocal voice')
	plt.legend()
	plt.show()

# for single_info in bet_info:
# 	splitted_voice = vocal_res[single_info[0]:single_info[1]]
# 	sd.play(splitted_voice)
# 	plt.plot(splitted_voice, color = 'c', label='No vocal voice')
# 	plt.legend()
# 	plt.show()

pdb.set_trace()
sd.play(vocal_res)
sd.play(accompan_res)
visualize_results(accompan_res,padding_length)