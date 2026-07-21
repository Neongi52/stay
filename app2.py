import streamlit as st
from openai import OpenAI

ai_client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])

st.title("영어공부 도우미")
st.header("단어", "문법", "어휘", "해석")
