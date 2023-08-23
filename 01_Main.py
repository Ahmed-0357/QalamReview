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
html_title = '<h2 align="center"> <b> draft a narrative review paper on your favorite topic </b></h2>'
st.markdown(html_title, unsafe_allow_html=True)
st.markdown('#')

# sidebar
# session state
st.session_state['openai_api'] = ''
st.session_state['openai_model_opt'] = ''
st.session_state['google_api'] = ''
st.session_state['google_search_engine_id'] = ''

# initial config
st.sidebar.header('🔧 Initial Configurations')
st.sidebar.subheader('OpenAI')
# api key
openai_api = st.sidebar.text_input(
    "API key", type='password')
# model
openai_model_opt = st.sidebar.selectbox(
    'Model',
    ('gpt-3.5 (LOW COST)', 'gpt-3.5 & gpt-4 (BETTER RESULTS)'))

openai_model_opt = 'gpt-3.5-turbo' if openai_model_opt == 'gpt-3.5 (LOW COST)' else 'gpt-3.5-turbo&gpt-4'


st.sidebar.subheader('Google')
# api key
google_api = st.sidebar.text_input(
    "Search API Key (optional)", type='password')
google_search_engine_id = st.sidebar.text_input(
    "Search Engine ID (optional)", type='password')

# update session
if openai_api != '':
    st.session_state['openai_api'] = openai_api
if openai_model_opt != '':
    st.session_state['openai_model_opt'] = openai_model_opt
if google_api != '':
    st.session_state['google_api'] = google_api
if google_search_engine_id != '':
    st.session_state['google_search_engine_id'] = google_search_engine_id

# Action Buttons
st.sidebar.markdown('')
if st.sidebar.button('Start ✨'):
    switch_page('Outline Creation')

# Introduction about the app
st.markdown(
    """
    <p style='font-size: 18px;'><b>Here is how it works:</b></p>

    <ul style='font-size: 18px;'>
        <li><b>📝Outline Creation:</b> You can submit your own outline, or use the app to create one tailored for your paper.</li>
        <li><b>🔎Web Search (optional):</b> The app scans the web to find academic papers relevant to your selected topic.</li>
        <li><b>📜Review Paper Generation:</b> The app then assembles a narrative review paper, highlighting the principal insights from the scholarly articles you've provided</li>
    </ul>

    <p style='font-size: 18px;'>Start by filling out the <b>initial configuration</b>. QalamReview will draft your narrative review paper, giving you a head start and saving precious time.</p>
    """, unsafe_allow_html=True
)

st.markdown('<hr style="border:3px solid #ffc83d;">', unsafe_allow_html=True)
st.markdown('')
# Footer
st.markdown(
    """
    💡 **Need assistance?** Our [user guide](https://github.com/Ahmed-0357/autoreviewpaper) provides in-depth guidance on how to make the most of QalamReview. 
    
    🤝 **Keen on contributing to the project?** QalamReview stands strong as an open-source initiative. If you're interested in contributing, just head over to our [GitHub](https://github.com/Ahmed-0357/autoreviewpaper), fork the project, and begin your creative journey!
    
    ---
    👩‍💻 **About me:** I'm an AI enthusiast and dedicated researcher, I have a passion for making academic work more accessible and efficient. Learn more [about me](https://www.linkedin.com/in/ahmed-abdulrahman-75b41a164/).
    
    💖 **Support my work:** If you find value in this and want to contribute to my efforts, you can support me by clicking the link below.
    """
)

button(username="ahmedabdulS", floating=False, width=221)
