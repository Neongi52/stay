import streamlit as st

with st.sidebar:
    st.header("프로필")
    user_name = st.text_input("닉네임")
    weather = st.selectbox("오늘 날씨", ["맑음", "흐림", "비/눈", "매우 추움"])
    st.markdown("---")
    st.infut(f"반가워요, {user_name}님! 오늘 날씨는 '{weather}'이네요.")

st.title("👗 AI 코디 메이커")
st.write("사이드바에서 날씨를 먼저 선택하고 코디를 시작하세요!") 

st.header("👕 아이템 조합하기") 
col1, col2 = st.columns(2)
with col1:
    st,subheader("상의")
    top_type = st.radio("종류", ["후드티", "셔츠", "맨투맨", "반팔 티셔츠"])
    top_color = st.select_slider("생상 톤", options=["밝음, "무난함", "어두움"])
with col2:
    st.subheader("하의")
    bottom_type = st.radio("종류", ["청바지", "슬랙스", "트레이닝 팬츠", "반바지"])
    bottom_color = st.select_slider("핏(Fit)", options=["슬림", "레귤러", "오버핏"])

st.markdown("---")
if st.button("코디 완성하기"):
    with st.container(border=True):
        st.subheader(f"{user_name}님의 오늘의 룩북")
        st.write(f"오늘 같은 **{wwather}** 날씨에는 이렇게 입어보세요!")
        st.markdown(f"""
        * **상의:** {top_color} {top_type}
        * **하의:** {bottom_color} {bottom_type}
        * **매칭:** {shoes}와 {', '.join(acc) if acc else '악세서리 없이 깔끔하게!'}
        """)
        st.success("오늘의 스타일링이 완성되었습니다! 자신 있게 외출하세요!")

with st.expander("코디 연출 팁 영상 보기"):
    st.video("https://youtu.be/SnRvPkzWzhg?si=F7dF256fTuxxrL2x")
    st.write("전문가가 제안하는 코디 연출법을 참고해 보세요.")




