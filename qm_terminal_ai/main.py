import os
import subprocess
from brain import QMBrain
from rich.console import Console
from rich.panel import Panel

console = Console()

def execute_tool(tool_name, args, brain):
    """Handles the actual system execution based on AI request."""
    if tool_name == "execute_command":
        console.print(f"[bold yellow]Running command:[/bold yellow] {args}")
        try:
            # Using shell=True for PowerShell/CMD compatibility
            result = subprocess.run(args, shell=True, capture_output=True, text=True, encoding="utf-8")
            output = result.stdout if result.stdout else result.stderr
            return output if output else "Command executed successfully (no output)."
        except Exception as e:
            return f"Execution error: {str(e)}"

    elif tool_name == "read_file":
        console.print(f"[bold yellow]Reading file:[/bold yellow] {args}")
        try:
            with open(args, "r", encoding="utf-8") as f:
                return f.read()
        except Exception as e:
            return f"Read error: {str(e)}"

    elif tool_name == "write_file":
        console.print(f"[bold yellow]Writing to file:[/bold yellow] {args.split('|')[0]}")
        try:
            path, content = args.split("|", 1)
            with open(path, "w", encoding="utf-8") as f:
                f.write(content)
            return "File written successfully."
        except Exception as e:
            return f"Write error: {str(e)}"

    return "Tool not found."

def main():
    # We use qwen2.5-coder:3b since you just pulled it (excellent for coding)
    brain = QMBrain(model_name="qwen2.5-coder:3b")
    
    console.print(Panel("[bold magenta]QM Intelligent Terminal AI[/bold magenta]\n[dim]Agent Engine: qwen2.5-coder:3b | Mode: UNLOCKED[/dim]"))
    console.print("[green]QM is ready. Type 'exit' to quit.[/green]")

    while True:
        try:
            user_input = input("\n[QM] > ")
            if user_input.lower() in ["exit", "quit"]:
                break
                
            # 1. Initial AI Thought
            response = brain.chat(user_input)
            
            # 2. Agentic Loop: Check if the AI wants to use a tool
            # We allow up to 5 tool calls per user prompt to prevent infinite loops
            loop_count = 0
            while "TOOL:" in response and loop_count < 5:
                # Simple parsing of "TOOL: name ARGS: value"
                try:
                    parts = response.split("TOOL:")[1].split("ARGS:")
                    tool_name = parts[0].strip()
                    tool_args = parts[1].strip().split("\n")[0] # Get only the first line
                    
                    # SAFETY: Ask user for permission
                    confirm = input(f"[bold red]QM wants to {tool_name} with {tool_args}. Allow? (y/n): [/bold red]")
                    if confirm.lower() != 'y':
                        result = "User denied permission to execute this tool."
                    else:
                        result = execute_tool(tool_name, tool_args, brain)
                    
                    # Feed the result back to the brain
                    brain.add_message("user", f"TOOL RESULT: {result}")
                    response = brain.chat(f"Based on the tool result, continue your task: {result}")
                    loop_count += 1
                except Exception as e:
                    console.print(f"[red]Parsing error: {e}[/red]")
                    break

            console.print(f"\n[bold cyan]QM:[/bold cyan] {response}")
            
        except KeyboardInterrupt:
            break

if __name__ == "__main__":
    main()
