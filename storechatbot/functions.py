
import datetime
from django.conf import settings
from django.contrib.auth.models import User
import requests
from django.http import FileResponse
from reportlab.pdfgen import canvas
import re
from .aifile import *
from .models import ChatSession, Transaction, Profiles
from django.core.exceptions import ObjectDoesNotExist


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


def Ans1(fromId):
    message = 'one'
    sendWhatsappMessage(fromId, message)


def Ans2(fromId):
    message = 'twos'
    sendWhatsappMessage(fromId, message)


def handleWhatsappChat(fromId, profileName, phoneId, text):
    try:
        chat = ChatSession.objects.get(profile__phoneNumber=fromId)
    except ObjectDoesNotExist:
        # Check that user does not already exist
        if User.objects.filter(username=phoneId).exists():
            user = User.objects.get(username=phoneId)
            user_profiles = user.profiles

        else:
            # create a user
            user = User.objects.create_user(
                username=phoneId,
                email='test@test.com',
                password='password',
                first_name=profileName,
            )

            # create a profile
            user_profiles = Profiles.objects.create(
                user=user,
                phoneNumber=fromId,
                phoneId=phoneId
            )

        # create a chat session
            chat = ChatSession.objects.create(profile=user_profiles)
            message = 'Welcome to the Apartment Bot 😀\n What would you like to do today?\n\n Please choose any of the following options by typing 1, 2 or 3\n\n1)Send in payment transaction\n2)Get payment details\n3)Request for maintanance'
            sendWhatsappMessage(fromId, message)
            return

    match text:
        case "1":
            Ans1(fromId)
        case "2":
            Ans2(fromId)
        case _:
            message = 'invalid'
            sendWhatsappMessage(fromId, message)

    # if chat.chat_purpose:
    #     if chat.chat_purpose == '1':
    #         parse_transaction_message(message)
    #     elif chat.chat_purpose == '2':

    #     else:

    # else:
    #     try:
    #         type = int(text.replace(" ", ""))
    #         if type == 1:
    #             chat.chat_purpose = '1'
    #             chat.save()
    #             message = "Kindly paste the payment transaction here"
    #             sendWhatsappMessage(fromId, message)
    #         elif type == 2:
    #             chat.chat_purpose = '2'
    #             chat.save()
    #             message = "Which country are you from?"
    #             sendWhatsappMessage(fromId, message)
    #         elif type == 3:
    #             chat.chat_purpose = '3'
    #             chat.save()
    #             message = "Which country are you from?"
    #             sendWhatsappMessage(fromId, message)
    #         else:
    #             message = "Please try again\n Please choose any of the following options by typing 1, 2 or 3\n\n1)Send in payment transaction\n2)Get payment details\n3)Request for maintanance "
    #             sendWhatsappMessage(fromId, message)
    #     except:
    #         message = "Please try again\n Please choose any of the following options by typing 1, 2 or 3\n\n1)Send in payment transaction\n2)Get payment details\n3)Request for maintanance "
    #         sendWhatsappMessage(fromId, message)


# def handleWhatsappChat(fromId, profileName, phoneId, text):
#     # CHeck if there is a chat session
#     try:
#         chat = ChatSession.objects.get(profile__phoneNumber=fromId)
#     except:
#         # Check that user does not already exist
#         if User.objects.filter(username=phoneId).exists():
#             user = User.objects.get(username=phoneId)
#             user_profiles = user.profile

#         else:
#             # create a user
#             user = User.objects.create_user(
#                 username=phoneId,
#                 email='test@test.com',
#                 password='password',
#                 first_name=profileName,
#             )

#             # create a profile
#             user_profiles = Profile.objects.create(
#                 user=user,
#                 phoneNumber=fromId,
#                 phoneId=phoneId
#             )

#         # create a chat session
#         chat = ChatSession.objects.create(profile=user_profiles)

#         message = 'Welcome to the AI Business Plan creator 😀\n Im going to take you throught the process of creating your business plan right here on whatsapp\n To get started enter your business name'
#         sendWhatsappMessage(fromId, message)


