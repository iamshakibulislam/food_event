from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from core.models import User
from django.http import HttpResponse, JsonResponse, HttpRequest
import requests
import re
from decimal import Decimal
from random import seed, randint
from recipes.models import *

from recipes.models import Events,RecipeOverview
from recipes.services import *
from datetime import date, datetime, timedelta 



def plan_create(request):
    
    startdate = date(2021, 3, 29)
    enddate = date(2021, 4, 4)
    dayIntensitys = DayIntensity.objects.filter(date__range=[startdate, enddate], user=request.user)
    
    print(dayIntensitys)

    for day in dayIntensitys:
        print(day.id)
        response = MealPlanning.meal_planning(dayIntensityId=day.id, user=request.user)
        print(response)

    return render(request, 'pages/generate-meal-plan.html')

def shopping_list(request, list_id):
    shoppingList = ShoppingList.objects.get(pk=list_id)
    items = ShoppingListItem.objects.filter(shoppingList=shoppingList)

    context = {
        'items': items,
        'shoppingList': shoppingList
    }


    return render(request, 'pages/shoppinglist.html', context)

def mealplan_view(request):
    def daterange(date1, date2):
        for n in range(int ((date2 - date1).days)+1):
            yield date1 + timedelta(n)
            
    startdate = date(2021, 3, 29)
    enddate = date(2021, 4, 4)
    mealPlans = Events.objects.filter(start__range=[startdate, enddate])
    datesList = []
    for dt in daterange(startdate, enddate):
        datesList.append(dt)

    print(datesList)
    context = {
        'dates': datesList,
        'mealPlans': mealPlans
    }

    return render(request, 'pages/mealPlanView.html', context)

def dashboard(request):
    
    #importRecipe = SyncRecipes.sync_json_from_local()
    #print(importRecipe)
    SyncRecipes.sync_recipes_with_files()


    if request.method == 'POST': 
        name = request.POST.get('name')
        print(name)
        startdate = request.POST.get('date')
        enddate = request.POST.get('enddate')
        shoppingList = ShoppingListManage.generate_list(start=startdate, end=enddate, name=name)
    else:
        shoppingList = ""

    shoppingLists = ShoppingList.objects.all()

    today = datetime.today()
    breakfast = Events.objects.get_or_create(start=today, mealPosition=Events.BREAKFAST, user=request.user)
    breakfast = breakfast[0]
    breakfastIngredients = Ingredient.objects.filter(recipe=breakfast.mealChosen)
    breakfastDirections = Direction.objects.filter(recipe=breakfast.mealChosen).order_by('id')
    print('today')
    morningSnack = Events.objects.get_or_create(start=today, mealPosition=Events.MORNING_SNACK, user=request.user)
    morningSnack = morningSnack[0]
    morningSnackIngredients = Ingredient.objects.filter(recipe=morningSnack.mealChosen)
    morningSnackDirection = Direction.objects.filter(recipe=morningSnack.mealChosen).order_by('id')
    print('today')
    lunch = Events.objects.get_or_create(start=today, mealPosition=Events.LUNCH, user=request.user)
    lunch = lunch[0]
    lunchIngredients = Ingredient.objects.filter(recipe=lunch.mealChosen)
    lunchDirections = Direction.objects.filter(recipe=lunch.mealChosen).order_by('id')
    print('today')

    afternoonSnack = Events.objects.get_or_create(start=today, mealPosition=Events.AFTERNOON_SNACK, user=request.user)
    afternoonSnack = afternoonSnack[0]
    afternoonSnackIngredients = Ingredient.objects.filter(recipe=afternoonSnack.mealChosen)
    afternoonSnackDirections = Direction.objects.filter(recipe=afternoonSnack.mealChosen).order_by('id')
    print('today')
    dinner = Events.objects.get_or_create(start=today, mealPosition=Events.DINNER, user=request.user)
    dinner = dinner[0]
    dinnerIngredients = Ingredient.objects.filter(recipe=dinner.mealChosen)
    dinnerDirections = Direction.objects.filter(recipe=dinner.mealChosen).order_by('id')
    print('today')
    print(breakfast.mealPosition)
    pastdays = today - timedelta(14)
    yesterday = today - timedelta(1)
    print(yesterday)

    #feedbackEvent = Events.objects.filter(start__range=[pastdays,yesterday])
    #feedbackEvent = feedbackEvent[0]
    
    
    
    context = {
        'breakfast': breakfast,
        'morningSnack': morningSnack,
        'lunch': lunch,
        'afternoonSnack': afternoonSnack,
        'dinner': dinner,
        'breakfastIngredients': breakfastIngredients,
        'breakfastDirections': breakfastDirections,
        'morningSnackDirections': morningSnackDirection,
        'morningSnackIngredients': morningSnackIngredients,
        'lunchDirections': lunchDirections, 
        'lunchIngredients': lunchIngredients,
        'afternoonSnackIngredients': afternoonSnackIngredients,
        'afternoonSnackDirections': afternoonSnackDirections,
        'dinnerIngredients': dinnerIngredients,
        'dinnerDirections': dinnerDirections,
        #'feedbackEvent': feedbackEvent,
        'shoppingLists':shoppingLists
    }

    

    return render(request, 'pages/dashboard.html', context)

def index(request):
    '''
    week = WeekDays.objects.get(pk=4)
    dayNeed1 = week.day1.id
    print(dayNeed1)
    '''

    return render(request, 'pages/index.html')

def calendar(request):

    all_events = Events.objects.filter(user=request.user)
    meal_list =RecipeOverview.objects.all()
    context = {
        "events":all_events,
        'meal_list':meal_list,
    }   


    return render(request,'pages/calendar.html',context)

