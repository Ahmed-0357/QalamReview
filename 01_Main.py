import streamlit as st
from streamlit_extras.buy_me_a_coffee import button
from streamlit_extras.switch_page_button import switch_page

# config
st.set_page_config(page_title="QalamReview", page_icon="🖋️",     layout="centered",
                   initial_sidebar_state="expanded")

# title
html_title = '<h1 align="center"> <b> 🖋️ QalamReview </b></h1>'

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
    ('gpt-3.5-turbo (LOW COST)', 'gpt-3.5-turbo and gpt-4 (BEST RESULTS)'))

openai_model_opt = 'gpt-3.5-turbo' if openai_model_opt == 'gpt-3.5-turbo (LOW COST)' else 'gpt-3.5-turbo&gpt-4'


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
    <p style='font-size: 18px;'><b>Here's a snapshot of how it works:</b></p>

    <p style='font-size: 18px;'> 📝 <b>Outline Creation: </b> Provide your own or let the app generate outline for your paper.</p>

    <p style='font-size: 18px;'> 🔎 <b>Web Search: </b>The app searches the internet to source relevant academic papers that align with your chosen topic</p>

    <p style='font-size: 18px;'> 📜 <b>Review Paper Generation:</b> Finally, the app crafts a narrative review paper that succinctly summarises the key findings from your selected scholarly works</p><br>

    <p style='font-size: 18px;'>Start by filling out the <b>initial configuration</b> and then sit back and relax. QalamReview will deliver a comprehensive narrative review paper, thereby saving your valuable time.</p>
    """, unsafe_allow_html=True
)


# Action Buttons
if st.button('Start the Magic ✨'):
    switch_page('Outline Creation')

# Footer
st.markdown(
    """
    ---
    💡 **Need assistance?** Our [user guide](https://github.com/Ahmed-0357/autoreviewpaper) provides in-depth guidance on how to make the most of this tool. 
    
    🤝 **Keen on contributing to the project?** As an open-source initiative, QalamReview will thrive on community contributions. If you're interested in contributing, just head over to our [GitHub](https://github.com/Ahmed-0357/autoreviewpaper), fork the project, and begin your creative journey!
    
    ---
    👩‍💻 **About me:** I'm an AI enthusiast and dedicated researcher, I have a passion for making academic work more accessible and efficient. Learn more [about me](https://github.com/Ahmed-0357).
    
    💖 **Support my work:** If you find value in this and want to contribute to my efforts, you can support me by clicking the link below.
    """
)

button(username="ahmedabdulS", floating=False, width=221)
