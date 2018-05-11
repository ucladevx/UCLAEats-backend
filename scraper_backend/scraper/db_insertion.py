from .util.scrape import *
from .models import *
from datetime import date

days_to_scrape = 7

def insert_activity_level():
    activity_level = scraper_for_activity_level()
    ActivityLevel.objects.create(level=activity_level)

def insert_hours():
    def insert_hour(hour_date):
        """
        date is a string: YYYY-MM-DD
        """
        hour = scraper_for_hours(hour_date)
        scraped_hour_date_arr = hour["hourDate"].split("-")
        scraped_hour_date = date(int(scraped_hour_date_arr[0]),int(scraped_hour_date_arr[1]),int(scraped_hour_date_arr[2]))
        scraped_hours = hour["hours"]

        obj = Hour.objects.filter(hourDate=scraped_hour_date).order_by("-updatedAt")

        if obj.count() == 0:
            Hour.objects.create(hourDate=scraped_hour_date,hours=scraped_hours)
        elif obj.count() == 1:
            obj.update(hours=scraped_hours)
        else:
            # in this case, there is some error
            print("Error in hour")
            obj.update(hours=scraped_hours)

    for i in range(0,days_to_scrape):
        date_to_scrape = (date.today() + timedelta(i)).isoformat()
        insert_hour(date_to_scrape)



def insert_overview_menu():
    overview_menus = multi_thread_menu_scraper(days_to_scrape,scraper_for_day_overview)
    for menu in overview_menus["menus"]:
        scraped_menu_date_arr = menu["menuDate"].split("-")
        if len(scraped_menu_date_arr) != 3:
            print("Error in insert_overview_menu: date format is not correct")
        scraped_menu_date = date(int(scraped_menu_date_arr[0]),int(scraped_menu_date_arr[1]),int(scraped_menu_date_arr[2]))
        scraped_overview_menu = menu["overviewMenu"]

        obj = OverviewMenu.objects.filter(menuDate=scraped_menu_date).order_by("-updatedAt")

        # this menu is for a new date
        if obj.count() == 0:
            OverviewMenu.objects.create(menuDate=scraped_menu_date,overviewMenu=scraped_overview_menu)
        elif obj.count() == 1:
            # update the menu anyway; if they are the same, no harm; if not, it needs to be updated
            obj.update(overviewMenu=scraped_overview_menu)
        else:
            # in this case, there is some error
            print("Error in overviewMenu")
            obj.update(overviewMenu=scraped_overview_menu)

def insert_detailed_menu_and_recipe():
    detailed_menus = multi_thread_menu_scraper(days_to_scrape,scraper_for_day_detail)
    for menu in detailed_menus["menus"]:
        scraped_menu_date_arr = menu["menuDate"].split("-")
        if len(scraped_menu_date_arr) != 3:
            print("Error in insert_detailed_menu: date format is not correct")
        scraped_menu_date = date(int(scraped_menu_date_arr[0]),int(scraped_menu_date_arr[1]),int(scraped_menu_date_arr[2]))
        scraped_detailed_menu = menu["detailedMenu"]

        obj = DetailedMenu.objects.filter(menuDate=scraped_menu_date).order_by("-updatedAt")

        # this menu is for a new date
        if obj.count() == 0:
            DetailedMenu.objects.create(menuDate=scraped_menu_date,detailedMenu=scraped_detailed_menu)
        elif obj.count() == 1:
            # update the menu anyway; if they are the same, no harm; if not, it needs to be updated
            obj.update(detailedMenu=scraped_detailed_menu)
        else:
            # in this case, there is some error
            print("Error in overviewMenu")
            obj.update(detailedMenu=scraped_detailed_menu)

        # insert into recipe table
        for meal_name, meal_dict in scraped_detailed_menu.items():
            for dining_hall_name, item_dict in meal_dict.items():
                for section_name, dishes_arr in item_dict.items():
                    for dish in dishes_arr:
                        recipe_link_arr = dish["recipe_link"].split("/")
                        scraped_recipe_link = recipe_link_arr[-2] + "/" + recipe_link_arr[-1]
                        scraped_nutrition = dish["nutrition"]

                        obj = Recipe.objects.filter(recipe_link=scraped_recipe_link).order_by("-updatedAt")

                        if obj.count() == 0:
                            Recipe.objects.create(recipe_link=scraped_recipe_link,nutrition=scraped_nutrition)
                        elif obj.count() == 1:
                            # update the menu anyway; if they are the same, no harm; if not, it needs to be updated
                            obj.update(nutrition=scraped_nutrition)
                        else:
                            # in this case, there is some error
                            print("Error in recipe")
                            obj.update(nutrition=scraped_nutrition)                                               



