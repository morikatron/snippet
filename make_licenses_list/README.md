# make_licenses_list

python で構築したソフトウェアを配布・公開する際に、利用しているライブラリのライセンス表記をまとめて出力するツールです。

pip-licenses を利用しています。

対象となるライブラリは pip でインストールしたものに限ります。

> コード生成には ChatGPT を利用しています。

## 仮想環境構築
```bash
conda create -n make_licenses_list_env python=3.11
conda activate make_licenses_list_env
pip install pip-licenses
```

## リポジトリインストール
```bash
git clone https://github.com/morikatron/snippet.git
cd snippet/make_licenses_list
```

## ライブラリインストール（サンプル）
```bash
conda activate make_licenses_list_env
pip install -r sample_requirements.txt
```

## 操作手順
```bash
python make_licenses_list.py
# created path: licenses_list.json
# License information has been written to licenses_list.txt
# created path: licenses_summary.txt
# License summary has been written to licenses_summary.txt
```

## 出力ファイル（サンプル）
- [sample_licenses_list.json](sample_licenses_list.json)
- [sample_licenses_list.txt](sample_licenses_list.txt)
- [sample_licenses_summary.txt](sample_licenses_summary.txt)

[ページの先頭に戻る](#)
