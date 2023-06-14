from django.urls import path, include
from . import views


urlpatterns = [
    path('', views.welcome, name='home'),
    path('pdf/<user>', views.GeneratePdf, name='pdf'),
    path('webhook', views.whatsappWebhook, name='whatsapp-webhook')
]
