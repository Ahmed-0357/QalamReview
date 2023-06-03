import streamlit as st

# config
page_title = "paper writing"
page_icon = "📜"
st.set_page_config(page_title=page_title, page_icon=page_icon)

# title
html_title = '<h1 align="center"> <b> 📜 Review Paper Writing </b></h1>'
st.markdown(html_title, unsafe_allow_html=True)
st.markdown('#')

st.write(st.session_state)

# check session state
if st.session_state['openai_api'] == '' or st.session_state['openai_model_opt'] == '' or st.session_state['google_api'] == '' or st.session_state['google_search_engine_id'] == '':
    st.error(
        'Please complete the initial configuration on the main page first.', icon="🚨")
elif st.session_state['paper_title'] == '' or st.session_state['expertise_areas'] == '' or st.session_state['paper_outline'] == '':

    st.error(
        'Please first fill paper title, areas of expertise and paper outlines on Outline page.', icon="🚨")
else:
    st.markdown("### 📚 Journal Paper Upload")
    st.markdown(
        "Upload downloaded journal papers that will be utilized in the composition of your review paper.")

    uploaded_papers = st.file_uploader("",
                                       type=['pdf'],
                                       accept_multiple_files=True, label_visibility="collapsed")
    if uploaded_papers:
        for uploaded_paper in uploaded_papers:
            pass
