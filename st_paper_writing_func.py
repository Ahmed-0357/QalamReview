import ast
import time

from langchain import LLMChain
from langchain.prompts.chat import (ChatPromptTemplate,
                                    HumanMessagePromptTemplate,
                                    SystemMessagePromptTemplate)


class PaperSummary:
    """summarizes a scholarly paper
    """

    def __init__(self, texts):
        """instantiation of paper summary class

        Args:
            texts (list): list of paper texts
        """
        self.texts = texts
        self.summarize_format = {
            "metadata": {
                "title": "",
                "author(s)": "",
                "journal": "",
                "year": ""},
            "summary": {
                "introduction": "",
                "methodology": "",
                "results/findings": "",
                "limitations/gaps": ""}
        }

    def paper_summary_prompt(self, p_type='once'):
        """outlines creation prompt
        Args:
            p_type(str): type of summary can be either once, many1 or many2. many1&2 for long paper that can not summarized via the 16k model 
        Returns:
            str: prompt string
        """

        if p_type == 'once':
            system_message_prompt = SystemMessagePromptTemplate.from_template("""Possessing a notable reputation as a researcher, and having exceptional skill in dissecting scholarly research papers, along with deep expertise in the field of {expertise_areas},
            your task is to meticulously analyze the provided document. Your goal is to craft a succinct summary of this intricate information, while preserving the integrity, accuracy, and precision of key concepts from the original academic material.
            
            Keep in mind that this summary will be a crucial part of the narrative review paper on the subject of {subject} and structured following the provided outline {outline}. During the construction of the summary, ensure diligent cross-referencing with the outline. If any information aligns with a section from the outline and is discussed or mentioned in the paper, it is crucial to incorporate it into the
            corresponding section of the summary in an appropriate manner.""")

            human_message_prompt = HumanMessagePromptTemplate.from_template("""Using the comprehensive content of the scholarly paper {paper_content}, your task is to distill, analyze, and categorize the information into two key structured sections: Metadata and Summary.
            
            Under "metadata", gather the following details
            
            "title": Identify the title of the paper.
            "author(s)": List the author(s) of the paper.
            "journal": Provide the name of the journal where the paper was published.
            "year": Mention the year of publication.
            
            If any of these details are absent from the paper content, please denote the corresponding field as 'None'.
            
            Under "summary", break down the information into the following categories:

            "introduction": Decode the background, problem statement, primary objectives, and motivations of the study from the paper content. If the content doesn't provide enough information for this, please denote this section as 'None'.

            "methodology": Develop a thorough understanding of the research methodologies used, drawing from the paper content. This might include data collection and analysis strategies, study design details, sample size, experimental setup, any simulations conducted, and analytical tools employed. If such details are not evident from the paper content, label this section as 'None'.

            "results/findings": Extract key findings, pivotal conclusions, and significant data trends or patterns from the paper content. If these details aren't sufficiently outlined, please mark this section as 'None'.

            "limitations/gaps": Identify potential limitations or gaps in the study, as suggested by the paper content. This could involve issues with the study design or research areas left unaddressed. If these aspects aren't clear, please denote this section as 'None'.

            Please assemble and structure the extracted information into a Python dictionary, adhering to the following format: {summarize_format}""")

        elif p_type == 'many1':
            system_message_prompt = SystemMessagePromptTemplate.from_template(
                """you have well known academic researcher specialized knowledge in {expertise_areas}""")

            human_message_prompt = HumanMessagePromptTemplate.from_template(
                """Could you please transform the academic article {paper_content} into a series of key points. Strive to retain as much information and details as you can and do not summarize. For the first key point, please incorporate the paper's title, authors, the publishing journal, and the date of publication""")

        else:
            system_message_prompt = SystemMessagePromptTemplate.from_template(
                """you have well known academic researcher specialized knowledge in {expertise_areas}""")

            human_message_prompt = HumanMessagePromptTemplate.from_template(
                """Could you please transform the academic article {paper_content} into a series of key points. Strive to retain as much information and details as you can and do not summarize. """)

        chat_prompt = ChatPromptTemplate.from_messages(
            [system_message_prompt, human_message_prompt])

        return chat_prompt

    def summarize(self, **kwargs):
        """summarize the scholarly paper

        Returns:
            dict: paper summary in the specified format
        """
        llm_model = kwargs.get('llm_model')
        expertise_areas = kwargs.get('expertise_areas')
        subject = kwargs.get('subject')
        outline = kwargs.get('outline')

        if len(self.texts) == 1:
            chat_prompt = self.paper_summary_prompt(p_type='once')
            chain = LLMChain(llm=llm_model, prompt=chat_prompt)

            output = chain.run(expertise_areas=expertise_areas, subject=subject, outline=outline,
                               paper_content=self.texts[0], summarize_format=self.summarize_format)
        else:
            section_summary = {}
            for i in range(len(self.texts)):
                if i == 0:
                    chat_prompt = self.paper_summary_prompt(p_type='many1')
                    chain = LLMChain(llm=llm_model, prompt=chat_prompt)
                    r = chain.run(expertise_areas=expertise_areas,
                                  paper_content=self.texts[i])
                    section_summary[i] = r
                else:
                    chat_prompt = self.paper_summary_prompt(p_type='many2')
                    chain = LLMChain(llm=llm_model, prompt=chat_prompt)
                    r = chain.run(expertise_areas=expertise_areas,
                                  paper_content=self.texts[i])
                    section_summary[i] = r

                    time.sleep(9)

            chat_prompt = self.paper_summary_prompt(p_type='once')
            chain = LLMChain(llm=llm_model, prompt=chat_prompt)
            all_sections = ' '.join(list(section_summary.values()))
            output = chain.run(expertise_areas=expertise_areas, subject=subject, outline=outline,
                               paper_content=all_sections, summarize_format=self.summarize_format)

        output_dict = ast.literal_eval(output)
        return output_dict


