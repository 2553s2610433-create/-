import streamlit as st
import google.generativeai as genai

# -----------------------------
# 페이지 설정
# -----------------------------
st.set_page_config(
    page_title="공부 도우미 챗봇",
    page_icon="📚",
    layout="centered"
)

st.title("📚 공부 도우미 챗봇")
st.caption("Gemini 기반 학습 챗봇")

# -----------------------------
# API KEY 불러오기
# -----------------------------
try:
    api_key = st.secrets["GEMINI_API_KEY"]
    genai.configure(api_key=api_key)

except Exception:
    st.error("API 키를 불러올 수 없습니다.")
    st.info(".streamlit/secrets.toml 파일을 확인하세요.")
    st.stop()

# -----------------------------
# 모델 설정
# -----------------------------
model = genai.GenerativeModel(
    model_name="gemini-2.5-flash-lite",
    system_instruction="""
    너는 공부를 도와주는 친절한 AI 튜터다.
    
    규칙:
    - 개념을 쉽게 설명한다.
    - 예시를 함께 제공한다.
    - 어려운 용어는 풀어서 설명한다.
    - 사용자의 학습 수준에 맞춰 답변한다.
    - 시험 대비, 요약, 암기 팁도 제공한다.
    """
)

# -----------------------------
# 세션 상태 초기화
# -----------------------------
if "messages" not in st.session_state:
    st.session_state.messages = []

# -----------------------------
# 이전 채팅 출력
# -----------------------------
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# -----------------------------
# 사용자 입력
# -----------------------------
prompt = st.chat_input("공부 관련 질문을 입력하세요")

if prompt:

    # 사용자 메시지 저장
    st.session_state.messages.append(
        {
            "role": "user",
            "content": prompt
        }
    )

    # 사용자 메시지 출력
    with st.chat_message("user"):
        st.markdown(prompt)

    # AI 응답 생성
    with st.chat_message("assistant"):

        with st.spinner("답변 생성 중..."):

            try:
                # 대화 기록 구성
                history = []

                for msg in st.session_state.messages[:-1]:

                    role = "user" if msg["role"] == "user" else "model"

                    history.append({
                        "role": role,
                        "parts": [msg["content"]]
                    })

                # 채팅 시작
                chat = model.start_chat(history=history)

                # 응답 생성
                response = chat.send_message(prompt)

                answer = response.text

                # 응답 출력
                st.markdown(answer)

                # 세션 저장
                st.session_state.messages.append(
                    {
                        "role": "assistant",
                        "content": answer
                    }
                )

            except Exception as e:
                error_message = f"오류가 발생했습니다: {str(e)}"

                st.error(error_message)

                st.session_state.messages.append(
                    {
                        "role": "assistant",
                        "content": error_message
                    }
                )
