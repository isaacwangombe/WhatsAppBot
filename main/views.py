import json
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse, HttpResponse
from django.conf import settings
from django.views.generic import View


from .functions import *
# Create your views here.
from whatsappbot.utils import render_to_pdf


def welcome(request):

    token = settings.WHATSAPP_TOKEN
    return render(request, 'business/index.html', {'token': token})


def GeneratePdf(request):
    data = {
        'today': 4/3/1995,
        'amount': 39.99,
        'customer_name': 'Cooper Mann',
        'order_id': 1233434,
    }
    pdf = render_to_pdf('business/business.html', data)
    return HttpResponse(pdf, content_type='application/pdf')


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
