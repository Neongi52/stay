import streamlit as st
from openai import OpenAI

ai_client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])

if 'grammar_list' not in st.session_state:
  st.session_state.grammar_list = []

