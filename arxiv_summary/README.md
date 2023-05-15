# arxiv_summary

arxiv の論文を要約してSlackに投稿するボットです。


## 実行確認環境
- Ubuntu18.04
- Python==3.10

## Requirementsのインストール
```
$ pip install -r requiremens.txt
```

## 実行方法
1. `slack_bot.py`中にあるSLACK_SIGNING_SECRET, SLACK_BOT_TOKEN, SLACK_CHANNEL, OPENAI_API_KEYを設定してください。  
https://github.com/morikatron/snippet/blob/d7725dbfc21a203f0241feb0907d97c3808844c9/arxiv_summary/slack_bot.py#L34-L40  
2. 以下を実行してください。

```
$ python slack_bot.py
```

## 各種機能

### 自動投稿機能

毎日決まった論文数の要約を投稿します。

- 投稿日時
  毎日 8 時頃（API の limit の影響で時間はまばら）
- 要約される論文数
  3 (デフォルト時)
- 論文の種類
  ['cs.AI', 'cs.CL', 'cs.CV', 'cs.LG', 'stat.ML'] の中から選ばれます。
- `arxiv_summaries.tsv`に要約された論文情報が蓄積されていきます。そのため一度要約した論文は基本的に再度自動投稿はされません。

### URL で要約機能

arxiv の URL を入力するとその論文を要約してくれます。  
arxiv 以外の論文は今のところ対応していません。

### クエリによる論文検索&要約機能

探したい論文の文字列を入力するとそれをクエリとし、arxiv から候補論文を 3 つ探します。またその 3 つの論文を要約します。  
数分かかるので結果が出るまで少しお待ちください。  
入力例: マルチモーダルで感情推定をして、その結果から何を購入したいかを分析する

### 要約先の言語の選択機能
要約先の言語を設定できます。  
デフォルトは日本語になっていますが、英語のまま要約してほしければ英語で、中国語で要約してほしければ中国語で、という風に設定が出来ます。

### コメント機能

文頭に#(シャープ)を入れて投稿すれば、クエリのための入力とは認識されず、コメントとして認識されます。  
メモ書きなどに使ってください。

## 参考
- https://qiita.com/GleamingCake/items/e8c53fb0c1508ba1449e
- https://zenn.dev/ozushi/articles/ebe3f47bf50a86