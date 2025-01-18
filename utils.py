from langchain.prompts import ChatPromptTemplate
from langchain_openai import ChatOpenAI
from langchain_community.utilities import WikipediaAPIWrapper

import os


def generate_script(subject, video_length,
                    creativity, api_key):
    title_template = ChatPromptTemplate.from_messages(
        [
            ("human", "Please create an engaging title for a video on the topic '{subject}'")
        ]
    )

    script_template = ChatPromptTemplate.from_messages(
        [
            (
                "human",
                """You are a content creator for short video channels. Based on the following title and related information, write a script for a short video.
    Video Title: {title}, Video Duration: {duration} minutes. The length of the generated script should follow the video's duration requirements as closely as possible.
    Make sure to grab attention at the beginning, provide value in the middle, and end with a surprise. The script structure should be divided into [Beginning, Middle, End].
    The overall tone should be as lighthearted and fun as possible, appealing to a young audience.
    The content of the script can reference information found via the following Wikipedia search, but it should only be used as a reference, incorporating only relevant parts and ignoring irrelevant ones:
    ```{wikipedia_search}```
    """
            )
        ]
    )

    model = ChatOpenAI(openai_api_key=api_key, temperature=creativity)

    title_chain = title_template | model
    script_chain = script_template | model

    title = title_chain.invoke({"subject": subject}).content

    #default parameter sets language to English
    search = WikipediaAPIWrapper()
    search_result = search.run(subject)

    script = script_chain.invoke({"title": title, "duration": video_length, "wikipedia_search": search_result}).content

    return search_result, title, script

#print(generate_script("Valorant", 1, 0.7, os.getenv("OPENAI_API_KEY")))