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
    
load_dotenv('.env')
openai_api_key = os.getenv('OPENAI_API_KEY')

urls = ["https://onemotoring.lta.gov.sg/content/onemotoring/home/driving/vocational_licence/vocational_licence_application.html",
        "https://www.gobusiness.gov.sg/browse-all-licences/land-transport-authority-(lta)/taxi-driver's-vocational-licence-(tdvl)---private-hire-car-driver's-vocational-licence-(pdvl)",
        "https://www.grab.com/sg/gcpdvl/",
        "https://www.gojek.com/sg/blog/dp-gojek-singapore-driver-vocational-licence-application",
        "https://www.ntuclearninghub.com/en-gb/-/course/private-hire-car-driver-vocational-licence-course-1-1",
        "https://www.cdgtaxi.com.sg/vocational-licences-tdvl-or-pdvl/",
        "https://onemotoring.lta.gov.sg/content/onemotoring/home/driving/vocational_licence/vocational_licence_renewal.html"]

final_text = ""

for url in urls:
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')
    clean_text = soup.text.replace('\n', '')
    final_text = final_text + clean_text

with st.sidebar:
    load_dotenv('.env')
    openai_api_key = os.getenv('OPENAI_API_KEY')

st.title("🔎 Singapore Vocational Driving License Application Chatbot")

"""
The Vocational License Registration Chatbot is an AI-powered assistant designed to guide users through the process of applying for vocational licenses in Singapore, specifically for roles such as private hire car drivers, taxi drivers, and bus operators. This chatbot is tailored to answer questions, provide step-by-step guidance, and clarify requirements set by the Land Transport Authority (LTA) for obtaining a vocational license.

**Key Features**

- License Information by Category 📝: The chatbot helps users understand the different types of vocational licenses available—Private Hire Car Driver's Vocational License (PDVL), Taxi Driver's Vocational License (TDVL), and Bus Driver's Vocational License (BDVL). Users can select their intended license type, and the chatbot provides specific information relevant to that category.

- Application Requirements Checklist 📋: Users receive detailed information on prerequisites such as minimum age, driving experience, medical examinations, background checks, and mandatory training courses. This ensures that applicants know exactly what they need before applying.

- Step-by-Step Application Guidance 👣: The chatbot walks users through each stage of the application process, from eligibility requirements and course registration to document submission and final licensing.

- Quick Access to Official Resources 🌐: The chatbot provides direct links to official LTA resources, such as online application portals, training provider websites, and FAQs, so users can easily access additional information or start their application directly.

- Interactive Q&A 🤖: Users can ask specific questions about any part of the licensing process. For example:

User: "How long does it take to get a PDVL?"

Chatbot: "It typically takes 4-6 weeks, including the time needed to complete mandatory training and exams."
"""

if "license_application_messages" not in st.session_state:
    st.session_state["license_application_messages"] = [
        {"role": "assistant", "content": "Hi, I'm a chatbot who knows all about applying for vocational driving license in Singapore. How can I help you?"}
    ]

for msg in st.session_state.license_application_messages:
    st.chat_message(msg["role"]).write(msg["content"])

if prompt := st.chat_input(placeholder="How long does it take to get a PDVL?"):
    #st.session_state.license_application_messages.append({"role": "user", "content": 'You are a chatbot designed to help users register for a vocational driving license in Singapore. Please use the information below to answer the user question below the information.'})
    #st.session_state.license_application_messages.append({"role": "user", "content": final_text})
    st.session_state.license_application_messages.append({"role": "user", "content": prompt})
    st.chat_message("user").write(prompt)


    license_application_messages = [
    {"role": "system", "content": "You are a chatbot designed to help users register for a vocational driving license in Singapore."},
    {"role": "system", "content": "Please use the information below to answer the user question below the information."},
    {"role": "system", "content": final_text},  # Pre-loaded information
]
    
    for message in st.session_state.license_application_messages:
        license_application_messages.append({"role": message['role'], "content": message['content']})

    client = OpenAI(api_key=os.getenv('OPENAI_API_KEY'))
    response = client.chat.completions.create( #originally was openai.chat.completions
        model="gpt-4o-mini",
        messages=license_application_messages,
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
        st.session_state.license_application_messages.append({"role": "assistant", "content": response.choices[0].message.content})
        st.write(response.choices[0].message.content)