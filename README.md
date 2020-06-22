### Demo

你可以在[这里](https://pren1.github.io/VAST/)找到demo和文档

### 介绍

Vtuber 联动时声音会混在一起，而这会对字幕组的工作造成困难。为了解决这个问题，我们提出了一个可以分离不同vtuber声音的模型。目前模型可以分离白上吹雪和夏色祭混合起来的声音，多个Vtuber的声音混合问题将会在下一步解决。顺便，诚招愿意在本项目上浪费时间的人。

### 相关工作

本模型来源于谷歌的[这篇](https://pren1.github.io/VAST/)论文。该论文提供了相关的Pytorch[代码](https://github.com/mindslab-ai/voicefilter.git)。然而，因为数据库等等原因，我们发现该模型并不能直接用于Vtuber语音分离。因此，本项目从头对数据库进行了建立，并且对模型进行了优化更改。

### 项目流程

1. #### 数据收集

   可以在[这里](https://colab.research.google.com/drive/1LYtwVfCYxlKUDYotXq-dauGZZ4aH-pix?usp=sharing)找到相关代码.

   1. ##### 数据选择

      假设说话人A和B的声音混了起来，而我们要对他们的声音进行分离。首先，我们要获取只包含说话人A或说话人B的音轨。然后，如同谷歌的论文所指导，两种音轨将会被混合以用于训练。因此，我们需要首先人工选取音轨。在本项目中，音轨选自Vtuber的youtube相关频道。

   2. ##### 数据下载

      本项目应用youtube-dl进行下载。利用 --extract-audio 选项，我们可以直接从视频中提取opus格式的音频。

   3. ##### 语音信号处理

      因为音频可能会包含背景音乐，本项目使用现成的Spleeter模型进行背景音乐分离。之后，48000Hz的音频被降采样到8000Hz。

2. #### 数据库构建

   可以在[这里](https://colab.research.google.com/drive/1m-UXb9fIFwFDEANQf3eBLFopsmFgbtSd?usp=sharing)找到相关代码.

   1. ##### 数据分割

      数据被切成三秒长的小段。

   2. ##### 数据清洗

      如果一小段语音中有一半时间没人说话，则舍弃之。从结果而言，这部分对模型表现非常重要。

   3. ##### 数据混合与数据增强

      首先，来自两个人的数据信号被归一化：

      ```python
      s1_target /= np.max(np.abs(s1_target))
      s2 /= np.max(np.abs(s2))
      ```

      然后，每条数据信号都按比例缩放。缩放比例来自一个连续型均匀分布。

      ```python
      w1_ratio = np.random.uniform(low=0.05, high=1.2)
      w2_ratio = np.random.uniform(low=0.05, high=1.2)
      w1 = s1_target * w1_ratio
      w2 = s2 * w2_ratio
      ```

      之后，来自不同vtuber的数据信号被相加，并且进一步归一化：

      ```python
      mixed = w1 + w2
      norm = np.max(np.abs(mixed)) * 1.1
      w1, w2, mixed = w1/norm, w2/norm, mixed/norm
      ```

      再然后，运用短时傅里叶变换将音频信号转入频域。

3. #### 模型结构

   这部分的相关代码可以在[这里](https://colab.research.google.com/drive/17KOywcQpox86Ey5CMGkioN-f5xWUBpTz?usp=sharing)找到。需要注意的是，模型的输入中包含了一个代表说话人的映射向量。输入的说话人映射向量不同，模型分离出的说话人也将不同。如果想要得知更多的细节，请参照原论文以及我们修改过的模型代码。这是模型结构图：

   <p>
    <img src="docs/model (9).png"/>
   </p>
   我们主要对原始模型做了以下更改：

   1. 增加了一个双向长短期记忆层。
   2. 应用了注意力机制。当模型产生遮罩时，它可以对卷积神经网络的输出分配不同的权重。（如果你看不懂这里的遮罩是什么，那证明你需要先去阅读谷歌的论文）