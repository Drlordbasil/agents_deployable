# this agent will be responsible for generating python code for the idea.

import re
import subprocess
from base_agent import BaseAgent

class PythonAgent(BaseAgent):
    """
    PythonAgent class to generate and process Python code based on conversation.
    """

    def create_chat_completion(self, messages, model="gpt-4"):
        """
        Include role-play as a Python developer participating in a brainstorming session with other AI agents and a user. Respond appropriately to messages from both agents and the user. Provide code within ```python``` code blocks when relevant.
        """
        messages.append({"role": "system", "content": "You are a Python developer participating in a brainstorming session with other AI agents and a user. Respond appropriately to messages from both agents and the user. Provide code within ```python``` code blocks when relevant."})
        return super().create_chat_completion(messages, model)

    def generate_python_code(self):
        """
        Generate Python code based on the idea stored in idea.txt.
        
        :return: Generated Python code as a string.
        """
        with open("idea.txt", "r") as file:
            idea = file.read()
        messages = [
            {"role": "system", "content": "You are a Python developer that generates Python code for the idea."},
            {"role": "user", "content": f"Generate Python code for the idea: {idea}."}
        ]
        return self.create_chat_completion(messages)

    def extract_code_blocks(self, text: str):
        """
        Extract Python code blocks from a given text.
        
        :param text: The text containing code blocks.
        :return: List of extracted code blocks.
        """
        code_blocks = re.findall(r'```python(.*?)```', text, re.DOTALL)
        return code_blocks

    def detect_language(self, code: str):
        """
        Detect the programming language of a given code.
        
        :param code: The code to analyze.
        :return: Detected language as a string.
        """
        messages = [
            {"role": "system", "content": "You are a developer that detects the language of the code."},
            {"role": "user", "content": f"Detect the language of the code: {code}."}
        ]
        return self.create_chat_completion(messages)

    def run_code(self, code: str):
        """
        Run the given Python code and capture the output.
        
        :param code: The Python code to run.
        :return: Dictionary with status and output of the code execution.
        """
        try:
            result = subprocess.run(
                ["python", "-c", code],
                capture_output=True,
                text=True,
                timeout=10
            )
            if result.returncode == 0:
                return {"status": "success", "output": result.stdout}
            else:
                return {"status": "error", "output": result.stderr}
        except subprocess.TimeoutExpired:
            return {"status": "error", "output": "Error: Code execution timed out."}

    def test_code(self, code: str):
        """
        Test the given Python code.
        
        :param code: The Python code to test.
        :return: Result of the code execution.
        """
        return self.run_code(code)

    def process_code(self, code: str):
        """
        Process the given code by detecting its language and testing it if it's Python.
        
        :param code: The code to process.
        :return: Dictionary with the result of the processing.
        """
        language = self.detect_language(code)
        if "python" in language.lower():
            test_result = self.test_code(code)
            if test_result["status"] == "error":
                return {
                    "status": "error",
                    "message": "Errors detected in the code.",
                    "details": test_result["output"]
                }
            else:
                return {
                    "status": "success",
                    "message": "Code executed successfully.",
                    "details": test_result["output"]
                }
        else:
            return {
                "status": "error",
                "message": "The provided code is not in Python."
            }

    def handle_generated_code(self, generated_text: str):
        """
        Handle the generated code by extracting and processing code blocks.
        
        :param generated_text: The text containing generated code.
        :return: List of results for each code block.
        """
        code_blocks = self.extract_code_blocks(generated_text)
        if not code_blocks:
            return {"status": "error", "message": "No Python code blocks found in the generated text."}

        results = []
        for code in code_blocks:
            result = self.process_code(code)
            results.append(result)

        return results

    def request_code_fix(self, error_details: str):
        """
        Request a fix for the given code errors.
        
        :param error_details: The details of the code errors.
        :return: Corrected code as a string.
        """
        messages = [
            {"role": "system", "content": "You are a Python developer that fixes code errors."},
            {"role": "user", "content": f"Fix the following code errors and provide a corrected version in Python:\n{error_details}"}
        ]
        return self.create_chat_completion(messages)

# Test
if __name__ == "__main__":
    python_agent = PythonAgent()

    generated_text = python_agent.generate_python_code()
    print("Generated Text:\n", generated_text)

    results = python_agent.handle_generated_code(generated_text)
    print("Processing Results:\n", results)

    for result in results:
        if result["status"] == "error":
            error_details = result["details"]
            fixed_code = python_agent.request_code_fix(error_details)
            print("Fixed Code:\n", fixed_code)


