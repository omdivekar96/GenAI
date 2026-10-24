#loading env variables......
from dotenv import load_dotenv
load_dotenv()


from langchain_community.utilities import GoogleSerperAPIWrapper   #library for google search agent...
from langchain_groq import ChatGroq  
from langchain.agents import create_agent  #agent framework
from langgraph.checkpoint.memory import MemorySaver  #memory framework

search=GoogleSerperAPIWrapper()
llm=ChatGroq(model="qwen/qwen3.6-27b")
agent=create_agent(model=llm,
                     tools=[search.run],
                     system_prompt='you are a google search agent',
                     checkpointer=MemorySaver())#connecting memory and agent to llm......

while True:
    query=input('\n',"Search Anything (User): ")
    if query.lower() in ['end','stop','exit']:
       print('goodbye')
       break

    res=agent.invoke({'messages':[{'role':'user','content':query}]},
                     {'configurable':{'thread_id':"omi123"}})#storing convo with unique id.....
    print('\n','AI: ', res['messages'][-1].content,'\n')




