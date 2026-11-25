from langgraph.graph import StateGraph,START,END
from typing import TypedDict , Annotated   
from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.messages import BaseMessage,HumanMessage
from langgraph.checkpoint.memory import MemorySaver
from langgraph.graph.message import add_messages


class ChatState(TypedDict):
    messages : Annotated[list[BaseMessage],add_messages]

load_dotenv()

llm = ChatGoogleGenerativeAI(
    model = "gemini-3.5-flash-lite",
    temperature = 0

)

def chat_node(state:ChatState):

    messages = state['messages']
    response = llm.invoke(messages)
    return {'messages': [response]}

checkpointer = MemorySaver()

graph = StateGraph(ChatState)

#add node 

graph.add_node('chat_node',chat_node)
graph.add_edge(START,'chat_node')
graph.add_edge('chat_node',END)

chatbot = graph.compile(checkpointer = checkpointer)


# ************************* Streaming **********************************
# stream = chatbot.stream({"messages": [HumanMessage(content="What is the recipe to make pasta?")]}
# ,
#     { "configurable": {"thread_id": "1"}}
# ,
#     stream_mode="messages"
# )

# for message_chunk, metadata in stream:
#     if message_chunk.content:
#         print(message_chunk.content, end=" ", flush=True)







# thread_id = '1'

# while True:
#     user_message = input('Type here ... : ')

#     print("USER : ", user_message)

#     if user_message.strip().lower() in ['exit','bye',quit]:
#         break
    
#     config = {'configurable' : {'thread_id' : thread_id}}

#     response = chatbot.invoke({'messages' : [HumanMessage(content=user_message)]},config=config)

#     print("AI : ", response['messages'][-1].content)