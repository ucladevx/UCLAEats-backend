from django.db import models
from django.contrib.postgres.fields import JSONField
import operator

# Create your models here.
class ActivityLevel(models.Model):
    level = JSONField(default={})
    createdAt = models.DateTimeField(auto_now=False,auto_now_add=True)
    updatedAt = models.DateTimeField(auto_now=True,auto_now_add=False)

    # get the activity level
    def getActivityLevel(self):
        return self.level

    @staticmethod
    def getLast():
        # TODO: check whether return type is a json or a dict
        try:
            obj = ActivityLevel.objects.latest("createdAt")
            return obj.level
        except DoesNotExist:
            return {}

class OverviewMenu(models.Model):
    overviewMenu = JSONField(default=dict)
    createdAt = models.DateTimeField(auto_now=False,auto_now_add=True)
    updatedAt = models.DateTimeField(auto_now=True,auto_now_add=False)
    menuDate = models.DateField()

    def __str__(self):
        return "menu: " + self.menuDate.isoformat()

    @staticmethod
    def getByDate(date):
        """
        date is a python datetime.date object
        """
        qs = OverviewMenu.objects.filter(menuDate=date).order_by("-createdAt")

        if qs.count() == 0:
            return {}
        else:
            # format date to YYYY-MM-DD
            date_str = qs[0].menuDate.isoformat()
            return {
                "menuDate": date_str,
                "overviewMenu": qs[0].overviewMenu
            }
    
    @staticmethod
    def getByDateRange(startDate,endDate):
        """
        startDate and endDate are python datetime.date objects
        startDate is inclusive and endDate is inclusivw
        """
        menu_arr = []

        # filter by range of date
        qs = OverviewMenu.objects.filter(menuDate__range=[startDate,endDate]).order_by("menuDate")

        if qs.count == 0:
            return menu_arr
        else:
            for q in qs:
                # exclude the createdAt and updatedAt
                menu_arr.append({
                    "menuDate": q.menuDate.isoformat(),
                    "overviewMenu": q.overviewMenu                    
                })
            
            return menu_arr
        
class DetailedMenu(models.Model):
    detailedMenu = JSONField(default=dict)
    createdAt = models.DateTimeField(auto_now=False,auto_now_add=True)
    updatedAt = models.DateTimeField(auto_now=True,auto_now_add=False)
    menuDate = models.DateField()

    def __str__(self):
        return "menu: " + self.menuDate.isoformat()

    @staticmethod
    def getByDate(date):
        """
        date is a python datetime.date object
        """
        qs = DetailedMenu.objects.filter(menuDate=date)

        if qs.count() == 0:
            return {}
        else:
            # format date to YYYY-MM-DD
            date_str = qs[0].menuDate.isoformat()
            return {
                "menuDate": date_str,
                "overviewMenu": qs[0].detailedMenu
            }
    
    @staticmethod
    def getByDateRange(startDate,endDate):
        """
        startDate and endDate are python datetime.date objects
        startDate is inclusive and endDate is inclusivw
        """
        menu_arr = []

        # filter by range of date
        qs = DetailedMenu.objects.filter(menuDate__range=[startDate,endDate]).order_by("menuDate")

        if qs.count == 0:
            return menu_arr
        else:
            for q in qs:
                # exclude the createdAt and updatedAt
                menu_arr.append({
                    "menuDate": q.menuDate.isoformat(),
                    "detailedMenu": q.detailedMenu                    
                })
            
            return menu_arr

