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
    overviewMenu = JSONField(default={})
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
    detailedMenu = JSONField(default={})
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

    item_id = models.CharField(max_length = 10, default = '')
    recipe_link = models.CharField(max_length=50, default = '')
    nutrition = JSONField(default=dict)
    createdAt = models.DateTimeField(auto_now=False,auto_now_add=True)
    updatedAt = models.DateTimeField(auto_now=True,auto_now_add=False)

    def __str__(self):
        return self.recipe_link
   
    
    @staticmethod
    def getNumberFromPercent(nutri):
        #print("get num from percent")
        old_number = nutri.replace('%', '')
        try:
            num_float = float(old_number)
        except:
            num_float = -1.0
        return old_number, num_float

    @staticmethod
    def getServingSizeFloat(serving_size, link):
        #print("get serving size float")
        serving_size_split_ = serving_size.split(' ')
        serving_size_frac = serving_size_split_[-1]
        serving_size_split = serving_size_frac.split('/')
        serving_size_float = -1.0
        if len(serving_size_split) == 1:
            serving_size_split.append('1')
        try:
            serving_size_float = float(serving_size_split[0]) / float(serving_size_split[1])    
        except:
            print("Invalid serving size in recipe link: {}".format(str(serving_size)))
            serving_size_float = -1.0
        if not serving_size_float == -1.0 and len(serving_size_split_) > 1:
            try:
                serving_size_float += float(serving_size_split_[0])
            except:
                print("Invalid serving size in recipe link. {}".format(str(serving_size)))
                serving_size_float = -1.0
        return serving_size_float

    @staticmethod
    def getNumberFromServingSize(nutri,compound = False):
        #print("get num from serving size")
        if not compound:
            old_number = nutri.replace('\xa0', ' ').split(' ')[2]
        else:
            val_list = nutri.replace('\xa0', ' ').split(' ')
            old_number = ' '.join(val_list[2:4])
            
        old_number_float = Recipe.getServingSizeFloat(old_number, None)
        return old_number, old_number_float

    @staticmethod
    def getNumbersFromPair(nutri):
        #print("get num from pair")
        num = nutri[0]
        percent = nutri[1]
        if 'mg' in num:
            old_num = num.replace('mg', '')
        else:
            old_num = num.replace('g','')

        try:
            num_float =  float(old_num)
        except:
            print("Exception getting number from pair: " + str(nutri[0]) + " " + str(nutri[1]))
            num_float = -1.0

        old_percent = percent.replace('%', '')
        try:
            percent_float = float(old_percent)
        except:
            print("Exception getting number from pair: " + str(nutri[0]) + " " + str(nutri[1]))
            percent_float = -1.0
        return old_num, old_percent, num_float, percent_float

    @classmethod
    def insert_or_update(cls, recipe_link, nutrition):

        #Note: As of now, calling this function modifies the original nutrition dictionary as well
        # i.e., the passed-in nutrition dict gets modified outside of this function too
        #use the dict() function to create a copy as below, renaming the function argument to nutri
        #nutrition = dict(nutri)  --> this ensures a copy is used, so the original will not change

        link_arr = recipe_link.split('/')
        item_id = link_arr[-2]
        serving_size = link_arr[-1]

        #### LOOK AT COMMENTS IN getRecipeByLink() TO UNDERSTAND THE USAGE OF serving_size_frac AND compound ####

        #serving_size_frac = None
        compound = False
        if len(serving_size.split('!')) > 1:
            if len(serving_size.split('_')) > 1:
                compound = True
            serving_size = serving_size.replace('!', '/').replace('_', ' ')
        serving_size_float = Recipe.getServingSizeFloat(serving_size, recipe_link)

        if serving_size_float == -1.0:
            #print("Returning without inserting")
            return
        link_arr[-1] = '1'
        recipe_link = '/'.join(link_arr)

        nutrition = Recipe.scale_nutrition_by_serving_size(dict(nutrition), serving_size_float, scale_up = False, compound=compound)

        qs = cls.objects.filter(item_id=item_id)
        if qs.count() > 1:
            print("Error in DB, more than one recipe for same item: " + item_id)
        elif qs.count() == 0:
            Recipe.objects.create(item_id = item_id, recipe_link=recipe_link, nutrition=nutrition)
        else:
            qs.update(nutrition=nutrition)
        #print("Returning normally from insert update")
        return

    @staticmethod
    def scale_num(num, serving_size, scale_up, make_int):
        print("scale num " + str(make_int))
        if num != -1:
            if(scale_up):
                if(make_int):
                    num = int(round(num * serving_size, 0))
                else:
                    num = round(num * serving_size, 1)
                    if(num.is_integer()):
                        num = int(num)
            else:
                num = float(num) / serving_size
        return num

    @staticmethod
    def scale_nutrition_by_serving_size(nutrition, serving_size, scale_up = True, serving_size_frac_repl = None, compound = False):
        #print("Inside scale by nutri")
        nutri = dict(nutrition)
        for key, value in nutrition.items():

            if type(value) == str:
                if key == 'serving_size':
                    old_number,num_float = Recipe.getNumberFromServingSize(value, compound=compound)
                    if not serving_size_frac_repl == None:
                        nutri[key] = value.replace(old_number, serving_size_frac_repl)
                        continue
                elif key not in ['ingredients', 'allergens']:
                    old_number, num_float = Recipe.getNumberFromPercent(value)
                else:
                    num_float = -1.0

                if not num_float == -1.0:
                    num = Recipe.scale_num(num_float, serving_size, scale_up=scale_up, make_int=True)
                    nutri[key] = value.replace(old_number, str(num))

            elif type(value) == list:
                old_num, old_percent, num_float, percent_float = Recipe.getNumbersFromPair(value)              
                if not num_float == -1:
                    num = Recipe.scale_num(num_float, serving_size, scale_up=scale_up, make_int=False)
                    val0 = value[0].replace(old_num, str(num))
                else:
                    val0 = value[0]

                if not percent_float == -1.0:
                    perc = Recipe.scale_num(percent_float, serving_size, scale_up=scale_up, make_int=True)
                    #print(str(perc) + "  " + str(percent_float))
                    val1 = value[1].replace(old_percent, str(perc))
                else:
                    val1 = value[1]

                nutri[key] = [val0, val1]
        return nutri

    @staticmethod
    def getByRecipeLink(link):
        """
        link is a python string
        """
        print("Inside get by recipe link: " + str(link))
        link_arr = link.split('/')

        serving_size = link_arr[-1]

        #### USAGE OF serving_size_frac AND compound ####
        """
        # serving_size_frac is not None IFF the resultant nutrition dict
        # needs to have a "serving size" field with a compound number. 
        # this is the case ONLY when we are GETTING data from the DB, and even then only sometimes
        # compound is True IFF the INPUT nutrition dict (i.e., not the resultant)
        # has a compound number for serving size. This is NEVER the case when GETTING from the DB
        # as serving size is always set to 1.0 in the DB.
        # """

        serving_size_frac = None
        compound = False

        # assumption that serving size is compound only if there is a ! in it
        if len(serving_size.split('!')) > 1:
            serving_size_frac = serving_size.replace('!', '/').replace('_', ' ')
            serving_size = serving_size_frac
        serving_size_float = Recipe.getServingSizeFloat(serving_size, link)        
        
        if serving_size_float == -1.0:
            serving_size_float = 1.0
        item_id = link_arr[-2]
        qs = Recipe.objects.filter(item_id=item_id)
        if qs.count() == 0:
            return None
        if qs.count() > 1:
            print("Error is recipe database, too many recipes for same item")

        nutrition = qs[0].nutrition
        nutrition = Recipe.scale_nutrition_by_serving_size(nutrition, serving_size_float, serving_size_frac_repl=serving_size_frac, compound=compound)
        #print("Returning nutrition")
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
