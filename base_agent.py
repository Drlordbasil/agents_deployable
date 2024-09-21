from typing import Dict, List
from openai import OpenAI

class BaseAgent:
    """
    BaseAgent class to interact with the OpenAI API for generating chat completions.
    """

    def __init__(self, client: OpenAI = None):
        """
        Initialize the BaseAgent with an OpenAI client.
        
        :param client: An instance of the OpenAI client.
        """
        self.client = client or OpenAI()

    def create_chat_completion(self, messages: List[Dict[str, str]], model: str = "gpt-4o-mini"):
        """
        Create a chat completion using the OpenAI API.
        
        :param messages: List of messages to send to the API.
        :param model: The model to use for the chat completion.
        :return: The content of the response message.
        """
        response = self.client.chat.completions.create(
            model=model,
            messages=messages
        )
        return response.choices[0].message.content

