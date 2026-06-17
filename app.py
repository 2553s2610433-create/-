import streamlit as st
from datetime import date

st.set_page_config(
    page_title="Study D-Day Dashboard",
    page_icon="📚",
    layout="centered"
)

# 시험일
EXAM_DATE = date(2026, 6, 30)

today = date.today()
days_left = (EXAM_DATE - today).days

st.title("📚 Study D-Day Dashboard")
st.caption("시험일까지 남은 시간을 확인하고 공부 계획을 세워보세요.")

# D-Day 표시
st.subheader("🎯 시험 D-Day")

if days_left > 0:
    st.metric("남은 기간", f"D-{days_left}")
elif days_left == 0:
    st.success("🔥 오늘이 시험일입니다!")
else:
    st.error(f"시험이 {-days_left}일 지났습니다.")

# 진행률 계산
START_DATE = date(2026, 1, 1)

total_days = (EXAM_DATE - START_DATE).days
elapsed_days = (today - START_DATE).days

if total_days > 0:
    progress = max(0.0, min(1.0, elapsed_days / total_days))
else:
    progress = 0.0

st.subheader("📈 시험일까지의 시간 진행률")
st.progress(progress)
st.write(f"{progress * 100:.1f}% 진행")

st.divider()

# 공부 목표 설정
st.subheader("📝 공부 목표 관리")

goal_hours = st.number_input(
    "총 공부 목표 시간",
    min_value=0.0,
    value=300.0,
    step=10.0
)

studied_hours = st.number_input(
    "현재까지 공부한 시간",
    min_value=0.0,
    value=100.0,
    step=1.0
)

# 목표 달성률
if goal_hours > 0:
    study_progress = min(100.0, (studied_hours / goal_hours) * 100)
else:
    study_progress = 0.0

st.write("### 📊 공부 진행률")
st.progress(min(study_progress / 100, 1.0))
st.write(f"{study_progress:.1f}% 달성")

remaining_hours = max(0.0, goal_hours - studied_hours)

col1, col2 = st.columns(2)

with col1:
    st.metric("남은 공부 시간", f"{remaining_hours:.1f}시간")

with col2:
    if days_left > 0:
        daily_needed = remaining_hours / days_left
        st.metric("하루 필요 공부량", f"{daily_needed:.1f}시간")
    else:
        st.metric("하루 필요 공부량", "-")

st.divider()

# 응원 메시지
st.subheader("💪 오늘의 메시지")

if days_left > 100:
    st.info("꾸준함이 가장 큰 무기입니다. 매일 조금씩 전진하세요!")
elif days_left > 30:
    st.warning("실전 대비를 시작할 좋은 시기입니다.")
elif days_left > 7:
    st.warning("마무리 정리와 문제풀이에 집중하세요!")
elif days_left > 0:
    st.error("마지막 스퍼트입니다. 컨디션 관리도 중요합니다!")
else:
    st.success("수고하셨습니다! 최선을 다한 자신을 칭찬하세요. 🎉")

st.divider()

st.caption("Study D-Day Dashboard • Streamlit")
