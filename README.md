# Colin — A Customer Support Chatbot for Adidas Online Store

Colin is a conversational assistant designed to handle customer support tasks such as inquiries, complaints, feedback, and technical support on the Adidas Online Store. Built with the Groq API and a LLaMA-based model, Colin provides real-time assistance to users in a polite, clear, and helpful manner.

## Features

- Interactive chatbot for customer support
- Handles diverse customer messages with empathy and professionalism
- Implements error-handling strategies and retry suggestions
- Maintains conversation context across messages
- Supports streamed response output for real-time interaction
- Customizable system prompt for different assistant personas

## Installation

1. Clone the repository or download the code.
2. Install the required packages using pip:

```bash
pip install groq python-dotenv
```

3. Create a .env file in the project directory and add your Groq API key:

```env
GROQ_API_KEY=your_groq_api_key_here
```

## Usage

Run the script:

```bash
python customer-support-assistant.py
```

Colin will begin the conversation and await your questions. Type `exit`, `leave`, or `stop` to end the session.

## Example Interaction

```
Hi there! I'm Colin.
My job is to help you with any difficulties while you navigate the Adidas Online Store.
Ask me any question or type 'exit', 'leave', 'stop' to end:

User: I haven’t received my order yet.
Colin: I’m sorry to hear that your order hasn’t arrived. Please ensure you have your order ID handy. You can also try checking your delivery status using the tracking link provided in your confirmation email. Do you need help with anything else?
```

## Customization

- System Prompt: You can modify the system prompt to change Colin’s personality, behavior, or domain of knowledge.

- Model ID: Replace `deepseek-r1-distill-llama-70b` with another supported model if needed.

Developed with ❤️ for conversational AI by Chidimma Ijoma
