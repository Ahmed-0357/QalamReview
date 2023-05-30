import ast
import time

import pandas as pd
import st_app_func as saf
import streamlit as st
from langchain import LLMChain
from langchain.chat_models import ChatOpenAI
from streamlit_extras.stateful_button import button

# config
page_title = "paper search - Train"
page_icon = ":mag_right:"
st.set_page_config(page_title=page_title, page_icon=page_icon)

# title
html_title = '<h1 align="center"> <b> 🔎 Let Us Find The Most Relevant Papers </b></h1>'
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
    st.markdown("### 📚🕵️ Papers Search")
    st.markdown(
        "Search the internet for the most relevant papers that align with the review paper outlines")

    # get years to look back
    years_back = st.slider('Number of past years for the search', min_value=1,
                           max_value=60, value=20, step=1)

    if st.button('Run papers search'):
        # df contains all papers
        all_df = []

        # create search terms
        with st.spinner('1. Creating search terms ...'):
            llm = ChatOpenAI(
                openai_api_key=st.session_state['openai_api'], temperature=1, model_name=st.session_state['openai_model_opt'])
            chat_prompt = saf.search_terms_prompt()
            chain = LLMChain(llm=llm, prompt=chat_prompt)
            search_terms = chain.run(expertise_areas=st.session_state['expertise_areas'],
                                     subject=st.session_state['paper_title'], outline=st.session_state['paper_outline'],
                                     num_search_terms=saf.num_search_terms, search_terms_formate=saf.search_terms_formate)
            search_terms_dict = ast.literal_eval(search_terms)
            st.write('####')
            st.write('Search terms to use')
            st.json(search_terms_dict)
        st.write('####')
        # search papers according to search terms
        for i in range(saf.num_search_terms):
            k = search_terms_dict[i+1]
            with st.spinner(f'{i+2}. Searching for journal papers related to {k} ...'):
                list_dict = []
                # google search
                search_results = saf.google_search(search_term=f'academic journal papers on {k}', api_key=st.session_state[
                                                   'google_api'], cse_id=st.session_state['google_search_engine_id'], dateRestrict=f'y{years_back}')
                # parsing
                for paper in search_results:
                    llm = ChatOpenAI(
                        openai_api_key=st.session_state['openai_api'], temperature=0, model_name=st.session_state['openai_model_opt'])
                    chat_prompt = saf.search_parsing_prompt()
                    chain = LLMChain(llm=llm, prompt=chat_prompt)
                    ppaper = chain.run(
                        paper_html=paper, journal_info_format=saf.journal_info_format)
                    ppaper_dict = ast.literal_eval(ppaper)
                    list_dict.append(ppaper_dict)
                    time.sleep(21)

                # display dfs
                df = pd.DataFrame(list_dict)
                df['search_term'] = k
                st.write(f'Papers related to {k}')
                st.dataframe(df)
                all_df.append(df)
                st.write('####')

        # final df with all papers
        df_final = pd.concat(all_df)
        df_final.insert(0, 'ID', range(1, 1 + len(df_final)))
        st.write('### 📄 List of Related Papers')
        st.dataframe(df_final)
