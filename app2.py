import streamlit as st
import time

st.title("10초 맞추기 게임!")
st.write("시작 버튼을 누르고, 마음속으로 10초를 센 뒤 종료 버튼을 누르세요.")

# 1. 세션 상태(session_state) 초기화 (시작 시간과 종료 시간을 저장할 공간 만들기)
if 'start_time' not in st.session_state:
    st.session_state.start_time = None
if 'end_time' not in st.session_state:
    st.session_state.end_time = None

# 레이아웃 구성 (시작, 종료 버튼을 한 줄에 배치)
col1, col2 = st.columns(2)

with col1:
    if st.button("시작"):
        # 현재 시간을 시작 시간으로 기록
        st.session_state.start_time = time.time()
        st.session_state.end_time = None  # 새로운 게임을 위해 종료 시간 초기화
        st.rerun()

with col2:
    is_already_ended = st.session_state.end_time is not None
    
    if st.button("종료", disabled=is_already_ended):
        # 시작 버튼을 안 누르고 종료부터 누른 경우 예외 처리
        if st.session_state.start_time is None:
            st.error("시작 버튼을 먼저 눌러주세요!")
        else:
            # 현재 시간을 종료 시간으로 기록
            st.session_state.end_time = time.time()
            st.rerun()

# 2. 결과 출력 로직
if st.session_state.start_time and st.session_state.end_time:
    # 시간 차이 계산 (실수형 데이터 차이)
    elapsed_time = st.session_state.end_time - st.session_state.start_time
    st.markdown(f"### 결과: {elapsed_time:.2f}초")
    
    # 10초와의 차이 계산
    diff = abs(10 - elapsed_time)
    
    # 결과 메시지 출력
    if diff == 0:
        st.success("대단해요! 정확히 10초를 맞추셨습니다!")
    else:
        st.error(f"10초와 {diff:.2f}초 차이가 납니다. 다시 도전해보세요!")

# 3. 다시 하기 버튼 (모든 세션 상태 초기화)
if st.button("다시 하기"):
    st.session_state.start_time = None
    st.session_state.end_time = None
    st.rerun()
