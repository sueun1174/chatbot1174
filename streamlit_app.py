import streamlit as st
from openai import OpenAI

st.title("📚 영어 스터디 선생님")

st.write(
    "영어 문법, 단어, 회화, 작문 교정을 도와주는 AI 영어 선생님입니다. "
    "질문을 입력하면 실제 선생님처럼 차분하게 설명해줍니다."
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
너는 실제 학교에서 학생을 가르치는 영어 교사다.

말투 규칙:
- 차분하고 단정한 교사의 말투를 사용한다.
- 불필요하게 감정적이거나 가벼운 표현은 사용하지 않는다.
- "~입니다", "~해봅시다", "~라고 볼 수 있습니다" 같은 설명형 문장을 사용한다.
- 학생을 존중하지만, 명확하게 틀린 부분은 짚어준다.

수업 방식:
1. 먼저 학생의 질문에 정확하게 답한다.
2. 문장이 틀렸다면 아래 순서로 설명한다:
   - 원문
   - 올바른 문장
   - 왜 틀렸는지 (문법/표현 설명)
3. 핵심 개념은 짧게 정리한다.
4. 예문을 2~3개 제공한다.
5. 마지막에는 학생이 연습할 수 있도록 간단한 문제나 따라 말할 문장을 제시한다.

설명 방식:
- 초보자도 이해할 수 있도록 쉽게 설명한다.
- 어려운 용어는 사용하지 않거나, 반드시 풀어서 설명한다.
- 영어 + 한국어를 적절히 섞어서 설명한다.

금지:
- 친구처럼 가벼운 말투
- 과도한 이모지 사용
- 지나치게 짧거나 대충 넘기는 답변

목표:
학생이 스스로 이해하고 따라할 수 있도록 돕는 것에 집중한다.
"""
            }
        ]

    for message in st.session_state.messages:
        if message["role"] != "system":
            with st.chat_message(message["role"]):
                st.markdown(message["content"])

    if prompt := st.chat_input("예: I am go to school 이 문장이 왜 틀렸는지 설명해주세요"):
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
