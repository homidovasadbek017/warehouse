from django.urls import path
from .views import *
urlpatterns = [
    path('', base_view),
    path('sections/', SectionsView.as_view(), name='sections'),
    path('sections/products/', ProductsView.as_view(), name='products'),
    path('products/<int:pk>/update/', ProductUpdateView.as_view()),
    path('products/<int:pk>/delete/', ProductDeleteView.as_view()),
    path('sections/clients/', ClientsView.as_view(), name='clients'),
    path('clients/<int:pk>/update/', ClientUpdateView.as_view()),
    path('clients/<int:pk>/delete/', ClientDeleteView.as_view()),

]
