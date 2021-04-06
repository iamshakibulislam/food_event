from django.db import models
from core.models import *

# Create your models here.

class RecipeOverview(models.Model):
    source = models.CharField(max_length=255)
    language = models.CharField(max_length=255)
    tags = models.CharField(max_length=255)
    title = models.TextField(max_length=1000)
    url = models.CharField(max_length=255, unique=True)
    image = models.CharField(max_length=255)
    ingredients = models.TextField(max_length=2500, null=True)
    directions = models.TextField(max_length=2500, null=True)

    highProtein = models.BooleanField(default=False)
    highCarbs = models.BooleanField(default=False)
    highFat = models.BooleanField(default=False)
    highCalories = models.BooleanField(default=False)
    lowCarbs = models.BooleanField(default=False)
    percentCarbs = models.FloatField(null=True)
    percentProtein = models.FloatField(null=True)
    percentFat = models.FloatField(null=True)
    percentCalories = models.FloatField(null=True)
    mealTypes = models.CharField(max_length=255, null=True)
    cookingMins = models.IntegerField(null=True)

    def __str__(self):
        return self.title
    

class Ingredient(models.Model):
    recipe = models.ForeignKey('RecipeOverview', on_delete=models.CASCADE)
    description = models.TextField(max_length=1000)

    def __str__(self):
        return self.recipe.title

class Direction(models.Model):
    recipe = models.ForeignKey('RecipeOverview', on_delete=models.CASCADE)
    description = models.TextField(max_length=1000)

    def __str__(self):
        return self.recipe.title

class Events(models.Model):
    BREAKFAST = 'breakfast'
    MORNING_SNACK = 'morning snack'
    LUNCH = 'lunch'
    AFTERNOON_SNACK = 'afternoon snack'
    DINNER = 'dinner'
    EVENING_SNACK = 'evening snack'

    MEALTYPE = [
        (BREAKFAST, ('Breakfast')),
        (MORNING_SNACK, ('Morning Snack')),
        (LUNCH, ('Lunch')),
        (AFTERNOON_SNACK, ('Afternoon Snack')),
        (DINNER, ('Dinner')),
        (EVENING_SNACK, ('Evening Snack'))
    ]
    
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=255,null=True,blank=True)
    
    start = models.DateField(null=True,blank=True)
    end = models.DateField(null=True,blank=True)
    mealPosition = models.CharField(max_length=255,
    choices=MEALTYPE, null=True)
    mealChosen = models.ForeignKey(RecipeOverview, null=True, on_delete=models.CASCADE)
    notMade = models.BooleanField(default=False)
    likedIt = models.BooleanField(default=False)
    notLiked = models.BooleanField(default=False)
    feedbackGiven = models.BooleanField(default=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE, default=1)
    

    def save(self, *args, **kwargs):
        self.end = self.start
        print('in the save')
        super(Events, self).save(*args, **kwargs)


    def __str__(self):
       return 'Event'
        

class UserInterest(models.Model):
    FAVORITE = 'Favorite'
    NOT_INTERESTED = 'Not Interested'
    MADE_IT = 'Made It'
    LOVED_IT = 'Loved It'
    INTEREST = [
        (FAVORITE, ('Favorite')), 
        (NOT_INTERESTED, ('Not Interested')),
        (MADE_IT, ('Made It')),
        (LOVED_IT, ('Love It'))
    ]
    
    user = models.ForeignKey(User, on_delete=models.CASCADE, default=1)
    recipe = models.ForeignKey(RecipeOverview, on_delete=models.CASCADE)
    interest = models.CharField(max_length=255, choices=INTEREST,
    null=True)


class ShoppingList(models.Model): 
    start = models.DateField()
    end = models.DateField()
    completed = models.BooleanField(default=False)
    name = models.CharField(max_length=255, null=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, default=1)

class ShoppingListItem(models.Model):
    shoppingList = models.ForeignKey(ShoppingList, on_delete=models.CASCADE)
    complete = models.BooleanField(default=False)
    ingredient = models.ForeignKey(Ingredient, on_delete=models.CASCADE, null=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, default=1)

class DayIntensity(models.Model):
    REST = 'rest'
    EASY = 'easy'
    WORKOUT = 'workout'
    ALL_OUT = 'all_out'
    
    STATUS = [
        (REST, ('Rest')),
        (EASY, ('Easy')),
        (WORKOUT, ('Workout')),
        (ALL_OUT, ('All_Out')),
    ]
    user = models.ForeignKey(User, on_delete=models.CASCADE, default=1)
    date = models.DateField()
    intensity = models.CharField(max_length=255, choices=STATUS)

    def __str__(self):
        return str(self.date)
