from http.server import HTTPServer, BaseHTTPRequestHandler
import json, requests
from loguru import logger


class Napcat_API():
        def __init__(self, url:str, post_port:int, post_token:str):
                        self.port = str(post_port)
                        self.token = post_token
                        self.url = url

        def send_group_msg(self, group_id, reply_id, msg):
                if reply_id:
                        body = json.dumps({
                                "group_id": group_id,
                                "message": [
                                        {
                                                "type": "reply",
                                                "data": {
                                                        "id": reply_id
                                                }
                                        },
                                        {
                                                "type": "text",
                                                "data": {
                                                       "text": msg
                                                }
                                        }
                                ]
                        })
                else:
                        body = json.dumps({
                                "group_id": group_id,
                                "message": [
                                        {
                                                "type": "text",
                                                "data": {
                                                       "text": msg
                                                }
                                        }
                                ]
                        })
                requests.request("POST", url=self.url+':'+self.port+'/send_group_msg', headers={'Content-Type':'application/json'}, data=body)

        def send_private_msg(self, user_id, msg):
                body = json.dumps({
                        "user_id": user_id,
                        "message": [
                                {
                                        "type": "text",
                                        "data": {
                                                "text": msg
                                        }
                                }
                        ]
                })
                requests.request("POST", url=self.url+':'+self.port+'/send_private_msg', headers={'Content-Type':'application/json'}, data=body)
