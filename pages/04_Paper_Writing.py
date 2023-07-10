import base64
import os
import time
from functools import reduce

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
    st.markdown("### ⚙️ Manuscript Preparation Setting")
    papers_per_sub = st.slider('📚 Quantity of research papers utilized for composing each individual sub-subsection', min_value=10,
                               max_value=50, value=10, step=1)

    st.markdown("####")

    generate_button = st.button('Generate')
    if generate_button and not uploaded_papers:
        st.error('Please upload journal papers before generating. 🚨')
    elif generate_button:
        # outline list and dict
        outline_list = [
            f"{main_key} - {sub_key} - {list(item.values())[0]}"
            for main_key, main_value in st.session_state['paper_outline'].items()
            for sub_key, sub_value in main_value.items()
            for item in sub_value
        ]

        # llm model name
        model_name, to_sleep = (st.session_state['openai_model_opt']+'-16k', 9) if st.session_state['openai_model_opt'] == 'gpt-3.5-turbo' else (
            st.session_state['openai_model_opt']+'-32k', 17)
        # llm models instantiation
        chat = ChatOpenAI(openai_api_key=st.session_state['openai_api'],
                          temperature=0, model_name=model_name)
        # relevance model
        chat_ = ChatOpenAI(openai_api_key=st.session_state['openai_api'],
                           temperature=0, model_name=st.session_state['openai_model_opt'])

        # summary spinner
        with st.spinner('**🚀 Working on summarizing the papers. Please wait...**'):
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
                    loader = PyPDFLoader(
                        os.path.join(papers_dir, paper_path))
                    pages = loader.load_and_split()
                    paper_content = ''.join(
                        page.page_content for page in pages)

                    # split paper token wise (12k token for gpt-3 and 28k gpt-4)
                    if model_name == 'gpt-3.5-turbo-16k':
                        text_splitter = TokenTextSplitter(
                            chunk_size=12000, chunk_overlap=0)
                    else:
                        text_splitter = TokenTextSplitter(
                            chunk_size=28000, chunk_overlap=0)
                    texts = text_splitter.split_text(paper_content)

                    try:
                        # summarization class
                        summ = spw.PaperSummary(texts)
                        output_summ = summ.summarize(**input_dict_summary)
                    except Exception as e:
                        time.sleep(to_sleep)
                        continue
                    else:
                        time.sleep(to_sleep)
                        try:
                            # relevance class
                            rele = spw.RelevanceAnalysis(output_summ)
                            output_rele = rele.relevancy_score(
                                **input_dict_relevance)
                        except Exception as e:
                            time.sleep(to_sleep)
                            continue
                        else:
                            with open(summary_file_path, 'a', encoding='utf-8') as file:
                                file.write(str(output_summ)+'\n\n')
                            with open(relevance_file_path, 'a', encoding='utf-8') as file:
                                file.write(str(output_rele)+'\n\n')
                            time.sleep(to_sleep)

        with st.spinner('**🖋️ Writing the narrative review paper. Please wait...**'):
            df_relevancy = spw.load_and_process_df(relevance_file_path)
            df_summary = spw.load_and_process_df(
                summary_file_path, numeric=False)

            summ_rele = pd.concat([df_summary, df_relevancy], axis=1)

            del df_relevancy
            del df_summary

            output_sections = []
            manwri = spw.ManuscriptWriting()
            for i in range(len(outline_list)):
                with st.spinner(f'Writing section: {outline_list[i]} ...'):
                    try:
                        # sort papers
                        summ_rele.sort_values(
                            by=outline_list[i], ascending=False, inplace=True)
                    except Exception as e:
                        st.write(e)
                        continue
                    else:
                        summ_rele_copy = summ_rele.iloc[:int(
                            papers_per_sub), :8].copy()
                        # split papers summary token wise (12k token for gpt-3 and 28k gpt-4)
                        summ_rele_list = summ_rele_copy.to_dict(
                            orient='records')
                        summ_rele_text = "\n\n".join(
                            str(item) for item in summ_rele_list)

                        del summ_rele_copy
                        del summ_rele_list

                        # split text
                        if model_name == 'gpt-3.5-turbo-16k':
                            text_splitter = TokenTextSplitter(
                                chunk_size=12000, chunk_overlap=0)
                        else:
                            text_splitter = TokenTextSplitter(
                                chunk_size=28000, chunk_overlap=0)
                        texts = text_splitter.split_text(summ_rele_text)

                        # input dict writing
                        input_dict_writing = {'llm_model': chat, 'expertise_areas': st.session_state[
                            'expertise_areas'], 'subject': st.session_state['paper_title'], 'section': outline_list[i], 'texts': texts, 'to_sleep': to_sleep}
                        try:
                            output = manwri.section_writing(
                                **input_dict_writing)
                        except Exception as e:
                            time.sleep(to_sleep)
                            continue
                        else:
                            output_sections.append((outline_list[i], output))
                            time.sleep(to_sleep)

            # merge all content and final write up
            output_sections_result = {}
            for keys, summary in [(tuple(j.strip() for j in i.split('-')), s) for i, s in output_sections]:
                reduce(lambda d, key: d.setdefault(key, {}),
                       keys[:-1], output_sections_result)[keys[-1]] = summary

            manwri.final_writeup(
                st.session_state['paper_title'], output_sections_result)

            # save summary and relevancy of scholarly papers
            csv = summ_rele.to_csv(index=False)
            b64 = base64.b64encode(csv.encode()).decode()
            href = f'<a href="data:text/csv;base64,{b64}" download="papers_summary_relevancy.csv">Download Papers Summaries and Relevancy Scores (CSV)</a>'
            st.markdown(href, unsafe_allow_html=True)

            # save manuscript
            with open(os.path.join('manuscript', 'narrative_review.docx'), 'rb') as f:
                data = f.read()
            bin_str = base64.b64encode(data).decode()
            href = f'<a href="data:application/octet-stream;base64,{bin_str}" download="narrative_review.docx">Download Final Narrative Review (DOCX)</a>'
            st.markdown(href, unsafe_allow_html=True)
