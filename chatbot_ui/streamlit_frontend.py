import streamlit as st
from langgraph_backend import chatbot
from langchain_core.messages import BaseMessage, HumanMessage

thread_id = 'thread-1'
CONFIG = {'configurable': {'thread_id': thread_id}}
# st.session_state -> dict -> accumulates the state of the chatbot across multiple user interactions. It allows the chatbot to remember previous messages and maintain context throughout the conversation. doesnt go away with Enter

if 'message_history' not in st.session_state:
    st.session_state['message_history'] = []


for m in st.session_state['message_history']:
    with st.chat_message(m['role']):
        st.text(m['content'])

user_input = st.chat_input('Say something')

if user_input:
    st.session_state['message_history'].append({'role': 'user', 'content': user_input})
    with st.chat_message('user'):
        st.text(user_input)

    # response = chatbot.invoke({'messages': [HumanMessage(content=user_input)]}, config=CONFIG)
    # ai_message = response['messages'][-1].content
    # st.session_state['message_history'].append({'role': 'assistant', 'content': ai_message})
    with st.chat_message('assistant'):
        ai_message = st.write_stream(
            message_chunk.content for message_chunk, metadata in chatbot.stream(
            {'messages': [HumanMessage(content=user_input)]}, 
            config= {'configurable': {'thread_id': 'thread-1'}}, 
            stream_mode= 'messages')
        )
    st.session_state['message_history'].append({'role': 'assistant', 'content': ai_message})

    
