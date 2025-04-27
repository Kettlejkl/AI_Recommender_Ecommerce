from django.urls import path
from . import views

urlpatterns = [
    path('', views.product_list, name='product_list'),  # Displays the product list page
    path('add/', views.add_product, name='add_product'),  # Displays the add product page
]
