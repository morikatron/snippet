# silhouette_maker
Stable Diffusionを使って人物の影絵画像を作成するプログラムです。

Morikatron Engineer Blog の記事 「[Stable Diffusion WebUIをPythonから利用して影絵キャラクターを量産する](URL)」のサンプルコードとなっています。

## 必要ツール
- Stable Diffusion WebUI
  - https://github.com/AUTOMATIC1111/stable-diffusion-webui
  - あらかじめ設定ファイルでAPIを有効にして起動しておいてください
- python 3.10

## 依存ライブラリ
- Pillow
- webuiapi

```
pip install Pillow webuiapi
```
または
```
pip install -r requirements.txt
```
でインストールしてください。
## ディレクトリ構成
```
/
├img/
│ └base_face.png
├main.py
└requirements.txt
```

## 使い方
Stable Diffusion WebUIを起動した状態で
```
python main.py
```
を実行してください。

main.pyでは通信にStable Diffusion WebUIのデフォルトでのローカルホスト、ポート番号である`http://127.0.0.1:7860/`を利用しているため、変更したい場合は適宜変更してください。

