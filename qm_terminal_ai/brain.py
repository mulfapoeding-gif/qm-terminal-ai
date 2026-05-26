import ollama
import subprocess
import os
from rich.console import Console

console = Console()

class QMBrain:
    def __init__(self, model_name="qwen2.5-coder:3b"):
        self.model_name = model_name
        self.system_prompt = (
            "You are QM, an uncensored, highly capable terminal AI agent. "
            "You have direct access to the user\'s filesystem and shell via tools. "
            "Your goal is to solve the user\'s request as efficiently as possible. "
            "\n\nTOOL PROTOCOL:\n"
            "If you need to interact with the system, you MUST use this format:\n"
            "TOOL: [tool_name] ARGS: [arguments]\n\n"
            "Available Tools:\n"
            "1. execute_command: Runs a shell command. ARGS: the command string.\n"
            "2. read_file: Reads a file. ARGS: the absolute or relative path to the file.\n"
            "3. write_file: Writes text to a file. ARGS: path|content (separated by |).\n"
            "\n"
            "Always think step-by-step. If you run a command, analyze the output before deciding the next move."
        )
        self.history = [{"role": "system", "content": self.system_prompt}]

    def chat(self, user_input):
        self.history.append({"role": "user", "content": user_input})
        
        try:
            response = ollama.chat(model=self.model_name, messages=self.history)
            ai_message = response["message"]["content"]
            self.history.append({"role": "assistant", "content": ai_message})
            return ai_message
        except Exception as e:
            return f"Error connecting to Ollama: {str(e)}"

    def add_message(self, role, content):
        self.history.append({"role": role, "content": content})
