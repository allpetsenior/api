import os
import requests
import json


class Chatbot():
    def __init__(self):
        api_key = os.getenv("CHATBOT_API_KEY", None)
        chatbot_id = os.getenv("CHATBOT_ID", None)
        chatbot_base_url = os.getenv("CHATBOT_BASE_URL", None)

        if api_key is None:
            raise Exception("CHATBOT_SECRET_KEY is None")
        if chatbot_base_url is None:
            raise Exception("CHATBOT_BASE_URL is None")
        if chatbot_id is None:
            raise Exception("CHATBOT_ID is None")

        self.chatbot_id = chatbot_id
        self.api_key = api_key
        self.chatbot_base_url = chatbot_base_url

    def send_message(self, messages):
        headers = {
            'Authorization': f'Bearer {self.api_key}',
            'Content-Type': 'application/json'
        }
        data = {
            "messages": messages,
            "chatbotId": self.chatbot_id,
            "stream": False,
            "temperature": 0
        }

        response = requests.post(
            self.chatbot_base_url, headers=headers, data=json.dumps(data))
        json_data = response.json()

        if response.status_code == 200:
            return {"data": json_data['text'], "status": response.status_code}
        else:
            return {"error": json_data['message'], "status": response.status_code}
