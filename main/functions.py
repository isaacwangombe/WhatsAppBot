from django.conf import settings
import requests

def sendWhatsappMessage(message):
  headers ={"Authorization":settings.WHATSAPP_TOKEN}
  payload ={"messaging_product": "whatsapp",
            "recipient_type": "individual",
            "to": "254706551562",
            "type":"text",
            "text":{"body":message}}
  response = requests.post(settings.WHATSAPP_URL, headers=headers, json=payload)
  ans = response.json()
  return ans


# phoneNumber = "254706551562"
message = "This works!! \n AWESOME \n "

sendWhatsappMessage(message)