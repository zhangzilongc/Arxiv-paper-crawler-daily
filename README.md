## Arxiv Interesting Papers Crawler
### Description: 
Customized personal paper downloading of the arxiv, 
the user can download papers they are interested in.

### The time range of the paper downloading: 
user can choose to download the interesting papers daily, in past week, 
in certain month of certain year (e.g. 2020.04). query_word: 'recent'(daily), 
'pastweek'(in past week), '2004'(2020.04).

### The mode of the downloading:
If user choose to download the interesting papers daily, the mode must be 'daily', otherwise, 
the mode must be 'all'. query_mode: 'all', 'daily'.

### The root of the downloading:
download_root_dir: e.g. '/Users/zhangzilong/Desktop/arxiv/' (Need to reset)

### The domain of the downloading:
domain: Computer Vision and Pattern Recognition 'cs.CV/', Machine learning 'cs.LG/' default: CV.

### The customized keywords:
The keywords in which the users are interested appears in the title of the paper. key_words: 'self-supervised', 'contrastive learning', 'anomaly detection', 
'novelty detection', 'representation learning', 'out-of-distribution'. (Need to reset)

### The customized keywords conference
The keywords conference appears in the comments of the committing paper. 
key_words_conference: 'ICLR', 'CVPR', 'ICML', 'ICCV'.

********
Usage: download the paper of interest daily, to run:
```
python3 main_arxiv.py
recent
daily
```
