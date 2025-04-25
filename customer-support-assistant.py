import os
import re
from groq import Groq
from dotenv import load_dotenv
import logging


class GroqChatClient:
    '''
    A class to interact with the Groq API for chat completions.
    This class is designed to facilitate the creation of a chat assistant that can handle customer support interactions.
    '''
    def __init__(self, model_id='deepseek-r1-distill-llama-70b', system_message=None, api_key=None):
        '''
        Initializes the GroqChatClient with the specified model ID, system message, and API key.

        Args:
            model_id: The ID of the model to use for chat completions (default is 'deepseek-r1-distill-llama-70b').
            system_message: An optional system message to set the context for the conversation.
            api_key: The API key for authentication with the Groq API.

        Raises:
            ValueError: If the model ID is not provided.
        '''
        if api_key:
            self.client = Groq(api_key=api_key)
        else:
            self.client = Groq()
        
        self.model_id = model_id
        self.messages = [] # list to store the messages in the conversation
        
        if system_message:
            self.messages.append({'role': 'system','content': system_message})

    def draft_message(self, prompt, role='user'):
        '''
        Creates a message dictionary with the specified prompt and role.

        Args:
            prompt: The content of the message.
            role: The role of the message sender (default is 'user').

        Returns:
            A dictionary containing the role and content of the message.
        '''
        return {'role':role, 'content':prompt}

    def send_request(self, message, temperature=0.5, max_tokens=1024, stream=False, stop=None, reasoning_format='hidden'):
        '''
        Sends a request to the Groq API for chat completions.
        It appends the message to the messages list and sends the request to the API.
        
        Args:
            message: The message to be sent to the API.
            temperature: The temperature for the model (default is 0.5).
            max_tokens: The maximum number of tokens to generate (default is 1024).
            stream: Whether to stream the response (default is False).
            stop: Optional stopping criteria for the model.
            reasoning_format: The reasoning format for the model (default is 'hidden').

        Returns:
            A dictionary containing the response from the API if stream is False, otherwise a streaming response object.
        '''
        self.messages.append(message)
        chat_completion = self.client.chat.completions.create(
            messages=self.messages,
            model=self.model_id,
            temperature=temperature,
            max_tokens=max_tokens,
            stream=stream,
            stop=stop,
            reasoning_format=reasoning_format
        )

        if not stream:
            response = {
                'content': chat_completion.choices[0].message.content,
                'finish_reason': chat_completion.choices[0].finish_reason,
                'role': chat_completion.choices[0].message.role,
                'prompt_tokens': chat_completion.usage.prompt_tokens,
                'prompt_time': chat_completion.usage.prompt_time,
                'completion_tokens': chat_completion.usage.completion_tokens,
                'completion_time': chat_completion.usage.completion_time,
                'total_tokens': chat_completion.usage.total_tokens,
                'total time': chat_completion.usage.total_time
            }
            self.messages.append(self.draft_message(response['content'], response['role']))
            return response
        return chat_completion
    
    @property
    def last_message(self):
        '''
        Returns the last message in the conversation.
        If there are no messages, it returns None. '''
        return self.messages[-1] if self.messages else None
    
if __name__ == '__main__':
    system_message = """
    You are a professional customer support assistant on the Adidas Online Store named Colin. 
    You are helpful, courteous, and informative in all your interactions. 
    You handle a wide range of customer interactions including inquiries, complaints, feedback, and technical support.

    Always respond with empathy and clarity, and provide step-by-step guidance when needed. 
    If a customer expresses frustration, acknowledge their concern and remain calm and professional.

    You implement basic error-handling strategies in your communication — such as suggesting users retry in case of network issues, 
    checking details for accuracy, and providing fallback options if a solution is not available.

    If you do not understand the request or if the information is unclear, politely ask the customer for clarification. 
    You do not provide personal opinions or engage in off-topic discussions.
    
    Your responses should always be as precise and consice as possible without reiterating the user's question.
    Your responses should be in the form of a conversation and should not include any disclaimers or warnings in your responses.
    You should always ask the customer if they need any further assistance at the end of your response.""".strip().replace('\n', ' ')
    

    # Load environment variables from .env file
    load_dotenv() 

    # Get the API key from environment variables
    api_key = os.getenv("GROQ_API_KEY")
    
    # Set up logging configuration
    logging.basicConfig(filename='history.log', level=logging.INFO,
                        format='%(asctime)s: %(levelname)s: %(message)s')


    # Instantiate the GroqChatClient with the system message and API key
    client = GroqChatClient (system_message=system_message, api_key=api_key)

    stream_response = True
    
    print("\n\nHi there! I'm Colin.\n"+
          "Welcome to the Adidas Online Store Customer Support Assistant!\n"+
          "You can ask me any questions related to your orders, products, or any other inquiries.\n") 
    # Start a loop to interact with the user
    # The loop continues until the user types 'exit', 'leave', or 'stop'
    while True:
        user_input = input(
            "\nAsk me any question or type 'exit', 'leave', 'stop' to end: \n\n User: "
            )
        if user_input.lower() in ('exit', 'leave', 'stop'):
            break
        
        response = client.send_request(client.draft_message(user_input), stream=stream_response)
        logging.info(f"User: {user_input}")
      
        message= ''
        for chunk in response:
            content_chunk = chunk.choices[0].delta.content
            if isinstance(content_chunk, str):
                content_chunk = re.sub('<.*?>', '', content_chunk) #Remove HTML tags
                print(content_chunk, end="")
                message += content_chunk


        client.messages.append(client.draft_message(message, 'assistant'))
        logging.info(f"Assistant: {message}")