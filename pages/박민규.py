import streamlit as st
import random

# Gemini 라이브러리
try:
    from google import genai
except:
    genai = None

st.set_page_config(
    page_title="과목별 공부 꿀팁 가이드",
    page_icon="📚",
    layout="wide"
)

# ------------------
# 공부 명언
# ------------------

quotes = [
    "오늘의 노력이 내일의 실력이 된다.",
    "포기하지 않는 사람이 결국 이긴다.",
    "천천히 가도 멈추지만 않으면 된다.",
    "공부는 미래의 나에게 주는 선물이다.",
    "꾸준함은 재능을 이긴다."
]

st.title("📚 과목별 공부 꿀팁 가이드")

st.info(f"💡 오늘의 명언\n\n{random.choice(quotes)}")

# ------------------
# 과목별 꿀팁
# ------------------

tips = {
    "국어": """
✔ 지문을 읽으며 핵심 문장 표시하기

✔ 문제를 먼저 보고 지문 읽기

✔ 틀린 문제는 오답노트 작성

✔ 독서 습관 기르기
""",
    "수학": """
✔ 개념 이해 후 문제 풀이

✔ 오답노트 작성하기

✔ 매일 30분 이상 꾸준히 풀기

✔ 풀이 과정을 직접 써보기
""",
    "영어": """
✔ 영단어 매일 암기

✔ 짧은 지문 매일 읽기

✔ 문법 개념 정리하기

✔ 틀린 단어 반복 학습
""",
    "사회": """
✔ 흐름 중심으로 이해하기

✔ 마인드맵 활용하기

✔ 표와 그래프 분석 연습

✔ 암기보다 이해 우선
""",
    "과학": """
✔ 원리 이해 후 암기

✔ 실험 과정 정리하기

✔ 그림과 도표 활용

✔ 개념 연결해서 공부하기
"""
}

st.header("📖 과목별 공부 꿀팁")

subject = st.selectbox(
    "과목 선택",
    list(tips.keys())
)

st.success(tips[subject])

# ------------------
# 시험 대비 전략
# ------------------

st.header("📝 시험 대비 전략")

strategy = st.radio(
    "시기 선택",
    ["시험 1주 전", "시험 3일 전", "시험 전날"]
)

if strategy == "시험 1주 전":
    st.write("""
- 전 범위 개념 정리
- 오답노트 확인
- 부족한 과목 집중 학습
    """)

elif strategy == "시험 3일 전":
    st.write("""
- 기출문제 풀이
- 핵심 내용 암기
- 실수 줄이기 연습
    """)

else:
    st.write("""
- 가볍게 복습
- 새로운 내용 공부 금지
- 충분한 수면
    """)

# ------------------
# AI 공부 조언
# ------------------

st.header("🤖 AI 맞춤 공부 조언")

question = st.text_area(
    "공부 고민을 입력하세요",
    height=120,
    placeholder="예: 수학 점수가 잘 안 올라요."
)

if st.button("조언 받기"):

    if not question.strip():
        st.warning("고민을 입력해주세요.")
    else:

        if genai is None:
            st.error("Gemini 라이브러리가 설치되지 않았습니다.")
        else:
            try:
                api_key = st.secrets["GEMINI_API_KEY"]

                client = genai.Client(api_key=api_key)

                prompt = f"""
너는 친절한 공부 코치다.

학생 고민:
{question}

학생이 이해하기 쉽게
구체적인 공부 방법을 알려줘.
"""

                response = client.models.generate_content(
                    model="gemini-2.5-flash-lite",
                    contents=prompt
                )

                st.markdown("### 📌 AI 조언")
                st.write(response.text)

            except KeyError:
                st.error(
                    "GEMINI_API_KEY가 Secrets에 설정되지 않았습니다."
                )

            except Exception as e:
                st.error(f"오류가 발생했습니다: {e}")

# ------------------
# 푸터
# ------------------

st.divider()
st.caption("📚 과목별 공부 꿀팁 가이드")
