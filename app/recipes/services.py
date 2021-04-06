import os
import re
from glob import glob
import json
from recipes.models import *
import requests
from random import randint
from django.db.models import Q


class SyncRecipes:

    def sync_json_from_local():
        path = 'recipes/recipe.json'
        with open(path) as f:
            data = json.load(f)
            print(path)
            print(f)
            for recipe in data: 
                try:
                    recipeExist = RecipeOverview.objects.get(url=recipe['fields']['url'])
                except: 
                    recipeExist = None 
                if not recipeExist:
                    newRecipe = RecipeOverview()
                    newRecipe.source = recipe['fields']['source']
                    newRecipe.language = recipe['fields']['language']
                    newRecipe.tags = recipe['fields']['tags']
                    newRecipe.title = recipe['fields']['title']
                    newRecipe.url = recipe['fields']['url']
                    newRecipe.image = recipe['fields']['image']
                    newRecipe.ingredients = recipe['fields']['ingredients']
                    newRecipe.directions = recipe['fields']['directions']
                    newRecipe.highProtein = recipe['fields']['highProtein']
                    newRecipe.highCarbs = recipe['fields']['highCarbs']
                    newRecipe.highFat = recipe['fields']['highFat']
                    newRecipe.highCalories = recipe['fields']['highCalories']
                    newRecipe.lowCarbs = recipe['fields']['lowCarbs']
                    newRecipe.percentCarbs = recipe['fields']['percentCarbs']
                    newRecipe.percentProtein = recipe['fields']['percentProtein']
                    newRecipe.percentFat = recipe['fields']['percentCalories']
                    newRecipe.percentCalories = recipe['fields']['percentCalories']
                    newRecipe.mealTypes = recipe['fields']['mealTypes']
                    newRecipe.cookingMins = recipe['fields']['cookingMins']
                    newRecipe.save()
                else: 
                    print('exists')
            return f





    def sync_allrecipes():
        path = 'recipes/jsonRecipes/allrecipes'
        for filename in glob(os.path.join(path, '*.json')):
            with open(filename) as currentFile:
                try:
                    data = json.load(currentFile)
                    recipeExist = RecipeOverview.objects.get(url=data['url'])
                    if recipeExist:
                        ingredients = data['ingredients']
                        ingredientList = []
                        for ingredient in ingredients:
                            ingredientList.append(ingredient)
                        recipeExist.ingredients = ingredientList
                        recipeExist.save()
                        directions = data['directions']
                        directionList = []
                        for direction in directions:
                            directionList.append(direction)
                        recipeExist.directions = directionList
                        recipeExist.save()
                        
                    else: 
                        try:
                            recipe = RecipeOverview(source=data['source'], language=data['language'], tags=data['tags'], 
                            title=data['title'], url=data['url'], image=data['image'], ingredients=data['ingredients'], directions=data['directions'])
                            recipe.save()
                        except Exception as e:
                            print(e)
                        if recipe:
                            ingredients = data['ingredients']
                            for ingredient in ingredients: 
                                newIngredient = Ingredient(recipe=recipe, description=ingredient)
                                newIngredient.save()
                            directions = data['directions']
                            for direction in directions:
                                newDirection = Direction(recipe=recipe, description=direction)
                                newDirection.save()
                            
                except Exception as e:
                    print(e)

    def sync_recipes_with_files():
        path = 'recipes/jsonRecipes/allrecipesimported'
        for filename in glob(os.path.join(path, '*.json')):
            with open(filename) as currentFile:
                try:
                    data = json.load(currentFile)
                    try:
                        recipeExist = RecipeOverview.objects.get(url=data['url'])
                    except:
                        recipeExist = None
                    if recipeExist:
                        """
                        ingredients = data['ingredients']
                        for ingredient in ingredients:
                            try:
                                ingredientExists = Ingredient.objects.get(recipe=recipeExist, description=ingredient)
                            except: 
                                ingredientExists = None
                            if ingredientExists is None:
                                newIngredient = Ingredient(recipe=recipeExist, description=ingredient)
                                newIngredient.save()
                            else: 
                                print('ingredient already exists from recipe' + str(recipeExist.id))
                        """
                        
                        """
                        directions = data['directions']
                        for direction in directions:
                            try:
                                directionExists = Direction.objects.get(recipe=recipeExist, description=direction)
                            except:
                                directionExists = None
                            
                           
                            if directionExists is None:    
                                newDirection = Direction(recipe=recipeExist, description=direction)
                                newDirection.save()
                            else:
                                print('direction exists from recipe' + str(recipeExist.id))
                        
                        """
                        """
                        directions = data['directions']
                        for direction in directions:
                            directionsExist = Direction.objects.filter(recipe=recipeExist, description=direction)
                            if directionsExist.count() > 1:
                                while directionsExist.count() > 1:
                                    for directionExist in directionsExist:
                                        directionExist.delete()
                            else:
                                print('count not greater than 1 ')
                        """
                    print('all good')
                        
                            
                except Exception as e:
                    print(e)


