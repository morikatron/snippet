# generate_licenses

python で構築したソフトウェアを配布・公開する際に、利用しているライブラリのライセンス表記をまとめて出力するツールです。

pip-licenses を利用しています。

対象となるライブラリは pip でインストールしたものに限ります。

> コード生成には ChatGPT を利用しています。

## 仮想環境構築
```bash
conda create -n generate_licenses_env python=3.11
conda activate generate_licenses_env
pip install pip-licenses
```

## リポジトリインストール
```bash
git clone https://github.com/morikatron/snippet.git
cd snippet/generate_licenses
```

## ライブラリインストール（サンプル）
```bash
conda activate generate_licenses_env
pip install -r sample_requirements.txt
```

## 操作手順
```bash
python generate_licenses.py
# created path: licenses.json
# License information has been written to licenses.txt
# created path: licenses_summary.txt
# License summary has been written to licenses_summary.txt
```

## 出力ファイル（サンプル）
- [licences.json](licenses.json)
- [licences.txt](licenses.txt)
- [licences_summary.txt](licenses_summary.txt)

[ページの先頭に戻る](#)
