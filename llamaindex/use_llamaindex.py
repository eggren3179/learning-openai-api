import openai #opanai==0.27.8で動作
import os
import sys
from dotenv import load_dotenv
import numpy as np
import logging
from llama_index import SimpleDirectoryReader, GPTVectorStoreIndex, StorageContext, load_index_from_storage, ServiceContext, LLMPredictor, PromptHelper
from langchain.chat_models import ChatOpenAI

#ログレベルの設定
logging.basicConfig(stream=sys.stdout, level=logging.INFO, force=True)

#環境変数からOpenAIのAPIキー読み込み
load_dotenv(override=True)
openai.api_key = os.getenv("openai_api_key")

def create_new_index(input_dir="./data", save_dir="./storage"):
    """input_dirのディレクトリ内のデータを基にインデックスを作成し、save_dirのディレクトリ内に保存する
    """
    # ドキュメント読み込み
    logging.info("----Start: loading documents-----")
    documents = SimpleDirectoryReader(input_dir=input_dir).load_data()
    logging.debug(f"documents: {documents}")
    logging.info("----End: loading documents-----\n")

    # モデルのカスタマイズ
    logging.info("----Start: setting models and chunk rules-----")
    llm_predictor = LLMPredictor(llm=ChatOpenAI(temperature=0, model_name="gpt-3.5-turbo", openai_api_key=openai.api_key))
    prompt_helper = PromptHelper(
        chunk_size_limit=4096, # MAX LLM input token
        num_output=256, # MAX LLM output token
        chunk_overlap_ratio = 0.2
    )
    service_context = ServiceContext.from_defaults(llm_predictor = llm_predictor, prompt_helper=prompt_helper)
    logging.info("----End: setting models and chunk rules-----")

    # インデックスの作成：時間がかかるので注意
    logging.info("----Start: making index-----")
    # index = GPTVectorStoreIndex.from_documents(documents)
    index = GPTVectorStoreIndex.from_documents(documents, service_context = service_context)
    logging.info(f"index:{index}")
    logging.info("----End: making index-----\n")

    # インデックスの保存
    logging.info("----Start: saving index-----")
    index.storage_context.persist(persist_dir=save_dir)
    logging.info("----End: saving index-----\n")

    return index

def send_query_and_response(query_engine, query):
    response = query_engine.query(query)
    print(f"query:{query}")
    print(f"response:{response}")
    return response


# 保存したインデックスがある場合には読み込み。なければインデックスの新規作成を実行
try:
    logging.info("----Start: loading index-----")
    storage_context = StorageContext.from_defaults(persist_dir="./storage")
    index = load_index_from_storage(storage_context)
    logging.info("----End: loading index-----\n")
except Exception as e:
     logging.info(f"Loading index failed.")
     logging.info(f"Try to create index...")
     index = create_new_index()

# query engineの作成
logging.info("----Start: making query engine-----")
query_engine = index.as_query_engine()
logging.info("----End: making query engine-----\n")

# 質問応答
query = "Azure OpenAI Serviceとは？"
send_query_and_response(query_engine, query)