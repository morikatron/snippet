Morikatron Engineer Blog の記事 「自動微分+XLA付き機械学習フレームワークJAXを使用してMNISTを学習させてみる」のサンプルコードです。
詳しくはブログ記事を参照ください。

# ファイルリスト
* grad_sample.py
  * 簡単な関数を用いてJAXの自動微分機能を試すためのサンプルコード
* mlp_sample.py
  * 多層パーセプトロン(MLP)を用いてJAXの自動微分機能を試すためのサンプルコード
* mnisit_sample.py
  * JAXによるMLPでMNISTデータセットを用いた分類タスクを学習させるためのサンプルコード
* mnisit_sample.py
  * mnisit_sample.pyのoptimizerをRMSPropに変更したコード
* tf_sample.py
  * mnisit_sample.pyと同一のタスクをTensorflow2で行う場合のサンプルコード
