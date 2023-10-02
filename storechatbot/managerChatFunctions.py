
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


def handleManagerChat(fromId, phoneId, text):

    try:
        chat = ChatSession.objects.get(profile__phoneNumber=fromId)
    except:

        profile = Profiles.objects.get(phoneNumber=fromId)
        chat = ChatSession.objects.create(profile=profile)

        # create a chat session
        message = 'Test Manager message'
        sendWhatsappMessage(fromId, message)
        return

    if chat.question_no == 0:
        match text:
            case "1":
                chat.chat_purpose = 'receipt'
                chat.question_no = chat.question_no+1
                chat.save()
                message = 'Kindly send in your M-PESA OR BANK payment Receipt message below \n\n type EXIT to go back to Exit or MENU to return to main Menu'
                sendWhatsappMessage(fromId,  message)

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

    elif chat.chat_purpose == 'complaint':
        Repair(fromId, text)
        chat.question_no = chat.question_no + 1
        chat.save()
