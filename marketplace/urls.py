from django.urls import path
from . import views

urlpatterns = [
    path('', views.marketplace, name='marketplace'),


    path('<slug:vendor_slug>/', views.vendor_detail, name='vendor_detail'),

    # ADD TO CART
    path('add_to_cart/<int:food_id>/', views.add_to_cart, name='add_to_cart'),
    # Decrease CART
    path('decrease_cart/<int:food_id>/', views.decrease_cart, name='decrease_cart'),
    # deleted from cart
    path('delete_from_cart/<int:cart_id>/', views.delete_from_cart, name='delete_from_cart')
    
]