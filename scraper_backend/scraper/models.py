from django.db import models
from django.contrib.postgres.fields import JSONField

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
    overviewMenu = JSONField()
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
        qs = OverviewMenu.objects.filter(menuDate=date)

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
    detailedMenu = JSONField()
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
    recipe_link = models.CharField(max_length=20)
    nutrition = JSONField(default={})
    createdAt = models.DateTimeField(auto_now=False,auto_now_add=True)
    updatedAt = models.DateTimeField(auto_now=True,auto_now_add=False)

    def __str__(self):
        return self.recipe_link
    
    @staticmethod
    def getByRecipeLink(link):
        """
        link is a python string
        """

        qs = Recipe.objects.filter(recipe_link=link).order_by("-createdAt")
        if qs.count() == 0:
            return {}
        else:
            return qs[0].nutrition


