# -*- coding: utf-8 -*-
"""
Created on Sun Oct 20 22:06:31 2024

Demerit simulator module
"""
# Set up OpenAI
from openai import OpenAI

# Set up and run this Streamlit App
import streamlit as st

import os
from dotenv import load_dotenv



# region <--------- Streamlit App Configuration --------->
st.set_page_config(
    layout="centered",
    page_title="Yvonne Capstone App"
)
# endregion <--------- Streamlit App Configuration --------->

# Sample data of traffic offenses and their corresponding demerit points
OFFENSES = {
    "Speeding": {"points": 6, "fine": 200},
    "Running a red light": {"points": 12, "fine": 400},
    "Illegal U-turn": {"points": 4, "fine": 150},
    "Using mobile phone while driving": {"points": 12, "fine": 300},
    # Add more offenses as needed
}

def get_completion(prompt, model="gpt-4o-mini", temperature=0, top_p=1.0, max_tokens=1024, n=1, json_output=False):
    if json_output == True:
      output_json_structure = {"type": "json_object"}
    else:
      output_json_structure = None

    messages = [{"role": "user", "content": prompt}]
    load_dotenv('.env')
    client = OpenAI(api_key=os.getenv('OPENAI_API_KEY'))
    response = client.chat.completions.create( #originally was openai.chat.completions
        model=model,
        messages=messages,
        temperature=temperature,
        top_p=top_p,
        max_tokens=max_tokens,
        n=1,
        response_format=output_json_structure,
    )
    return response.choices[0].message.content

"""
def explain_offense(offense):
    # Call OpenAI or another LLM to explain the offense in detail
    response = openai.Completion.create(
        engine="text-davinci-003",
        prompt=f"Explain the traffic offense '{offense}' in Singapore.",
        max_tokens=150
    )
    return response['choices'][0]['text'].strip()
"""

def display():
    st.title("Demerit Point Simulator")

    st.markdown("""
    ### Select the offenses you have committed to simulate your total demerit points and fines.
    """)

    # Multiselect for offenses
    selected_offenses = st.multiselect("Choose offenses", list(OFFENSES.keys()))

    if selected_offenses:
        total_points = sum(OFFENSES[offense]["points"] for offense in selected_offenses)
        total_fine = sum(OFFENSES[offense]["fine"] for offense in selected_offenses)
        
        # Display results
        st.subheader(f"Total Demerit Points: {total_points}")
        st.subheader(f"Total Fine: ${total_fine}")

        # Threshold warning
        if total_points >= 24:
            st.error("Warning: You are at risk of having your license revoked.")
        elif total_points >= 12:
            st.warning("Warning: You are close to a suspension.")
        
        # Explanation for each offense (LLM-powered logic can be added here)
        for offense in selected_offenses:
            st.markdown(f"**{offense}**: {OFFENSES[offense]['points']} demerit points, ${OFFENSES[offense]['fine']} fine")
            for offense in selected_offenses:
                st.markdown(f"**{offense}**: {OFFENSES[offense]['points']} demerit points, ${OFFENSES[offense]['fine']} fine")
                # Get explanation from LLM
                explanation = get_completion(offense)
                st.write(explanation)
    else:
        st.info("Select offenses to simulate the demerit points.")
