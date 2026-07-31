from django.urls import path
from . import views

urlpatterns = [
    path('', views.contact_view, name='contact'),
    path('test-smtp/', views.test_smtp, name='test_smtp'),
    path('subscribe/', views.subscribe_newsletter, name='subscribe_newsletter'),
]
