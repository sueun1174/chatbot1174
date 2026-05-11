import streamlit as st
from openai import OpenAI

# =========================
# 기본 설정
# =========================
st.set_page_config(
    page_title="잠들기 전 대화 챗봇",
    page_icon="🌙",
    layout="centered"
)

# =========================
# 다크 감성 CSS
# =========================
st.markdown("""
<style>
/* 전체 배경 */
.stApp {
    background: radial-gradient(circle at top, #1e293b 0%, #020617 75%);
    color: #F8FAFC;
}

/* 상단 여백 */
.block-container {
    padding-top: 3rem;
    max-width: 760px;
}

/* 제목 */
h1 {
    color: #F8FAFC !important;
    text-align: center;
    font-size: 2.4rem !important;
    font-weight: 700 !important;
    margin-bottom: 0.5rem;
}

/* 설명 텍스트 */
p, label {
    color: #CBD5E1 !important;
}

/* API 입력창 */
.stTextInput input {
    background-color: rgba(15, 23, 42, 0.9);
    color: #F8FAFC;
    border: 1px solid #334155;
    border-radius: 14px;
    padding: 12px;
}

/* 정보 박스 */
.stAlert {
    background-color: rgba(30, 41, 59, 0.75);
    border-radius: 14px;
    color: #E2E8F0;
}

/* 채팅 메시지 카드 */
[data-testid="stChatMessage"] {
    background-color: rgba(255, 255, 255, 0.06);
    border: 1px solid rgba(148, 163, 184, 0.18);
    border-radius: 20px;
    padding: 14px 16px;
    margin-bottom: 14px;
    box-shadow: 0 8px 24px rgba(0, 0, 0, 0.25);
}

/* 채팅 입력창 */
[data-testid="stChatInput"] {
    background-color: rgba(2, 6, 23, 0.8);
    border-radius: 18px;
}

/* 버튼 */
.stButton button {
    background-color: rgba(148, 163, 184, 0.16);
    color: #F8FAFC;
    border: 1px solid rgba(148, 163, 184, 0.25);
    border-radius: 999px;
    padding: 0.5rem 1rem;
}

.stButton button:hover {
    background-color: rgba(148, 163, 184, 0.28);
    border-color: rgba(226, 232, 240, 0.5);
}

/* 감성 카드 */
.moon-card {
    background: rgba(15, 23, 42, 0.75);
    border: 1px solid rgba(148, 163, 184, 0.18);
    border-radius: 24px;
    padding: 24px;
    margin: 18px 0 24px 0;
    box-shadow: 0 18px 45px rgba(0, 0, 0, 0.35);
}

.sub-text {
    text-align: center;
    color: #CBD5E1;
    font-size: 0.95rem;
    line-height: 1.7;
}

.good-night {
    background: linear-gradient(135deg, rgba(30, 41, 59, 0.9), rgba(51, 65, 85, 0.55));
    border: 1px solid rgba(148, 163, 184, 0.22);
    border-radius: 20px;
    padding: 18px;
    margin-top: 16px;
    color: #E2E8F0;
    text-align: center;
    font-size: 0.95rem;
}
</style>
""", unsafe_allow_html=True)

# =========================
# 화면 상단
# =========================
st.title("🌙 잠들기 전 대화")

st.markdown("""
<div class="moon-card">
    <p class="sub-text">
        오늘 하루를 조용히 돌아보고,<br>
        복잡한 마음과 내일 할 일을 천천히 정리하는 밤의 대화 공간입니다.
    </p>
</div>
""", unsafe_allow_html=True)

# =========================
# API KEY 입력
# =========================
openai_api_key = st.text_input("OpenAI API 키를 입력하세요", type="password")

if not openai_api_key:
    st.info("계속하려면 OpenAI API 키가 필요합니다.", icon="🗝️")

