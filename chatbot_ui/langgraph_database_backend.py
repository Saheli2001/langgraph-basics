from langgraph.graph import StateGraph, START, END
from langchain_openai import ChatOpenAI
from dotenv import load_dotenv
from typing import TypedDict, Annotated
from langchain_core.messages import BaseMessage, HumanMessage
from langgraph.graph.message import add_messages
from langgraph.checkpoint.sqlite import SqliteSaver
import sqlite3
load_dotenv()  # Load environment variables from .env file

class ChatState(TypedDict):

    messages: Annotated[list[BaseMessage] , add_messages]

llm = ChatOpenAI(model='gpt-4o-mini')

def chat_node(state: ChatState):
    #user quesry
    messages = state['messages']

    #send to llm
    response = llm.invoke(messages)
    # print(response)
# 
    #store to state
    return {'messages': [response]}

conn = sqlite3.connect(database='chatbot.db', check_same_thread=False)
checkpointer = SqliteSaver(conn)

graph = StateGraph(ChatState)

graph.add_node('chat_node', chat_node)

graph.add_edge(START, 'chat_node')
graph.add_edge('chat_node', END)

chatbot = graph.compile(checkpointer=checkpointer)

def retrieve_all_threads():
    all_threads = set()
    for c in checkpointer.list(None):
        all_threads.add(c.config['configurable']['thread_id'])
    return list(all_threads)

# thread_id = 'thread-1'
# CONFIG = {'configurable': {'thread_id': thread_id}}

# response = chatbot.invoke(
#             {'messages': [HumanMessage(content='Hi')]}, 
#             config= {'configurable': {'thread_id': thread_id}}, 
#             stream_mode= 'messages'
#         )

# print(chatbot.get_state(config=CONFIG).values['messages'])