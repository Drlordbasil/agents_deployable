# this is for the ai to talk to eachother not the user.

from typing import List, Dict, Callable
from base_agent import BaseAgent
import json
import threading

class AIChatroom:
    """
    AIChatroom class to manage a conversation between multiple AI agents.
    """

    def __init__(self, agents: List[BaseAgent], on_message_callback: Callable[[str, str], None]):
        """
        Initialize the AIChatroom with a list of agents and a callback for new messages.
        
        :param agents: List of BaseAgent instances.
        :param on_message_callback: Function to call when a new message is available.
        """
        self.agents = agents
        self.conversation_history = []
        self.on_message_callback = on_message_callback
        self.new_message_event = threading.Event()

    def start_conversation(self, topic: str):
        """
        Start a conversation on a given topic.
        
        :param topic: The topic to discuss.
        """
        initial_message = {"role": "system", "content": f"You are AI agents in a brainstorming session. {topic}", "sender": "System"}
        self.conversation_history.append(initial_message)
        self.on_message_callback("System", initial_message["content"])
        self.broadcast_message()

    def add_user_message(self, message: str):
        """
        Add a user's message to the conversation and notify the chat loop.
        """
        user_message = {"role": "user", "content": message, "sender": "User"}
        self.conversation_history.append(user_message)
        self.on_message_callback("You", message)
        self.new_message_event.set()  # Notify the conversation loop

    def broadcast_message(self):
        """
        Broadcast messages among agents and handle their responses.
        """
        while True:
            any_agent_replied = False
            for agent in self.agents:
                if self.should_reply(agent):
                    response = agent.create_chat_completion(self.conversation_history)
                    message = {"role": "assistant", "content": response, "sender": agent.__class__.__name__}
                    self.conversation_history.append(message)
                    self.on_message_callback(agent.__class__.__name__, response)
                    any_agent_replied = True

            # Wait for new user message or a short timeout
            if not any_agent_replied:
                self.new_message_event.wait(timeout=1)
                self.new_message_event.clear()

    def should_reply(self, agent: BaseAgent) -> bool:
        """
        Determine if an agent should reply based on the conversation history.
        
        :param agent: The agent to decide.
        :return: True if the agent should reply, False otherwise.
        """
        last_message = self.conversation_history[-1]
        last_sender = last_message.get("sender")

        if last_sender == agent.__class__.__name__:
            return False  # Avoid self-replying

        # Encourage agents to reply more frequently to user messages
        if last_sender == "User":
            return True

        analysis_message = [
            {"role": "system", "content": "You are an AI agent deciding whether to reply to the conversation."},
            {"role": "assistant", "content": f"Conversation so far: {json.dumps(self.conversation_history[-5:])}"},  # Consider the last 5 messages
            {"role": "user", "content": "Should you contribute a message to this conversation? Reply 'Yes' or 'No'."}
        ]
        decision = agent.create_chat_completion(analysis_message)
        return "yes" in decision.lower()
