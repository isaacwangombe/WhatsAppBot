import json
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse, HttpResponse
from django.conf import settings


from .functions import *
# Create your views here.

import pdfkit
from django.template.loader import get_template
import os


def createPDF(request):
  # The name of your PDF file
    filename = 'filename.pdf'
    # HTML FIle to be converted to PDF - inside your Django directory
    template = get_template('business/business.html')
    # Add any context variables you need to be dynamically rendered in the HTML
    context = {}
    context['name'] = 'Mariga'
    context['surname'] = 'TheBomb'

  # Render the HTML
    html = template.render(context)

  # Options - Very Important [Don't forget this]
    options = {
        'encoding': 'UTF-8',
        'enable-local-file-access': None,  # To be able to access CSS
        'page-size': 'A4',
        'custom-header': [
            ('Accept-Encoding', 'gzip')
        ],
    }
    # Javascript delay is optional

    # Remember that location to wkhtmltopdf
    config = pdfkit.configuration(wkhtmltopdf='/usr/local/bin/wkhtmltopdf')

    # Create the file
    file_content = pdfkit.from_string(
        html, False, configuration=config, options=options)

    # Create the HTTP Response
    response = HttpResponse(file_content, content_type='application/pdf')
    response['Content-Disposition'] = 'inline; filename = {}'.format(filename)

    # Return
    return response


def welcome(request):

    token = settings.WHATSAPP_TOKEN
    return render(request, 'business/index.html', {'token': token})


@csrf_exempt
def whatsappWebhook(request):
    if request.method == 'GET':
        VERIFY_TOKEN = 'test'
        mode = request.GET['hub.mode']
        token = request.GET['hub.verify_token']
        challenge = request.GET['hub.challenge']

        if mode == 'subscribe' and token == VERIFY_TOKEN:
            return HttpResponse(challenge, status=200)
        else:
            return HttpResponse('error', status=403)

    if request.method == 'POST':
        data = json.loads(request.body)
        if 'object' in data and 'entry' in data:
            if data['object'] == 'whatsapp_business_account':
                try:
                    for entry in data['entry']:
                        phoneId = entry['changes'][0]['value']['metadata']['phone_number_id']
                        profileName = entry['changes'][0]['value']['contacts'][0]['profile']['name']
                        whatsAppId = entry['changes'][0]['value']['contacts'][0]['wa_id']
                        fromId = entry['changes'][0]['value']['messages'][0]['from']
                        text = entry['changes'][0]['value']['messages'][0]['text']['body']

                        # phoneNumber = '254706551542'
                        # message = 'RE: {} test was received'.format(text)
                        # sendWhatsappMessage(fromId, message)

                        handleWhatsappChat(fromId, profileName, phoneId, text)
                except:
                    pass

        return HttpResponse('success', status=200)
