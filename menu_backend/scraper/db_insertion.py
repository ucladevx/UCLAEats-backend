from .scrape import *
from .models import *
from datetime import date
from .scraper_thread import Scraper_thread

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

def parse_date(date_str):
    date_arr = date_str.split("-")
    if len(date_arr) != 3:
        return None

    return date(int(date_arr[0]),int(date_arr[1]),int(date_arr[2]))

def execute_thread(func):
    menu_dict = {}

    s = Scraper_thread(func, menu_dict)
    s.start()
    s.join()

    return menu_dict

def insert_slow_scrape():
    menu_dict = execute_thread(slow_scrape)

    insert_detailed_menu(menu_dict['detailed'])
    insert_overview_menu(menu_dict['overview'])

def insert_hourly_scrape():
    menu_dict = execute_thread(hourly_scrape)

    for detailed_menu in menu_dict['detailed']:
        insert_detailed_menu(detailed_menu)

    for overview_menu in menu_dict['overview']:
        insert_overview_menu(overview_menu)

def insert_overview_menu(menu):
    menu_date = parse_date(menu["menuDate"])

    if not menu_date:
        print("Error in insert_detailed_menu_and_recipe: invalid date format")

    overview_menu = menu["overviewMenu"]

    obj = OverviewMenu.objects.filter(menuDate=menu_date).order_by("-updatedAt")

    # this menu is for a new date
    if obj.count() == 0:
        OverviewMenu.objects.create(menuDate=menu_date,overviewMenu=overview_menu)
    elif obj.count() == 1:
        # update the menu anyway; if they are the same, no harm; if not, it needs to be updated
        obj.update(overviewMenu=overview_menu)
    else:
        # in this case, there is some error
        print("Error in overviewMenu")
        obj.update(overviewMenu=overview_menu)

def insert_detailed_menu(menu):
    menu_date = parse_date(menu["menuDate"])

    if not menu_date:
        print("Error in insert_detailed_menu_and_recipe: invalid date format")

    detailed_menu = menu["detailedMenu"]

    obj = DetailedMenu.objects.filter(menuDate=menu_date).order_by("-updatedAt")

    # this menu is for a new date
    if obj.count() == 0:
        DetailedMenu.objects.create(menuDate=menu_date,detailedMenu=detailed_menu)
    elif obj.count() == 1:
        # update the menu anyway; if they are the same, no harm; if not, it needs to be updated
        obj.update(detailedMenu=detailed_menu)
    else:
        # in this case, there is some error
        print("Error in overviewMenu")
        obj.update(detailedMenu=detailed_menu)

    """
    # insert into recipe table
    for meal_name, meal_dict in detailed_menu.items():
        for dining_hall_name, item_dict in meal_dict.items():
            for section_name, dishes_arr in item_dict.items():
                for dish in dishes_arr:
                    insert_recipe(dish)
    """

"""
def insert_recipe(dish):
    recipe_link_arr = dish["recipe_link"].split("/")
    scraped_recipe_link = recipe_link_arr[-2] + "/" + recipe_link_arr[-1]
    scraped_nutrition = dish["nutrition"]
    Recipe.insert_or_update(recipe_link=scraped_recipe_link, nutrition=scraped_nutrition)
"""
