import streamlit as st

# config
page_title = "paper search - Train"
page_icon = ":mag_right:"
st.set_page_config(page_title=page_title, page_icon=page_icon)

# title
html_title = '<h1 align="center"> <b> Let Us Find The Most Relevant Papers </b></h1>'
st.markdown(html_title, unsafe_allow_html=True)
st.markdown('#')

st.write(st.session_state)

# check session state
if st.session_state['openai_api'] == '' or st.session_state['openai_model_opt'] == '' or st.session_state['google_api'] == '':
    st.error(
        'Please complete the initial configuration on the main page first.', icon="🚨")

st.write(st.session_state)
