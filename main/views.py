from django.shortcuts import render
from functions import sendWhatsappMessage
# Create your views here.


def welcome(request):

    return render(request, 'business/index.html')



