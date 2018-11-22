from django.db import models
from django.db.models import CharField, IntegerField, TextField, DateField, ForeignKey
from django.contrib.postgres.fields import JSONField, ArrayField

# Create your models here.

useJSONforitemcodes = False
usingPSQL = False

class Item(models.Model):

    item_id = CharField(max_length = 10)
    name = CharField(max_length = 100)
    recipe_link = CharField(max_length = 100)
    if not useJSONforitemcodes:
        itemcodes = CharField(max_length = 200)
    else:
        itemcodes = JSONField()
    
    
    if usingPSQL:
        nutrition_facts = JSONField()
    else:
        serving_size = CharField(max_length = 10)
        calories = DecimalField(max_digits = 6, decimal_places = 2)
        fat_cal = DecimalField(max_digits = 6, decimal_places = 2)
        total_fat = DecimalField(max_digits = 6, decimal_places = 2)
        total_fat_percent = DecimalField(max_digits = 6, decimal_places = 2)
        saturated_fat = DecimalField(max_digits = 6, decimal_places = 2)
        saturated_fat_percent = DecimalField(max_digits = 6, decimal_places = 2)
        trans_fat = DecimalField(max_digits = 6, decimal_places = 2)
        trans_fat_percent = DecimalField(max_digits = 6, decimal_places = 2)
        cholestrol = DecimalField(max_digits = 6, decimal_places = 2) # in milligrams
        cholestrol_percent = DecimalField(max_digits = 6, decimal_places = 2)
        sodium  = DecimalField(max_digits = 6, decimal_places = 2) # in milligrams
        sodium_percent  = DecimalField(max_digits = 6, decimal_places = 2)
        total_carbohydrate = DecimalField(max_digits = 6, decimal_places = 2)
        total_carbohydrate_percent = DecimalField(max_digits = 6, decimal_places = 2)
        dietary_fiber = DecimalField(max_digits = 6, decimal_places = 2)
        dietary_fiber_percent = DecimalField(max_digits = 6, decimal_places = 2)
        sugars = DecimalField(max_digits = 6, decimal_places = 2)
        sugars_percent = DecimalField(max_digits = 6, decimal_places = 2)
        protein = DecimalField(max_digits = 6, decimal_places = 2)
        protein_percent = DecimalField(max_digits = 6, decimal_places = 2)

        #percentages
        vitamin_a = DecimalField(max_digits = 6, decimal_places = 2)
        vitamin_c = DecimalField(max_digits = 6, decimal_places = 2)
        calcium = DecimalField(max_digits = 6, decimal_places = 2)
        iron = DecimalField(max_digits = 6, decimal_places = 2)
        
        ingredients = TextField()
        allergens = CharField(max_length = 100)

    last_updated = DateField(auto_now = True, auto_now_add = True)
    
class MenuItem(models.Model):

    item = ForeignKey(Item, on_delete=models.CASCADE)
    item_id = CharField(max_length = 10)
    location = CharField(max_length = 30)
    dining_hall = CharField(max_length = 20)
    dining_period = CharField(max_length = 10)
    date = DateField(auto_now = False, auto_now_add = False)