else:
    client = OpenAI(api_key=openai_api_key)

    # =========================
    # 세션 상태 초기화
    # =========================
    if "messages" not in st.session_state:
        st.session_state.messages = [
            {
                "role": "system",
                "content": """
너는 잠들기 전 사용자의 하루와 감정을 정리해주는 다정한 AI 대화 선생님이다.

역할:
- 사용자의 하루를 차분하게 회고하도록 돕는다.
- 스트레스와 감정을 부드럽게 정리해준다.
- 내일 해야 할 일을 정리하고 우선순위를 잡아준다.
- 사용자가 잠들기 전 마음을 내려놓을 수 있도록 돕는다.
- 사용자의 감정을 판단하지 않고 존중한다.

답변 방식:
1. 먼저 사용자의 말을 부드럽게 받아준다.
2. 사용자가 말한 하루의 핵심 감정을 정리한다.
3. 스트레스가 있다면 가벼운 호흡, 내려놓기, 정리 루틴을 제안한다.
4. 내일 할 일이 있다면 보기 쉽게 정리한다.
5. 마지막에는 짧고 따뜻한 잠들기 전 한마디를 남긴다.

답변 구조:
- 오늘의 마음 정리
- 괜찮았던 점
- 내려놓아도 되는 것
- 내일 할 일 정리
- 잠들기 전 한마디

말투:
- 조용하고 다정한 말투를 사용한다.
- 너무 밝거나 가볍게 말하지 않는다.
- 과한 이모지는 사용하지 않는다.
- 한국어로 답변한다.
- “오늘은 여기까지 해도 충분합니다”, “천천히 쉬어도 괜찮습니다” 같은 안정적인 표현을 사용한다.

주의:
- 의학적 진단이나 치료처럼 말하지 않는다.
- 사용자가 심각한 위기 상황을 말하면 혼자 버티지 말고 가까운 사람이나 전문가에게 도움을 요청하라고 안내한다.
"""
            }
        ]

    # =========================
    # 빠른 입력 버튼
    # =========================
    st.markdown("#### 오늘은 어떤 밤인가요?")

    col1, col2, col3 = st.columns(3)

    with col1:
        if st.button("😌 차분한 하루"):
            st.session_state.quick_prompt = "오늘은 비교적 차분한 하루였어요. 잠들기 전에 하루를 정리하고 싶어요."

    with col2:
        if st.button("😵 피곤한 하루"):
            st.session_state.quick_prompt = "오늘 너무 피곤했어요. 마음이 복잡해서 잠들기 전에 정리하고 싶어요."

    with col3:
        if st.button("📋 내일 준비"):
            st.session_state.quick_prompt = "내일 해야 할 일들이 많아요. 잠들기 전에 우선순위를 정리하고 싶어요."

    # =========================
    # 기존 메시지 출력
    # =========================
    for message in st.session_state.messages:
        if message["role"] != "system":
            with st.chat_message(message["role"]):
                st.markdown(message["content"])

    # =========================
    # 사용자 입력 처리
    # =========================
    user_input = None

    if "quick_prompt" in st.session_state:
        user_input = st.session_state.quick_prompt
        del st.session_state.quick_prompt

    prompt = st.chat_input("오늘 하루는 어땠나요? 내일 할 일도 함께 적어보세요.")

    if prompt:
        user_input = prompt

    if user_input:
        st.session_state.messages.append(
            {"role": "user", "content": user_input}
        )

        with st.chat_message("user"):
            st.markdown(user_input)

        with st.chat_message("assistant"):
            stream = client.chat.completions.create(
                model="gpt-4o-mini",
                messages=st.session_state.messages,
                stream=True,
            )

            response = st.write_stream(stream)

        st.session_state.messages.append(
            {"role": "assistant", "content": response}
        )

    # =========================
    # 하단 감성 문구
    # =========================
    st.markdown("""
    <div class="good-night">
        오늘을 완벽하게 끝내지 않아도 괜찮습니다.<br>
        지금은 천천히 내려놓고 쉬어도 되는 시간입니다.
    </div>
    """, unsafe_allow_html=True)
