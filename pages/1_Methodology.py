import streamlit as st
from PIL import Image
#import os

st.title("📊 Methodology")

"""
My methodology focuses on building a user-centered, interactive chatbot that serves as a one-stop resource for Singapore’s road regulations and vocational driving license information. The chatbot is developed on Streamlit and powered by a language model that interacts with users, adapting responses based on the information provided from verified sources.

**Problem Statement**

In Singapore, there is no central platform or chatbot that consolidates and provides information on traffic demerit points and vocational license applications, causing confusion and unnecessary administrative hurdles. Users often struggle to find accurate and accessible information on these topics due to fragmented resources across multiple sites and agencies.

**Approach**

- Data Integration from Official Sources 🌐: The chatbot pulls data from various government and transport authority resources, enabling it to answer questions accurately. Information on demerit points, penalties, and licensing processes is aggregated to ensure users get comprehensive and updated guidance in one place.

- Interactive, User-Specific Responses 🤖: By integrating a language model, the chatbot can offer personalized and contextually relevant responses to users. Each response is crafted to clarify rules, procedures, and penalties in easy-to-understand language, helping users to grasp regulations quickly.

**Use Case Implementation**

- Demerit Point Chatbot: This use case was developed to provide users with real-time insights into the demerit point system. By simulating traffic infractions, the chatbot can demonstrate how demerit points accumulate for each violation, showing users the associated risks and penalties, fostering more responsible driving behavior.

- Vocational Driving License Application Chatbot: To simplify and help users understand the application process for various types of vocational driving licenses, the chatbot guides users step-by-step, covering requirements, training courses, and documentation needs. This component is tailored to each license type, ensuring applicants know exactly what to expect and how to prepare.

**Session-Specific Functionality**🔄 

Each use case is deployed on a separate page within the Streamlit app, with independent session states to maintain distinct histories. This allows for focused interactions specific to each use case, whether users are interested in demerit points or vocational licensing.

**Process Flow for Use Cases**

Each use case operates in a streamlined sequence. This flow enables the chatbot to respond swiftly, allowing users to interact with real-time answers to their questions.

"""

# Print the current working directory for debugging
#st.write("Current working directory:", os.getcwd())

#Display the draw.io diagram
image_path_1 = 'flowchart_on_demerit_point_query.png'
image1 = Image.open(image_path_1)
st.image(image1, caption='Flowchart for demerit point chatbot', width = 250)

image_path_2 = 'flowchart_on_vocational_license_use_case.png'
image2 = Image.open(image_path_2)
st.image(image2, caption='Flowchart for vocational driving license chatbot', width = 250)

