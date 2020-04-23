"""
Morikatron Engineer Blog の記事 「【GiNZA】三点リーダーで文を区切らないようにする」のサンプルコードです。詳しくは下記URLのブログ記事をご参照ください。
https://tech.morikatron.ai/entry/2020/04/29/100000
"""
import spacy

text = '花子さんですか～？……えっと、あの……そうです……。'

# GiNZAのモデルをロード
nlp = spacy.load('ja_ginza')
# テキストの解析
doc = nlp(text)

# テキストの中で文単位に分割されているので文を順に参照
for sent in doc.sents:
    # 分割された文を出力
    print(sent)

    # 文の中でトークン単位に分割されているのでトークンを順に参照
    for token in sent:
        info = [
            token.orth_,     # 元のテキスト
            token.lemma_,    # 正規化表記
            token.pos_,      # 品詞
            token.tag_,      # 品詞詳細
            token.dep_,      # 依存関係ラベル
        ]
        # 分割されたトークンの情報を出力
        print(info)
