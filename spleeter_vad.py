from spleeter.separator import Separator
# Use audio loader explicitly for loading audio waveform :
from spleeter.audio.adapter import get_default_audio_adapter
import pdb
from tqdm import tqdm
import matplotlib.pyplot as plt
import sounddevice as sd
import numpy as np
import noisereduce as nr

audio_path = 'audio/test.m4a'
# Using embedded configuration.
separator = Separator('spleeter:2stems')
audio_loader = get_default_audio_adapter()
sample_rate = 44100
waveform, _ = audio_loader.load(audio_path, sample_rate=sample_rate)
window_size = 44100 * 1
padding_length = 44100

def stereoToMono(audiodata):
	return np.array(audiodata[:, 0] / 2 + audiodata[:, 1] / 2, dtype='int16')

def visualize_results(accompaniment, padding_length):
	plt.plot(accompaniment, color='c', label='data with padding')
	plt.plot(np.arange(padding_length, len(accompaniment) - padding_length),
	         accompaniment[padding_length:-padding_length], color='r', label='clipped data')
	plt.legend()
	plt.show()
vocal_res = []
accompan_res = []

for split_waveform_index in tqdm(range(0, window_size*10, window_size)):
	# Perform the separation :
	print(f"{split_waveform_index}/{len(waveform)}")
	print(waveform[split_waveform_index:min(split_waveform_index + window_size, len(waveform))].shape)
	clipped_waveform = waveform[split_waveform_index:min(split_waveform_index + window_size, len(waveform))]
	'add padding zeros to each waveform'
	zero_padded_waveform = np.zeros((clipped_waveform.shape[0] + padding_length*2, clipped_waveform.shape[1]))
	zero_padded_waveform[padding_length:-padding_length] = clipped_waveform
	prediction = separator.separate(zero_padded_waveform)
	'clip'
	prediction['vocals'] = prediction['vocals'][padding_length: -padding_length]
	prediction['accompaniment'] = prediction['accompaniment'][padding_length: -padding_length]

	vocal_res.extend(prediction['vocals'])
	accompan_res.extend(prediction['accompaniment'])
	# sd.play(prediction['vocals'][padding_length: -padding_length])
	# visualize_results(prediction['vocals'],padding_length)
	# pdb.set_trace()
	# sd.play(prediction['accompaniment'][padding_length: -padding_length])
	# visualize_results(prediction['accompaniment'], padding_length)

pdb.set_trace()
sd.play(vocal_res)
sd.play(accompan_res)
visualize_results(vocal_res,padding_length)