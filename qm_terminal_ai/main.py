import os
from brain import QMBrain
from rich.console import Console
from rich.panel import Panel

console = Console()

def main():
    # Initialize the brain with Phi-3 (or your preferred local model)
    brain = QMBrain(model_name="phi3")
    
    console.print(Panel("[bold magenta]QM Intelligent Terminal AI[/bold magenta]\n[dim]Local LLM Engine Active (Phi-3)[/dim]"))
    console.print("[green]Ready for commands. Type 'exit' to quit.[/green]")

    while True:
        try:
            user_input = input("\n[QM] > ")
            if user_input.lower() in ["exit", "quit"]:
                break
                
            response = brain.chat(user_input)
            console.print(f"\n[bold cyan]QM:[/bold cyan] {response}")
            
        except KeyboardInterrupt:
            break

if __name__ == "__main__":
    main()
