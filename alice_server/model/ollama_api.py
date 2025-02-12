import ollama, requests

# response = ollama.generate(model="deepseek-r1:14b-qwen-distill-q4_K_M", prompt="")
# print(response.response)

from bs4 import BeautifulSoup
from urllib.parse import urljoin
import json

class WebAccess:
        @staticmethod
        def search_web(query: str):
                """调用Serper API进行网络搜索"""
                url = "https://google.serper.dev/search"
                headers = {
                        "X-API-KEY": "your_serper_api_key",
                        "Content-Type": "application/json"
                }
                payload = json.dumps({"q": query})
                try:
                        response = requests.post(url, headers=headers, data=payload)
                        results = []
                        if response.status_code == 200:
                                data = response.json()
                                for item in data.get("organic", [])[:3]:
                                        results.append({
                                                "title": item.get("title"),
                                                "snippet": item.get("snippet"),
                                                "link": item.get("link")
                                        })
                        return results
                except Exception as e:
                        print(f"搜索失败：{str(e)}")
                        return []

        @staticmethod
        def fetch_page_content(url: str):
                """获取网页正文内容"""
                try:
                        response = requests.get(url, timeout=10)
                        soup = BeautifulSoup(response.text, "html.parser")
                        # 提取主要正文内容
                        main_content = soup.find("main") or soup.find("article") or soup.body
                        return main_content.get_text(separator="\n", strip=True)[:5000]
                except Exception as e:
                        print(f"页面获取失败：{str(e)}")
                        return ""

from functools import lru_cache

class EnhancedR1:
        def __init__(self):
                self.web = WebAccess()
                
        @lru_cache(maxsize=100)
        def process_query(self, prompt: str):
                if "[联网搜索]" in prompt:
                        search_query = prompt.split("]")[1].strip()
                        web_results = self.web.search_web(search_query)
                        context = "\n".join([f"来源：{res['link']}\n摘要：{res['snippet']}" for res in web_results])
                        augmented_prompt = f"基于以下网络信息回答：{context}\n问题：{search_query}"
                        return self.generate_response(augmented_prompt)
                else:
                        return self.generate_response(prompt)

        def generate_response(self, text):
                '''这部分需要用ollama接口重写'''
                # inputs = tokenizer(text, return_tensors="pt").to(model.device)
                # outputs = model.generate(
                #         **inputs,
                #         max_new_tokens=1024,
                #         repetition_penalty=1.1,
                #         do_sample=True
                # )
                # return tokenizer.decode(outputs[0], skip_special_tokens=True)
                response = ollama.generate(model="deepseek-r1:14b-qwen-distill-q4_K_M", prompt=text)
                return response.response
