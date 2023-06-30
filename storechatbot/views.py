from django.shortcuts import render
from .forms import MessageForm
from .aifile import SalesAI
from .models import *
import json


# Create your views here.

from django.shortcuts import render
# Create your views here.


def welcome(request):
    message = ""
    answer = ""
    sales = Sales()
    if request.method == "POST":
        form = MessageForm(request.POST)
        if form.is_valid():
            message = form.cleaned_data["message"]
            answers = SalesAI(message)
            answer = json.loads(answers)
            sales.amount = answer["amount"]
            sales.phoneNumber = answer["phoneNumber"]
            sales.transactionCode = answer["transactionCode"]
            sales.date = answer["date"]
            sales.save()

    else:
        form = MessageForm()

    return render(request, 'test.html', {"form": form, "message": message, "answer": answer})
