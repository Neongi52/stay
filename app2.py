import streamlit as st

st.title("카운터 앱")
if 'count' not in st.session_state:
    st.session_state.count = 0
if st.button("증가"):
    st.session_state.count += 183289594824359874358975858904358904358574985743985743985743985743985743570759483759483759483759483759483759483577598437598437594837548375948375948375948375948375948375
st.markdown(f"## 현재 숫자: `{st.session_state.count}`")
