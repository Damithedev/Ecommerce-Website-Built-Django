from django.urls import path
from . import views

urlpatterns = [
    path('getorder/', views.OrderList.as_view(), name='getorderlist'),
]