class RelevanceAnalysis:
    """"Assign a relevancy rating (0-100) to each paper summary, guided by the outline" 
    """
    def __init__(self, paper_summary):
        """instantiate the class

        Args:
            paper_summary (dict): paper summary
        """
        self.paper_summary = paper_summary
        
    def relevancy_analysis_prompt(self):
        """relevancy prompt
        Returns:
            str: prompt string
        """
        system_message_prompt = SystemMessagePromptTemplate.from_template(
            """Equipped with substantial expertise in {expertise_areas}, you're an accomplished researcher renowned for crafting insightful narrative review papers and conducting thorough assessments of journal paper summaries.
            Your task harnesses your unique aptitude for aligning the essence of a journal summary with the framework of a narrative review paper. Apply your knowledge and experience to successfully complete this assignment.""")
        human_message_prompt = HumanMessagePromptTemplate.from_template(
            """With the provided summary of a specific paper {paper_summary} and the outline of a narrative review paper {outline} titled {subject}, your mission is to determine which main section of the review most closely aligns with the paper.
            Conduct a thorough analysis of the content, mapping it to the most relevant section(s) within the review outline.
            For each identified section, allot a similarity score ranging from 0 to 100, where 100 indicates strong relevance
            and 0 implies no relevance. Compile your results in a Python dictionary,
            adhering strictly to the provided format {relevance_format}""")
        chat_prompt = ChatPromptTemplate.from_messages(
            [system_message_prompt, human_message_prompt])
        
        return chat_prompt
    
    def relevancy_score(self, **kwargs):
        """get relevancy score using llm model. relevancy score ranges between 0 to 100

        Returns:
            dict: relevancy score
        """
        llm_model = kwargs.get('llm_model')
        expertise_areas = kwargs.get('expertise_areas')
        subject = kwargs.get('subject')
        outline = kwargs.get('outline')
        relevance_format = {i: "" for i in outline}
        
        chat_prompt = self.relevancy_analysis_prompt()
        chain = LLMChain(llm=llm_model, prompt=chat_prompt)
        output = chain.run(expertise_areas = expertise_areas, paper_summary=self.paper_summary, outline=outline, subject = subject, relevance_format=relevance_format)
        
        output_dict = ast.literal_eval(output)
        return output_dict
        