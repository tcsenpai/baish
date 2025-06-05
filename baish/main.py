#!/usr/bin/env python3
import os
import subprocess
import sys
from pathlib import Path

import click
import requests
from dotenv import load_dotenv
from rich.console import Console
from rich.panel import Panel
from rich.prompt import Confirm, Prompt
from rich.text import Text
from rich.rule import Rule

load_dotenv()

console = Console()

OLLAMA_URL = os.getenv("OLLAMA_URL", "http://localhost:11434")
OLLAMA_MODEL = os.getenv("OLLAMA_MODEL", "llama3.2:latest")

SYSTEM_PROMPT = """You are a bash command generator. Convert natural language to exact bash/linux commands.

CRITICAL RULES:
1. Return ONLY the exact command - no explanations, no markdown, no extra text
2. One command per request
3. Use standard Linux utilities and correct syntax
4. For URLs/domains: use them exactly as provided
5. For file operations: use relative paths unless absolute path specified
6. Chain multiple operations with && or ; if needed

EXAMPLES:
"show my ip address" -> "ip addr show"
"ping google.com" -> "ping google.com"
"ping discus.sh" -> "ping discus.sh"
"list files" -> "ls -la"
"check disk space" -> "df -h"
"find python files" -> "find . -name '*.py'"
"download file from url" -> "wget [url]"
"check if service is running" -> "systemctl status [service]"
"stop nginx" -> "sudo systemctl stop nginx"
"show processes" -> "ps aux"
"show memory usage" -> "free -h"
"tail log file" -> "tail -f /var/log/[logfile]"

OUTPUT FORMAT: Just the command, nothing else. No backticks, no explanations."""


def query_ollama(prompt: str) -> str:
    """Query Ollama API for command conversion."""
    try:
        response = requests.post(
            f"{OLLAMA_URL}/api/generate",
            json={
                "model": OLLAMA_MODEL,
                "prompt": f"System: {SYSTEM_PROMPT}\n\nUser: {prompt}",
                "stream": False,
                "options": {
                    "temperature": 0.1,
                    "top_p": 0.9,
                    "num_predict": 100,
                }
            },
            timeout=120
        )
        response.raise_for_status()
        result = response.json()
        return result.get("response", "").strip()
    except requests.exceptions.RequestException as e:
        console.print(f"[red]Error connecting to Ollama: {e}[/red]")
        return ""
    except Exception as e:
        console.print(f"[red]Unexpected error: {e}[/red]")
        return ""


def is_safe_command(command: str) -> bool:
    """Basic safety check for potentially destructive commands."""
    dangerous_patterns = [
        "rm -rf /",
        "rm -rf /*",
        "format",
        "fdisk",
        "mkfs",
        "dd if=",
        ":(){ :|:& };:",  # fork bomb
        "chmod -R 777 /",
        "chown -R root",
        "> /dev/",
        "curl | sh",
        "wget | sh",
        "shutdown",
        "reboot",
        "init 0",
        "init 6",
    ]
    
    command_lower = command.lower()
    return not any(pattern in command_lower for pattern in dangerous_patterns)


def execute_command(command: str) -> None:
    """Execute the bash command with real-time output."""
    try:
        console.print(f"[dim]Executing: {command}[/dim]")
        console.print(Rule(style="dim"))
        
        process = subprocess.Popen(
            command,
            shell=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            universal_newlines=True,
            bufsize=1
        )
        
        for line in iter(process.stdout.readline, ''):
            console.print(line.rstrip())
        
        process.wait()
        console.print(Rule(style="dim"))
        
        if process.returncode == 0:
            console.print("[green]✓ Command completed successfully[/green]")
        else:
            console.print(f"[yellow]⚠ Command exited with code {process.returncode}[/yellow]")
            
    except KeyboardInterrupt:
        console.print("\n[yellow]Command interrupted by user[/yellow]")
    except Exception as e:
        console.print(f"[red]Error executing command: {e}[/red]")