# # continue with function

#     if chat.business_name:
#         if chat.business_type:
#             if chat.country:
#                 if chat.product_service:
#                     if chat.short_description:
#                         if chat.years:
#                             # continue
#                             if chat.progress:
#                                 message = "Give us a moment, we will message you when your business plan is ready"
#                                 sendWhatsappMessage(fromId, message)
#                             else:
#                                 chat.progress = text
#                                 chat.save()
#                                 message = "Great! We have everything we need to build your business plan"
#                                 sendWhatsappMessage(fromId, message)
#                                 createNewBusinessPlan(chat, fromId)
#                         else:
#                             try:
#                                 years = int(text.replace(" ", ""))
#                                 chat.years = years
#                                 chat.save()
#                                 message = "How much progress have you made in your business?"
#                                 sendWhatsappMessage(fromId, message)
#                             except:
#                                 message = "Please try again, enter only a number like 1 or 2"
#                                 sendWhatsappMessage(fromId, message)
#                     else:
#                         chat.short_description = text
#                         chat.save()
#                         message = "How many years have you been in business for? Enter a number like 1 or 2"
#                         sendWhatsappMessage(fromId, message)
#                 else:
#                     chat.product_service = text
#                     chat.save()
#                     message = "Describe your business idea in one or two sentenses"
#                     sendWhatsappMessage(fromId, message)
#             else:
#                 chat.country = text
#                 chat.save()
#                 # Send next message
#                 message = "What product or service will your business be providing"
#                 sendWhatsappMessage(fromId, message)
#         else:
#             # Text for the number
#             try:
#                 type = int(text.replace(" ", ""))
#                 if type == 1:
#                     chat.business_type = 'Private'
#                     chat.save()
#                     message = "Which country are you from?"
#                     sendWhatsappMessage(fromId, message)
#                 elif type == 2:
#                     chat.business_type = 'Partnership'
#                     chat.save()
#                     message = "Which country are you from?"
#                     sendWhatsappMessage(fromId, message)
#                 elif type == 3:
#                     chat.business_type = 'Non-Profit'
#                     chat.save()

#                     message = "Which country are you from?"
#                     sendWhatsappMessage(fromId, message)
#                 else:
#                     message = "Please try again Please select the type of business. Enter the number corresponding to the Business Type \n 1. Private\n 2. Partnership \n3. Non-Profit \n \n Enter just the number "
#                     sendWhatsappMessage(fromId, message)
#             except:
#                 message = "Please try again Please select the type of business. Enter the number corresponding to the Business Type \n 1. Private\n 2. Partnership \n3. Non-Profit \n \n Enter just the number "
#                 sendWhatsappMessage(fromId, message)
#         # Test for the number
#     else:
#         chat.business_name = text
#         chat.save()
#         # Send next message
#         message = "Great, Thank you. \n Please select the type of business. Enter the number corresponding to the Business Type \n 1. Private\n 2. Partnership \n3. Non-Profit \n \n Enter just the number "
#         sendWhatsappMessage(fromId, message)


def parse_transaction_message(message):
    transaction_code = re.search(
        r'(?:Ref\. Number|Transaction ID): ([A-Z0-9]+)', message).group(1)
    amount = float(
        re.search(r'(?i)Ksh[.\s]*([\d,]+\.\d+)', message).group(1).replace(',', ''))
    date_str = re.search(
        r'(\d{1,2}[/-]\d{1,2}[/-]\d{2,4})[,\s]*(\d{1,2}:\d{2}[^\d\s]*)', message).group(1, 2)
    date = datetime.strptime(' '.join(date_str), '%d-%m-%Y %H:%M')
    recipient_name = re.search(r'-\s*(.*?)\s*,', message).group(1)
    recipient_account = re.search(r'to\s*(\d+)', message).group(1)

    transaction = Transaction(transaction_code=transaction_code, amount=amount,
                              date=date, recipient_name=recipient_name, recipient_account=recipient_account)

    transaction.save()
    return transaction
