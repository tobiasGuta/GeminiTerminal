import os
import sys
import getpass
import google.generativeai as genai
from rich.console import Console
from rich.markdown import Markdown

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
model = "gemini-1.5-flash"
try:
    chat = genai.GenerativeModel(model).start_chat()
    console.print("\n[bold cyan]Start your conversation with Gemini![/bold cyan] (Type 'exit' or 'quit' to stop)\n")
except Exception as e:
    console.print(f"\n[bold red]Error starting chat:[/bold red] {e}")
    sys.exit(1)

# Conversation loop
while True:
    console.print("\n[bold cyan]Enter your message (press Ctrl+Z then Enter when done on Windows, or Ctrl+D on Linux/macOS):[/bold cyan]")

    # Capture multi-line user input (one single input)
    try:
        user_input = sys.stdin.read().strip()  # Read multi-line input, treats as a single input
    except EOFError:
        console.print("\n[bold red]Input ended unexpectedly.[/bold red]")
        break

    # Exit conditions based on specific commands like 'exit' or 'quit'
    if user_input.lower() in ["exit", "quit"]:
        console.print("\n[bold red]Ending the conversation...[/bold red]")
        break

    # Display the input with "You:"
    console.print(f"\n[bold cyan]You:[/bold cyan] {user_input}")  # Display user's message with "You:"

    # Send the input (even if it's multi-line) as one message
    try:
        response = chat.send_message(user_input)
        response_text = response.text.strip() if response.text else "**[No response received]**"
        
        console.print("\n[bold green]Gemini's Response:[/bold green]\n")
        console.print(Markdown(response_text))  # Display AI response in Markdown format
    except Exception as e:
        console.print(f"\n[bold red]Error processing input:[/bold red] {e}")
