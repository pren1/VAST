# git clone https://github.com/pren1/VAST.git
# pip install spleeter-gpu
# pip install pyvad
# pip3 install --upgrade youtube-dl

from util import *
import os
name_dict = return_download_dict('file_name_dict.npy').tolist()
import pdb
import librosa

create_folders("audio")
for single_key in name_dict:
  create_folders(f"/audio/{single_key}/")
  file_list = name_dict[single_key]
  for single_file in file_list:
    print(single_file)
    os.system(f"youtube-dl --extract-audio -o '/audio/{single_key}/%(title)s.%(ext)s' {single_file}")
    pdb.set_trace()
#     os.system(f"youtube-dl --extract-audio -o /content/audio/白上吹雪/%(title)s.%(ext)s 'https://www.youtube.com/playlist?list=PL6sZ3uYmeG1vDQ-jvuaMA1hl3GvcHyMcp'")
#
# os.system("youtube-dl --get-filename -o '%(title)s.%(ext)s' https://www.youtube.com/watch?v=D4bjfOkb9GM&list=PLKo9UD3uKyyFxwwUwt3EBf5_ehCNic5tx")
#
# youtube-dl --extract-audio -o '%(title)s.%(ext)s' https://www.youtube.com/watch?v=D4bjfOkb9GM&list=PLKo9UD3uKyyFxwwUwt3EBf5_ehCNic5tx

import pprint
'rebuild dict according to the files in folder'
rebuilt_dict = {}
for single_key in name_dict:
  rebuilt_dict[single_key] = files_in_target_folder(f'/audio/{single_key}/')
# total_files = files_in_target_folder('/content/audio')
pprint.pprint(rebuilt_dict)

from spleeter.separator import Separator
from IPython.display import Audio
import IPython
import numpy as np
# Use audio loader explicitly for loading audio waveform:
from spleeter.audio.adapter import get_default_audio_adapter
import pdb
from tqdm import tqdm
import matplotlib.pyplot as plt
import numpy as np
from pyvad import vad, split
import soundfile as sf

sample_rate = 48000
window_size = 48000 * 1
padding_length = 48000

'five minutes'
stride_size = window_size*60*5

post_process_clip_threshold = 0.007
std_window_size = 960

separator = Separator('spleeter:2stems')
audio_loader = get_default_audio_adapter()

def generate_vocal_res(start_point, end_point, waveform):
  vocal_res = []
  # accompan_res = []
  for split_waveform_index in tqdm(range(start_point, end_point, window_size)):
    # Perform the separation :
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
    # prediction['accompaniment'] = prediction['accompaniment'][padding_length: -padding_length]
    'merge results together'
    vocal_res.extend(prediction['vocals'])
    # accompan_res.extend(prediction['accompaniment'])
  return vocal_res

def clip_one_second_data(seq_data, samplerate, resulted_rate = 8000):
  if len(seq_data) < samplerate:
    print("Insufficient length")
    return []
  'First, let us down sample'
  # y_16k = librosa.resample(seq_data, samplerate, resulted_rate)
  clipped_res = []
  'Then, clip it'
  for index in range(0, len(seq_data), resulted_rate):
    'make sure you get the 1 seconds clipped data'
    current_clip = seq_data[index:index + resulted_rate]
    if len(current_clip) == resulted_rate:
      if np.max(np.abs(current_clip)) > 0.02:
        clipped_res.append(current_clip)
  return clipped_res

def vad_merge(w):
    intervals = librosa.effects.split(w, top_db=20)
    temp = []
    for s, e in intervals:
        temp.append(w[s:e])
    return np.concatenate(temp, axis=None)
    # return counter

'Turn to Mono'
def save_vocal_res(vocal_res, output_audio_path, split_index, target_label):
  vocal_res = stereoToMono(np.asarray(vocal_res))
  vocal_res = np.clip(vocal_res, -1, 1)
  vocal_res = librosa.resample(vocal_res, sample_rate, 8000)
  vocal_res = vad_merge(vocal_res)

  # mode_2 = vad(vocal_res, fs=sample_rate, fs_vad=sample_rate, hop_length=10, vad_mode=1)
  # _dh, dur_info = interval_to_info(mode_2)
  splitted_voice = vocal_res
  data_res = clip_one_second_data(splitted_voice, sample_rate, 8000)
  label_res = [target_label] * len(data_res)
  # for info_index, single_info in enumerate(dur_info):
  #   if single_info[1] - single_info[0] > sample_rate:
  #     splitted_voice = vocal_res[single_info[0]:single_info[1]]
  #     clipped_data = clip_one_second_data(splitted_voice, sample_rate, 8000)
  #     corresponding_label = [target_label] * len(clipped_data)
  #     if len(clipped_data) > 0:
  #       data_res.append(clipped_data)
  #       label_res.extend(corresponding_label)
  # 'in the end, get data_res vstack'
  # data_res = np.vstack(data_res)
  assert len(data_res) == len(label_res)
  # IPython.display.display(IPython.display.Audio(np.asarray(data_res[5]).T, rate=8000))
  # pdb.set_trace()
  save_data_array_as_npy(data_res, output_audio_path + f'/data_{split_index}')
  save_data_array_as_npy(label_res, output_audio_path + f'/label_{split_index}')

def process_whole_seq_data(waveform, output_audio_path, target_label):
  five_minutes_numbers = int(len(waveform)/(stride_size))
  for i in range(2, five_minutes_numbers):
    start_point = i * stride_size
    end_point = (i + 1) * stride_size # Process 10 seconds data in total
    vocal_res = generate_vocal_res(start_point, end_point, waveform)
    save_vocal_res(vocal_res, output_audio_path, split_index = i, target_label = target_label)

vtb_list = [
"宝钟玛琳",
"天音彼方",
"白上吹雪",
"夏色祭"
]

vtb_audio = "gdrive/My Drive/Holo_VAST_New/"
for vtb_name in rebuilt_dict:
  create_folders(f"{vtb_audio}/{vtb_name}")
  file_list = rebuilt_dict[vtb_name]
  target_label = vtb_list.index(vtb_name)
  for name in file_list:
    print(f"processing: {vtb_name}/{name}")
    output_audio_path = f"{vtb_audio}/{vtb_name}/{name}/"
    create_folders(output_audio_path)
    input_audio_path = f'audio/{vtb_name}/{name}'
    'load file'
    waveform, _ = audio_loader.load(input_audio_path, sample_rate=sample_rate)
    'process target file'
    process_whole_seq_data(waveform, output_audio_path, target_label)