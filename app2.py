import streamlit as st

st.title("카운터 앱")
if 'time.time()' not in st.session_state:
    st.session_state.count = 0
if st.button("증가"):
    st.session_state.count += 
st.markdown(f"## 현재 숫자: `{st.session_state.count}`")
