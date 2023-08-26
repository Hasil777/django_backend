from django.urls import path
from .views import getRoute, getProducts, getProduct

urlpatterns = [
    path('', getRoute.as_view()),
    path('products/', getProducts.as_view()),
    path('products/<pk>/', getProduct.as_view()),
]
