from django.urls import path, include


from . import views
urlpatterns = [
    path('', views.welcome, name='test'),
    path('webhook', views.whatsappWebhook, name='whatsapp-webhook'),

]
