from django.urls import path

from .views import *

urlpatterns = [
    path('items/', items, name='items'),
    path('items/<int:pk>/', item_detail, name='item-detail'),
]