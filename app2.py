import streamlit as st
from openai import OpenAI

ai_client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])

if 'vacab_book' not in st.session_state:
  st.session_state.vocab_book = []
if 'quiz_word' not in st.session_state:
  st.session_state.quiz_word = None
  st.session_state.quiz_meaning = None
  st.session_state.quiz_options = []
  st.session_state.quiz_checked = False

st.title("AI 영어 공부 도우미")
st.write("어휘, 문법, 해석, 그리고 단어장 관리까지 AI와 함께.")
st.markdown("---")



