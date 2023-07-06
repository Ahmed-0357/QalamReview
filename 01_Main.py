import streamlit as st
from streamlit_extras.buy_me_a_coffee import button
from streamlit_extras.switch_page_button import switch_page

# config
st.set_page_config(page_title="auto review", page_icon=":book:",     layout="centered",
                   initial_sidebar_state="expanded")

# title
html_title = '<h1 align="center"> <b> 📖 Auto Review </b></h1>'

st.markdown(html_title, unsafe_allow_html=True)
# title
html_title = '<h2 align="center"> <b> generate up to date narrative review paper in any topic of your choice! </b></h2>'
st.markdown(html_title, unsafe_allow_html=True)
st.markdown('#')

# sidebar
# session state
st.session_state['openai_api'] = ''
st.session_state['openai_model_opt'] = ''
st.session_state['google_api'] = ''
st.session_state['google_search_engine_id'] = ''

# initial config
st.sidebar.header('🔧 Initial Configuration')
st.sidebar.subheader('OpenAI')
# api key
openai_api = st.sidebar.text_input(
    "API key", type='password')
# model
openai_model_opt = st.sidebar.selectbox(
    'Model',
    ('gpt-3.5-turbo',))  # add gpt 4 later on

st.sidebar.subheader('Google')
# api key
google_api = st.sidebar.text_input(
    "Search API Key", type='password')
google_search_engine_id = st.sidebar.text_input(
    "Search Engine ID", type='password')

# update session
if openai_api != '':
    st.session_state['openai_api'] = openai_api
if openai_model_opt != '':
    st.session_state['openai_model_opt'] = openai_model_opt
if google_api != '':
    st.session_state['google_api'] = google_api
if google_search_engine_id != '':
    st.session_state['google_search_engine_id'] = google_search_engine_id


# Introduction about the app
st.markdown(
    """
    <p style='font-size: 18px;'><b>Here's how it works:</b></p>

    <p style='font-size: 18px;'> 📝 <b>Outline Creation: </b> The app generates or accepts a paper's outline.</p>

    <p style='font-size: 18px;'>🌐 <b>Internet Search: </b>It then searches the internet for relevant academic papers.</p>

    <p style='font-size: 18px;'>📚 <b>Paper Writing:</b> Finally, it creates a narrative review paper, summarizing the findings from the selected scholarly papers</p><br>

    <p style='font-size: 18px;'>Simply Fill the <b>initial configuration</b> and relax, this app will generate comprehensive, well-structured narrative review papers, saving you valuable time</p>
    """, unsafe_allow_html=True
)


# Action Buttons
if st.button('Start the Magic ✨'):
    switch_page('Outline')

# Footer
st.markdown(
    """
    ---
    💡 **Need help?** For comprehensive guidance on using this tool, we encourage you to refer to our detailed documentation available on our [GitHub](https://github.com/Ahmed-0357/autoreviewpaper).
    
    🤝 **Contribute to the Project:** This project is open source and exists for the benefit of the community. If would like to make a contribution, simply head over to our [GitHub](https://github.com/Ahmed-0357/autoreviewpaper), initiate a fork, and commence your creative contributions.
    
    ---
    👩‍💻 **About me:** I'm an AI enthusiast and dedicated researcher, I have a passion for making academic work more accessible and efficient. Learn more [about me](https://github.com/Ahmed-0357).
    
    💖 **Support my work:** If you find value in this and want to contribute to my efforts, you can support me by clicking the link below.
    """
)

button(username="ahmedabdulS", floating=False, width=221)

openai_key = "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"
google_key = "AIzaSyByT_NHJkzlSj3SurOOvsNOEZ2WwC98qQY"
cse_id = "90421513b2347450d"
