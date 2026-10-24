# from dotenv import load_dotenv
# load_dotenv()

# from langchain_groq import ChatGroq
# llm=ChatGroq(model='qwen/qwen3.6-27b')
# while True:
#     query=input('user:')
    
#     if query.lower in ['bye','stop','exit','end']:
#        print("goodbye!")
#     break
# res=llm.invoke(query)
# print('AI: ',res.content)
# above is our qna chatbot


#.................................................................................

#now to convert this chatbot into a webapp we are using streamlit
from dotenv import load_dotenv
load_dotenv()
import streamlit as st
from langchain_groq import ChatGroq

llm=ChatGroq(model='qwen/qwen3.6-27b')


st.title('QNA Chatbot!!')
st.markdown('QNA bot with Groq')

# now we are adding memory to bot.....
if 'messages' not in st.session_state:
  st.session_state.messages=[]#here we created a backend memory by session_state of variable messages


for message in st.session_state.messages:#printing previous messages using loop
   role=message['role']
   content=message['content']
   st.chat_message(role).markdown(content)
   
query=st.chat_input("Ask Anything?.....")


if query:   #created actual chat window
    if query.lower() in ["exit", "bye", "stop", "end"]:
            st.markdown("Thanks for using chatbot!")
    
    else:        
        st.session_state.messages.append({'role':'user','content':query})
        st.chat_message('human').markdown(query)
        res=llm.invoke(query)
        st.chat_message('ai').markdown(res.content)
        st.session_state.messages.append({'role':'ai','content':res.content})
        


