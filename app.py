import streamlit as st

st.markdown("# AI 챗봇 만들기")
st.markdown("---")
st.markdown("## 질문을 하시면 AI 친구가 응답합니다.")
st.header("1. 기본 정보 입력")
user_id = st.text_input("아이디(ID)를 입력하세요", placeholder="example_user")
age = st.number_input("나이를 입력하세요", min_value=1, max_value=100, value=17)
question = st.text_area("AI에게 보낼 질문을 입력하세요", placeholder="여기에 질문을 작성해 주세요.")

st.header("2. 챗봇 설정")
ai_model = st.radio("사용할 AI 모델을 선택하세요", ["GPT-4", "Claude 3", "Gemini Pro"], horizontal=True)
tone = st.selectbox("답변의 말투를 골라주세요", ["친절하게", "냉철하게", "유머러스하게"])
features = st.multiselect("추가 기능을 선택하세요", ["이미지 생성", "웹 검색", "코드 분석", "번역"])
creativity = st.slider("AI의 창의성 수준을 설정하세요", 0, 100, 50)
ai_speed = st.select_slider("응답 처리 속도를 선택하세요",options=["매우 느림", "느림", "보통", "빠름", "실시간"],value="보통")
agree = st.checkbox("개인정보 수집 및 AI 학습 이용에 동의합니다.")
st.markdown("---")

if st.button("질문 전송하기"):
    if agree:
        st.success(f"성공적으로 전송되었습니다! ({user_id}님)")
        
        # ─── 👇 [여기서부터 새로 추가/수정되는 코드] ───
        with st.spinner("AI 친구가 답변을 생각하고 있습니다... 잠시만 기다려 주세요."):
            try:
                # 1. 사용할 모델 설정 (사용자가 선택한 ai_model 변수를 활용해도 좋지만, 기본적으로 gemini-1.5-flash 가 빠르고 좋습니다)
                model = genai.GenerativeModel("gemini-1.5-flash")
                
                # 2. 사용자가 선택한 '말투'와 '질문 내용'을 하나로 합쳐서 요청 메시지 만들기
                prompt = f"사용자 질문: {question}\n\n[지시사항: 이 질문에 대해 반드시 '{tone}' 말투로 답변해줘.]"
                
                # 3. 구글 AI에게 전송하고 답변 받아오기
                response = model.generate_content(prompt)
                
                # 4. 화면에 AI 답변 예쁘게 출력하기
                st.markdown("---")
                st.subheader("🤖 AI 친구의 답변")
                st.write(response.text)
                
            except Exception as e:
                st.error(f"AI 호출 중 오류가 발생했습니다: {e}")
        # ─── 👆 [여기까지 추가/수정] ───

        st.markdown("---")
        st.markdown(f"""
        * **선택 모델:** `{ai_model}` | **말투:** `{tone}`
        * **활성화 기능:** {', '.join(features) if features else '없음'}
        * **창의성:** `{creativity}%` | **처리 속도:** `{ai_speed}`
        """)
        
        if age < 14:
            st.info("참고: 14세 미만 사용자이므로 보호자 모드가 활성화됩니다.")
    else:
        st.error("⚠️ 동의 항목에 체크해야 전송이 가능합니다.")








