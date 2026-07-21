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

if st.button("AI분석 시작", type="primary"):
  if user_sentence.strip():
    prompt = f"""
당신은 전임 영어 강사이자 친절한 AI 튜터입니다. 
            사용자가 입력한 다음 영어 문장을 철저하게 분석해 주세요.
            
            [입력 문장]
            "{user_sentence}"
            
            [출력 형식]
            1. 🔍 **정확한 해석**: 문장의 의미를 자연스럽고 매끄러운 한국어로 번역해 줘.
            2. 🛠️ **문법 오류 교정**: 문법이나 자연스럽지 못한 표현이 있다면 올바른 문장(Corrected Version)으로 제시하고, 어떤 부분이 왜 틀렸는지 중학생도 이해할 수 있게 핵심 포인트를 짚어줘. (틀린 게 없다면 완벽한 문장이라고 극찬해 줘.)
            3. 💡 **핵심 어휘 정리**: 문장에 등장한 중요 단어나 숙어 2~3개를 골라 [단어 - 뜻 - 간단한 예문] 형태로 정리해 줘.
            """
            try:
                with st.spinner("AI 선생님이 문장을 꼼꼼하게 채점하고 있습니다... ⏳"):
                    response = ai_client.chat.completions.create(
                        model="gpt-4o-mini",
                        messages=[{"role": "user", "content": prompt}],
                        temperature=0.6
                    )
                    st.markdown("### 📋 AI 코칭 리포트")
                    st.info(response.choices[0].message.content)
            except Exception as e:
                st.error(f"분석 중 오류가 발생했습니다: {e}")
        else:
            st.warning("분석할 문장을 먼저 입력해 주세요!")

with tab2:
    st.subheader("🎲 갓생 영단어 챌린지")
    st.write("AI가 무작위로 고등학교 및 토익 필수 영단어 퀴즈를 즉석에서 출제합니다.")
    
    if st.button("새 퀴즈 출제하기 🔄"):
        prompt = """
        고등학교 및 TOEIC 필수 영단어 중 난이도가 있는 단어 하나를 골라 4지선다형 객관식 퀴즈를 만들어줘.
        반드시 아래의 JSON 형식으로만 답변해야 해. 다른 부연 설명은 절대 하지 마.
        
        {
            "word": "출제할 영단어",
            "meaning": "정답 뜻 (반드시 options 배열 내에 완벽히 일치하는 항목이 있어야 함)",
            "options": ["1번 보기", "2번 보기", "3번 보기", "4번 보기"]
        }
        """
        try:
            with st.spinner("AI가 알맞은 문제를 출제하는 중입니다... 🎲"):
                response = ai_client.chat.completions.create(
                    model="gpt-4o-mini",
                    messages=[{"role": "user", "content": prompt}],
                    response_format={"type": "json_object"}
                )
                result = json.loads(response.choices[0].message.content)
                st.session_state.quiz_word = result["word"]
                st.session_state.quiz_meaning = result["meaning"]
                st.session_state.quiz_options = result["options"]
                st.session_state.quiz_checked = False
        except Exception as e:
            st.error(f"퀴즈를 불러오는 데 실패했습니다: {e}")
            
    if st.session_state.quiz_word:
        st.markdown(f"### 💡 다음 단어의 올바른 뜻은?\n## **{st.session_state.quiz_word}**")
        
        user_ans = st.radio("보기를 읽고 정답을 선택하세요:", st.session_state.quiz_options, key="quiz_radio")
        
        col1, col2 = st.columns([1, 4])
        with col1:
            if st.button("정답 확인 🔓"):
                st.session_state.quiz_checked = True
                
        with col2:
            if st.button("이 단어 내 단어장에 추가 📌"):
                word_pair = {"word": st.session_state.quiz_word, "meaning": st.session_state.quiz_meaning}
                if word_pair not in st.session_state.vocab_book:
                    st.session_state.vocab_book.append(word_pair)
                    st.toast("단어장에 성공적으로 추가되었습니다!")
                else:
                    st.toast("이미 단어장에 존재하는 단어입니다.")
                    
        if st.session_state.quiz_checked:
            if st.session_state.quiz_meaning in user_ans:
                st.success(f"🎉 정답입니다! 멋져요! (정답 뜻: {st.session_state.quiz_meaning})")
            else:
                st.error(f"❌ 아쉽습니다! 정답은 **'{st.session_state.quiz_meaning}'** 입니다. 단어장에 추가해 복습해 보세요!")

with tab3:
    st.subheader("📖 나만의 암기 노트")
    st.write("공부하면서 헷갈렸던 단어들을 기록하고 관리해 보세요.")
    
    with st.expander("➕ 수동으로 단어 추가하기"):
        c1, c2 = st.columns(2)
        with c1:
            new_w = st.text_input("영어 단어", placeholder="apple")
        with c2:
            new_m = st.text_input("한국어 뜻", placeholder="사과")
        if st.button("단어 저장"):
            if new_w.strip() and new_m.strip():
                st.session_state.vocab_book.append({"word": new_w.strip(), "meaning": new_m.strip()})
                st.toast("단어가 저장되었습니다! 🔥")
                st.rerun()
                
    st.markdown("---")
    
    if not st.session_state.vocab_book:
        st.info("아직 저장된 단어가 없습니다. 문장을 분석하거나 퀴즈를 풀며 단어를 채워보세요!")
    else:
        st.write(f"현재 총 **{len(st.session_state.vocab_book)}개**의 단어가 저장되어 있습니다.")
        
        for idx, item in enumerate(st.session_state.vocab_book):
            col_v1, col_v2, col_v3 = st.columns([2, 3, 1])
            with col_v1:
                st.markdown(f"**{item['word']}**")
            with col_v2:
                st.write(item['meaning'])
            with col_v3:
                if st.button("삭제", key=f"del_{idx}"):
                    st.session_state.vocab_book.pop(idx)
                    st.rerun()
                    
        if st.button("단어장 전체 비우기", type="primary"):
            st.session_state.vocab_book = []
