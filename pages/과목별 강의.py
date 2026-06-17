import streamlit as st

st.set_page_config(
    page_title="내신 대비 강의 정리함",
    page_icon="📖",
    layout="wide"
)

# =========================
# 고등학교 강의 데이터
# =========================
LECTURES = {
    "국어": [
        {
            "title": "문학 개념 정리",
            "url": "https://www.youtube.com/watch?v=1N4Aq0tK3nM",
            "desc": "문학 작품 분석 기본 개념",
            "star": True
        },
        {
            "title": "비문학 독해 전략",
            "url": "https://www.youtube.com/watch?v=eIho2S0ZahI",
            "desc": "지문 빠르게 푸는 방법",
            "star": False
        }
    ],
    "수학": [
        {
            "title": "함수 개념 완전정리",
            "url": "https://www.youtube.com/watch?v=YjL3V3J8r0M",
            "desc": "고1 함수 핵심 개념",
            "star": True
        },
        {
            "title": "순열과 조합 기초",
            "url": "https://www.youtube.com/watch?v=L_jWHffIx5E",
            "desc": "경우의 수 기본",
            "star": False
        }
    ],
    "영어": [
        {
            "title": "영문법 핵심 정리",
            "url": "https://www.youtube.com/watch?v=eIho2S0ZahI",
            "desc": "시험에 자주 나오는 문법",
            "star": True
        }
    ],
    "한국사": [
        {
            "title": "근현대사 핵심 요약",
            "url": "https://www.youtube.com/watch?v=1N4Aq0tK3nM",
            "desc": "시험 직전 정리용",
            "star": False
        }
    ],
    "과학": [
        {
            "title": "물리 개념 기초",
            "url": "https://www.youtube.com/watch?v=L_jWHffIx5E",
            "desc": "힘과 운동 기본 개념",
            "star": False
        }
    ]
}

# =========================
# 제목
# =========================
st.title("📖 내신 대비 강의 정리함")
st.caption("고등학교 과목별로 강의를 빠르게 찾아보고 복습할 수 있는 앱")

# =========================
# 과목 탭
# =========================
tabs = st.tabs(list(LECTURES.keys()))

for i, subject in enumerate(LECTURES.keys()):
    with tabs[i]:
        st.subheader(f"📘 {subject}")

        lectures = LECTURES[subject]

        selected = st.selectbox(
            f"{subject} 강의 선택",
            [l["title"] for l in lectures],
            key=subject
        )

        lecture = next(l for l in lectures if l["title"] == selected)

        # 중요 표시
        if lecture["star"]:
            st.markdown("⭐ **시험에 중요한 강의**")

        st.write("📌", lecture["desc"])

        st.video(lecture["url"])

        st.link_button("🔗 유튜브에서 따로 보기", lecture["url"])

        # =========================
        # 간단 메모 기능
        # =========================
        st.markdown("---")
        st.write("📝 나만의 필기")

        memo_key = f"memo_{subject}_{lecture['title']}"

        memo = st.text_area(
            "복습 메모 작성",
            key=memo_key,
            placeholder="여기에 중요한 내용 정리"
        )

# =========================
# 전체 통계
# =========================
st.markdown("---")
st.subheader("📊 전체 강의 현황")

total = sum(len(v) for v in LECTURES.values())

st.write(f"전체 강의 수: **{total}개**")

for subject, lectures in LECTURES.items():
    st.write(f"- {subject}: {len(lectures)}개")
