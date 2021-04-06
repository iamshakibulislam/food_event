from django.urls import path

from . import views
from django.conf.urls import url

urlpatterns = [
    path('home/', views.home, name='home'),
    path('login/', views.login, name='login'),  
    path('signup/', views.signup, name='signup'),  
    path('cart/', views.cart, name='cart'), 

]
