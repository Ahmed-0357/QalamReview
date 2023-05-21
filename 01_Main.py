import streamlit as st
from streamlit_extras.switch_page_button import switch_page

import st_app_func as saf

# config
st.set_page_config(page_title="auto review", page_icon=":book:",     layout="centered",
                   initial_sidebar_state="expanded")

# title
html_title = '<h1 align="center"> <b> 📖 Auto Review </b></h1>'
st.markdown(html_title, unsafe_allow_html=True)
# title
html_title = '<h2 align="center"> <b> generate up to date review papers in any topic of your choice! </b></h2>'
st.markdown(html_title, unsafe_allow_html=True)
st.markdown('#')

# sidebar
# session state
st.session_state['openai_api'] = ''
st.session_state['openai_model_opt'] = ''
st.session_state['google_api'] = ''

# initial config
st.sidebar.header('🔧 Initial Configuration')
st.sidebar.subheader('OpenAI')
# api key
openai_api = st.sidebar.text_input("API key", type='password')
# model
openai_model_opt = st.sidebar.selectbox(
    'Model',
    ('', 'GPT-4', 'GPT-3.5'))

st.sidebar.subheader('Google')
# api key
google_api = st.sidebar.text_input("API Key", type='password')

# update session
if openai_api != '':
    st.session_state['openai_api'] = openai_api
if openai_model_opt != '':
    st.session_state['openai_model_opt'] = openai_model_opt
if google_api != '':
    st.session_state['google_api'] = google_api


# Introduction about the app
st.markdown(
    """
    <p style='font-size: 18px;'>This powerful tool leverages advanced AI technology to create automatic review papers on any topic of your choice.</p>
    
    <p style='font-size: 18px;'><b>Here's how it works:</b></p>

    <p style='font-size: 18px;'>🔍 <b>Search:</b> my tool begins by creating an outline of the paper, or you can upload your own.</p>

    <p style='font-size: 18px;'>🌐 <b>Internet Surfing:</b> It then scours the internet for the most relevant academic papers that match your topic and outline.</p>

    <p style='font-size: 18px;'>📚 <b>Generation:</b> Finally, it produces a comprehensive review paper by summarizing and connecting the findings from these papers.</p>

    <p style='font-size: 18px;'>Simply Fill the initial configuration and relax. my tool generates comprehensive, well-structured review papers, saving you valuable time</p>
    """, unsafe_allow_html=True
)


# Action Buttons
if st.button('Start the Magic ✨'):
    switch_page('Outlines')

# Footer
st.markdown(
    """
    ---
    💡 **Need help?** For more information about how to use this tool, please visit our [github](#).
    
    👩‍💻 **About me:** I'm an AI enthusiast and researcher who decided to make academic work a piece of cake. So, you're welcome! 😄 Learn more [about me](https://github.com/Ahmed-0357).
    """
)
