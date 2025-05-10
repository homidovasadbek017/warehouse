from django.urls import path
from .views import *

urlpatterns = [
    path('sales/', SalesView.as_view(), name='sales'),
    path('sales/<int:pk>/update/', SaleUpdateView.as_view()),
    path('sales/<int:pk>/delete/', SaleDeleteView.as_view()),
]


