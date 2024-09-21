from idea_agent import IdeaAgent
from python_agent import PythonAgent
from ai_chatroom import AIChatroom
from gui_chatroom import ChatroomGUI
import tkinter as tk

def main():
    """
    Main function to initialize agents, create the AI chatroom, and start the GUI.
    """
    try:
        # Initialize the agents
        idea_agent = IdeaAgent()
        python_agent = PythonAgent()

        root = tk.Tk()

        # Create the GUI without the chatroom reference yet
        gui = ChatroomGUI(root, None)

        # Create the AI chatroom with the agents and pass the GUI callback
        chatroom = AIChatroom([idea_agent, python_agent], gui.on_new_message)
        gui.chatroom = chatroom  # Assign the chatroom to the GUI

        # Start the conversation
        gui.start_conversation_thread()

        root.mainloop()

    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    main()




