import streamlit as st
import pandas as pd

st.set_page_config(
    page_title="과목별 강의 모아보기",
    page_icon="📚",
    layout="wide"
)

# ==========================
# 강의 데이터
# ==========================
LECTURES = {
    "수학": [
        {
            "title": "중학교 수학 개념 정리",
            "url": "https://www.youtube.com/embed/1N4Aq0tK3nM",
            "watch_url": "https://www.youtube.com/watch?v=1N4Aq0tK3nM",
            "description": "중학교 수학 핵심 개념을 정리한 강의입니다."
        },
        {
            "title": "함수 기초",
            "url": "https://www.youtube.com/embed/YjL3V3J8r0M",
            "watch_url": "https://www.youtube.com/watch?v=YjL3V3J8r0M",
            "description": "함수의 기본 개념을 설명합니다."
        }
    ],

    "영어": [
        {
            "title": "기초 영어 문법",
            "url": "https://www.youtube.com/embed/eIho2S0ZahI",
            "watch_url": "https://www.youtube.com/watch?v=eIho2S0ZahI",
            "description": "영어 문법의 기초를 학습합니다."
        }
    ],

    "과학": [
        {
            "title": "과학 개념 완성",
            "url": "https://www.youtube.com/embed/L_jWHffIx5E",
            "watch_url": "https://www.youtube.com/watch?v=L_jWHffIx5E",
            "description": "과학 핵심 개념을 쉽게 설명합니다."
        }
    ]
}

# ==========================
# 제목
# ==========================
st.title("📚 과목별 강의 모아보기")
st.write("원하는 과목을 선택하여 강의를 바로 시청하거나 따로 열어볼 수 있습니다.")

# ==========================
# 사이드바
# ==========================
subjects = list(LECTURES.keys())

selected_subject = st.sidebar.selectbox(
    "과목 선택",
    subjects
)

st.sidebar.markdown("---")
st.sidebar.info(
    "강의를 추가하려면 app.py의 LECTURES 데이터를 수정하세요."
)

# ==========================
# 선택 과목 표시
# ==========================
st.header(f"📖 {selected_subject}")

lectures = LECTURES.get(selected_subject, [])

if not lectures:
    st.warning("등록된 강의가 없습니다.")
    st.stop()

# ==========================
# 강의 목록
# ==========================
lecture_titles = [lecture["title"] for lecture in lectures]

selected_title = st.selectbox(
    "강의 선택",
    lecture_titles
)

selected_lecture = next(
    (lecture for lecture in lectures if lecture["title"] == selected_title),
    None
)

# ==========================
# 강의 표시
# ==========================
if selected_lecture:
    st.subheader(selected_lecture["title"])

    st.write(selected_lecture["description"])

    st.video(selected_lecture["watch_url"])

    st.link_button(
        "🔗 새 탭에서 따로 보기",
        selected_lecture["watch_url"]
    )

# ==========================
# 전체 강의 목록
# ==========================
st.markdown("---")
st.subheader("전체 강의 현황")

summary = []

for subject, items in LECTURES.items():
    summary.append({
        "과목": subject,
        "강의 수": len(items)
    })

df = pd.DataFrame(summary)

st.dataframe(
    df,
    use_container_width=True,
    hide_index=True
)
