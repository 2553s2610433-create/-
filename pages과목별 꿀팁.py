import streamlit as st
import random

# Gemini 라이브러리
try:
    from google import genai
except Exception:
    genai = None

st.set_page_config(
    page_title="과목별 공부 꿀팁 안내소",
    page_icon="📚",
    layout="wide"
)

# -----------------------
# 데이터
# -----------------------

tips = {
    "국어": {
        "공부법": [
            "교과서를 여러 번 읽기",
            "핵심 내용을 스스로 설명해보기",
            "지문을 읽고 요약하기"
        ],
        "시험 팁": [
            "문제보다 지문을 먼저 이해하기",
            "선지의 차이를 비교하기"
        ],
        "암기 팁": [
            "문학 작품 특징 정리하기",
            "비문학 핵심어 표시하기"
        ]
    },
    "수학": {
        "공부법": [
            "개념 → 예제 → 유형 → 응용 순서로 공부",
            "틀린 문제 오답노트 만들기"
        ],
        "시험 팁": [
            "쉬운 문제부터 풀기",
            "계산 실수 검토 시간 확보"
        ],
        "암기 팁": [
            "공식의 의미를 이해하며 암기하기"
        ]
    },
    "영어": {
        "공부법": [
            "매일 단어 암기",
            "지문 해석 연습"
        ],
        "시험 팁": [
            "문맥으로 단어 뜻 추론하기",
            "시간 배분 연습"
        ],
        "암기 팁": [
            "단어를 문장과 함께 외우기"
        ]
    },
    "사회": {
        "공부법": [
            "개념 연결하며 공부",
            "지도와 자료 분석 연습"
        ],
        "시험 팁": [
            "그래프와 표 문제 대비"
        ],
        "암기 팁": [
            "마인드맵 활용"
        ]
    },
    "과학": {
        "공부법": [
            "원리 이해 중심 학습",
            "실험 과정 정리"
        ],
        "시험 팁": [
            "계산 문제 반복 연습"
        ],
        "암기 팁": [
            "그림과 함께 암기"
        ]
    }
}

quotes = [
    "오늘의 노력이 내일의 실력이 된다.",
    "천재는 노력하는 사람을 이길 수 없다.",
    "작은 습관이 큰 결과를 만든다.",
    "포기하지 않는 사람이 결국 이긴다.",
    "공부는 미래의 나에게 주는 선물이다."
]

# -----------------------
# 제목
# -----------------------

st.title("📚 과목별 공부 꿀팁 안내소")
st.write("과목별 공부법과 AI 공부 상담을 제공하는 앱입니다.")

# -----------------------
# 오늘의 명언
# -----------------------

st.subheader("🌟 오늘의 공부 명언")

if "quote" not in st.session_state:
    st.session_state.quote = random.choice(quotes)

st.info(st.session_state.quote)

# -----------------------
# 과목별 팁
# -----------------------

st.subheader("📖 과목별 공부 꿀팁")

subject = st.selectbox(
    "과목 선택",
    list(tips.keys())
)

with st.container():
    st.markdown("### 📌 공부법")

    for item in tips[subject]["공부법"]:
        st.write("✅", item)

    st.markdown("### 📝 시험 팁")

    for item in tips[subject]["시험 팁"]:
        st.write("✅", item)

    st.markdown("### 🧠 암기 팁")

    for item in tips[subject]["암기 팁"]:
        st.write("✅", item)

# -----------------------
# 공부 계획 추천
# -----------------------

st.subheader("⏰ 공부 계획 추천")

study_time = st.slider(
    "하루 공부 가능 시간(시간)",
    1,
    10,
    3
)

focus_subject = st.selectbox(
    "집중할 과목",
    list(tips.keys()),
    key="planner"
)

if st.button("공부 계획 만들기"):

    main_time = int(study_time * 0.6)
    review_time = study_time - main_time

    st.success("추천 공부 계획")

    st.write(f"📚 {focus_subject}: {main_time}시간")
    st.write(f"🔄 복습: {review_time}시간")
    st.write("📝 자기 전 10분 복습하기")

# -----------------------
# AI 공부 상담
# -----------------------

st.subheader("🤖 AI 공부 상담")

question = st.text_area(
    "공부 관련 질문을 입력하세요"
)

if st.button("AI에게 질문하기"):

    if not question.strip():
        st.warning("질문을 입력해주세요.")
    else:
        try:

            api_key = st.secrets["GEMINI_API_KEY"]

            if genai is None:
                st.error("Gemini 라이브러리를 불러올 수 없습니다.")
            else:

                client = genai.Client(api_key=api_key)

                prompt = f"""
                너는 학생을 도와주는 친절한 공부 코치다.

                질문:
                {question}

                쉬운 말로 설명하고,
                실천 가능한 공부 팁도 함께 알려줘.
                """

                response = client.models.generate_content(
                    model="gemini-2.5-flash-lite",
                    contents=prompt
                )

                st.markdown("### 💡 AI 답변")
                st.write(response.text)

        except KeyError:
            st.error(
                "GEMINI_API_KEY가 설정되지 않았습니다."
            )

        except Exception as e:
            st.error(
                f"AI 응답 중 오류가 발생했습니다.\n\n{e}"
            )

# -----------------------
# 하단
# -----------------------

st.divider()

st.caption("Made with Streamlit + Gemini")
