import streamlit as st
from openai import OpenAI

# 페이지 설정
st.set_page_config(
    page_title="잠들기 전 대화 챗봇",
    page_icon="🌙",
    layout="centered"
)

# 다크모드 스타일
st.markdown("""
<style>
.stApp {
    background: linear-gradient(180deg, #111827 0%, #1f2937 100%);
    color: #F9FAFB;
}

h1, h2, h3, p, label {
    color: #F9FAFB !important;
}

.stTextInput input {
    background-color: #374151;
    color: #F9FAFB;
    border-radius: 12px;
    border: 1px solid #4B5563;
}

.stChatInput {
    background-color: #111827;
}

[data-testid="stChatMessage"] {
    background-color: rgba(255, 255, 255, 0.06);
    border-radius: 16px;
    padding: 12px;
    margin-bottom: 10px;
}
</style>
""", unsafe_allow_html=True)

st.title("🌙 잠들기 전 대화 챗봇")

st.write(
    "오늘 하루를 차분히 돌아보고, 마음을 정리한 뒤 편안하게 잠들 수 있도록 도와주는 AI 챗봇입니다."
)

openai_api_key = st.text_input("OpenAI API 키를 입력하세요", type="password")

if not openai_api_key:
    st.info("계속하려면 OpenAI API 키가 필요합니다.", icon="🗝️")

else:
    client = OpenAI(api_key=openai_api_key)

    if "messages" not in st.session_state:
        st.session_state.messages = [
            {
                "role": "system",
                "content": """
너는 잠들기 전 사용자의 마음을 차분하게 정리해주는 감성적인 AI 대화 친구다.

역할:
- 사용자의 하루를 부드럽게 회고하도록 돕는다.
- 스트레스와 감정을 차분히 정리해준다.
- 사용자가 잠들기 전 마음이 편안해지도록 따뜻한 말을 건넨다.
- 내일 해야 할 일을 정리하고 우선순위를 세울 수 있게 돕는다.
- 사용자의 말을 판단하지 않고 공감한다.

대화 방식:
1. 먼저 사용자의 감정과 상황을 부드럽게 받아준다.
2. 사용자가 하루를 말하면 핵심 감정을 정리해준다.
3. 스트레스가 있어 보이면 가벼운 호흡, 정리, 내려놓기 루틴을 제안한다.
4. 내일 할 일을 말하면 중요도 순서로 정리해준다.
5. 마지막에는 잠들기 전 한마디를 짧고 따뜻하게 전한다.

말투:
- 조용하고 다정한 말투를 사용한다.
- 너무 활발하거나 가볍게 말하지 않는다.
- 과한 이모지는 사용하지 않는다.
- “괜찮아요”, “오늘은 여기까지 해도 충분합니다”, “천천히 내려놓아도 됩니다” 같은 안정감을 주는 표현을 사용한다.
- 답변은 한국어로 한다.

답변 구조:
- 공감 한마디
- 오늘의 감정 정리
- 마음을 가라앉히는 제안
- 내일을 위한 작은 정리
- 잠들기 전 한마디

주의:
- 의학적 진단이나 치료처럼 말하지 않는다.
- 사용자가 심각한 위기 상황을 말하면, 혼자 버티지 말고 가까운 사람이나 전문가에게 도움을 요청하라고 안내한다.
"""
            }
        ]

    # 기존 메시지 출력
    for message in st.session_state.messages:
        if message["role"] != "system":
            with st.chat_message(message["role"]):
                st.markdown(message["content"])

    # 사용자 입력
    if prompt := st.chat_input("오늘 하루는 어땠나요? 내일 할 일도 함께 적어보세요."):
        st.session_state.messages.append(
            {"role": "user", "content": prompt}
        )

        with st.chat_message("user"):
            st.markdown(prompt)

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
