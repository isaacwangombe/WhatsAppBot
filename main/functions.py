
from django.conf import settings
from django.contrib.auth.models import User
from .models import *
import requests
from django.http import FileResponse
from reportlab.pdfgen import canvas
import io
from .aifile import *


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


# def handleWhatsappChat(fromId, profileName, phoneId, text):
# 	try:
# 		chat = ChatSession.objects.get(profile__phoneNumber=fromId)
# 	except:
# 		# Check that user does not already exist

# 		if User.objects.filter(username=phoneId).exists():
# 			user = User.objects.get(username=phoneId)
# 			user_profiles = user.profile
# 		else:
# 			# Create new user
# 			user = User.objects.create_user(
# 				username=phoneId,
# 				email='test@test.com',
# 				password='password',
# 				first_name=profileName
# 			)
# 			# Create a profile
# 			user_profiles = Profile.objects.create(
# 				user=user,
# 				phoneNumber=fromId,
# 				phoneId=phoneId
# 			)
# 		# create chat session
# 		chat = ChatSession.objects.create(profile=user_profiles)
# 		message = 'Welcome to the AI Business Plan creator 😀\n Im going to take you throught the process of creating your business plan right here on whatsapp\n To get started enter your business name'
# 		sendWhatsappMessage(fromId, message)
# 		return ""


# continue with function
    # Check if the business name exists
    # if chat.business_name:
    # 	if chat.business_type:
    # 		message = "Already entered business name"
    # 	else:
    # 		message = "Already entered business name"

    # else:
    # 	chat.business_name = text
    # 	chat.save()
    # 	# Ask for business type
    # 	message = "Great, Thank you. \n Please select the type of business. Enter the number corresponding to the Business Type \n 1. Private\n 2. Partnership \n3. Non-Profit \n \n Enter just the number "
    # 	sendWhatsappMessage(fromId, message)
    # 	return ""

def createPDF(chat, businessPlan):

    # Variables
    profile = chat.profile
    filename = businessPlan.uniqueId+'.pdf'

    buffer = io.BytesIO()
    x = canvas.Canvas(buffer)
    x.drawString(100, 100, "Let's generate this pdf file.")
    x.showPage()
    x.save()
    buffer.seek(0)

    # Saving the File
    filepath = settings.MEDIA_ROOT + \
        '/business_plans/{}/'.format(profile.uniqueId)
    os.makedirs(filepath, exist_ok=True)
    pdf_save_path = filepath+filename
    # Save the PDF
    return 'https://whatsappbot.herokuapp.com/media/' + \
        'business_plans/{}/{}'.format(profile.uniqueId, filename)


def buildBusinessPlan(chat):
    company_description = companyDescription("test", 1, "Kenya",
                                             "Shoes", "shoe company", 1, "5 sales")
    # company_description = companyDescription(chat.business_name, chat.business_type, chat.country,
    #                                          chat.product_service, chat.short_description, chat.years_operation, chat.progress)

    businessPlan = BusinessPlan.objects.create(
        profile=chat.profile,
        company_description=company_description
    )
    businessPlan.save()

    return businessPlan


def createNewBusinessPlan(chat, fromId):
    # Build the business plan
    businessPlan = buildBusinessPlan(chat)

    # Create the pdf document
    doc_url = createPDF(chat, businessPlan)

    # Send the document Link
    # /usr/local/bin/wkhtmltopdf
    message = 'Here:\n \n {}'.format(doc_url)
    sendWhatsappMessage(fromId, message)
    # delete the chat ata the end
    chat.delete()


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
                                createNewBusinessPlan(chat, fromId)
                        else:
                            try:
                                years = int(text.replace(" ", ""))
                                chat.years = years
                                chat.save()
                                message = "How much progress have you made in your business?"
                                sendWhatsappMessage(fromId, message)
                            except:
                                message = "Please try again, enter only a number like 1 or 2"
                                sendWhatsappMessage(fromId, message)
                    else:
                        chat.short_description = text
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
                    chat.save()

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
        chat.save()
        # Send next message
        message = "Great, Thank you. \n Please select the type of business. Enter the number corresponding to the Business Type \n 1. Private\n 2. Partnership \n3. Non-Profit \n \n Enter just the number "
        sendWhatsappMessage(fromId, message)
