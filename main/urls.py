from django.urls import path, include
from . import views, functions
urlpatterns = [
  path('', views.welcome,name = 'home'),
  path('', functions.sendWhatsappMessage, name = 'send')
]
