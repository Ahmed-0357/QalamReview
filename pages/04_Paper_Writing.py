import ast
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

    # Directory to temporary save papers
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

    # Delete user removed papers
    for filename in os.listdir(papers_dir):
        if filename not in [uploaded_paper.name for uploaded_paper in uploaded_papers]:
            file_path = os.path.join(papers_dir, filename)
            try:
                if os.path.isfile(file_path):
                    os.remove(file_path)
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
            # dir to and file to save summary data
            dir_name = "summary"
            if not os.path.exists(dir_name):
                os.makedirs(dir_name)
            summary_file = "papers_summary.txt"
            summary_file_path = os.path.join(dir_name, summary_file)
            relevance_file = "papers_relevance.txt"
            relevance_file_path = os.path.join(dir_name, relevance_file)
            # clean files
            with open(summary_file_path, 'w') as file:
                pass
            with open(relevance_file_path, 'w') as file:
                pass

            # llm models instantiation
            # summary model
            model_name = st.session_state['openai_model_opt']+'-16k'
            chat = ChatOpenAI(openai_api_key=st.session_state['openai_api'],
                              temperature=0, model_name=model_name)
            # relevance model
            chat_ = ChatOpenAI(openai_api_key=st.session_state['openai_api'],
                               temperature=0, model_name=st.session_state['openai_model_opt'])

            # input dicts
            # input dict summary
            input_dict_summary = {'llm_model': chat, 'expertise_areas': st.session_state[
                'expertise_areas'], 'subject': st.session_state['paper_title'], 'outline': outline_list}
            # input dict relevance
            input_dict_relevance = {'llm_model': chat_, 'expertise_areas': st.session_state[
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
                        output_summ = summ.summarize(**input_dict_summary)
                    except Exception as e:
                        time.sleep(9)
                        continue
                    else:
                        time.sleep(9)
                        try:
                            # relevance class
                            rele = spw.RelevanceAnalysis(output_summ)
                            output_rele = rele.relevancy_score(
                                **input_dict_relevance)
                        except Exception as e:
                            time.sleep(3)
                            continue
                        else:
                            with open(summary_file_path, 'a') as file:
                                file.write(str(output_summ)+'\n\n')
                            with open(relevance_file_path, 'a') as file:
                                file.write(str(output_rele)+'\n\n')
                            time.sleep(3)

            with open('summary\papers_relevance.txt', 'r') as f:
                content = f.read()
            parts = content.split('\n\n')
            parts = parts[:-1]
            dicts = [ast.literal_eval(part) for part in parts]

            df = pd.DataFrame(dicts)
            df = df.apply(lambda x: pd.to_numeric(x, errors='coerce'))
            df['ID'] = range(len(df))
            cols = ['ID'] + [col for col in df.columns if col != 'ID']
            df = df.reindex(columns=cols)
            st.dataframe(df)
