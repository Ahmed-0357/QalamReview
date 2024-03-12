import ast
import base64
import os
import time

import streamlit as st
import yaml
from langchain import LLMChain
from langchain.chat_models import ChatOpenAI

import st_outline_search_func as sos

# config
page_title = "paper outline"
page_icon = ":bulb:"
st.set_page_config(page_title=page_title, page_icon=page_icon)

# title
html_title = '<h1 align="center"> <b> 💡 Let Us Make The Perfect Outline </b></h1>'
st.markdown(html_title, unsafe_allow_html=True)
st.markdown("#")
icon_ = "🚨"

# check session state for api
if st.session_state["openai_api"] == "" or st.session_state["openai_model_opt"] == "":
    st.error("Please complete OpenAI configuration on the main page first.", icon=icon_)


else:
    # session state
    st.session_state["paper_title"] = ""
    st.session_state["expertise_areas"] = ""
    st.session_state["paper_outline"] = ""

    # get message and expertise_areas
    st.markdown("### 📝 Review Paper Title")
    st.markdown(
        "Please provide a comprehensive title for the review paper you intend to write."
    )
    subject = st.text_input(
        "",
        placeholder="example: The Impact of CO2 Diffusion Mechanism on Underground CO2 Storage in Aquifers",
        label_visibility="collapsed",
    )
    subject = subject.title()

    st.markdown("### 📚 Areas of Expertise")
    st.markdown(
        "Please list areas of expertise to guide the AI in generating more refined and tailored results."
    )
    expertise_areas = st.text_input(
        "",
        placeholder="example: reservoir engineering,  petroleum engineering, CO2 storage, enhanced oil recovery",
        label_visibility="collapsed",
    )

    # update session
    st.session_state["paper_title"] = subject
    st.session_state["expertise_areas"] = expertise_areas

    st.markdown("---")

    # Outline upload
    st.markdown("### 📄 Upload Your Outline")
    outline_file = st.file_uploader("", type=["yaml"])
    if outline_file:
        outline_user = yaml.safe_load(outline_file)
        st.session_state["paper_outline"] = outline_user

    st.markdown("####")
    # show and download sample
    with open(os.path.join("files", "outline_sample.yaml"), "r") as yaml_file:
        outline_sample = yaml.safe_load(yaml_file)
    if st.toggle("Show example of outline format"):
        st.text(yaml.dump(outline_sample, sort_keys=False))
    # download outline sample
    yaml_str = yaml.dump(outline_sample, sort_keys=False)
    b64 = base64.b64encode(yaml_str.encode()).decode()
    href = f'<a href="data:application/x-yaml;base64,{b64}" download="outline_sample.yaml">Download Outline Sample (YAML)</a>'
    st.markdown(href, unsafe_allow_html=True)

    st.markdown("---")
    # AI Generated Outline
    st.markdown("### 🧠 AI-Generated Outline")
    st.markdown(
        "If you wish to generate the outline using AI, check the toggle bottom below."
    )
    if st.toggle("Start AI-Generated outline"):
        # st.markdown("#####")
        elaborate_user = st.text_area(
            "Elaborate your needs (optional)",
            placeholder="""example: focus on comparing traditional and modern methods in the field, and include a detailed discussion on recent experimental results.""",
        )

        if st.button("Generate"):
            # session check
            if (
                st.session_state["paper_title"] == ""
                or st.session_state["expertise_areas"] == ""
            ):
                st.error(
                    "Please complete the paper title and areas of expertise first.",
                    icon=icon_,
                )
            else:
                with st.spinner("generating, please wait..."):
                    # chose model
                    model_name = (
                        st.session_state["openai_model_opt"].split("&")[1]
                        if "&" in st.session_state["openai_model_opt"]
                        else st.session_state["openai_model_opt"]
                    )
                    time.sleep(10)

                    llm = ChatOpenAI(
                        openai_api_key=st.session_state["openai_api"],
                        temperature=1,
                        model_name=model_name,
                    )
                    chat_prompt = sos.generate_outline_prompt()

                    try:
                        chain = LLMChain(llm=llm, prompt=chat_prompt)
                        result = chain.run(
                            expertise_areas=expertise_areas,
                            subject=subject,
                            elaborate_user=elaborate_user,
                            outline_format=sos.outline_format,
                        )
                    except Exception as e:
                        st.error(f"An unexpected error has occurred: {e}", icon=icon_)
                    else:
                        try:
                            result_dict = ast.literal_eval(result)
                            st.text(yaml.dump(result_dict, sort_keys=False))
                        except Exception as e:
                            st.error(
                                "An unexpected error has occurred please click Generate button again",
                                icon=icon_,
                            )
                        else:
                            # update session
                            st.session_state["paper_outline"] = result_dict

                            # download generated outline
                            yaml_gen = yaml.dump(result_dict, sort_keys=False)
                            b64_g = base64.b64encode(yaml_gen.encode()).decode()
                            href = f'<a href="data:application/x-yaml;base64,{b64_g}" download="outline_generated.yaml">Download Generated Outline (YAML)</a>'
                            st.markdown(href, unsafe_allow_html=True)
