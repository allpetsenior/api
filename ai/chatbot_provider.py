import requests
import json
from app.settings import CHATBOT_API_KEY, CHATBOT_AGENT_ID, CHATBOT_BASE_URL, RECOMMENDATION_AGENT_ID


class Chatbot():
    def __init__(self):
        api_key = CHATBOT_API_KEY
        chatbot_id = CHATBOT_AGENT_ID
        recommendation_agent_id = RECOMMENDATION_AGENT_ID
        chatbot_base_url = CHATBOT_BASE_URL

        if api_key is None:
            raise Exception("CHATBOT_API_KEY is None")
        if chatbot_base_url is None:
            raise Exception("CHATBOT_BASE_URL is None")
        if chatbot_id is None:
            raise Exception("CHATBOT_ID is None")
        if recommendation_agent_id is None:
            raise Exception("RECOMMENDATION_AGENT_ID is None")

        self.chatbot_id = chatbot_id
        self.recommendation_agent_id = recommendation_agent_id
        self.api_key = api_key
        self.chatbot_base_url = chatbot_base_url

    def get_recommendation(self, message):
        headers = {
            'Authorization': f'Bearer {self.api_key}',
            'Content-Type': 'application/json'
        }
        data = {
            "messages": message,
            "chatbotId": self.recommendation_agent_id,
            "stream": False,
        }

        response = requests.post(
            self.chatbot_base_url, headers=headers, data=json.dumps(data))
        json_data = response.json()

        if response.status_code == 200:
            return {"data": json_data['text'], "status": response.status_code}
        else:
            return {"error": json_data['message'], "status": response.status_code}

    def send_message(self, messages):
        headers = {
            'Authorization': f'Bearer {self.api_key}',
            'Content-Type': 'application/json'
        }
        data = {
            "messages": messages,
            "chatbotId": self.chatbot_id,
            "stream": False,
        }

        response = requests.post(
            self.chatbot_base_url, headers=headers, data=json.dumps(data))
        json_data = response.json()

        if response.status_code == 200:
            return {"data": json_data['text'], "status": response.status_code}
        else:
            return {"error": json_data['message'], "status": response.status_code}
