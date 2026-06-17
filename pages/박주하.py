import streamlit as st
import pandas as pd
import google.generativeai as genai
from datetime import datetime, timedelta

# ---------------------------
# 페이지 설정
# ---------------------------
st.set_page_config(
    page_title="AI 공부 도우미",
    page_icon="📚",
    layout="centered"
)

st.title("📚 AI 공부 도우미")

# ---------------------------
# Gemini 설정
# ---------------------------
try:
    api_key = st.secrets["GEMINI_API_KEY"]
    genai.configure(api_key=api_key)
    model = genai.GenerativeModel("gemini-2.5-flash-lite")
except Exception:
    model = None

# ---------------------------
# 세션 상태
# ---------------------------
if "messages" not in st.session_state:
    st.session_state.messages = []

# ---------------------------
# 입력
# ---------------------------
st.header("오늘의 공부 계획 만들기")

total_hours = st.number_input(
    "총 공부 시간(시간)",
    min_value=1,
    max_value=24,
    value=3
)

subjects = st.text_input(
    "과목 입력 (쉼표로 구분)",
    "국어,사회"
)

break_minutes = st.slider(
    "쉬는 시간(분)",
    0,
    30,
    10
)

start_time = st.time_input(
    "시작 시간",
    datetime.strptime("09:00", "%H:%M").time()
)

# ---------------------------
# 시간표 생성
# ---------------------------
if st.button("📅 시간표 생성"):

    try:
        subject_list = [
            s.strip()
            for s in subjects.split(",")
            if s.strip()
        ]

        if not subject_list:
            st.error("과목을 입력해주세요.")
            st.stop()

        total_minutes = total_hours * 60

        total_break = break_minutes * (len(subject_list) - 1)

        study_minutes = total_minutes - total_break

        if study_minutes <= 0:
            st.error("쉬는 시간이 너무 깁니다.")
            st.stop()

        per_subject = study_minutes // len(subject_list)

        current = datetime.combine(
            datetime.today(),
            start_time
        )

        schedule = []

        for idx, subject in enumerate(subject_list):

            study_start = current
            study_end = current + timedelta(
                minutes=per_subject
            )

            schedule.append(
                {
                    "구분": "공부",
                    "내용": subject,
                    "시작": study_start.strftime("%H:%M"),
                    "종료": study_end.strftime("%H:%M")
                }
            )

            current = study_end

            if idx < len(subject_list) - 1:

                break_end = current + timedelta(
                    minutes=break_minutes
                )

                schedule.append(
                    {
                        "구분": "휴식",
                        "내용": "쉬는 시간",
                        "시작": current.strftime("%H:%M"),
                        "종료": break_end.strftime("%H:%M")
                    }
                )

                current = break_end

        st.subheader("📋 오늘의 시간표")

        for item in schedule:

            if item["구분"] == "공부":
                st.success(
                    f"{item['시작']} ~ {item['종료']} | {item['내용']}"
                )
            else:
                st.info(
                    f"{item['시작']} ~ {item['종료']} | 휴식"
                )

        # -----------------------
        # 그래프
        # -----------------------
        chart_df = pd.DataFrame(
            {
                "과목": subject_list,
                "공부시간(분)": [per_subject]
                * len(subject_list)
            }
        )

        st.subheader("📊 과목별 공부 시간")

        st.bar_chart(
            chart_df.set_index("과목")
        )

        # -----------------------
        # Gemini 공부 팁
        # -----------------------
        if model:

            prompt = f"""
            총 공부시간: {total_hours}시간
            과목: {', '.join(subject_list)}

            학생에게 짧고 실용적인 공부 팁 3개를 제공해줘.
            """

            try:
                response = model.generate_content(prompt)

                st.subheader("🤖 AI 공부 팁")

                st.write(response.text)

            except Exception:
                st.warning(
                    "AI 공부 팁 생성에 실패했습니다."
                )

    except Exception as e:
        st.error(f"오류 발생: {e}")

# ---------------------------
# AI 채팅
# ---------------------------
st.divider()

st.header("🤖 공부 상담 챗봇")

for msg in st.session_state.messages:

    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

user_input = st.chat_input(
    "공부 관련 질문을 해보세요"
)

if user_input:

    st.session_state.messages.append(
        {
            "role": "user",
            "content": user_input
        }
    )

    with st.chat_message("user"):
        st.markdown(user_input)

    if model:

        try:
            response = model.generate_content(
                f"""
                너는 공부 코치야.

                질문:
                {user_input}
                """
            )

            answer = response.text

        except Exception:
            answer = "AI 응답 생성 중 오류가 발생했습니다."

    else:
        answer = "Gemini API 설정이 필요합니다."

    st.session_state.messages.append(
        {
            "role": "assistant",
            "content": answer
        }
    )

    with st.chat_message("assistant"):
        st.markdown(answer)
