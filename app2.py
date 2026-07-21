import streamlit as st
from openai import OpenAI
import json

st.set_page_config(page_title="AI 영어 코치", page_icon="🔤")

if 'OPENAI_API_KEY' in st.secrets:
    ai_client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])
else:
    st.error("⚠️ API Key 미설정")
    st.stop()

if 'vocab' not in st.session_state: st.session_state.vocab = []
if 'q' not in st.session_state: st.session_state.q = None

st.title("🔤 AI 영어 공부")
t1, t2, t3 = st.tabs(["📝 문장 분석", "🎯 단어 퀴즈", "📖 단어장"])

with t1:
    txt = st.text_area("영어 문장 입력:", placeholder="He don't know how to speaking English.")
    if st.button("AI 분석") and txt.strip():
        with st.spinner("분석 중..."):
            res = ai_client.chat.completions.create(
                model="gpt-4o-mini",
                messages=[{"role": "user", "content": f"다음 문장의 [정확한 번역], [문법 교정 및 이유], [주요 단어 정리]를 간결하게 작성해줘:\n\"{txt}\""}]
            )
            st.info(res.choices[0].message.content)

with t2:
    # 1. 퀴즈 출제 버튼
    if st.button("퀴즈 출제"):
        with st.spinner("새로운 퀴즈를 생성하는 중..."):
            try:
                # OpenAI API를 통해 JSON 형태의 응답을 유도
                res = ai_client.chat.completions.create(
                    model="gpt-4o-mini",
                    messages=[
                        {
                            "role": "system", 
                            "content": "You must respond ONLY with a JSON object. Format: {\"word\": \"영어단어\", \"meaning\": \"뜻\"}"
                        },
                        {
                            "role": "user", 
                            "content": "랜덤한 토익 필수 영단어 1개와 그 뜻을 JSON 형식으로 출제해줘."
                        }
                    ],
                    response_format={"type": "json_object"} # JSON 모드 강제 (선택 사항)
                )
                
                # API 결과를 딕셔너리로 변환하여 '세션 상태'에 저장 🌟
                result_dict = json.loads(res.choices[0].message.content)
                st.session_state.q = result_dict
                
            except Exception as e:
                st.error(f"퀴즈를 생성하는 중 오류가 발생했습니다: {e}")

    # --- 화면에 퀴즈를 그려주는 부분 ---
    st.write("---") # 구분선
    
    # 2. 세션 상태에 퀴즈 데이터가 존재하는지 확인 후 출력 🌟
    if st.session_state.q is not None:
        # 일반 변수 q가 아니라 st.session_state.q에서 키를 가져옵니다.
        current_word = st.session_state.q.get('word', '알 수 없는 단어')
        correct_meaning = st.session_state.q.get('meaning', '')

        st.markdown(f"### 🎯 **{current_word}**의 뜻은?")
        
        # 정답 확인용 간단한 토글 토글 (정답 보기 버튼 대신 확장러 사용)
        with st.expander("정답 확인하기"):
            st.success(f"정답은 **'{correct_meaning}'** 입니다!")
            
    else:
        # 데이터가 아직 없을 때 보여줄 안내 메시지
        st.info("💡 위의 '퀴즈 출제' 버튼을 누르면 영어 단어 퀴즈가 시작됩니다.")

with t3:
    with st.expander("단어 직접 추가"):
        w, m = st.columns(2)
        nw = w.text_input("단어")
        nm = m.text_input("뜻")
        if st.button("저장") and nw.strip() and nm.strip():
            st.session_state.vocab.append({"word": nw.strip(), "meaning": nm.strip()})
            st.rerun()

    if st.session_state.vocab:
        st.write(f"총 {len(st.session_state.vocab)}개 단어")
        for i, item in enumerate(st.session_state.vocab):
            v1, v2, v3 = st.columns([2, 3, 1])
            v1.markdown(f"**{item['word']}**")
            v2.write(item['meaning'])
            if v3.button("삭제", key=f"d_{i}"):
                st.session_state.vocab.pop(i)
                st.rerun()
