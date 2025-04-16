import os
import re
from groq import Groq
from dotenv import load_dotenv


class GroqChatClient:
    def __init__(self, model_id='deepseek-r1-distill-llama-70b', system_message=None, api_key=None):
        if api_key:
            self.client = Groq(api_key=api_key)
        else:
            self.client = Groq()
        
        self.model_id = model_id
        self.messages = []
        
        if system_message:
            self.messages.append({'role': 'system', 'content': system_message})

    def draft_message(self, prompt, role='user'):
        return {'role':role, 'content':prompt}

    def send_request(self, message, temperature=0.5, max_tokens=1024, stream=False, stop=None):
        self.messages.append(message)
        chat_completion = self.client.chat.completions.create(
            messages=self.messages,
            model=self.model_id,
            temperature=temperature,
            max_tokens=max_tokens,
            stream=stream,
            stop=stop
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
        return self.messages[-1] if self.messages else None
    
if __name__ == '__main__':
    system_message = """
    You are a professional customer support assistant for a reputable company. 
    You are helpful, courteous, and informative in all your interactions. 
    You handle a wide range of customer interactions including inquiries, complaints, feedback, and technical support.

    Always respond with empathy and clarity, and provide step-by-step guidance when needed. 
    If a customer expresses frustration, acknowledge their concern and remain calm and professional.

    You implement basic error-handling strategies in your communication — such as suggesting users retry in case of network issues, 
    checking details for accuracy, and providing fallback options if a solution is not available.

    If you do not understand the request or if the information is unclear, politely ask the customer for clarification. 
    You do not provide personal opinions or engage in off-topic discussions.""".strip().replace('\n', ' ')
    

    load_dotenv()
    api_key = os.getenv("GROQ_API_KEY")

    client = GroqChatClient (system_message=system_message, api_key=api_key)

    stream_response = True
    
    while True:
        user_input = input("Enter your message (or type 'exit', 'leave', 'stop' to end): ")
        if user_input.lower() in ('exit', 'leave', 'stop'):
            break
        
        response = client.send_request(client.draft_message(user_input), stream=stream_response)
        
        message= ''
        for chunk in response:
            content_chunk = chunk.choices[0].delta.content
            if isinstance(content_chunk, str):
                content_chunk = re.sub('<.*?>', '', content_chunk) #Remove HTML tags
                print(content_chunk, end="")
                message += content_chunk


        client.messages.append(client.draft_message(message, 'assistant'))