import os

import streamlit as st
from PIL import Image
from streamlit_extras.buy_me_a_coffee import button
from streamlit_extras.switch_page_button import switch_page

# config
st.set_page_config(
    page_title="QalamReview",
    page_icon="🖋️",
    layout="centered",
    initial_sidebar_state="expanded",
)


col1, col2, col3 = st.columns((1, 4, 1))
with col2:
    st.image(Image.open(os.path.join("files", "logo.png")))

html_title = '<h2 align="center"> <b> draft a narrative review paper on your favorite topic </b></h2>'
st.markdown(html_title, unsafe_allow_html=True)
st.markdown("#")

# sidebar
# session state
st.session_state["openai_api"] = ""
st.session_state["openai_model_opt"] = ""
st.session_state["google_api"] = ""
st.session_state["google_search_engine_id"] = ""

# initial config
st.sidebar.header("🔧 Configuration:")
st.sidebar.subheader("OpenAI")
# api key
openai_api = st.sidebar.text_input("API key", type="password")
# model
openai_model_opt = st.sidebar.selectbox(
    "ChatGPT Model", ("gpt-3.5 (LOW COST)", "gpt-3.5 & gpt-4 (BETTER RESULTS)")
)

openai_model_opt = (
    "gpt-3.5-turbo-1106"
    if openai_model_opt == "gpt-3.5 (LOW COST)"
    else "gpt-3.5-turbo-1106&gpt-4"
)


st.sidebar.subheader("Google")
# api key
google_api = st.sidebar.text_input("Search API Key (optional)", type="password")
google_search_engine_id = st.sidebar.text_input(
    "Search Engine ID (optional)", type="password"
)

# update session
if openai_api != "":
    st.session_state["openai_api"] = openai_api
if openai_model_opt != "":
    st.session_state["openai_model_opt"] = openai_model_opt
if google_api != "":
    st.session_state["google_api"] = google_api
if google_search_engine_id != "":
    st.session_state["google_search_engine_id"] = google_search_engine_id

# Action Buttons
st.sidebar.markdown("")
if st.sidebar.button("Start ✨"):
    switch_page("Outline Creation")

# Introduction about the app
st.markdown(
    """
    <p style='font-size: 18px;'><b>Here's how it works in simple steps:</b></p>

    <ul style='font-size: 18px;'>
        <li><b>📝 Create Outline:</b> Craft customized outlines for your review paper using the app, or upload your own outlines.</li>
        <li><b>🔎 Search Articles (optional):</b> Leverage the search tool to discover academic papers that align with your topic of interest.</li>
        <li><b>📜 Summarize & Write Review:</b> Utilize the app to distill key insights from academic papers into concise summaries, or go further by assembling these insights into a comprehensive draft of your narrative review paper.</li>
    </ul>

    <p style='font-size: 18px;'>Start by filling out the <b>configuration</b> on the sidebar and simply follow the three steps above.</p>
    """,
    unsafe_allow_html=True,
)


st.markdown('<hr style="border:3px solid #c55a11;">', unsafe_allow_html=True)
st.markdown("")
# Footer
st.markdown(
    """
    💡 **Need assistance?** Our [user guide](https://github.com/Ahmed-0357/QalamReview/blob/main/docs/user_guide.md) provides in-depth guidance on how to make the most of QalamReview. 
    
    🤝 **Keen on contributing to the project?** QalamReview stands strong as an open-source initiative. If you're interested in contributing, just head over to our [GitHub](https://github.com/Ahmed-0357/QalamReview), fork the project, and begin your creative journey!
    
    ---
    👨‍💻          **About me:** I'm an AI enthusiast and dedicated researcher, I have a passion for making academic work more accessible and efficient. Learn more [about me](https://www.linkedin.com/in/ahmed-abdulrahman-75b41a164/).
    
    💖 **Support my work:** If you find value in this and want to contribute to my efforts, you can support me here.
    """
)

button(username="ahmedabdulS", floating=False, width=221)
