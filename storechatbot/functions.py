
from datetime import datetime
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


def AreYouDone(fromId):
    message = 'Thank You for renting with us!\n\n If you want to perform another task Kindly type MENU to return to main Menu \n\n Otherwise, have an amazing day'
    sendWhatsappMessage(fromId, message)


def renter_payment(fromId, text):
    if text == "y":
        sendWhatsappMessage(fromId, "transaction.amount")
    else:
        sendWhatsappMessage(fromId, "still?")


def parse_transaction_message(fromId, text):
    if transaction:
        renter_payment(fromId, text)
    else:

        sender = Profiles.objects.get(phoneNumber=fromId)
        # apartment = sender__apartment

        # Getting Transaction code
        transaction_code_regex = re.search(
            r'(?:Ref. Number|Ref. Number:|Transaction ID|MPESA Ref.|Ref.|Ref) ([A-Z0-9]+)', text)

        if transaction_code_regex:
            transaction_code = transaction_code_regex.group(1)

        else:
            transaction_code = re.search(r'(\b[0-9A-Z]+\b)', text).group()

        # Getting amount
        amount_regex = float(
            re.search(r'(?i)(?:KES|Kshs?\.?)\s?([0-9,]+(?:\.\d{1,2})?)', text).group(1).replace(',', ''))

        amount = amount_regex

        # Getting Date
        date_regex = re.search(
            r'(\b\d{1,2}[ /-]\d{1,2}[ /-]\d{2,4}\b)', text).group(1)

        date_str = date_regex.replace("/", "-")
        year = date_str.split("-")[-1]
        if len(year) == 2:
            date = datetime.strptime(date_str, "%d-%m-%y").date()
        else:
            date = datetime.strptime(date_str, "%d-%m-%Y").date()

        transaction = Transaction.objects.create(
            sender=sender,
            transaction_code=transaction_code,
            amount=amount,
            date=date,
            recipient_name="Me",
            recipient_account="Mine"
        )
        message = f"Thank you for uploading the transaction,\n Are these the right transaction details?\n\napartment = {sender.apartment.number} \ntenant = {sender.first_name}\n transaction code = {transaction_code}\n amount = {amount} \n date = {date}\n\n If yes, reply with Y\n if no, reply with N"
        sendWhatsappMessage(fromId, message)
        # sendWhatsappMessage(fromId, "Kindly reupload the message")

    # return transaction


def createUsers(fromId, phoneId, text):
    chat = ChatSession.objects.get(profile__phoneNumber=fromId)
    question = chat.question_no
    creator = User.objects.get(username=phoneId)

    match question:
        case 1:
            profile = Profiles.objects.create(creator=creator)
            chat.question_no = chat.question_no + 1
            chat.save()
            message = "What is the tenants first name?"
            sendWhatsappMessage(fromId, message)

        case 2:
            profile = Profiles.objects.filter(creator=creator).last()
            profile.first_name = text
            profile.save()
            chat.question_no = chat.question_no + 1
            chat.save()
            message = "What is the tenant's last name?"
            sendWhatsappMessage(fromId, message)

        case 3:
            profile = Profiles.objects.filter(creator=creator).last()
            profile.last_name = text
            profile.save()
            chat.question_no = chat.question_no + 1
            chat.save()
            message = "What is the tenant's phone number?"
            sendWhatsappMessage(fromId, message)

        case 4:
            profile = Profiles.objects.filter(creator=creator).last()
            profile.phoneNumber = text
            profile.save()
            chat.question_no = chat.question_no + 1
            chat.save()
            message = "What is the tenant's email address?"
            sendWhatsappMessage(fromId, message)

        case 5:
            profile = Profiles.objects.filter(creator=creator).last()
            profile.first_name = text
            profile.save()
            chat.question_no = chat.question_no + 1
            chat.save()
            message = "What is the tenant's role?"
            sendWhatsappMessage(fromId, message)


def SendReceipt(fromId, text):
    message = 'Kindly send in your M-PESA OR BANK payment Receipt message below \n\n type EXIT to go back to Exit or MENU to return to main Menu'
    sendWhatsappMessage(fromId, message)
    parse_transaction_message(text)


def PaymentDetails(fromId):
    message = 'The Payment details \n\n type EXIT to go back to Exit or MENU to return to main Menu'
    sendWhatsappMessage(fromId, message)


def RepairRequest(fromId):
    message = 'Which kind of repair do you require today?\n\n 1) Water (eg lack of water, plumbing, water leakages)\n\n2) Electric (e.g. light not working, socket not working, shower not hot, broken fixtures)\n 3)Structural issues (e.g. broken window, door issues)\n\n type EXIT to go back to Exit or MENU to return to main Menu'
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
                creator=user,
                phoneNumber=fromId,
                phoneId=phoneId
            )

        # create a chat session
            chat = ChatSession.objects.create(profile=user_profiles)
            message = 'Welcome to the Apartment Bot 😀\n What would you like to do today?\n\n Please choose any of the following options by typing 1, 2 or 3\n\n1)Send in payment transaction\n2)Get payment details\n3)Request for maintanance'
            sendWhatsappMessage(fromId, message)
            return
    if chat.question_no == 0:
        match text:
            case "1":
                chat.chat_purpose = 'receipt'
                chat.question_no = chat.question_no+1
                chat.save()
                message = 'Kindly paste the message below'
                sendWhatsappMessage(fromId,  message)
                SendReceipt(fromId, text)
            case "2":
                chat.chat_purpose = 'payment'
                chat.question_no = chat.question_no+1
                chat.save()
                PaymentDetails(fromId)
            case "3":
                chat.chat_purpose = 'complaint'
                chat.question_no = chat.question_no+1
                chat.save()
                RepairRequest(fromId)
            case "4":
                chat.chat_purpose = 'complaint'
                chat.question_no = chat.question_no+1
                chat.save()
                message = 'What house Number are you creating a user for'
                sendWhatsappMessage(fromId,  message)
                createUsers(fromId, phoneId)
                return
                # RepairRequest(fromId)
            case _:
                message = 'invalid'
                sendWhatsappMessage(fromId, message)
    elif chat.chat_purpose == 'receipt' and chat.question_no == 1:
        # message = text
        # sendWhatsappMessage(fromId, message)
        parse_transaction_message(fromId, text)

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
