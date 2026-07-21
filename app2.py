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

st.title("🔤 AI 영어 공부 헬퍼")
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
    if st.button("퀴즈 출제"):
        with st.spinner("출제 중..."):
            res = ai_client.chat.completions.create(
                model="gpt-4o-mini",
                messages=[{"role": "user", "content": "고등학교 필수 영단어 객관식 퀴즈를 JSON 형식을 지켜서 만들어줘. 양식: {'word':'단어', 'meaning':'정답뜻', 'options':['1','2','3','4']}"}],
                response_format={"type": "json_object"}
            )
            st.session_state.q = json.loads(res.choices[0].message.content)
            st.session_state.chk = False

    if st.session_state.q:
        q = st.session_state.q
        st.markdown(f"### **{q['word']}**의 뜻은?")
        ans = st.radio("보기:", q['options'])
        
        c1, c2 = st.columns(2)
        if c1.button("정답 확인"): st.session_state.chk = True
        if c2.button("단어장 추가") and {"word": q['word'], "meaning": q['meaning']} not in st.session_state.vocab:
            st.session_state.vocab.append({"word": q['word'], "meaning": q['meaning']})
            st.toast("추가 완료!")
            
        if st.session_state.get('chk'):
            if q['meaning'] in ans: st.success("정답입니다! 🎉")
            else: st.error(f"오답! 정답은: {q['meaning']}")

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
