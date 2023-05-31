from apiclient.discovery import build
from langchain.prompts.chat import (ChatPromptTemplate,
                                    HumanMessagePromptTemplate,
                                    SystemMessagePromptTemplate)

# outlines format
outline_format = """{
    "I. Header": {
        "A. Section": [
            {"1": "to discuss"},
            {"2": "to discuss"},
            {"3": "to discuss"}
        ],
        "B. Section": [
            {"1": "to discuss"},
            {"2": "to discuss"},
            {"3": "to discuss"}
        ]
    }
    """
# journal info collection
journal_info_format = {
    "title": "",
    "author(s)": "",
    "publishing date": "",
    "abstract": "",
    "journal": "",
    "link": ""
}

# search terms format
search_terms_formate = """{1: 'search_term_1', 2: 'search_term_2', 3: 'search_term_3', ....}"""

# number of search terms
num_search_terms = 2


def generate_outline_prompt():
    """outlines creation prompt

        Returns:
        str: prompt string
    """
    system_message_prompt = SystemMessagePromptTemplate.from_template(
        "You have exceptional proficiency in the area(s) of {expertise_areas}, also you are specialized in creating well-structured outlines for review papers that meet the rigorous standards of top academic journals")
    human_message_prompt = HumanMessagePromptTemplate.from_template(
        """Create an outline for academic review papers on the topic of "{subject}". Please ensure you integrate these specific criteria "{elaborate_user}" into your outline formation process. Follow this format: {outline_format} and include as many sections as necessary to thoroughly cover the topic. For the final output, please structure the outline as a Python dictionary""")

    chat_prompt = ChatPromptTemplate.from_messages(
        [system_message_prompt, human_message_prompt])

    return chat_prompt


def search_terms_prompt():
    """create prompt for most effective google search terms needed to look for academic papers from certain outlines 

        Returns:
        str: prompt string
    """
    system_message_prompt = SystemMessagePromptTemplate.from_template(
        "You have strong background in the field(s) of {expertise_areas}, also your have specialty in academic research and internet searching for the most relevant academic papers needed for writing review paper about {subject}. You excel at developing google search terms guided by this review paper's outline.")
    human_message_prompt = HumanMessagePromptTemplate.from_template(
        """Given the existing outline "{outline}", formulate {num_search_terms} Google search terms that would yield the most relevant academic papers. Present these terms as a Python dictionary using this format {search_terms_formate}.""")

    chat_prompt = ChatPromptTemplate.from_messages(
        [system_message_prompt, human_message_prompt])

    return chat_prompt


def google_search(search_term, api_key, cse_id, total_results=10, dateRestrict=None):
    """Perform a Google search using the Custom Search JSON API.

    Args:
        search_term (str): The search term to query.
        api_key (str): The API key for accessing the Google API.
        cse_id (str): The ID for the Custom Search Engine (CSE).
        total_results (int, optional): The total number of results to return. Default is 20.
        dateRestrict (str, optional): Limits results to a date range specified as [unit][time] (e.g., 'y5' for past 5 years). Default is None.

    Returns:
        list: A list of search results obtained from the Google API.
    """
    service = build("customsearch", "v1", developerKey=api_key)
    results = []
    for i in range(0, total_results, 10):
        start = i + 1
        res = service.cse().list(q=search_term, cx=cse_id, start=start,
                                 dateRestrict=dateRestrict).execute()
        results.extend(res['items'])
    return results


def search_parsing_prompt():
    """parse google search items 

        Returns:
        str: prompt string
    """
    system_message_prompt = SystemMessagePromptTemplate.from_template(
        "You are an academic researcher specializing in data extraction with advanced skills in JSON and HTML parsing.")
    human_message_prompt = HumanMessagePromptTemplate.from_template(
        """Given this JSON data "{paper_html}", extract and organize the information according to the following format "{journal_info_format}". If certain information isn't clear or is unavailable, insert "None". """)

    chat_prompt = ChatPromptTemplate.from_messages(
        [system_message_prompt, human_message_prompt])

    return chat_prompt


def combine_search_term(search_term):
    """Custom aggregation function to concatenate unique search terms.

    Args:
        search_term (list): List of search terms.

    Returns:
        str: Concatenated search terms separated by commas if there are multiple terms, or the single term if there is only one.
    """
    unique_search_term = set(search_term)
    if len(unique_search_term) > 1:
        return ', '.join(unique_search_term)
    else:
        return list(unique_search_term)[0]
