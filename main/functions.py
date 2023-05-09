from django.conf import settings
import requests

def sendWhatsappMessage(message,phoneNumber):
  headers ={"Authorization":settings.WHATSAPP_TOKEN}
  payload ={"messaging_product": "whatsapp",
            "recipient_type": "individual",
            "to": phoneNumber,
            "type":"text",
            "text":{"body":message}}
  response = requests.post(settings.WHATSAPP_URL, headers=headers, json=payload)
  ans = response.json()
  return ans



phoneNumber = '254706551542'
message = 'RE: message was received'
sendWhatsappMessage(phoneNumber, message)

