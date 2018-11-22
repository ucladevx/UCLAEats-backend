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
    itemcodes = JSONField()
    nutrition_facts = JSONField()
    last_updated = DateField(auto_now = True, auto_now_add = True)
    
class OverviewMenu(models.Model):

    #item = ForeignKey(Item, on_delete=models.CASCADE)
    #item_id = CharField(max_length = 10)
    #location = CharField(max_length = 30)
    #dining_hall = CharField(max_length = 20)
    #dining_period = CharField(max_length = 10)
    date = DateField(auto_now = False, auto_now_add = False)
    menu = JSONField()
