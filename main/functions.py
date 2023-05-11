from django.conf import settings
import requests

WHATSAPP_TOKEN =settings.WHATSAPP_TOKEN

def sendWhatsappMessage(message,phoneNumber):
  WHATSAPP_TOKEN =settings.WHATSAPP_TOKEN

  headers ={"Authorization":WHATSAPP_TOKEN}
  payload ={"messaging_product": "whatsapp",
            "recipient_type": "individual",
            "to": phoneNumber,
            "type":"text",
            "text":{"body":message}}
  response = requests.post(settings.WHATSAPP_URL, headers=headers, json=payload)
  ans = response.json()
  return ans




# phoneNumber = "254706551542"
# message = "This works!! \n AWESOME \n "

# ans = sendWhatsappMessage(message, phoneNumber)