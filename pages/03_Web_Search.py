import ast
import base64
import time

import pandas as pd
import st_outline_search_func as sos
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
if st.session_state['openai_api'] == '' or st.session_state['openai_model_opt'] == '':
    st.error(
        'Please complete OpenAI configuration on the main page first.', icon="🚨")

if st.session_state['google_api'] == '' or st.session_state['google_search_engine_id'] == '':
    st.error(
        'Please complete Google search engine configuration on the main page first.', icon="🚨")

elif st.session_state['paper_title'] == '' or st.session_state['expertise_areas'] == '' or st.session_state['paper_outline'] == '':

    st.error(
        'Please first fill paper title, areas of expertise and paper outlines on Outline page.', icon="🚨")
else:
    st.markdown("### 📚🕵️ Scholarly Paper Search")
    st.markdown(
        "Search the internet for the most relevant papers that align with the review paper outlines")

    # get years to look back
    years_back = st.slider('📅 Indicate the number of past years to encompass in your search', min_value=1,
                           max_value=60, value=20, step=1)

    num_search_terms = st.slider('🔑 Please select the number of search terms', min_value=2,
                                 max_value=15, value=3, step=1)

    total_results = st.slider('🌐 Please specify the number of search results per search term', min_value=5,
                              max_value=100, value=10, step=5)

    if st.button('Start Web Search'):
        # df contains all papers
        all_df = []

        # create search terms
        with st.spinner('🧠 Creating search terms. Please wait...'):
            # chose model
            model_name = st.session_state['openai_model_opt'].split(
                '&')[1] if '&' in st.session_state['openai_model_opt'] else st.session_state['openai_model_opt']
            llm = ChatOpenAI(
                openai_api_key=st.session_state['openai_api'], temperature=1, model_name=model_name)
            chat_prompt = sos.search_terms_prompt()
            chain = LLMChain(llm=llm, prompt=chat_prompt)
            search_terms = chain.run(expertise_areas=st.session_state['expertise_areas'],
                                     subject=st.session_state['paper_title'], outline=st.session_state['paper_outline'],
                                     num_search_terms=num_search_terms)
            try:
                search_terms_list = ast.literal_eval(search_terms)
            except Exception as e:  # in case the formate is not correct
                st.error(
                    f'An unexpected error has occurred: {e}, please click Start Web Search again', icon="🚨")
            else:
                st.write('####')
                st.write('Search terms to use')
                st.json(search_terms_list)

        st.write('####')
        # search papers according to search terms
        for i in range(num_search_terms):
            k = search_terms_list[i]
            with st.spinner(f'🔎 Searching for journal papers related to {k.lower()}. Please wait...'):
                list_dict = []
                # google search
                search_results = sos.google_search(search_term=f'academic journal papers on {k}', api_key=st.session_state[
                                                   'google_api'], cse_id=st.session_state['google_search_engine_id'], total_results=int(total_results), dateRestrict=f'y{int(years_back)}')
                # parsing
                # chose model --> (gpt-3.5)
                model_name = st.session_state['openai_model_opt'].split(
                    '&')[0] if '&' in st.session_state['openai_model_opt'] else st.session_state['openai_model_opt']
                for paper in search_results:
                    llm = ChatOpenAI(
                        openai_api_key=st.session_state['openai_api'], temperature=0, model_name=model_name)
                    chat_prompt = sos.search_parsing_prompt()
                    # in case of tokens higher than 4k
                    try:
                        chain = LLMChain(llm=llm, prompt=chat_prompt)
                        ppaper = chain.run(
                            paper_html=paper, journal_info_format=sos.journal_info_format)
                        ppaper_dict = ast.literal_eval(ppaper)
                    except:
                        time.sleep(5)
                        continue
                    else:
                        list_dict.append(ppaper_dict)
                        time.sleep(5)

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
        df_final['publishing date'] = df_final['publishing date'].dt.strftime(
            '%d-%m-%Y')

        # remove duplicate papers
        df_final = df_final.drop_duplicates(
            subset=['title', 'author(s)'], keep='last')

        # add id column
        df_final.insert(0, 'ID', range(1, 1 + len(df_final)))
        df_final.reset_index(drop=True, inplace=True)

        st.write('### 📑 Relevant Paper List')
        st.dataframe(df_final)

        # Convert DataFrame to CSV for download
        csv = df_final.to_csv(index=False)
        # Convert CSV string to bytes
        b64 = base64.b64encode(csv.encode()).decode()
        href = f'<a href="data:text/csv;base64,{b64}" download="relevant_papers.csv">Download Relevant Paper (CSV)</a>'
        st.markdown(href, unsafe_allow_html=True)
