
from datetime import datetime
from django.conf import settings
from django.contrib.auth.models import User
import requests
import re
from .aifile import *
from .models import *


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


def AreYouDone(fromId, text):
    match text:
        case "1":
            sendWhatsappMessage(fromId, '1')
        case "2":
            sendWhatsappMessage(fromId, '2')


def afterDeleteTransaction(fromId, text):
    match text:
        case "1":
            sendWhatsappMessage(fromId, '1')
        case "2":
            sendWhatsappMessage(fromId, '2')


def verifyTransaction(fromId, text):
    chat = ChatSession.objects.get(profile__phoneNumber=fromId)
    transaction = Transaction.objects.filter(
        sender__phoneNumber=fromId).last()
    if text.upper() == "Y":

        apartment = Profiles.objects.filter(
            phoneNumber=fromId).last().apartment
        new_balance = apartment.balance - transaction.amount

        apartment.balance = int(new_balance)
        apartment.save()
        chat.question_no = chat.question_no + 1
        chat.save()
        sendWhatsappMessage(fromId, apartment.balance)
    elif text.upper() == "N":
        # transaction.delete()
        chat.question_no = chat.question_no + 2
        chat.save()

    else:
        sendWhatsappMessage(
            fromId, 'Kindly either send a "Y" or "N" to complete the interaction')


def parse_transaction_message(fromId, text):

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
        message=text,
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


def PaymentDetails(fromId, text):
    message = 'The Payment details \n\n type EXIT to go back to Exit or MENU to return to main Menu'
    sendWhatsappMessage(fromId, message)


def Repair(fromId, text):
    chat = ChatSession.objects.get(profile__phoneNumber=fromId)
    question = chat.question_no
    renter = Profiles.objects.get(phoneNumber=fromId)
    request = RepairRequest.objects.create(
        renter=renter, status="1")
    match question:
        case 1:
            match text:
                case "1":
                    request.type = "1"
                    request.save()

                case "2":
                    request.type = "2"
                case "3":
                    request = RepairRequest.objects.create(
                        renter=renter, type="3")
                case "4":
                    request = RepairRequest.objects.create(
                        renter=renter, type="4")
                case "5":
                    request = RepairRequest.objects.create(
                        renter=renter, type="5")
                case "6":
                    request = RepairRequest.objects.create(
                        renter=renter, type="6")
            chat.question_no = chat.question_no + 1
            chat.save()
            message = "Kindly describe the issue"
            sendWhatsappMessage(fromId, message)
        case 2:
            request.description = text
            request.save()
            message = "Thank You, We will send over a repair man  as soon as possible"
            sendWhatsappMessage(fromId, "Why?")


def handleUserChat(fromId, phoneId, text):

    try:
        chat = ChatSession.objects.get(profile__phoneNumber=fromId)
    except:

        profile = Profiles.objects.get(phoneNumber=fromId)
        chat = ChatSession.objects.create(profile=profile)

        # create a chat session
        message = 'Welcome to the Apartment Bot 😀\n What would you like to do today?\n\n Please choose any of the following options by typing 1, 2 or 3\n\n1)Send in payment transaction\n2)Get payment details\n3)Request for maintanance'
        sendWhatsappMessage(fromId, message)

    if chat.question_no == 0:
        match text:
            case "1":
                chat.chat_purpose = 'receipt'
                chat.question_no = chat.question_no+1
                chat.save()
                message = 'Kindly send in your M-PESA OR BANK payment Receipt message below \n\n type EXIT to go back to Exit or MENU to return to main Menu'
                sendWhatsappMessage(fromId,  message)
            case "2":
                chat.chat_purpose = 'payment'
                chat.question_no = chat.question_no+1
                chat.save()
                PaymentDetails(fromId)
            case "3":
                chat.chat_purpose = 'complaint'
                chat.question_no = chat.question_no+1
                chat.save()
                message = 'Which kind of repair do you require today?\n\n 1) Water (eg lack of water, plumbing, water leakages)\n\n2) Electric (e.g. light not working, socket not working, shower not hot, broken fixtures)\n\n 3)Carpentry(e.g. door issues, closet issues, cupboard issues)\n\n 4) MetalWork (e.g. Main door issues, railing issues) \n\n5) Masonry (e.g Wall issues, tile issues)\n\n6) Other \n\n type EXIT to go back to Exit or MENU to return to main Menu'
                sendWhatsappMessage(fromId, message)
            case "4":
                chat.chat_purpose = 'create'
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
    elif chat.chat_purpose == 'receipt':
        match chat.question_no:
            case 1:
                parse_transaction_message(fromId, text)
                chat.question_no = chat.question_no + 1
                chat.save()
            case 2:
                verifyTransaction(fromId, text)
            case 3:
                sendWhatsappMessage(
                    fromId, "Your upload has been successfully saved\n Would you like to go back to main menu or Exit \n\n 1) Main Menu) \n 2) Exit")
                AreYouDone(fromId, text)
            case 4:
                sendWhatsappMessage(
                    fromId, "Your upload has been deleted,\n Would you like to reupload it, go back to main menu or Exit \n\n 1) Reupload it \n 2) Main Menu) \n 3) Exit")
                afterDeleteTransaction(fromId, text)
    elif chat.chat_purpose == 'payment':
        match chat.question_no:
            case 1:
                PaymentDetails(fromId, text)
                chat.question_no = chat.question_no + 1
                chat.save()

    elif chat.chat_purpose == 'complaint':
        Repair(fromId, text)
        chat.question_no = chat.question_no + 1
        chat.save()
