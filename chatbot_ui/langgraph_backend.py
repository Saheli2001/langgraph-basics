from langgraph.graph import StateGraph, START, END
from langchain_openai import ChatOpenAI
from dotenv import load_dotenv
from typing import TypedDict, Annotated
from langchain_core.messages import BaseMessage, HumanMessage
from langgraph.graph.message import add_messages
from langgraph.checkpoint.memory import MemorySaver #Memorysaver is a RAM based checkpointer. In production, we use databases to store data which is to be used even after the program is closed

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

checkpointer = MemorySaver()

graph = StateGraph(ChatState)

graph.add_node('chat_node', chat_node)

graph.add_edge(START, 'chat_node')
graph.add_edge('chat_node', END)

chatbot = graph.compile(checkpointer=checkpointer)

# thread_id = 'thread-1'
# CONFIG = {'configurable': {'thread_id': thread_id}}

# response = chatbot.invoke(
#             {'messages': [HumanMessage(content='Hi')]}, 
#             config= {'configurable': {'thread_id': thread_id}}, 
#             stream_mode= 'messages'
#         )

# print(chatbot.get_state(config=CONFIG).values['messages'])