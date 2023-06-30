import os
import openai
from django.conf import settings
from dotenv import load_dotenv
load_dotenv()

# openai.api_key = settings.OPENAI_API_KEY
openai.api_key = os.environ.get('OPENAI_API_KEY')


def SalesAI(Message):
    response = openai.Completion.create(
        model="text-davinci-002",
        prompt=f"convert this text into json with the following keys : amount, phoneNumber, transactionCode, date:{Message}",
        temperature=0,
        max_tokens=2000,
        frequency_penalty=0,
        presence_penalty=0

    )

    if 'choices' in response:
        answer = response['choices'][0]['text']
        return answer

    else:
        return ""
