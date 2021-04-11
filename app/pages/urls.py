from django.urls import path

from . import views
from django.conf.urls import url

urlpatterns = [
    path('', views.index, name='index'), 
    path('dashboard/', views.dashboard, name='dashboard'), 
    #path('home/', views.home, name='home'),    
    #path('register', views.register, name='register'),
    #path('login', views.login, name='login'),
    path('calendar/', views.calendar, name='calendar'),
    path('shoppinglist/<int:list_id>/', views.shopping_list, name='shoppingList'),
    path('plan-create/', views.plan_create, name='plancreate'),
    path('mealplanview/', views.mealplan_view, name='mealplanView'),
  

]

