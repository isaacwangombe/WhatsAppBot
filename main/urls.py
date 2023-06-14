from django.urls import path, include
from . import views
urlpatterns = [
    path('', views.welcome, name='home'),
    path('webhook', views.whatsappWebhook, name='whatsapp-webhook'),
    path('pdf', views.generatePDF, name='generatePDF')
]