class Recipe(models.Model):

    item_id = models.CharField(max_length = 10)
    recipe_link = models.CharField(max_length=50)
    nutrition = JSONField(default=dict)
    createdAt = models.DateTimeField(auto_now=False,auto_now_add=True)
    updatedAt = models.DateTimeField(auto_now=True,auto_now_add=False)

    def __str__(self):
        return self.recipe_link

    @staticmethod
    def getNumberFromPercent(nutri):
        old_number = nutri.replace('%', '')
        try:
            num_float = float(old_number)
        except:
            num_float = -1
        return old_number, num_float

    @staticmethod
    def getNumberFromServingSize(nutri):
        old_number = nutri.replace('\xa0', ' ').split(' ')[2]
        try:
            num_float = float(old_number)
        except:
            num_float = -1
        
        return old_number, num_float

    @staticmethod
    def getNumbersFromPair(nutri):
        num = nutri[0]
        percent = nutri[1]
        if 'mg' in num:
            old_num = num.replace('mg', '')
        else:
            old_num = num.replace('g','')

        try:
            num_float =  float(old_num)
        except:
            num_float = -1
        
        old_percent = percent.replace('%', '')
        try:
            percent_float = float(old_percent)
        except:
            percent_float = -1
        return old_num, old_percent, num_float, percent_float

    @classmethod
    def insert_or_update(cls, recipe_link, nutrition):

        link_arr = recipe_link.split('/')
        item_id = link_arr[-2]
        serving_size = link_arr[-1]
        try:
            serving_size = int(serving_size)
        except:
            print("Invalid recipe link, serving size must be an int: " + recipe_link)
            return
        link_arr[-1] = '1'
        recipe_link = '/'.join(link_arr)
        
        nutrition = Recipe.scale_nutrition_by_serving_size(nutrition, serving_size, scale_up = False)

        qs = cls.objects.filter(item_id=item_id)
        if qs.count() > 1:
            print("Error in DB, more than one recipe for same item: " + item_id)
        elif qs.count() == 0:
            Recipe.objects.create(item_id = item_id, recipe_link=recipe_link, nutrition=nutrition)
        else:
            qs.update(nutrition=nutrition)
        return

    @staticmethod
    def scale_nutrition_by_serving_size(nutrition, serving_size, scale_up = True):

        #op = operator.mul if scale_up else operator.truediv
        for key, value in nutrition.items():
            
            if type(value) == str:
                if key == 'serving_size':
                    old_number,num_float = Recipe.getNumberFromServingSize(value)
                    
                    #print(old_number + "  " + str(num_float))
                elif key not in ['ingredients', 'allergens']:
                    old_number, num_float = Recipe.getNumberFromPercent(value)
                    #print(key + " "+ value + " " + old_number + " " + str(num_float))
                else:
                    num_float = -1

                if num_float != -1:
                    if(scale_up):
                        num_float = int(round(num_float * serving_size, 0))
                        #if(num.is_integer()):
                        #    tmp = int(num)
                        #else:
                        #    num = round(num, 2)
                        #num_float = num
                    else:
                        num_float = num_float / serving_size
                        
                    #if key != 'serving_size':
                    nutrition[key] = value.replace(old_number, str(num_float))
                    #else:
                        #split_by_space = value.split(' ')
                        #print(split_by_space[0])
                        #replaced = split_by_space[0].replace(old_number,str(num_float))
                        #nutrition[key] = ' '.join(replaced, '\\x0a', split_by_space[1])
                        
                        
                    
            elif type(value == list):
                old_num, old_percent, num_float, percent_float = Recipe.getNumbersFromPair(value)
                if num_float != -1:
                    if(scale_up):
                        num = round(num_float * serving_size,2)
                        perc = int(round(percent_float * serving_size,0))
                        if(num.is_integer()):
                            num = int(num)
                        #else:
                        #    num = round(num, 2)
                        #if(perc.is_integer()):
                        #    perc = int(perc)
                        #else:
                        #    perc = round(perc, 2)
                        num_float = num
                        percent_float = perc
                    else:
                        num_float = num_float / serving_size
                        percent_float = percent_float / serving_size
                    val0 = value[0].replace(old_num, str(num_float))
                    val1 = value[1].replace(old_percent, str(percent_float))
                else:
                    val0 = value[0]
                    val1 = value[1]
                
                nutrition[key] = [val0, val1]
                
        return nutrition
        
    @staticmethod
    def getByRecipeLink(link):
        """
        link is a python string
        """
        
        link_arr = link.split('/')
        serving_size = link_arr[-1]
        item_id = link_arr[-2]
        try:
            serving_size = int(serving_size)
        except:
            print("Invalid serving size in recipe link")

        qs = Recipe.objects.filter(item_id=item_id)
        if qs.count() == 0:
            return None
        if qs.count() > 1:
            print("Error is recipe database, too many recipes for same item")

        nutrition = qs[0].nutrition
        nutrition = Recipe.scale_nutrition_by_serving_size(nutrition, serving_size)
        return nutrition
    
class Hour(models.Model):
    hours = JSONField()
    hourDate = models.DateField()
    createdAt = models.DateTimeField(auto_now=False,auto_now_add=True)
    updatedAt = models.DateTimeField(auto_now=True,auto_now_add=False)

    def __str__(self):
        return self.hourDate.isoformat()

    @staticmethod
    def getByDateRange(startDate,endDate):
        """
        startDate and endDate are python datetime.date objects
        startDate is inclusive and endDate is inclusivw
        """
        hour_arr = []

        # filter by range of date
        qs = Hour.objects.filter(hourDate__range=[startDate,endDate]).order_by("hourDate")

        if qs.count == 0:
            return hour_arr
        else:
            for q in qs:
                # exclude the createdAt and updatedAt
                hour_arr.append({
                    "hourDate": q.hourDate.isoformat(),
                    "hours": q.hours
                })
            
            return hour_arr

