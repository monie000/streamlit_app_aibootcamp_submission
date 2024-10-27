import streamlit as st
from openai import OpenAI
from dotenv import load_dotenv
import pandas as pd
import os
from bs4 import BeautifulSoup
import requests

from langchain.agents import initialize_agent, AgentType
from langchain.callbacks import StreamlitCallbackHandler
from langchain.chat_models import ChatOpenAI
from langchain.tools import DuckDuckGoSearchRun
  
from helper_functions.utility import check_password  

# Check if the password is correct.  
if not check_password():  
    st.stop()

if load_dotenv('.env'):
   # for local development
   openai_api_key = os.getenv('OPENAI_API_KEY')
else:
   openai_api_key = st.secrets['OPENAI_API_KEY']

urls = ["https://www.motorist.sg/article/534/2024-update-traffic-offences-in-singapore-that-carry-demerit-points-composition-fines",
        "https://www.police.gov.sg/Advisories/Traffic/Traffic-Matters/Driver-Improvement-Points-System",
        "https://woodlandsdrivingschool.com/driver-resources/demerit-points/",
        "https://www.police.gov.sg/Advisories/Traffic/Traffic-Matters/Penalties-for-Traffic-Offences"]

final_text = ""

for url in urls:
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')
    clean_text = soup.text.replace('\n', '')
    final_text = final_text + clean_text


#with st.sidebar:
    #load_dotenv('.env')
    #openai_api_key = os.getenv('OPENAI_API_KEY')

st.title("🔎 Singapore Traffic Offences with Demerit Point Chatbot")

"""
This chatbot is an interactive 🤖 AI-powered assistant designed to help users navigate and understand Singapore’s 🇸🇬 traffic demerit points system and related penalties. 
Built specifically for users seeking information on traffic violations governed by Singapore’s Land Transport Authority (LTA) 🚦, it consolidates information from trusted sources 📚 to answer user queries accurately and efficiently.

**Example Interactions**

User: "What are the demerit points for speeding over the limit by 20 km/h? 🚗💨"

Chatbot: "Speeding by 20 km/h over the limit incurs 6 demerit points and a fine of S$200 💸."
"""

if "demerit_simulator_messages" not in st.session_state:
    st.session_state["demerit_simulator_messages"] = [
        {"role": "assistant", "content": "Hi, I'm a chatbot who knows all about demerit points in Singapore. How can I help you?"}
    ]

for msg in st.session_state.demerit_simulator_messages:
    st.chat_message(msg["role"]).write(msg["content"])

if prompt := st.chat_input(placeholder="What are the demerit points for speeding over the limit by 20 km/h?"):
    #st.session_state.demerit_simulator_messages.append({"role": "user", "content": 'You are a chatbot designed to help users to identify traffic demerit points and penalties in Singapore. Please use the information below to answer the user question below the information.'})
    #st.session_state.demerit_simulator_messages.append({"role": "user", "content": final_text})
    st.session_state.demerit_simulator_messages.append({"role": "user", "content": prompt})
    st.chat_message("user").write(prompt)


    demerit_simulator_messages = [
    {"role": "system", "content": "You are a chatbot designed to help users identify traffic demerit points and penalties in Singapore."},
    {"role": "system", "content": "Please use the information below to answer the user question below the information."},
    {"role": "system", "content": final_text},  # Pre-loaded information
]
    
    for message in st.session_state.demerit_simulator_messages:
        demerit_simulator_messages.append({"role": message['role'], "content": message['content']})

    client = OpenAI(api_key=os.getenv('OPENAI_API_KEY'))
    response = client.chat.completions.create( #originally was openai.chat.completions
        model="gpt-4o-mini",
        messages=demerit_simulator_messages,
        temperature=0,
        top_p=1.0,
        max_tokens=1024,
        n=1
    )

    #llm = ChatOpenAI(model_name="gpt-3.5-turbo", openai_api_key=openai_api_key, streaming=True)
    #search = DuckDuckGoSearchRun(name="Search")
    #search_agent = initialize_agent([search], llm, agent=AgentType.ZERO_SHOT_REACT_DESCRIPTION, handle_parsing_errors=True)
    
    with st.chat_message("assistant"):
        #st_cb = StreamlitCallbackHandler(st.container(), expand_new_thoughts=False)
        #response = search_agent.run(st.session_state.messages, callbacks=[st_cb])
        st.session_state.demerit_simulator_messages.append({"role": "assistant", "content": response.choices[0].message.content})
        st.write(response.choices[0].message.content)
    