from django.urls import path
from . import views

urlpatterns = [
    path('', views.ContactView.as_view(), name='contact'),
    path('subscribe/', views.subscribe_newsletter, name='subscribe_newsletter'),
]
