# URLs are like a map of your website - they tell Django which page to show for each web address
# Think of it like a phone book: when someone dials a number, it connects to the right person

from django.contrib import admin  # This brings in Django's admin panel tools
from django.urls import path, include  # These help us create URL routes (like street addresses)
from . import views  # This brings in all our view functions from views.py

# This list contains all the "addresses" in our website
# Each path() is like saying "when someone visits this address, show them this page"
urlpatterns = [
    path('', views.home, name='home'),
    path('login/', views.login_view, name='login'),
    path('signup/', views.signup, name='signup'),
    path('dash/', views.dash, name='dash'),
    path('add/', views.add, name='add'),
    path('cart/', views.cart, name='cart'),
    path('add-to-cart/<int:product_id>/', views.add_to_cart, name='add_to_cart'),
    path('update-cart/<int:item_id>/', views.update_cart, name='update_cart'),
    path('toggle-favorite/<int:product_id>/', views.toggle_favorite, name='toggle_favorite'),
    path('logout/', views.logout_view, name='logout'),
    
]