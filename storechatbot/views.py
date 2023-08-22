from django.shortcuts import render
from .forms import MessageForm
from .models import *
import json


# Create your views here.

from django.shortcuts import render
# Create your views here.


def two(request):
    message = Message()
    question = "Question 2"
    if request.method == "POST":
        message.three = request.POST["message"]
        message.save()
        return render(request, 'test.html', {"message": message, "question": question})
    else:
        return render(request, 'test.html', {"message": message, "question": question})


def one(request):
    if Message.one:
        two(request)

    else:
        question = "Question 1"
        if request.method == "POST":
            message = Message()
            message.two = request.POST["message"]
            message.save()
            return render(request, 'test.html', {"message": message, "question": question})
        else:
            return render(request, 'test.html', {"message": message, "question": question})


def welcome(request):
    if Message.objects.exists():
        # question = "test"
        one(request)

    else:
        question = "Question"
        if request.method == "POST":
            message = Message()
            message.one = request.POST["message"]
            message.save()
            return render(request, 'test.html', {"message": message, "question": question})
        else:
            return render(request, 'test.html', {"message": message, "question": question})
    # return render(request, 'test.html', {"message": message, "question": question})
