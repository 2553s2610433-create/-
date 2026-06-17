import streamlit as st
import pandas as pd
from datetime import datetime, timedelta

st.set_page_config(
    page_title="공부 도우미",
    page_icon="📚",
    layout="centered"
)

st.title("📚 공부 도우미")
st.write("과목별 공부 시간표를 자동으로 만들어줍니다.")

# 입력
total_hours = st.number_input(
    "총 공부 시간(시간)",
    min_value=1,
    max_value=24,
    value=3
)

subjects_text = st.text_input(
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
    "공부 시작 시간",
    value=datetime.strptime("09:00", "%H:%M").time()
)

if st.button("📅 시간표 생성"):

    try:
        subjects = [
            s.strip()
            for s in subjects_text.split(",")
            if s.strip()
        ]

        if not subjects:
            st.error("과목을 입력해주세요.")
            st.stop()

        total_minutes = total_hours * 60
        total_break = break_minutes * (len(subjects) - 1)
        study_minutes = total_minutes - total_break

        if study_minutes <= 0:
            st.error("쉬는 시간이 너무 많습니다.")
            st.stop()

        per_subject = study_minutes // len(subjects)

        current = datetime.combine(
            datetime.today(),
            start_time
        )

        schedule = []

        for i, subject in enumerate(subjects):

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

            if i < len(subjects) - 1:

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

        df = pd.DataFrame(schedule)

        st.dataframe(
            df,
            use_container_width=True
        )

        st.subheader("📊 과목별 공부 시간")

        chart_df = pd.DataFrame(
            {
                "과목": subjects,
                "공부시간(분)": [per_subject]
                * len(subjects)
            }
        )

        st.bar_chart(
            chart_df.set_index("과목")
        )

        st.success("시간표 생성 완료!")

    except Exception as e:
        st.error(f"오류 발생: {e}")
