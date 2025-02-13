import requests, json
from openai import OpenAI


class YunAi_API():
        def __init__(self, key:str, url:str):
                self.client = OpenAI(api_key=key, base_url=url)
        def Chat_Send(self, model:str, text:str):
                response = self.client.chat.completions.create(
                        model = model,
                        stream = False,
                        timeout = 300,
                        messages = [
                                {"role": "user", "content": text}
                        ]
                )
                if response.choices[0].message.content:
                        return response.choices[0].message.content
                else:
                        return "API error."


