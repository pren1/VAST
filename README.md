# V_Voice
voice dataset for VTB for neural network training. IN PROGRESS

### Raw data Google drive link
Unavailable currently

### Video download
from: https://www.findyoutube.net/result

### Raw data list
This list explains the details of each raw data

| 名称      | vtb     | 可用程度     | 噪音情况 | 需要校正|
| ---------- | :-----------:  | :-----------: | :-----------: | :-----------: |
| 【PC版-PUBG参加者募集！】初！PUBGプレイをフブキちゃんとリスナーに捧ぐ     | aki/fubuki     | 可用   | 无噪声 | 无需校正 | 
| 青鬼【検証】ホラー耐性と辛さ耐性ゼロが一度に摂取したら大丈夫説【バイノーラルホラゲ実況】 | aki  | 可用 | 有bgm | 可不校正 |
| ---------- | -----------  | ----------- | ----------- | ----------- |

### Process pipline
1. Download all the files --> In progress
2. Rectify the vad label
3. Extract audio information
4. Clip the audio according to the vad label
5. Try to remove bgm using spleeter