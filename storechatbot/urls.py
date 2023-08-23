from django.urls import path, include


from . import views
urlpatterns = [
    path('test', views.welcome, name='test'),
]
