# VAST-Vtuber-Augmented-Sound-Archive
voice dataset for VTB for neural network training.

⚠ This program is simply not well documented, and in progress. Please **wait**

### Dataset link <- ⚠ ️In progress!
[Here](https://drive.google.com/drive/folders/1fr6fs3Q3069oMHHr8NSmksOfVz-f9mp3?usp=sharing)

### Supported vtuber names

* 宝鐘マリン
* 白上フブキ
* 天音かなた
* 夏色まつり

### Task list
- [x] Select 16 suitable youtube video links for each vtuber 
- [x] Use [youtube-dl](https://github.com/ytdl-org/youtube-dl.git) to extract the audio information
- [x] Remove bgm using [spleeter](https://github.com/deezer/spleeter.git)
- [x] Perform a simple [vad](https://pypi.org/project/pyvad/)
- [x] train a [neural network](https://github.com/douglas125/SpeechCmdRecognition.git) to classify the speakers
- [ ] Add more vtubers to the dataset
- [ ] Try to use new models to split the overlapped voices (Which is challenging)