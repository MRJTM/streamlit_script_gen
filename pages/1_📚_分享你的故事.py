import streamlit as st
from openai import OpenAI

st.set_page_config(page_title="分享你的故事", page_icon="📈")
st.sidebar.header("请分享你的故事")

st.title("Visal Bot")

client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"],base_url=st.secrets["BASE_URL"])
if "openai_model" not in st.session_state:
    st.session_state['openai_model']="gpt-4o-mini-2024-07-18"

def response_generator():
    # response = random.choice(
    #     [
    #         "Hello there! How can I assist you today?",
    #         "Hi, human! Is there anything I can help you with?",
    #         "Do you need help?",
    #     ]
    # )
    # # word by word output
    # for word in response.split():
    #     yield word + " "
    #     time.sleep(0.05)

    stream = client.chat.completions.create(
        model=st.session_state["openai_model"],
        messages=[
            {"role": m["role"], "content": m["content"]}
            for m in st.session_state.messages
        ],
        stream=True,
    )
    return stream

# Initialize chat history
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display chat messages from history on app rerun
for message in st.session_state.messages:
    if "role" in message and "content" in message:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

# 相应chat-input的输入
if prompt := st.chat_input("你想聊点什么？"):
    # Display user message in chat message container
    with st.chat_message("user"):
        st.markdown(prompt)
    # Add user message to chat history
    st.session_state.messages.append({"role": "user", "content": prompt})

    # Display assistant response in chat message container
    with st.chat_message("assistant"):
        response = st.write_stream(response_generator())

    # Add assistant response to chat history
    st.session_state.messages.append({"role": "assistant", "content": response})