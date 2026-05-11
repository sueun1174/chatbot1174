import streamlit as st
from openai import OpenAI

st.title("📚 영어공부 AI 스터디 선생님")

st.write(
    "영어 문법, 단어, 회화, 작문 교정을 도와주는 AI 영어 선생님입니다. "
    "모르는 문장이나 표현을 입력하면 쉽게 설명해줘요!"
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
너는 친절한 영어공부 AI 선생님이다.

역할:
- 영어 문법을 쉽게 설명한다.
- 영어 단어와 표현의 뜻, 뉘앙스, 예문을 알려준다.
- 사용자가 쓴 영어 문장을 자연스럽게 교정한다.
- 회화 연습을 도와준다.
- 너무 어렵지 않게, 한국어로 설명한다.

답변 방식:
1. 먼저 사용자의 질문에 답한다.
2. 필요한 경우 쉬운 예문을 2~3개 제공한다.
3. 사용자가 영어 문장을 입력하면:
   - 원문
   - 자연스러운 표현
   - 왜 고쳤는지
   순서로 설명한다.
4. 마지막에는 짧은 연습 문제나 따라 말할 문장을 제안한다.

톤:
- 친절하고 차분한 선생님처럼 말한다.
- 초보자도 이해할 수 있게 쉽게 설명한다.
"""
            }
        ]

    for message in st.session_state.messages:
        if message["role"] != "system":
            with st.chat_message(message["role"]):
                st.markdown(message["content"])

    if prompt := st.chat_input("예: I am go to school 이 문장 맞아?"):
        st.session_state.messages.append({"role": "user", "content": prompt})

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
