
from django.conf import settings
from django.contrib.auth.models import User
from .models import *
import requests


def sendWhatsappMessage(fromId, message):
    headers = {"Authorization": settings.WHATSAPP_TOKEN}
    payload = {"messaging_product": "whatsapp",
               "recipient_type": "individual",
               "to": fromId,
               "type": "text",
               "text": {"body": message}}
    response = requests.post(settings.WHATSAPP_URL,
                             headers=headers, json=payload)
    ans = response.json()
    return ans


# phoneNumber = "254706551542"
# message = "This works!! \n AWESOME \n "

# ans = sendWhatsappMessage(message, phoneNumber)

def handleWhatsappChat(fromId, profileName, phoneId, text):
    # CHeck if there is a chat session
    try:
        chat = ChatSession.objects.get(profile__phoneNumber=fromId)
    except:
        # Check that user does not already exist
        if User.objects.filter(username=phoneId).exists():
            user = User.objects.get(username=phoneId)
            user_profiles = user.profile

        else:
            # create a user
            user = User.objects.create_user(
                username=phoneId,
                email='test@test.com',
                password='password',
                first_name=profileName,
            )

            # create a profile
            user_profiles = Profile.objects.create(
                user=user,
                phoneNumber=fromId,
                phoneId=phoneId
            )

        # create a chat session
        chat = ChatSession.objects.create(profile=user_profiles)

    message = 'Welcome to the AI Business Plan creator 😀\n Im going to take you throught the process of creating your business plan right here on whatsapp\n To get started enter your business name'
    sendWhatsappMessage(fromId, message)

# continue with function

    if chat.business_name:
        if chat.business_type:
            if chat.country:
                if chat.product_service:
                    if chat.short_description:
                        if chat.years:
                            # continue
                            if chat.progress:
                                message = "Give us a moment, we will message you when your business plan is ready"
                                sendWhatsappMessage(fromId, message)

                            else:
                                chat.progress = text
                            chat.save()

                            message = "Great! We have everything we need to build your business plan"
                            sendWhatsappMessage(fromId, message)

                        else:
                            try:
                                years = int(text.replace(' ', ''))
                                chat.years = years
                                chat.save()

                                message = "How much progress have you made in your business?"
                                sendWhatsappMessage(fromId, message)
                            except:
                                message = "Please try again, enter only a number like 1 or 2"
                                sendWhatsappMessage(fromId, message)

                    else:
                        chat.product_service = text
                        chat.save()
                        message = "How many years have you been in business for? Enter a number like 1 or 2"
                        sendWhatsappMessage(fromId, message)

                else:
                    chat.product_service = text
                    chat.save()
                    message = "Describe your business idea in one or two sentenses"
                    sendWhatsappMessage(fromId, message)

            else:
                chat.country = text
                chat.save()
                # Send next message
                message = "What product or service will your business be providing"

                sendWhatsappMessage(fromId, message)
        else:
            # Text for the number
            try:
                type = int(text.replace(" ", ""))
                if type == 1:
                    chat.business_type = 'Private'
                    chat.save()
                    message = "Which country are you from?"
                    sendWhatsappMessage(fromId, message)

                elif type == 2:
                    chat.business_type = 'Partnership'
                    chat.save()
                    message = "Which country are you from?"
                    sendWhatsappMessage(fromId, message)
                elif type == 3:
                    chat.business_type = 'Non-Profit'
                    message = "Which country are you from?"
                    sendWhatsappMessage(fromId, message)
                else:
                    message = "Please try again Please select the type of business. Enter the number corresponding to the Business Type \n 1. Private\n 2. Partnership \n3. Non-Profit \n \n Enter just the number "
                    sendWhatsappMessage(fromId, message)

            except:
                message = "Please try again Please select the type of business. Enter the number corresponding to the Business Type \n 1. Private\n 2. Partnership \n3. Non-Profit \n \n Enter just the number "
                sendWhatsappMessage(fromId, message)

        # Test for the number

    else:
        chat.business_name = text
        chat.save
        # Send next message
        message = "Great, Thank you. \n Please select the type of business. Enter the number corresponding to the Business Type \n 1. Private\n 2. Partnership \n3. Non-Profit \n \n Enter just the number "
        sendWhatsappMessage(fromId, message)
