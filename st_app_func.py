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
        "You have exceptional proficiency in the area(s) of {expertise_areas}, also you are specialized in creating well-structured outlines for review papers that meet the rigorous standards of top academic journals")
    human_message_prompt = HumanMessagePromptTemplate.from_template(
        """Create an outline for academic review papers on the topic of "{subject}". Please ensure you integrate these specific criteria "{elaborate_user}" into your outline formation process. Follow this format: {outline_format} and include as many sections as necessary to thoroughly cover the topic. For the final output, please structure the outline as a Python dictionary""")

    chat_prompt = ChatPromptTemplate.from_messages(
        [system_message_prompt, human_message_prompt])

    return chat_prompt
