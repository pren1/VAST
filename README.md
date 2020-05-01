# VAST-Vtuber-Augmented-Sound-Archive
voice dataset for VTB for neural network training. IN PROGRESS

### Raw data Google drive link
Unavailable currently

### Video download
from: https://www.findyoutube.net/result

### Raw data list
This list explains the details of each raw data

| 名称      | vtb     | 可用程度     | 噪音情况 | 需要校正|
| ---------- | :-----------:  | :-----------: | :-----------: | :-----------: |
| [【PC版-PUBG参加者募集！】初！PUBGプレイをフブキちゃんとリスナーに捧ぐ](https://www.youtube.com/watch?v=-FByG6gkiHU)     | aki/fubuki     | 可用   | 无噪声 | 无需校正 | 
| [青鬼【検証】ホラー耐性と辛さ耐性ゼロが一度に摂取したら大丈夫説【バイノーラルホラゲ実況】](https://www.youtube.com/watch?v=Lq7OSuc8MoQ) | aki  | 可用 | 有bgm | 可不校正 |
| [【#塩がゆ】あるようでなかった雑談配信【ホロライブ_猫又おかゆと紫咲シオン】]( https://www.youtube.com/watch?v=NLDLd8u3Vss&t=54s) | 猫又/紫咲  | 可用 | 有bgm | 可不校正 |
| [(已复查)已校实轴【歌枠】僕は歌うのさ【Vtuber】](https://www.youtube.com/watch?v=AtTkFe6C3tA) | 猫又  | 可用 | 有bgm | 可以不校正 |
| [【空轴】デビュー配信から1ヶ月経ったみたい！](https://www.youtube.com/watch?v=vQzkm8CO37A) | 猫又  | 可用 | 有bgm | bgm处需要校正 |
| [【空轴】【マリオカート】可愛い声縛り！7位以下で即終了！【ホロライブ_猫又おかゆ】](https://www.youtube.com/watch?v=AXwr1Nyzq-k) | 猫又  | 不可用 | 有bgm | 重新打吧 |
| [【収益化記念】おにぎりあげる！【猫又おかゆ】](https://www.youtube.com/watch?v=HVqGLGm8StI) | 猫又  | 不可用 | 有bgm | 重新打吧 |
| [【雑談】前髪は伸びる【猫又おかゆ】](https://www.youtube.com/watch?v=U4i5vAKCY3A) | 猫又  | 不可用 | 有bgm | 重新打吧 |
| [【Vtuber】5分で分かる猫又おかゆ【公式】](https://www.youtube.com/watch?v=YAKJvA1ZZAU) | 猫又  | 不可用 | 有bgm | 很短，用作打轴man体验例子吧 |
| [【Vtuber】大きなバックパックがある生活＃2【Stardew Valley】-B8sNGHFq1NY](https://www.youtube.com/watch?v=B8sNGHFq1NY) | 猫又  | 可用 | 有bgm | 可校正 |
| [卡比p3【Vtuber】これがお望みのフルパワーだ【星のカービィ 夢の泉の物語】](https://www.youtube.com/watch?v=j9RuPurJDFE) | 猫又  | 可用 | 有bgm | 可校正 |
| [【Vtuber】僕の暮らし＃1【Stardew Valley】](https://www.youtube.com/watch?v=qIm_XZo9_pw) | 猫又  | 不可用 | 有bgm | 重新打吧 |
| [（已校）【Vtuber】バーチャルメイド、歌います！](https://www.youtube.com/watch?v=GdUkBdLi-as) | aqua  | 可用 | 有bgm | 可不校正 【前段缺失】 |
| [【悲報】不健康メイド、野菜ジュースに追われる【Overcooked】](https://www.youtube.com/watch?v=HGaHDR_n_wE) | aqua  | 可用 | 有bgm |  youtube 源有问题|
| [【脳トレ】IQ3の天才児が脳を鍛えてみた結果](https://www.youtube.com/watch?v=PrLLinsseM0) | aqua  | 不可用 | 无bgm | 重新打吧 |
| []() | -----------  | ----------- | ----------- | ----------- |
| []() | -----------  | ----------- | ----------- | ----------- |
| []() | -----------  | ----------- | ----------- | ----------- |
| []() | -----------  | ----------- | ----------- | ----------- |
| []() | -----------  | ----------- | ----------- | ----------- |
| []() | -----------  | ----------- | ----------- | ----------- |
| []() | -----------  | ----------- | ----------- | ----------- |
| []() | -----------  | ----------- | ----------- | ----------- |
| []() | -----------  | ----------- | ----------- | ----------- |
| []() | -----------  | ----------- | ----------- | ----------- |
| []() | -----------  | ----------- | ----------- | ----------- |


### Process pipline
1. Download all the files --> In progress
2. Rectify the vad label
3. Extract audio information
4. Clip the audio according to the vad label
5. Try to remove bgm using spleeter