class Spoonacular:

    def getRecipeInfo(recipeUrl):
        apiKey = '04162bc40c7b427daaa43e35cb3fd42c'

        """Get recipe from provided URL"""
                
        recipeUrl = recipeUrl

        url = f'https://api.spoonacular.com/recipes/extract?apiKey={apiKey}'
        recipeUrl = recipeUrl
        querystring = {"url":recipeUrl, "includeNutrition":'true'}
        r = requests.request("GET", url, params=querystring)

        data = r.json()
        try: 
            nutrition = data['nutrition']

        
            data = r.json()

            nutrients = data['nutrition']['nutrients']
            nutrition = []

            for nutrient in nutrients:
                if nutrient['title'] == 'Calories':
                    calories = nutrient['amount']
                    caloriesUnit = nutrient['unit']
                    needsCalories = nutrient['percentOfDailyNeeds']
                    caloriesArray = {
                        'calories':{
                            'amount': calories,
                            'unit': caloriesUnit,
                            'percent': needsCalories
                        }
                    }
                    nutrition.append(caloriesArray)
                elif nutrient['title'] == 'Fat':
                    fat = nutrient['amount']
                    fatUnit = nutrient['unit']
                    needsFat = nutrient['percentOfDailyNeeds']
                    fatArray = {
                        'fat':{
                            'amount': fat,
                            'unit': fatUnit,
                            'percent': needsFat
                        }
                    }
                    nutrition.append(fatArray)
                elif nutrient['title'] == 'Carbohydrates':
                    carbohydrate = nutrient['amount']
                    carbUnit = nutrient['unit']
                    needsCarb = nutrient['percentOfDailyNeeds']
                    carbsArray = {
                        'carbohydrates':{
                            'amount': carbohydrate,
                            'unit': carbUnit,
                            'percent': needsCarb
                        }
                    }
                    nutrition.append(carbsArray)
                elif nutrient['title'] == 'Protein':
                    protein = nutrient['amount']
                    proteinUnit = nutrient['unit']
                    needsProtein = nutrient['percentOfDailyNeeds']
                    proteinArray = {
                        'protein':{
                            'amount': protein,
                            'unit': proteinUnit,
                            'percent': needsProtein
                        }
                    }
                    nutrition.append(proteinArray)
            try:
                completeTime = data['cookingMinutes'] + data['preparationMinutes']
            except: 
                completeTime = ""

            try: 
                dishType = data['dishTypes']
            except: 
                dishType = "" 

            additionalInfo = {
                'additionalInfo':{
                    'completeTime': completeTime,
                    'dishType': dishType
                }
            }
            nutrition.append(additionalInfo)

            print('fuck you')
            return nutrition
        except:
            return None
        

