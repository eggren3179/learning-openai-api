# OpenAI API学習用レポジトリ
OpenAIのAPIを利用したアプリ開発用の学習レポジトリです。

## Embedding
 - embedding_text.py：OpenAIを用いたEmbeddingとFaissのベクトルデータベースを使ったベクトル検索のスクリプト

## Fine-tuning
 - make_fine_tuning_dataset.py: OpenAIにおけるFine-tuning用のデータセットを作成するスクリプト

## LlamaIndex
 #### 1. LlamaIndexとは
  - LLMでは学習されていないデータを参照して質問応答を作成するための[ライブラリ](https://github.com/jerryjliu/llama_index)
  - 「LlamaHub」ライブラリを利用してPDFなどの各種ファイルやYoutubeなどのWebサービスの情報も質問応答に活用できる
  - 内部ではLangChainのライブラリが使われている
  - ドキュメントは[こちら](https://gpt-index.readthedocs.io/en/stable/)