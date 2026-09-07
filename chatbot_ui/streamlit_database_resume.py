import streamlit as st
from langgraph_database_backend import chatbot, retrieve_all_threads
from langchain_core.messages import BaseMessage, HumanMessage
import uuid

def generate_thread_id():
    return str(uuid.uuid4())

def reset_chat():
    thread_id = generate_thread_id()
    st.session_state['thread_id'] = thread_id
    add_thread_to_history(st.session_state['thread_id'])
    st.session_state['message_history'] = []

def add_thread_to_history(thread_id):
    if thread_id not in st.session_state['chat_threads']:
        st.session_state['chat_threads'].append(thread_id)

def load_chat(thread_id):
    state = chatbot.get_state(config={'configurable': {'thread_id': thread_id}})
    # Check if messages key exists in state values, return empty list if not
    return state.values.get('messages', [])

thread_id = generate_thread_id()
CONFIG = {'configurable': {'thread_id': thread_id}}
# st.session_state -> dict -> accumulates the state of the chatbot across multiple user interactions. It allows the chatbot to remember previous messages and maintain context throughout the conversation. doesnt go away with Enter

if 'message_history' not in st.session_state:
    st.session_state['message_history'] = []
if 'thread_id' not in st.session_state:
    st.session_state['thread_id'] = generate_thread_id()
if 'chat_threads' not in st.session_state:
    st.session_state['chat_threads'] = retrieve_all_threads()

add_thread_to_history(st.session_state['thread_id'])

st.sidebar.title("Langgraph Chatbot")
if st.sidebar.button('New Chat'):
    reset_chat()

st.sidebar.header("Chat History")

for thread_id in st.session_state['chat_threads'][::-1]:
   if st.sidebar.button(str(thread_id)):
       st.session_state['thread_id'] = thread_id
       messages = load_chat(thread_id)

       temp_history = []
       for m in messages:
            if isinstance(m, HumanMessage):
                temp_history.append({'role': 'user', 'content': m.content})
            else:
                temp_history.append({'role': 'assistant', 'content': m.content})

       st.session_state['message_history'] = temp_history

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
            config= {'configurable': {'thread_id': st.session_state['thread_id']}}, 
            stream_mode= 'messages')
        )
    st.session_state['message_history'].append({'role': 'assistant', 'content': ai_message})

    
