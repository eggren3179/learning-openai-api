"""
Streamlitを利用したOpenAI向けChat Webアプリケーション
"""
import streamlit as st
from dotenv import load_dotenv
import openai
import os
from PyPDF2 import PdfReader

#環境変数からOpenAIのAPIキー読み込み
load_dotenv(override=True)
openai.api_key = os.getenv("openai_api_key")

st.title("Chat application with OpenAI")

# セッションステートの初期化
if 'input_text' not in st.session_state:
    st.session_state.input_text_list = []
if 'input_count' not in st.session_state:
    st.session_state.input_count = 0
if 'messages' not in st.session_state:
    st.session_state.messages = []

# #OpenAIのクライアント初期化
print(openai.api_key)
llm_client = openai.OpenAI(api_key=openai.api_key)

def get_pdf_text():
    """
    pdfファイルをテキストに変換
    """
    uploaded_file = st.file_uploader(
        label='Upload your PDF here',
        type='pdf'  # アップロードを許可する拡張子 (複数設定可)
    )
    if uploaded_file:
        pdf_reader = PdfReader(uploaded_file)
        text = '\n\n'.join([page.extract_text() for page in pdf_reader.pages])
        # text_splitter = RecursiveCharacterTextSplitter.from_tiktoken_encoder(
        #     model_name=st.session_state.emb_model_name,
        #     # 適切な chunk size は質問対象のPDFによって変わるため調整が必要
        #     # 大きくしすぎると質問回答時に色々な箇所の情報を参照することができない
        #     # 逆に小さすぎると一つのchunkに十分なサイズの文脈が入らない
        #     chunk_size=250,
        #     chunk_overlap=0,
        # )
        # return text_splitter.split_text(text)
        return text
    else:
        return ""
    
#ファイルアップロード
uploaded_file_text = get_pdf_text()

#アップロードした内容を表示
st.write(uploaded_file_text)

def add_input_text():
    """
    テキストをブラウザに保存
    """
    input_text = st.session_state.input_text.strip()
    if input_text:
        st.session_state.input_count += 1
        st.session_state.input_text_list.append(input_text)
        st.session_state.input_text = ""

# テキスト入力[ToDo:テキスト入力部分はチャット部分に置き換えるため消去予定]
text_input = st.text_input("Enter some text", key="input_text")
submit_button = st.button("Submit", on_click=add_input_text)

st.write("#### User input:")
for count, text in enumerate(st.session_state.input_text_list):
    # 2列表示
    col1, col2 = st.columns(2)
    col1.write(f"{count+1}:")
    col2.write(f"{text}")

#チャット履歴(st.session_state.messages)の表示
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

#チャットの表示
prompt = st.chat_input("Input some text")

if prompt:
    #ユーザの入力内容をst.session_state.messagesに追加
    st.session_state.messages.append({"role":"user", "content":prompt})

    with st.chat_message("user"):
        st.markdown(prompt)
    
    with st.chat_message("assistant"):
        # OpenAI APIを呼び出して回答を取得
        response = llm_client.chat.completions.create(
            model="gpt-3.5-turbo-1106",
            # response_format={ "type": "json_object" }, #Jsonフォーマットでレスポンス生成
            messages=[{"role":"user", "content":prompt}],
            max_tokens=150
        )
        respons_str = response.choices[0].message.content
        st.markdown(respons_str)

    #応答をst.session_state.messagesに追加
    st.session_state.messages.append({"role":"assistant", "content":respons_str})
