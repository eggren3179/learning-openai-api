"""
Streamlitを利用したOpenAI向けChat Webアプリケーション
"""
import streamlit as st

st.title("Chat application with OpenAI")

# セッションステートの初期化
if 'input_text' not in st.session_state:
    st.session_state.input_text_list = []
if 'input_count' not in st.session_state:
    st.session_state.input_count = 0

def add_input_text():
    input_text = st.session_state.input_text.strip()
    if input_text:
        st.session_state.input_count += 1
        st.session_state.input_text_list.append(input_text)
        st.session_state.input_text = ""

# テキスト入力
text_input = st.text_input("Enter some text", key="input_text")
submit_button = st.button("Submit", on_click=add_input_text)

st.write("#### User input:")
for count, text in enumerate(st.session_state.input_text_list):
    # 2列表示
    col1, col2 = st.columns(2)
    col1.write(f"{count+1}:")
    col2.write(f"{text}")

