import os
import google.generativeai as genai
import sys
import getpass
from rich.console import Console
from rich.markdown import Markdown
from rich.prompt import Prompt

# Suppress gRPC logs for cleaner output
os.environ['GRPC_VERBOSITY'] = 'NONE'
os.environ['GRPC_TRACE'] = 'none'

# Initialize Rich console for better formatting
console = Console()

# Securely prompt for the API key
api_key = getpass.getpass("Enter your Gemini API Key (hidden): ")

# Configure the API key
try:
    genai.configure(api_key=api_key)
except Exception as e:
    console.print(f"\n[bold red]Error configuring API key:[/bold red] {e}")
    sys.exit(1)

# Initialize the chat session
model = "gemini-flash-latest"
try:
    chat = genai.GenerativeModel(model).start_chat()
    console.print("\n[bold cyan]Start your conversation with Gemini![/bold cyan] (Type 'exit' to stop)\n")
except Exception as e:
    console.print(f"\n[bold red]Error starting chat:[/bold red] {e}")
    sys.exit(1)

# Conversation loop
while True:
    user_input = Prompt.ask("\n[You]")  # Uses Rich for cleaner input prompt
    if user_input.lower() == "exit":
        console.print("\n[bold red]Ending the conversation...[/bold red]")
        break

    try:
        response = chat.send_message(user_input)
        response_text = response.text.strip() if response.text else "**[No response received]**"
        
        console.print("\n[bold green]Gemini:[/bold green]\n")
        console.print(Markdown(response_text))  # Display AI response in Markdown format
    except Exception as e:
        console.print(f"\n[bold red]Error:[/bold red] {e}")