@click.command()
@click.option('--interactive', '-i', is_flag=True, help='Run in interactive mode')
@click.option('--help', '-h', is_flag=True, help='Show this help message and exit')
@click.argument('instruction', required=False)
def main(interactive: bool, help: bool, instruction: str) -> None:
    """🐚 Baish - Convert natural language to bash commands using Ollama
    
    Examples:
        baish "show my ip address"     # Single command
        baish -i                       # Interactive mode
        python main.py "list files"    # Direct execution
    """
    
    console.print(Panel(
        Text.assemble(
            ("🐚 ", "bold cyan"),
            ("Baish", "bold white"),
            (" - Natural Language to Bash", "dim")
        ),
        border_style="cyan"
    ))
    
    # Check Ollama connection
    try:
        response = requests.get(f"{OLLAMA_URL}/api/tags", timeout=10)
        if response.status_code != 200:
            console.print("[red]❌ Cannot connect to Ollama. Make sure it's running.[/red]")
            console.print(f"[dim]Trying to connect to: {OLLAMA_URL}[/dim]")
            sys.exit(1)
            
        # Check if model exists
        models = response.json().get('models', [])
        model_names = [model.get('name', '') for model in models]
        if not any(OLLAMA_MODEL in name for name in model_names):
            console.print(f"[yellow]⚠️  Model '{OLLAMA_MODEL}' not found.[/yellow]")
            console.print(f"[dim]Available models: {', '.join(model_names) if model_names else 'None'}[/dim]")
            
    except requests.exceptions.RequestException as e:
        console.print("[red]❌ Cannot connect to Ollama. Make sure it's running.[/red]")
        console.print(f"[dim]Trying to connect to: {OLLAMA_URL}[/dim]")
        console.print(f"[dim]Error: {e}[/dim]")
        sys.exit(1)
    
    console.print(f"[dim]Using model: {OLLAMA_MODEL} at {OLLAMA_URL}[/dim]\n")
    
    if help:
        show_help()
        return
    
    if interactive or not instruction:
        # Interactive mode
        while True:
            try:
                instruction = Prompt.ask(
                    "\n[cyan]What would you like to do?[/cyan]",
                    default="",
                ).strip()
                
                if not instruction or instruction.lower() in ['quit', 'exit', 'q']:
                    console.print("[dim]Goodbye! 👋[/dim]")
                    break
                
                if instruction.lower() in ['/help', 'help']:
                    show_help()
                    continue
                    
                process_instruction(instruction)
                
            except KeyboardInterrupt:
                console.print("\n[dim]Goodbye! 👋[/dim]")
                break
    else:
        # Single command mode
        process_instruction(instruction)


def show_help() -> None:
    """Display help information."""
    help_text = """
[bold cyan]🐚 Baish - Natural Language to Bash Commands[/bold cyan]

[bold]Usage:[/bold]
  baish "<instruction>"          # Convert and execute single command
  baish -i                       # Interactive mode
  python main.py "<instruction>" # Direct execution

[bold]Options:[/bold]
  -i, --interactive     Run in interactive mode
  -h, --help           Show this help message

[bold]Examples:[/bold]
  baish "show my ip address"
  baish "list files in current directory"
  baish "check disk usage"
  baish "find python files"
  baish "stop nginx service"

[bold]Interactive Commands:[/bold]
  /help, help          Show this help
  quit, exit, q        Exit the program

[bold]Configuration:[/bold]
  Edit .env file to configure:
  - OLLAMA_URL (default: http://localhost:11434)
  - OLLAMA_MODEL (default: llama3.2:latest)

[bold]Safety:[/bold]
  Baish includes safety checks for potentially dangerous commands.
  You'll be prompted before executing any command.
    """
    console.print(Panel(help_text, border_style="cyan", padding=(1, 2)))


def process_instruction(instruction: str) -> None:
    """Process a single instruction."""
    console.print(f"\n[blue]🤔 Thinking...[/blue]")
    
    command = query_ollama(instruction)
    
    if not command:
        console.print("[red]❌ Could not generate command[/red]")
        return
    
    # Clean up the command (remove any markdown or extra formatting)
    command = command.replace('`', '').replace('```bash', '').replace('```', '').strip()
    
    # Handle multi-line responses - take only the first non-empty line
    if '\n' in command:
        lines = [line.strip() for line in command.split('\n') if line.strip()]
        command = lines[0] if lines else command.strip()
    
    # Display the generated command
    console.print(Panel(
        Text(command, style="bold green"),
        title="[bold]Generated Command",
        border_style="green"
    ))
    
    # Safety check
    if not is_safe_command(command):
        console.print("[red]⚠️  Warning: This command might be potentially dangerous![/red]")
        if not Confirm.ask("[yellow]Are you absolutely sure you want to run this?[/yellow]"):
            console.print("[dim]Command cancelled for safety.[/dim]")
            return
    
    # Ask for confirmation
    if Confirm.ask("[cyan]Execute this command?[/cyan]", default=True):
        execute_command(command)
    else:
        console.print("[dim]Command cancelled.[/dim]")


if __name__ == "__main__":
    main()