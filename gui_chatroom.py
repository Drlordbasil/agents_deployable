import tkinter as tk
from tkinter import font

class ChatroomGUI:
    def __init__(self, root, chatroom):
        self.root = root
        self.chatroom = chatroom
        self.root.title("ChaosChat - AI Agents in Conversation")
        self.root.geometry("800x600")
        self.root.resizable(False, False)

        # Set up the AIM color scheme
        self.background_color = "#D6E3F3"  # Light blue background
        self.chat_bg_color = "#FFFFFF"     # White chat background
        self.font_color = "#000000"        # Black font color
        self.highlight_color = "#B3C7E6"   # Highlight color for messages

        self.root.configure(bg=self.background_color)

        # Load AIM-like fonts (using Arial as a placeholder)
        self.chat_font = font.Font(family="Arial", size=10)
        self.label_font = font.Font(family="Arial", size=12, weight="bold")

        # Main frame to hold chat and side panels
        main_frame = tk.Frame(self.root, bg=self.background_color)
        main_frame.pack(fill=tk.BOTH, expand=True)

        # Left frame for chat display
        chat_frame = tk.Frame(main_frame, bg=self.background_color)
        chat_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        chat_label = tk.Label(chat_frame, text="ChaosChat", bg=self.background_color, fg=self.font_color, font=self.label_font)
        chat_label.pack(pady=(10, 0))

        self.chat_display = tk.Text(chat_frame, state='disabled', width=60, wrap='word', bg=self.chat_bg_color, fg=self.font_color, font=self.chat_font, bd=1, relief=tk.SUNKEN)
        self.chat_display.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        # Right frame for idea and code display
        side_frame = tk.Frame(main_frame, bg=self.background_color)
        side_frame.pack(side=tk.RIGHT, fill=tk.BOTH)

        # Idea display
        idea_label = tk.Label(side_frame, text="Current Idea", bg=self.background_color, fg=self.font_color, font=self.label_font)
        idea_label.pack(padx=10, pady=(10, 0))
        self.idea_display = tk.Text(side_frame, state='disabled', width=30, height=15, wrap='word', bg=self.chat_bg_color, fg=self.font_color, font=self.chat_font, bd=1, relief=tk.SUNKEN)
        self.idea_display.pack(fill=tk.BOTH, padx=10, pady=(0, 10))

        # Code display
        code_label = tk.Label(side_frame, text="Current Code", bg=self.background_color, fg=self.font_color, font=self.label_font)
        code_label.pack(padx=10, pady=(10, 0))
        self.code_display = tk.Text(side_frame, state='disabled', width=30, height=15, wrap='word', bg=self.chat_bg_color, fg=self.font_color, font=self.chat_font, bd=1, relief=tk.SUNKEN)
        self.code_display.pack(fill=tk.BOTH, padx=10, pady=(0, 10))

        # Add an AIM-like status bar at the bottom
        self.status_bar = tk.Label(self.root, text="Connected", bd=1, relief=tk.SUNKEN, anchor=tk.W, bg=self.background_color, fg=self.font_color, font=self.chat_font)
        self.status_bar.pack(side=tk.BOTTOM, fill=tk.X)

        # Input frame at the bottom for user messages
        input_frame = tk.Frame(self.root, bg=self.background_color)
        input_frame.pack(side=tk.BOTTOM, fill=tk.X, padx=10, pady=5)

        self.user_input = tk.Entry(input_frame, width=80, font=self.chat_font)
        self.user_input.pack(side=tk.LEFT, fill=tk.X, expand=True)

        send_button = tk.Button(input_frame, text="Send", command=self.send_user_message)
        send_button.pack(side=tk.RIGHT)

    def start_conversation_thread(self):
        """
        Starts the conversation in a separate thread.
        """
        import threading
        conversation_thread = threading.Thread(target=self.chatroom.start_conversation, args=("Let's brainstorm project ideas and implement them.",))
        conversation_thread.start()

    def on_new_message(self, sender: str, message: str):
        """
        Callback function to handle new messages from the chatroom.
        """
        self.root.after(0, self.display_message, sender, message)
        self.root.after(0, self.extract_and_display_content, sender, message)

    def display_message(self, sender, message):
        """
        Display a message in the chat display.
        """
        from datetime import datetime

        self.chat_display.config(state='normal')

        # Get current time
        timestamp = datetime.now().strftime('%I:%M %p')

        # Apply different formatting based on sender
        if sender == "IdeaAgent":
            sender_color = "#0000FF"  # Blue
        elif sender == "PythonAgent":
            sender_color = "#008000"  # Green
        elif sender == "You":
            sender_color = "#B22222"  # Firebrick (red)
        else:
            sender_color = self.font_color

        # Insert sender name and timestamp
        self.chat_display.insert(tk.END, f"{sender} [{timestamp}]: ", ('sender',))
        self.chat_display.tag_config('sender', foreground=sender_color, font=self.label_font)

        # Insert message
        self.chat_display.insert(tk.END, f"{message}\n\n", ('message',))
        self.chat_display.tag_config('message', foreground=self.font_color, font=self.chat_font)

        self.chat_display.config(state='disabled')
        self.chat_display.see(tk.END)  # Scroll to the end

    def extract_and_display_content(self, sender, message):
        """
        Extract idea and code from messages and display them.
        """
        if sender == "IdeaAgent":
            # Update idea display
            self.idea_display.config(state='normal')
            self.idea_display.delete(1.0, tk.END)
            self.idea_display.insert(tk.END, message)
            self.idea_display.config(state='disabled')
        elif sender == "PythonAgent":
            # Extract and update code display
            code_blocks = self.extract_code_blocks(message)
            if code_blocks:
                self.code_display.config(state='normal')
                self.code_display.delete(1.0, tk.END)
                for code in code_blocks:
                    self.code_display.insert(tk.END, f"{code}\n\n")
                self.code_display.config(state='disabled')

    def extract_code_blocks(self, text):
        """
        Extract code blocks from text.
        """
        import re
        return re.findall(r'```python(.*?)```', text, re.DOTALL)

    def send_user_message(self):
        """
        Send the user's message into the conversation.
        """
        message = self.user_input.get()
        if message.strip():
            # Display user's message in the chat display
            self.display_message("You", message)

            # Clear the input field
            self.user_input.delete(0, tk.END)

            # Inject the user's message into the conversation
            self.chatroom.add_user_message(message)

