import streamlit as st
from openai import OpenAI

st.title("✈️ 여행 플래너 챗봇")

st.write(
    "여행지 추천, 일정 짜기, 맛집 추천, 교통 안내, 예산 계획까지 도와주는 여행용 챗봇입니다. "
    "가고 싶은 지역, 여행 기간, 예산, 취향을 입력해보세요!"
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
너는 친절한 여행 전문 챗봇이다.
사용자의 여행 목적지, 일정, 예산, 취향을 바탕으로 여행 계획을 추천한다.

답변할 때는 다음을 포함해라:
1. 추천 여행 일정
2. 이동 동선
3. 맛집 또는 카페 추천
4. 예상 비용
5. 여행 팁

답변은 한국어로 하고, 너무 딱딱하지 않게 설명해라.
사용자가 정보가 부족하게 말하면 필요한 질문을 자연스럽게 물어봐라.
"""
            }
        ]

    for message in st.session_state.messages:
        if message["role"] != "system":
            with st.chat_message(message["role"]):
                st.markdown(message["content"])

    if prompt := st.chat_input("예: 제주도 2박 3일 여행 일정 짜줘"):
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
