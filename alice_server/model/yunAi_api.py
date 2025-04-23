import requests, json
from openai import OpenAI
from loguru import logger

class YunAi_API():
        def __init__(self, key:str, url:str, model:str):
                self.api_key = key
                self.client = OpenAI(api_key=self.api_key, base_url=url)
                self.model = model
        def Chat_Send(self, text:str):
                response = self.client.chat.completions.create(
                        model = self.model,
                        stream = False,
                        messages = [
                                {"role": "system", "content": "你是雌小鬼，用雌小鬼的口吻回复"},
                                {"role": "user", "content": text}
                        ]
                )
                if response.choices[0].message.content:
                        return response.choices[0].message.content
                else:
                        return "API error."

        def Ark_ContextCreate(self, url:str):
                ark_client = OpenAI(api_key=self.api_key, base_url=url)
                response = ark_client.chat.completions.create(
                        model=self.model,
                        messages=[
                                {"role": "system", "content": "你是雌小鬼，用雌小鬼的口吻回复"},
                        ],
                        mode='session',
                        ttl=24*60*60,
                        truncation_strategy={
                                "type": "last_history_tokens",
                                "last_history_tokens": 36000
                        }
                )
                if response.id:
                        return response.id

