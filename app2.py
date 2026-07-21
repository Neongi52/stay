import streamlit as st
from openai import OpenAI

ai_client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])

st.header("영어공부 도우미")
gram, voca, talk = st.colums(3)

