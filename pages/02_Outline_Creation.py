import ast
import base64
import json
import os

import st_outline_search_func as sos
import streamlit as st
from langchain import LLMChain
from langchain.chat_models import ChatOpenAI

# config
page_title = "paper outline"
page_icon = ":bulb:"
st.set_page_config(page_title=page_title, page_icon=page_icon)

# st.write(st.session_state)

# title
html_title = '<h1 align="center"> <b> 💡 Let Us Make The Perfect Paper\'s Outline </b></h1>'
st.markdown(html_title, unsafe_allow_html=True)
st.markdown('#')

# check session state for api
if st.session_state['openai_api'] == '' or st.session_state['openai_model_opt'] == '':
    st.error(
        'Please complete the initial configuration on the main page first.', icon="🚨")


else:
    # session state
    st.session_state['paper_title'] = ''
    st.session_state['expertise_areas'] = ''
    st.session_state['paper_outline'] = ''

    # get message and expertise_areas
    st.markdown("### 📝 Review Paper Title")
    st.markdown(
        "Provide a comprehensive title for the review paper you wish to create.")
    subject = st.text_input(
        '', placeholder='example: The Impact of CO2 Diffusion Mechanism on Underground CO2 Storage in Aquifers', label_visibility='collapsed')
    subject = subject.title()

    st.markdown("### 📚 Areas of Expertise")
    st.markdown(
        "Please list the areas of expertise that will guide the AI to create more refined and tailored paper.")
    expertise_areas = st.text_input(
        '', placeholder="example: reservoir engineering,  petroleum engineering, CO2 storage, enhanced oil recovery", label_visibility='collapsed')

    # update session
    st.session_state['paper_title'] = subject
    st.session_state['expertise_areas'] = expertise_areas

    st.markdown("---")

    # Outline upload
    st.markdown("### 📄 Upload Outline File")
    outline_file = st.file_uploader('', type=['json'])
    if outline_file:
        outline_user = json.load(outline_file)
        st.session_state['paper_outline'] = outline_user

    st.markdown('####')
    # show and download sample
    with open(os.path.join('files', 'outline_sample.json'), 'r') as json_file:
        outline_sample = json_file.read()
    if st.checkbox('Show outline sample'):
        st.json(outline_sample)

    # download outline sample
    json_str = json.dumps(outline_sample)
    b64 = base64.b64encode(json_str.encode()).decode()
    href = f'<a href="data:application/json;base64,{b64}" download="outline_sample.json">Download Outline Sample (JSON)</a>'
    st.markdown(href, unsafe_allow_html=True)

    st.markdown("---")
    # AI Generated Outline
    st.markdown("### 🧠 AI Generated Outline")
    st.markdown(
        "If you wish to generate an outline for your paper using AI, check the botton below.")

    if st.checkbox('Start AI generated outline'):
        # st.markdown("#####")
        elaborate_user = st.text_area('Elaborate your needs (optional)',
                                      placeholder='''example: focus on comparing traditional and modern methods in the field, and include a detailed discussion on recent experimental results.''')

        if st.button('Generate'):
            # session check
            if st.session_state['paper_title'] == '' or st.session_state['expertise_areas'] == '':
                st.error(
                    'Please complete the paper title and areas of expertise first.', icon="🚨")
            else:
                with st.spinner('Wait for it...'):
                    llm = ChatOpenAI(
                        openai_api_key=st.session_state['openai_api'], temperature=1, model_name=st.session_state['openai_model_opt'])
                    chat_prompt = sos.generate_outline_prompt()

                    try:
                        chain = LLMChain(llm=llm, prompt=chat_prompt)
                        result = chain.run(expertise_areas=expertise_areas,
                                           subject=subject, elaborate_user=elaborate_user, outline_format=sos.outline_format)
                    except Exception as e:
                        st.error(
                            f'An unexpected error has occurred: {e}', icon="🚨")
                    else:
                        try:
                            result_dict = ast.literal_eval(result)
                            st.json(result_dict)
                        except:
                            st.error(
                                'An unexpected error has occurred please click Generate button again', icon="🚨")
                        else:
                            # update session
                            st.session_state['paper_outline'] = result_dict

                            # download generated outline
                            json_gen = json.dumps(result_dict)
                            b64_g = base64.b64encode(
                                json_gen.encode()).decode()
                            href = f'<a href="data:application/json;base64,{b64_g}" download="outline_generated.json">Download Generated Outline (JSON)</a>'
                            st.markdown(href, unsafe_allow_html=True)
