from base_agent import BaseAgent


class IdeaAgent(BaseAgent):
    """
    IdeaAgent class to generate creative ideas based on a given topic.
    """

    def generate_idea(self, topic: str):
        """
        Generate an idea about a given topic.
        
        :param topic: The topic to generate an idea about.
        :return: Generated idea as a string.
        """
        messages = [
            {"role": "system", "content": "You are a creative entrepreneur that generates thought out plans and ideas."},
            {"role": "user", "content": f"Generate an idea about {topic}."}
        ]
        return self.create_chat_completion(messages)

