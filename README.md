<html lang="en">
  <head>
    <title>Play Sounds with JavaScript</title>
    <meta charset="utf-8">
    <script src="sounds.js" type="text/javascript"></script>
    <link rel="stylesheet" type="text/css" href="style.css" />
  </head>
  <body>
    <h2>Try it out</h2>
    <ul>
      <li><a href="#" onclick="playSound('dead'); return false;">Dead</a></li>
      <li><a href="#" onclick="playSound('smash'); return false;">Smash</a></li>
      <li><a href="#" onclick="playSound('ping'); return false;">Ping</a></li>
      <li><a href="#" onclick="playSound('bump');">Bump</a></li>
      <li><a href="#" onclick="playSound('jump');">Jump</a></li>
      <li><a href="#" onclick="playSound('coin');">Coin</a></li>
    </ul>
  </body>
</html>

### Introduction

When the vtubers are streaming together, their voices sometimes get mixed. In this condition, it could be hard for the fansub members to figure out what the target vtuber is saying. So, we would like to propose a model that could filter the voices that come from different vtubers. In this way, the heavy burden of the fansub could get relieved. Thus, in this project, we come up with a model that could filter the mixed two vtuber voices. More vtubers will be taken into consideration in future work. Besides, we need more people to contribute to this project. Please feel free to contact me if you are willing to waste your time on these things :D

### Related work

The main idea of this model comes from the [Google paper](https://arxiv.org/abs/1810.04826). In this paper, the authors are able to filter a specific person's voice using the d-vector as an extra input. The PyTorch code of this paper exists [here](https://github.com/mindslab-ai/voicefilter.git). However, we found that their model does not really work for the Japanese vtubers. That is, the dataset they used is not suitable for our task. So, it becomes necessary for us to build the dataset from scratch and modify the model to pursue better performance.

### Process pipline

1. ### Data collection

   The code of this part could be found [here](https://colab.research.google.com/drive/1LYtwVfCYxlKUDYotXq-dauGZZ4aH-pix?usp=sharing).

   1. #### Data selection

      So, suppose we would like to filter the mixed voices from speakers A and B. To do this, we first need to obtain the audio that only contains A's voice and B's voice. Then, as presented in the voice filter paper, one could easily mix the two person's voices and build a synthesis dataset to train the model. Thus, at the very beginning, we need to select the data by ourselves. That is, we go to youtube and find the videos that meet the requirement above.

   2. #### Data download

      The youtube-dl is utilized here. We directly extract the opus format audio using the --extract-audio command provided by the youtube-dl.

   3. #### Audio signal processing

      Since the videos may contain background music, one should remove the bgm first. Fortunately, the [Spleeter model](https://github.com/deezer/spleeter.git) is ready to use, and it works well. The audios are then split and downsampled from 48000Hz to 8000Hz.

2. ### Build dataset

   The code of this part could be found [here](https://colab.research.google.com/drive/1m-UXb9fIFwFDEANQf3eBLFopsmFgbtSd?usp=sharing).

   1. #### Clip data

      We clip the data into 3-second slices this time.

   2. #### Data cleaning

      If a speaker does not speak longer than 1.5 seconds within an audio slice, we remove that. As it turns out, this data cleaning process is quite important for model performance.

   3. #### Data mixture and data augmentation

      For better performance, we perform the data augmentation here. That is, for each audio signal sequence, we first normalize it:

      ```python
      s1_target /= np.max(np.abs(s1_target))
      s2 /= np.max(np.abs(s2))
      ```

      Then, we multiply the two waves with two different ratios that are sampled from a uniform distribution. 

      ```python
      w1_ratio = np.random.uniform(low=0.05, high=1.2)
      w2_ratio = np.random.uniform(low=0.05, high=1.2)
      w1 = s1_target * w1_ratio
      w2 = s2 * w2_ratio
      ```

      After that, the two signals are added up and normalized again:

      ```python
      mixed = w1 + w2
      norm = np.max(np.abs(mixed)) * 1.1
      w1, w2, mixed = w1/norm, w2/norm, mixed/norm
      ```

      Additionally, we use the Short-time Fourier transform technique to transfer the audio signals to the frequency domain.

3. ### Model structure

   The code of this part could be found [here](https://colab.research.google.com/drive/17KOywcQpox86Ey5CMGkioN-f5xWUBpTz?usp=sharing). For the model input, we also need to specify the target speaker. In this condition, an embedding vector that specifies the speaker is utilized as an extra input. For more details of this model, please refer to the original paper and our modified code. Here is the model structure:

   <p>
    <img src="model (9).png"/>
   </p>

   Note that we mainly modify the original model structure in the following ways.

   1. Add another bidirectional LSTM to enhance the model ability
   2. The attention mechanism is implemented so that the model could focus on different parts of the CNN output when it generates the mask. (If you do not understand what the mask is, please read google's paper first!)
