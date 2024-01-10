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
    "journal": "",
    "abstract": "",
    "link": ""
}


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
        """Given this JSON data "{paper_html}", extract and organize the information according to the following format "{journal_info_format}". If certain information isn't clear or is unavailable, insert "None". For the final output, make it as a python dictionary without anything else""")

    chat_prompt = ChatPromptTemplate.from_messages(
        [system_message_prompt, human_message_prompt])

    return chat_prompt
