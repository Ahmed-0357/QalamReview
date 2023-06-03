import ast
import base64
import time

# import dateparser
import numpy as np
import pandas as pd
import st_app_func as saf
import streamlit as st
from langchain import LLMChain
from langchain.chat_models import ChatOpenAI

# config
page_title = "paper search"
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

    if st.button('Start Web Search'):
        # df contains all papers
        all_df = []

        # create search terms
        with st.spinner('🧠 Creating search terms. please wait...'):
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
            with st.spinner(f'🔎 Searching for journal papers related to {k.lower()}. please wait...'):
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
                    time.sleep(2)

                # display dfs
                df = pd.DataFrame(list_dict)
                df['search_term'] = k
                st.write(f'Papers on {k.lower()}')
                st.dataframe(df)
                all_df.append(df)
                st.write('####')

        # final df with all papers
        df_final = pd.concat(all_df)

        # data cleaning (none, data and remove duplicates)
        df_final.replace("None", "", inplace=True)
        df_final['publishing date'] = df['publishing date'].apply(
            lambda x: pd.to_datetime(x, errors='coerce') if pd.notnull(x) else pd.NaT)

        # remove duplicate papers and combine search term
        df_final = df_final.groupby(df_final.columns.tolist()[
            :-1], as_index=False).agg({df_final.columns.tolist()[-1]: saf.combine_search_term})

        # add id column
        df_final.insert(0, 'ID', range(1, 1 + len(df_final)))
        st.write('### 📑 Relevant Paper List')
        st.dataframe(df_final)

        # Convert DataFrame to CSV for download
        csv = df_final.to_csv(index=False)
        # Convert CSV string to bytes
        b64 = base64.b64encode(csv.encode()).decode()
        href = f'<a href="data:text/csv;base64,{b64}" download="relevant_papers.csv">Download as CSV</a>'
        st.markdown(href, unsafe_allow_html=True)
