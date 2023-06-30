import io
import os

import pandas as pd
import streamlit as st

# config
page_title = "paper writing"
page_icon = "📜"
st.set_page_config(page_title=page_title, page_icon=page_icon)

# title
html_title = '<h1 align="center"> <b> 📜 Review Paper Writing </b></h1>'
st.markdown(html_title, unsafe_allow_html=True)
st.markdown('#')

# st.write(st.session_state)

# check session state
if st.session_state['openai_api'] == '' or st.session_state['openai_model_opt'] == '' or st.session_state['google_api'] == '' or st.session_state['google_search_engine_id'] == '':
    st.error(
        'Please complete the initial configuration on the main page first.', icon="🚨")
elif st.session_state['paper_title'] == '' or st.session_state['expertise_areas'] == '' or st.session_state['paper_outline'] == '':

    st.error(
        'Please first fill paper title, areas of expertise and paper outlines on Outline page.', icon="🚨")
else:
    st.markdown("### 📚 Journal Papers")
    st.markdown(
        "Upload downloaded journal papers which will be utilized in the composition of your review paper.")

    uploaded_papers = st.file_uploader("",
                                       type=['pdf'],
                                       accept_multiple_files=True, label_visibility="collapsed")

    # Directory to save files
    papers_dir = 'papers'
    # Ensure directory exists
    os.makedirs(papers_dir, exist_ok=True)

    if uploaded_papers:
        for uploaded_paper in uploaded_papers:
            try:
                # Create a temporary file and write the uploaded file's bytes to it
                with open(f'{papers_dir}/{uploaded_paper.name}', 'wb') as f:
                    f.write(uploaded_paper.getbuffer())

            except:
                continue

    st.markdown("### 📚 Papers Metadata")
    st.markdown(
        "Upload papers metadata which will be used for papers citing")
    # File uploader for metadata
    uploaded_metadata = st.file_uploader(
        "", type=['csv'], label_visibility="collapsed")

    # Directory to save files
    meta_dir = 'metadata'

    # Ensure directory exists
    os.makedirs(meta_dir, exist_ok=True)

    # If there is an uploaded file
    if uploaded_metadata:
        try:
            # Save the uploaded file
            meta_file_path = os.path.join(meta_dir, uploaded_metadata.name)
            with open(meta_file_path, 'wb') as f:
                f.write(uploaded_metadata.getbuffer())
        except:
            st.error(
                f'Error reading metadata file', icon="🚨")
        else:
            meta = pd.read_csv(meta_file_path)
            st.write(meta)
            st.dataframe(meta)
