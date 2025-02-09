import os
import google.generativeai as genai
import sys
from rich.console import Console
from rich.markdown import Markdown

# Set environment variables to suppress gRPC logs
os.environ['GRPC_VERBOSITY'] = 'NONE'
os.environ['GRPC_TRACE'] = 'none'

# Initialize Rich console for better output formatting
console = Console()

# Prompt the user for the API key (not hardcoded)
api_key = input("Enter your Gemini API Key: ")

# Initialize the API key
genai.configure(api_key=api_key)

# Create a chat session with the Gemini model
model = "gemini-1.5-flash"  # Use the latest model version
chat = genai.GenerativeModel(model).start_chat()

console.print("\n[bold cyan]Start your conversation with Gemini![/bold cyan] (Type 'exit' to stop)\n")

# Start the conversation loop
while True:
    user_input = input("\n[You]: ")  # Get user input
    if user_input.lower() == "exit":  # If the user types 'exit', end the chat
        console.print("\n[bold red]Ending the conversation...[/bold red]")
        break

    # Send the user message to the model and get the response
    response = chat.send_message(user_input)

    # Print the AI's response with better formatting
    console.print("\n[bold green]Gemini:[/bold green]\n")
    console.print(Markdown(response.text))  # Display AI response in Markdown format
