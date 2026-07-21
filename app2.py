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

tap1, tap2, tap3 = st.taps(["문장 분석과 교정, 오늘의 단어 퀴즈, 나만의 단어장"])

with tap1:
  st.subheader("영문법 교정과 상세 해석")
  st.write("궁금한거 있으면 AI한테 물어보세요")

user_sentence = st.text_area("분석할 영어 문장을 입력하세요")

