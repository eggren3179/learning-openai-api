import openai
import os
from dotenv import load_dotenv
import numpy as np
import faiss

#環境変数からOpenAIのAPIキー読み込み
load_dotenv(override=True)
openai.api_key = os.getenv("openai_api_key")

input_text = "これはテストです。"

print(f"input_text:{input_text}")

# テキストからEmbeddingを実行
response = openai.Embedding.create(
    input=input_text,
    model="text-embedding-ada-002"
)

# --input_textの内容確認--
# モデル
print(f"model:{response['model']}")
# ベクトル表現の次元
print(f"len of embedding input_text:{len(response['data'][0]['embedding'])}")
# Embeddingのベクトル表現
print(f"response['data'][0]['embedding'] of input_text: \n{response['data'][0]['embedding']}")

input_embeds = [record["embedding"] for record in response["data"]]
input_embeds = np.array(input_embeds).astype("float32")

print(f"\ninput_embeds:\n{input_embeds}")

# --target_textのEmbedding--
target_texts = [
    "ここは学校です",
    "朝は何時に起きますか？",
    "遊ぼう！",
    "実験を始めましょう",
    "お腹が空きました"
]

print(f"target_texts:{target_texts}")

# target_textからEmbeddingを実行
response = openai.Embedding.create(
    input=target_texts,
    model="text-embedding-ada-002"
)

target_embeds = [record["embedding"] for record in response["data"]]
target_embeds = np.array(target_embeds).astype("float32")

print(f"\ntarget_embeds:{target_embeds}")


# --ベクトルデータベースfaissの利用--
# Embeddingの次元として1536（Adaモデルで固定）を指定してL2ノルムにより検索
index = faiss.IndexFlatL2(1536)
# target_embedsを追加
index.add(target_embeds)

# 近傍探索の実行
D, I = index.search(input_embeds, 1)
# 近傍探索の結果
print(f"\ninput_text:{input_text}")
print(f"the nearest target_text:{target_texts[I[0][0]]}")

print(f"(Nearest distance:{D}, Nearest index:{I})")