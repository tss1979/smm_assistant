from openai import OpenAI
from config import OPENAI_API_KEY

class TextGenerator:
    def __init__(self, openai_key: str, tone: str, topic: str):
        self.tone = tone,
        self.topic = topic
        self.client = OpenAI(api_key=openai_key)

    def get_openapi_response(self, content: str):
        response = self.client.chat.completions.create(
            model="gpt-4o",
            messages=[
                {
                    "role": "system",
                    "content": content
                },
                {
                    "role": "user",
                    "content": f"Сгенерируй пост для соцсетей с темой {self.topic}, используя тон: {self.tone}"
                }
            ],
        )
        return response

    def generate_text(self):
        response = self.get_openapi_response("Ты высококвалифицированный сомелье, который будет помогать в генерации текста для постов с заданной тебе тематикой и заданным тоном.")
        return response.choices[0].message.content

    def generate_image_description(self):
        response = self.get_openapi_response("Ты высококвалифицированный SMM специалист, который будет помогать в генерации текста для постов с заданной тебе тематикой и заданным тоном.")
        return  response.choices[0].message.content
