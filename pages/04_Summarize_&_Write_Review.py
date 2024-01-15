import base64
import os
import shutil
import time
from functools import reduce

import pandas as pd
import streamlit as st
from langchain.chat_models import ChatOpenAI
from langchain.document_loaders import PyPDFLoader
from langchain.text_splitter import TokenTextSplitter

import st_paper_writing_func as spw

# config
st.set_page_config(page_title="paper writing", page_icon="📜")

# titles
html_title = '<h1 align="center"> <b> 📜 Summary and Review Paper Creation </b></h1>'
st.markdown(html_title, unsafe_allow_html=True)
st.markdown("#")
icon_ = "🚨"

# check session state
if st.session_state["openai_api"] == "" or st.session_state["openai_model_opt"] == "":
    st.error(
        "Please complete OpenAI configuration configuration on the main page first.",
        icon=icon_,
    )
elif (
    st.session_state["paper_title"] == ""
    or st.session_state["expertise_areas"] == ""
    or st.session_state["paper_outline"] == ""
):
    st.error(
        "Please first fill paper title, areas of expertise and paper outlines on Outline page.",
        icon=icon_,
    )
else:
    st.markdown("### 📝 Academic Papers")
    st.markdown(
        "Upload the academic papers that you intend to use for crafting your narrative review paper"
    )

    uploaded_papers = st.file_uploader(
        "", type=["pdf"], accept_multiple_files=True, label_visibility="collapsed"
    )

    # Directory to temporary save papers
    papers_dir = "papers"
    # Ensure directory exists
    os.makedirs(papers_dir, exist_ok=True)

    if uploaded_papers:
        for uploaded_paper in uploaded_papers:
            try:
                # Create a temporary file and write the uploaded file's bytes to it
                with open(os.path.join(papers_dir, uploaded_paper.name), "wb") as f:
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
    summary_toggle = st.toggle("Summarize only")
    if not summary_toggle:
        st.markdown("### ⚙️ Manuscript Writeup Settings")
        rel_score_cutoff = st.slider(
            "🥇 Set relevance score threshold (0-100)",
            min_value=0,
            max_value=100,
            value=90,
            step=1,
        )

        papers_per_sub = st.slider(
            "📄 Specify number of papers per subsection",
            min_value=3,
            max_value=50,
            value=10,
            step=1,
        )
    else:
        rel_score_cutoff, papers_per_sub = 100, 3  # in case of summary only

    generate_button = st.button("Start")
    if generate_button and not uploaded_papers:
        st.error("Please upload journal papers before generating. ")
    elif generate_button:
        # outline list and dict
        outline_list = [
            f"{main_key} - {sub_key} - {list(item.values())[0]}"
            for main_key, main_value in st.session_state["paper_outline"].items()
            for sub_key, sub_value in main_value.items()
            for item in sub_value
        ]

        # llm models instantiation
        # chose model --> (gpt-3.5 - summary)
        model_name_s, to_sleep_s = (
            st.session_state["openai_model_opt"].split("&")[0]
            if "&" in st.session_state["openai_model_opt"]
            else st.session_state["openai_model_opt"],
            17,
        )
        chat = ChatOpenAI(
            openai_api_key=st.session_state["openai_api"],
            temperature=0,
            model_name=model_name_s,
        )

        # relevance model
        # chose model
        model_name_r = (
            st.session_state["openai_model_opt"].split("&")[1]
            if "&" in st.session_state["openai_model_opt"]
            else st.session_state["openai_model_opt"]
        )
        to_sleep_r = 60 if "&" in st.session_state["openai_model_opt"] else 17
        chat_ = ChatOpenAI(
            openai_api_key=st.session_state["openai_api"],
            temperature=0,
            model_name=model_name_r,
        )

        # summary file and dir
        dir_name = "summary"
        summary_file = "papers_summary.txt"
        summary_file_path = os.path.join(dir_name, summary_file)
        relevance_file = "papers_relevance.txt"
        relevance_file_path = os.path.join(dir_name, relevance_file)

        # summary spinner
        working_on_text = " and ranking them." if not summary_toggle else "."
        with st.spinner(
            f"""**🚀 Working on summarizing the papers{working_on_text} Please wait...**"""
        ):
            # dir to and file to save summary data
            if os.path.exists(dir_name):
                shutil.rmtree(dir_name)
            if not os.path.exists(dir_name):
                os.makedirs(dir_name)

            # clean files
            with open(summary_file_path, "w") as file:
                pass
            with open(relevance_file_path, "w") as file:
                pass

            # input dicts
            # input dict summary
            input_dict_summary = {
                "llm_model": chat,
                "expertise_areas": st.session_state["expertise_areas"],
                "subject": st.session_state["paper_title"],
                "outline": outline_list,
                "sum_only": summary_toggle,
            }  # when sum_only, outlines as not used during summary
            # input dict relevance
            input_dict_relevance = {
                "llm_model": (chat_, chat),
                "expertise_areas": st.session_state["expertise_areas"],
                "subject": st.session_state["paper_title"],
                "outline": outline_list,
                "sum_only": summary_toggle,
            }  # chat is used as parser # when sum_only, rel value of 200 is assigned

            # loop through papers
            working_on_text_ = (
                "and generating relevance scores for " if not summary_toggle else ""
            )
            for paper_path in os.listdir(papers_dir):
                with st.spinner(f"Summarizing {working_on_text_}{paper_path} ..."):
                    # read paper content
                    loader = PyPDFLoader(os.path.join(papers_dir, paper_path))
                    pages = loader.load_and_split()
                    paper_content = "".join(page.page_content for page in pages)

                    # split paper token wise (12k token for gpt-3 and 28k gpt-4)
                    if model_name_s == "gpt-3.5-turbo-1106":
                        text_splitter = TokenTextSplitter(
                            chunk_size=12000, chunk_overlap=0
                        )
                    # else:
                    #     text_splitter = TokenTextSplitter(
                    #         chunk_size=28000, chunk_overlap=0)
                    texts = text_splitter.split_text(paper_content)

                    try:
                        # summarization class
                        summ = spw.PaperSummary(texts)
                        output_summ = summ.summarize(**input_dict_summary)
                    except Exception as e:
                        time.sleep(to_sleep_s)
                        continue
                    else:
                        time.sleep(to_sleep_s)
                        try:
                            # relevance class
                            rele = spw.RelevanceAnalysis(output_summ)
                            output_rele = rele.relevancy_score(**input_dict_relevance)
                        except Exception as e:
                            if (
                                not summary_toggle
                            ):  # in case of summary only, no rel sleep
                                time.sleep(to_sleep_r)
                            continue
                        else:
                            # show to user
                            st.json(output_summ)
                            if not summary_toggle:
                                st.json(output_rele)
                            st.markdown(
                                '<hr style="border:1.5px solid #808080;">',
                                unsafe_allow_html=True,
                            )
                            with open(summary_file_path, "a", encoding="utf-8") as file:
                                file.write(str(output_summ) + "\n\n")
                            with open(
                                relevance_file_path, "a", encoding="utf-8"
                            ) as file:
                                file.write(str(output_rele) + "\n\n")
                            if (
                                not summary_toggle
                            ):  # in case of summary only, no rel sleep
                                time.sleep(to_sleep_r)

        if summary_toggle:  # just show summary csv
            # save summary of scholarly papers
            df_summary = spw.load_and_process_df(summary_file_path, numeric=False)
            # sort papers by year
            df_summary.sort_values(by="year", inplace=True)
            csv = df_summary.to_csv(index=False)
            b64 = base64.b64encode(csv.encode()).decode()
            href = f'<a href="data:text/csv;base64,{b64}" download="papers_summary.csv">Download Summaries of Academic Papers (CSV)</a>'
            st.markdown(href, unsafe_allow_html=True)
        else:  # just show summary, relevance and paper writeup
            with st.spinner(
                "**✒️ Writing the narrative review paper. Please wait...**"
            ):
                df_relevancy = spw.load_and_process_df(relevance_file_path)
                df_summary = spw.load_and_process_df(summary_file_path, numeric=False)

                summ_rele = pd.concat([df_summary, df_relevancy], axis=1)

                del df_relevancy
                del df_summary

                references_list = []
                output_sections = []
                manwri = spw.ManuscriptWriting()
                for i in range(len(outline_list)):
                    with st.spinner(f"Writing section: {outline_list[i]} ..."):
                        try:
                            # relevance cutoff
                            summ_rele_filtered = summ_rele[
                                summ_rele[outline_list[i]] >= rel_score_cutoff
                            ].copy()
                            # sort papers by year
                            summ_rele_filtered.sort_values(by="year", inplace=True)
                        except Exception as e:
                            st.write(e)
                            continue
                        else:
                            summ_rele_filtered_copy = summ_rele_filtered.iloc[
                                : int(papers_per_sub), :8
                            ].copy()
                            # if filtered df is empty just add note
                            if len(summ_rele_filtered_copy) == 0:
                                output_sections.append(
                                    (
                                        outline_list[i],
                                        "Scholarly papers do not provide enough information to write this section.",
                                    )
                                )
                            else:
                                # get text from df
                                summ_rele_list = summ_rele_filtered_copy.to_dict(
                                    orient="records"
                                )
                                summ_rele_text = "\n\n".join(
                                    str(item) for item in summ_rele_list
                                )

                                del summ_rele_filtered_copy
                                del summ_rele_list

                                # split text select llm model and set sleeping time
                                if "&" in st.session_state["openai_model_opt"]:
                                    text_splitter = TokenTextSplitter(
                                        chunk_size=6600, chunk_overlap=0
                                    )
                                    llm_model = chat_
                                    to_sleep = 60
                                else:
                                    text_splitter = TokenTextSplitter(
                                        chunk_size=12000, chunk_overlap=0
                                    )
                                    llm_model = chat
                                    to_sleep = 17
                                texts = text_splitter.split_text(summ_rele_text)

                                # input dict writing
                                input_dict_writing = {
                                    "llm_model": llm_model,
                                    "expertise_areas": st.session_state[
                                        "expertise_areas"
                                    ],
                                    "subject": st.session_state["paper_title"],
                                    "section": outline_list[i],
                                    "texts": texts,
                                    "to_sleep": to_sleep,
                                }
                                try:
                                    output = manwri.section_writing(
                                        **input_dict_writing
                                    )
                                except Exception as e:
                                    time.sleep(to_sleep)
                                    continue
                                else:
                                    output_sections.append((outline_list[i], output))
                                    time.sleep(to_sleep)

                                    # references
                                    references_df = summ_rele_filtered.iloc[
                                        : int(papers_per_sub), :4
                                    ].copy()
                                    references_list.append(references_df)

                # merge all content and final write up
                output_sections_result = {}
                for keys, summary in [
                    (tuple(j.strip() for j in i.split("-")), s)
                    for i, s in output_sections
                ]:
                    reduce(
                        lambda d, key: d.setdefault(key, {}),
                        keys[:-1],
                        output_sections_result,
                    )[keys[-1]] = summary

                manwri.final_writeup(
                    st.session_state["paper_title"], output_sections_result
                )

                # add references
                # concat refer df and remove duplicates
                if (
                    references_list
                ):  # in case no writeup, just return empty list of references
                    combined_refer_df = pd.concat(references_list, ignore_index=True)

                    combined_refer_df = combined_refer_df.drop_duplicates()

                    # get text from df
                    refer_list = combined_refer_df.to_dict(orient="records")
                    references_text = "\n\n".join(str(item) for item in refer_list)

                    # list of references (APA)
                    input_dict_refer = {
                        "llm_model": chat,
                        "references_text": references_text,
                    }
                    try:
                        output = manwri.references(**input_dict_refer)
                    except:
                        pass
                    else:
                        manwri.add_text("References", "Heading 1", bold=True, size=12)
                        manwri.add_text(output, "Normal", size=11)

                else:
                    manwri.add_text("References", "Heading 1", bold=True, size=12)
                    manwri.add_text("", "Normal", size=11)

                # save summary and relevancy of scholarly papers
                csv = summ_rele.to_csv(index=False)
                b64 = base64.b64encode(csv.encode()).decode()
                href = f'<a href="data:text/csv;base64,{b64}" download="papers_summary_relevancy.csv">Download Summaries of Academic Papers and Relevancy Scores (CSV)</a>'
                st.markdown(href, unsafe_allow_html=True)

                # save manuscript
                with open(
                    os.path.join("manuscript", "narrative_review.docx"), "rb"
                ) as f:
                    data = f.read()
                bin_str = base64.b64encode(data).decode()
                href = f'<a href="data:application/octet-stream;base64,{bin_str}" download="narrative_review.docx">Download Final Narrative Review (DOCX)</a>'
                st.markdown(href, unsafe_allow_html=True)
