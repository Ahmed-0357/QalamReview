import os
import time

import pandas as pd
import st_paper_writing_func as spw
import streamlit as st
from langchain.chat_models import ChatOpenAI
from langchain.document_loaders import PyPDFLoader
from langchain.text_splitter import TokenTextSplitter

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
    st.markdown("### 📝 Journal Papers")
    st.markdown(
        "Upload downloaded journal papers which will be utilized in the composition of your narrative review paper.")

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
                with open(os.path.join(papers_dir, uploaded_paper.name), 'wb') as f:
                    f.write(uploaded_paper.getbuffer())

            except:
                continue

    st.markdown("####")
    generate_button = st.button('Generate')
    if generate_button and not uploaded_papers:
        st.error('Please upload journal papers before generating. 🚨')
    elif generate_button:
        # outline list and dict
        outline_list = [
            f"{main_key}: {sub_key}: {list(item.values())[0]}"
            for main_key, main_value in st.session_state['paper_outline'].items()
            for sub_key, sub_value in main_value.items()
            for item in sub_value
        ]

        # summary spinner
        with st.spinner('**🖋️ Working on summarizing the papers. Please wait...**'):
            # dir to and file to save summary
            dir_name = "summary"
            if not os.path.exists(dir_name):
                os.makedirs(dir_name)
            file_name = "papers_summary.txt"
            full_path = os.path.join(dir_name, file_name)

            # llm model instantiation
            model_name = st.session_state['openai_model_opt']+'-16k'
            chat = ChatOpenAI(openai_api_key=st.session_state['openai_api'],
                              temperature=0, model_name=model_name)
            # imput dict
            input_dict = {'llm_model': chat, 'expertise_areas': st.session_state[
                'expertise_areas'], 'subject': st.session_state['paper_title'], 'outline': outline_list}
            # loop through papers
            for paper_path in os.listdir(papers_dir):
                with st.spinner(f'Summarizing {paper_path} ...'):
                    # read paper content
                    loader = PyPDFLoader(os.path.join(papers_dir, paper_path))
                    pages = loader.load_and_split()
                    paper_content = ''.join(
                        page.page_content for page in pages)

                    # split paper token wise (12k token)
                    text_splitter = TokenTextSplitter(
                        chunk_size=12000, chunk_overlap=0)
                    texts = text_splitter.split_text(paper_content)

                    try:
                        # summarization class
                        summ = spw.PaperSummary(texts)
                        output = summ.summarize(**input_dict)

                    except Exception as e:
                        st.write(e)
                        continue
                    else:
                        st.json(output)
                        with open(full_path, 'a') as file:
                            file.write(str(output)+'\n\n')

                    time.sleep(9)

        # relevance analysis spinner
        with st.spinner('** 🥇 Working on summarizing the papers. Please wait...**'):
            # dir to and file to save summary
