Morikatron Engineer Blog の記事 「[英語をカタカナ表記に変換してみる](https://tech.morikatron.ai/entry/2020/05/25/100000)」のサンプルコードです。  
詳しくはブログ記事を参照ください。  
  
プログラムの実行にあたっては  
http://svn.code.sf.net/p/cmusphinx/code/trunk/cmudict/cmudict-0.7b  
http://svn.code.sf.net/p/cmusphinx/code/trunk/cmudict/scripts/make_baseform.pl  
上記の2つのファイルを本プログラムと同一ディレクトリにダウンロードして、  
以下のコマンドを実行してください。  
perl make_baseform.pl cmudict-0.7b cmudict-0.7b_baseform  
これにより作成されるファイル　cmudict-0.7b_baseform　を本プログラムで読み込んで利用します。  

# ファイルリスト

* [english_to_kana.py](english_to_kana.py)
  * 英語をカタカナ表記に変換するプログラム（Python 3.4以降）
