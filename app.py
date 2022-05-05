import streamlit as st
from janome.tokenizer import Tokenizer
from janome.analyzer import Analyzer
from janome.tokenfilter import *

import matplotlib.pyplot as plt
import japanize_matplotlib
import numpy as np
import pandas as pd
import collections
import itertools
from collections import Counter
import networkx as nx
from wordcloud import WordCloud

text = st.text_area(label='テキストを貼り付けてください', value='')

if len(text) > 0:

  # トークン化
  tokenizer = Tokenizer()
  stop_word_list = []
  noun_list = []

  for token in tokenizer.tokenize(text):
      split_token = token.part_of_speech.split(',')
      
      if (split_token[0] == '名詞') | (split_token[0] == '動詞'):

          if token.surface not in stop_word_list:
              noun_list.append(token.surface)

  # ワードクラウドの作成
  wordcloud = WordCloud(
      background_color='whitesmoke',  # 背景色
      font_path="font/ipaexg.ttf",  # ダウンロードしたフォントのパス
      width=500,  # 横幅
      height=500,  # 高さ
  )
  noun_space = ' '.join(noun_list)
  wordcloud.generate(noun_space)

  # 共起行列
  pair_list = list(itertools.combinations([n for n in noun_list if len(n) >= 2], 2))
  cnt_pairs = Counter(pair_list)
  tops = sorted(
      cnt_pairs.items(), 
      key=lambda x: x[1], reverse=True
      )[:50]

  # 重み付きデータの生成
  noun_1 = []
  noun_2 = []
  frequency = []

  # データフレームの作成
  for n,f in tops:
      noun_1.append(n[0])    
      noun_2.append(n[1])
      frequency.append(f)

  df_G = pd.DataFrame({'前出名詞': noun_1, '後出名詞': noun_2, '出現頻度': frequency})

  # 重み付きデータの設定
  weighted_edges = np.array(df_G)

  # グラフオブジェクトの生成
  G = nx.Graph()

  # 重み付きデータの読み込み
  G.add_weighted_edges_from(weighted_edges)


  # ワードクラウドとネットワーク図の表示
  # ネットワーク図の描画
  fig = plt.figure(figsize=(12, 20))
  plt.rcParams["font.size"] = 18

  plt.subplot(2, 1, 1)
  plt.title("ネットワーク図")
  nx.draw_networkx(G,
                  node_shape = "s",
                  node_color = "c", 
                  node_size = 200,
                  edge_color = "gray", 
                  font_family = "IPAexGothic"  #"ipaexg00401/ipaexg.ttf" # フォント指定
  );

  plt.subplot(2, 1, 2)
  plt.title("ワードクラウド")
  plt.axis('off')
  plt.imshow(wordcloud)

  plt.tight_layout()
  
  st.pyplot(fig)