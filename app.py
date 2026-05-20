import streamlit as st
st.title('천안오성고등학교 화이팅')
st.write('바이브코딩 재미있다')
import streamlit as st
import pandas as pd
import numpy as np

# 페이지 설정
st.set_page_config(
    page_title="My Streamlit App",
    page_icon="🚀",
    layout="wide"
)

# 세션 상태 초기화
if "messages" not in st.session_state:
    st.session_state.messages = []

# 사이드바
with st.sidebar:
    st.title("📌 메뉴")

    menu = st.radio(
        "이동",
        ["홈", "데이터 분석", "AI 챗봇"]
    )

    st.divider()

    st.info("스트림릿 웹앱 예제")

# 홈 화면
if menu == "홈":

    st.title("🚀 Streamlit 웹앱")

    st.write("이 앱은 Streamlit 기본 템플릿입니다.")

    col1, col2, col3 = st.columns(3)

    with col1:
        st.metric("사용자", 128)

    with col2:
        st.metric("매출", "$12,340")

    with col3:
        st.metric("성장률", "23%")

    st.divider()

    st.subheader("📈 샘플 차트")

    chart_data = pd.DataFrame(
        np.random.randn(20, 3),
        columns=["A", "B", "C"]
    )

    st.line_chart(chart_data)

# 데이터 분석 페이지
elif menu == "데이터 분석":

    st.title("📊 데이터 분석")

    uploaded_file = st.file_uploader(
        "CSV 파일 업로드",
        type=["csv"]
    )

    if uploaded_file:

        df = pd.read_csv(uploaded_file)

        st.subheader("데이터 미리보기")
        st.dataframe(df)

        st.subheader("기초 통계")
        st.write(df.describe())

        numeric_cols = df.select_dtypes(include=np.number).columns

        if len(numeric_cols) > 0:

            selected_col = st.selectbox(
                "차트 컬럼 선택",
                numeric_cols
            )

            st.line_chart(df[selected_col])

# AI 챗봇 페이지
elif menu == "AI 챗봇":

    st.title("🤖 AI 챗봇")

    # 이전 메시지 출력
    for msg in st.session_state.messages:

        with st.chat_message(msg["role"]):
            st.markdown(msg["content"])

    # 사용자 입력
    prompt = st.chat_input("메시지를 입력하세요")

    if prompt:

        # 사용자 메시지 저장
        st.session_state.messages.append({
            "role": "user",
            "content": prompt
        })

        with st.chat_message("user"):
            st.markdown(prompt)

        # 임시 AI 응답
        response = f"'{prompt}' 라고 입력하셨네요!"

        st.session_state.messages.append({
            "role": "assistant",
            "content": response
        })

        with st.chat_message("assistant"):
            st.markdown(response)