class ShoppingListManage: 
    def generate_list(start, end, name):
        meals = Events.objects.filter(start__range=[start, end])
        shoppingList = ShoppingList(start=start, end=end, name=name)
        shoppingList.save()

        for meal in meals:
            ingredients = Ingredient.objects.filter(recipe=meal.mealChosen)
            for ingredient in ingredients:
                shoppingItem = ShoppingListItem(shoppingList=shoppingList, complete=False, ingredient=ingredient)
                shoppingItem.save()
        return shoppingList

        print('complete')

class NeedsSorting:
    def needs(recipeId):
        recipe = RecipeOverview.objects.get(pk=recipeId)
        
        if recipe.percentCalories >= 30.00:
            recipe.highCalories = True
            recipe.save()
        else: 
            print('not high calories')
        
        if recipe.percentCarbs >= 25.00:
            recipe.highCarbs = True
            recipe.save()
        elif recipe.percentCarbs <= 10.00:
            recipe.lowCarbs = True
            recipe.save()
        else:
            print('normal')
        
        if recipe.percentProtein >= 25.00:
            recipe.highProtein = True
            recipe.save()



class MealPlanning:
    
    def updateRecipes():
        a_set = set()
        while True:
            a_set.add(randint(1020, 4256))
            print()
            if len(a_set) == 500:
                break
        reciepIdList = list(a_set)
       
        for recipeId in reciepIdList:
            recipe = RecipeOverview.objects.get(pk=recipeId)
            print(recipeId)
            if not recipe.percentCalories:
                recipeInfo = Spoonacular.getRecipeInfo(recipeUrl=recipe.url)
                print(recipe.id)
                print(recipeInfo)
                try:
                    recipe.cookingMins = recipeInfo[4]['additionalInfo']['completeTime']
                except:
                    print('no cooking time')
                try: 
                    recipe.mealTypes = recipeInfo[4]['additionalInfo']['dishType']
                    recipe.percentCalories = recipeInfo[0]['calories']['percent']
                    recipe.percentFat = recipeInfo[1]['fat']['percent']
                    recipe.percentCarbs = recipeInfo[2]['carbohydrates']['percent']
                    recipe.percentProtein = recipeInfo[3]['protein']['percent']
                    recipe.save()
                except:
                    print('didnt work')
                try: 
                    if recipe.percentCalories >= 30.00:
                        recipe.highCalories = True
                        recipe.save()
                    else: 
                        print('not high calories')
                    
                    if recipe.percentCarbs >= 30.00:
                        recipe.highCarbs = True
                        recipe.save()
                    elif recipe.percentCarbs <= 10.00:
                        recipe.lowCarbs = True
                        recipe.save()
                    else:
                        print('normal')
                    
                    if recipe.percentProtein >= 15.00:
                        recipe.highProtein = True
                        recipe.save()
                    else: 
                        print('not high protein')
                except:
                    print('something went wrong, moving on')
            else:
                print('already done it')

    def meal_planning(dayIntensityId, user):
        print('in the meal planning')
        dayIntensity = DayIntensity.objects.get(pk=dayIntensityId)

        if dayIntensity.intensity == dayIntensity.REST:
            print(dayIntensity.id)
            options = MealPlanning.rest_day(dayIntensity.date, user)
            return options
        elif dayIntensity.intensity == dayIntensity.EASY:
            print(dayIntensity.id)
            options = MealPlanning.easy_day(dayIntensity.date, user)
            
            return options
        elif dayIntensity.intensity == dayIntensity.WORKOUT:
            print(dayIntensity.id)
            options = MealPlanning.workout_day(dayIntensity.date, user)
            
            return options
        elif dayIntensity.intensity == dayIntensity.ALL_OUT:
            print(dayIntensity.id)
            options = MealPlanning.all_out_day(dayIntensity.date, user)
            
            return options
        else: 
            return 'nothing'

    def rest_day(date, user):
        mealsBreakfast = RecipeOverview.objects.filter((Q(title__icontains= 'Smoothie' ) & Q(cookingMins__lte=20.00)) & (Q(highProtein=True) | Q(lowCarbs=True)))
        mealsAmSnack = RecipeOverview.objects.filter(Q(cookingMins__lte=20.00) & (Q(highProtein=True) | Q(lowCarbs=True)))
        mealsLunch = RecipeOverview.objects.filter(Q(cookingMins__gte=30.00) & (Q(percentCalories__gte=20.00) & (Q(highProtein=True) | Q(lowCarbs=True))))
        mealsPmSnack = RecipeOverview.objects.filter(Q(cookingMins__lte=20.00) & Q(highProtein=True) | Q(lowCarbs=True))
        mealsDinner = RecipeOverview.objects.filter((Q(cookingMins__gte=30.00) & Q(percentCalories__gte=20.00)) & (Q(highProtein=True) | Q(lowCarbs=True)))

        #breakfast 
        length = mealsBreakfast.count()
        print(length)
        chooseInt = randint(0, (length-1))
        breakfastMeal = mealsBreakfast[chooseInt]
        mealSave = Events.objects.update_or_create(user=user, start=date, mealPosition=Events.BREAKFAST, defaults ={'mealChosen': breakfastMeal, })
        mealSave[0].save()


        #amSnack
        length = mealsAmSnack.count()
        print(length)
        chooseInt = randint(0, (length-1))
        amSnack = mealsAmSnack[chooseInt]
        mealSave = Events.objects.update_or_create(user=user, start=date, mealPosition=Events.MORNING_SNACK, defaults ={'mealChosen': amSnack, })
        mealSave[0].save()
        
        #lunch
        length = mealsLunch.count()
        print(length)
        chooseInt = randint(0, (length-1))
        lunch = mealsLunch[chooseInt]
        mealSave = Events.objects.update_or_create(user=user, start=date, mealPosition=Events.LUNCH, defaults ={'mealChosen': lunch, })
        mealSave[0].save()

        #pm snack
        length = mealsPmSnack.count()
        print(length)
        chooseInt = randint(0, (length-1))
        pmSnack = mealsPmSnack[chooseInt]
        mealSave = Events.objects.update_or_create(user=user, start=date, mealPosition=Events.AFTERNOON_SNACK, defaults ={'mealChosen': pmSnack, })
        mealSave[0].save()
        #dinner 
        length = mealsDinner.count()
        print(length)
        chooseInt = randint(0, (length-1))
        dinner = mealsDinner[chooseInt]
        mealSave = Events.objects.update_or_create(user=user, start=date, mealPosition=Events.DINNER, defaults ={'mealChosen': dinner, })
        mealSave[0].save()
        
        options = {
            'breakfast': breakfastMeal,
            'amSnack': amSnack,
            'lunch': lunch,
            'pmSnack': pmSnack,
            'dinner': dinner
        }


        return options

    def easy_day(date, user):
        mealsBreakfast = RecipeOverview.objects.filter((Q(title__icontains= 'smoothie' ) & Q(cookingMins__lte=20.00)) & (Q(highCalories=False) | Q(highProtein=True) | Q(lowCarbs=True)))
        mealsAmSnack = RecipeOverview.objects.filter(Q(cookingMins__lte=20.00) & (Q(highProtein=True) | Q(lowCarbs=True)))
        mealsLunch = RecipeOverview.objects.filter((Q(cookingMins__gte=30.00) & Q(percentCalories__gte=20.00)) & (Q(highProtein=True) | Q(lowCarbs=True)))
        mealsPmSnack = RecipeOverview.objects.filter(Q(cookingMins__lte=20.00) & Q(highProtein=True) | Q(lowCarbs=True))
        mealsDinner = RecipeOverview.objects.filter((Q(cookingMins__gte=30.00) & Q(percentCalories__gte=20.00)) & (Q(highProtein=True) | Q(lowCarbs=True)))

        #breakfast 
        length = mealsBreakfast.count()
        print(length)
        chooseInt = randint(0, (length-1))
        breakfastMeal = mealsBreakfast[chooseInt]
        mealSave = Events.objects.update_or_create(user=user, start=date, mealPosition=Events.BREAKFAST, defaults ={'mealChosen': breakfastMeal, })
        mealSave[0].save()


        #amSnack
        length = mealsAmSnack.count()
        print(length)
        chooseInt = randint(0, (length-1))
        amSnack = mealsAmSnack[chooseInt]
        mealSave = Events.objects.update_or_create(user=user, start=date, mealPosition=Events.MORNING_SNACK, defaults ={'mealChosen': amSnack, })
        mealSave[0].save()
        
        #lunch
        length = mealsLunch.count()
        print(length)
        chooseInt = randint(0, (length-1))
        lunch = mealsLunch[chooseInt]
        mealSave = Events.objects.update_or_create(user=user, start=date, mealPosition=Events.LUNCH, defaults ={'mealChosen': lunch, })
        mealSave[0].save()

        #pm snack
        length = mealsPmSnack.count()
        print(length)
        chooseInt = randint(0, (length-1))
        pmSnack = mealsPmSnack[chooseInt]
        mealSave = Events.objects.update_or_create(user=user, start=date, mealPosition=Events.AFTERNOON_SNACK, defaults ={'mealChosen': pmSnack, })
        mealSave[0].save()
        #dinner 
        length = mealsDinner.count()
        print(length)
        chooseInt = randint(0, (length-1))
        dinner = mealsDinner[chooseInt]
        mealSave = Events.objects.update_or_create(user=user, start=date, mealPosition=Events.DINNER, defaults ={'mealChosen': dinner, })
        mealSave[0].save()
        
        options = {
            'breakfast': breakfastMeal,
            'amSnack': amSnack,
            'lunch': lunch,
            'pmSnack': pmSnack,
            'dinner': dinner
        }


        return options

    def workout_day(date, user):
        mealsBreakfast = RecipeOverview.objects.filter((Q(title__icontains= 'smoothie' ) & Q(cookingMins__lte=20.00)) & (Q(highProtein=True) | Q(highCarbs=True)| Q(highCalories=True)))
        print('breakfast')
        mealsAmSnack = RecipeOverview.objects.filter(Q(cookingMins__lte=20.00) & Q(highProtein=True) | Q(highCarbs=True))
        print('am snack')
        mealsLunch = RecipeOverview.objects.filter((Q(cookingMins__gte=30.00) & Q(percentCalories__gte=20.00)) & (Q(highProtein=True) | Q(highCarbs=True)))
        print('lunch')
        mealsPmSnack = RecipeOverview.objects.filter(Q(cookingMins__lte=30.00) & (Q(highProtein=True) | Q(highCarbs=True)))
        print('pm snack')
        mealsDinner = RecipeOverview.objects.filter((Q(cookingMins__gte=30.00) & Q(percentCalories__gte=20.00)) & (Q(highProtein=True) | Q(highCarbs=True)| Q(highCalories=True)))
        print('dinner')

        #breakfast 
        length = mealsBreakfast.count()
        print(length)
        chooseInt = randint(0, (length-1))
        breakfastMeal = mealsBreakfast[chooseInt]
        mealSave = Events.objects.update_or_create(user=user, start=date, mealPosition=Events.BREAKFAST, defaults ={'mealChosen': breakfastMeal, })
        mealSave[0].save()
        print('wkout breakfast saved')

        #amSnack
        length = mealsAmSnack.count()
        print(length)
        chooseInt = randint(0, (length-1))
        amSnack = mealsAmSnack[chooseInt]
        mealSave = Events.objects.update_or_create(user=user, start=date, mealPosition=Events.MORNING_SNACK, defaults ={'mealChosen': amSnack, })
        mealSave[0].save()
        print('wkout am snack saved')
        #lunch
        length = mealsLunch.count()
        print(length)
        chooseInt = randint(0, (length-1))
        lunch = mealsLunch[chooseInt]
        mealSave = Events.objects.update_or_create(user=user, start=date, mealPosition=Events.LUNCH, defaults ={'mealChosen': lunch, })
        mealSave[0].save()
        print('wkout lunch saved')
        #pm snack
        length = mealsPmSnack.count()
        print(length)
        chooseInt = randint(0, (length-1))
        pmSnack = mealsPmSnack[chooseInt]
        mealSave = Events.objects.update_or_create(user=user, start=date, mealPosition=Events.AFTERNOON_SNACK, defaults ={'mealChosen': pmSnack, })
        mealSave[0].save()
        print(' wkout pm snack saved')
        #dinner 
        length = mealsDinner.count()
        print(length)
        chooseInt = randint(0, (length-1))
        dinner = mealsDinner[chooseInt]
        mealSave = Events.objects.update_or_create(user=user, start=date, mealPosition=Events.DINNER, defaults ={'mealChosen': dinner, })
        mealSave[0].save()
        print(' workout dinner saved')
        options = {
            'breakfast': breakfastMeal,
            'amSnack': amSnack,
            'lunch': lunch,
            'pmSnack': pmSnack,
            'dinner': dinner
        }


        return options

    def all_out_day(date, user):
        mealsBreakfast = RecipeOverview.objects.filter(Q(cookingMins__lte=30.00) & (Q(highCarbs=True)))
        mealsAmSnack = RecipeOverview.objects.filter(Q(cookingMins__lte=20.00) & (Q(highProtein=True) | Q(highCarbs=True)))
        mealsLunch = RecipeOverview.objects.filter((Q(cookingMins__gte=30.00) & Q(percentCalories__gte=20.00)) & (Q(highProtein=True) | Q(highCarbs=True)))
        mealsPmSnack = RecipeOverview.objects.filter((Q(cookingMins__lte=20.00) & Q(percentCalories__gte=15.00)) & Q(highProtein=True) | Q(highCarbs=True))
        mealsDinner = RecipeOverview.objects.filter((Q(cookingMins__gte=30.00) & Q(percentCalories__gte=20.00)) & (Q(highCarbs=True) | Q(highCalories=True)))

        #breakfast 
        length = mealsBreakfast.count()
        print(length)
        chooseInt = randint(0, (length-1))
        breakfastMeal = mealsBreakfast[chooseInt]
        mealSave = Events.objects.update_or_create(user=user, start=date, mealPosition=Events.BREAKFAST, defaults ={'mealChosen': breakfastMeal, })
        mealSave[0].save()


        #amSnack
        length = mealsAmSnack.count()
        print(length)
        chooseInt = randint(0, (length-1))
        amSnack = mealsAmSnack[chooseInt]
        mealSave = Events.objects.update_or_create(user=user, start=date, mealPosition=Events.MORNING_SNACK, defaults ={'mealChosen': amSnack, })
        mealSave[0].save()
        
        #lunch
        length = mealsLunch.count()
        print(length)
        chooseInt = randint(0, (length-1))
        lunch = mealsLunch[chooseInt]
        mealSave = Events.objects.update_or_create(user=user, start=date, mealPosition=Events.LUNCH, defaults ={'mealChosen': lunch, })
        mealSave[0].save()

        #pm snack
        length = mealsPmSnack.count()
        print(length)
        chooseInt = randint(0, (length-1))
        pmSnack = mealsPmSnack[chooseInt]
        mealSave = Events.objects.update_or_create(user=user, start=date, mealPosition=Events.AFTERNOON_SNACK, defaults ={'mealChosen': pmSnack, })
        mealSave[0].save()
        #dinner 
        length = mealsDinner.count()
        print(length)
        chooseInt = randint(0, (length-1))
        dinner = mealsDinner[chooseInt]
        mealSave = Events.objects.update_or_create(user=user, start=date, mealPosition=Events.DINNER, defaults ={'mealChosen': dinner, })
        mealSave[0].save()
        
        options = {
            'breakfast': breakfastMeal,
            'amSnack': amSnack,
            'lunch': lunch,
            'pmSnack': pmSnack,
            'dinner': dinner
        }


        return options




#MealPlanning.updateRecipes()
#SyncRecipes.sync_json()

