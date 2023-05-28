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
    }"""

# outline creation prompt


def generate_outline_prompt():
    """outlines creation prompt

        Returns:
        str: prompt string
    """
    system_message_prompt = SystemMessagePromptTemplate.from_template(
        "You have exceptional proficiency in the area of {expertise_areas}, also you are specialized in creating well-structured outlines for review papers that meet the rigorous standards of top academic journals")
    human_message_prompt = HumanMessagePromptTemplate.from_template(
        """Create an outline for academic review papers on the topic of "{subject}". Please follow this format: {outline_format}. add as many section as possible and make it as python dictionary""")

    chat_prompt = ChatPromptTemplate.from_messages(
        [system_message_prompt, human_message_prompt])

    return chat_prompt
