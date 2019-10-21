import requests
from bs4 import BeautifulSoup
from bs4 import element
from .scraper_thread import Scraper_thread
from datetime import date,timedelta
import datetime
import re
import json
import time
from .models import *
# utility function for getting next_sibling and igore new line
def get_next_sibling(element):
    sibling = element.next_sibling
    if sibling == "\n":
        return get_next_sibling(sibling)
    else:
        return sibling

def get_prev_sibling(element):
    sibling = element.previous_sibling
    if sibling == "\n":
        return get_prev_sibling(sibling)
    else:
        return sibling

def legend_to_sentence(soup):
    dic = {}

    for div in soup.find_all("div",class_="fp-legend-item"):
        code = div.find("img")["alt"]
        sentence = get_next_sibling(div.find("img")).string.strip()
        dic[code] = sentence

    return dic

def scraper_for_activity_level():
    url = "http://menu.dining.ucla.edu/Menus"
    soup = BeautifulSoup(requests.get(url).text,"lxml")
    activity_level = {
        "Covel": "-1",
        "De Neve": "-1",
        "FEAST at Rieber": "-1",
        "Bruin Plate": "-1"
    }

    for span_activity_level_wrapper in soup.find_all("span",class_="activity-level-wrapper"):
        percentage = get_next_sibling(span_activity_level_wrapper).string.strip()
        dining_hall_name = get_prev_sibling(span_activity_level_wrapper.parent).string.strip()
        activity_level[dining_hall_name] = percentage

    return activity_level

def scraper_for_hours(date):
    """
    date
    """
    url = "http://menu.dining.ucla.edu/Hours" + "/" + date
    hours = {
        "hourDate": date.strip(),
        "hours":[]
    }

    soup = BeautifulSoup(requests.get(url).text,"lxml")
    hour_table = soup.find("table",class_="hours-table")
    if hour_table == None:
        return hours
    elif hour_table.find("tbody") == None:
        return hours
    else:
        header_order_dict = {}
        counter = 0
        # header
        for tr in hour_table.find("thead"):
            for td in tr.find_all("th"):
                if td.string.strip() == "":
                    header_order_dict[str(counter)] = "hall_name"
                else:
                    title = td.string.strip().lower()
                    if "/" in title:
                        header_order_dict[str(counter)] = title.split("/")[0]
                    elif " " in title:
                        header_order_dict[str(counter)] = title.replace(" ","_")
                    else:
                        header_order_dict[str(counter)] = title

                counter = counter + 1

        # data
        for tr in hour_table.find("tbody").find_all("tr"):
            counter = 0
            dining_hall_dict = {}
            for td in tr.find_all("td"):
                if td.find("span") != None:
                    dining_hall_dict[header_order_dict[str(counter)]] = td.find("span").string.strip()
                else:
                    dining_hall_dict[header_order_dict[str(counter)]] = td.string.strip()

                counter = counter + 1

            hours["hours"].append(dining_hall_dict)

        return hours

def scrape_nutrition(recipe_link):
    # print("scraping nutrition")
    soup = BeautifulSoup(requests.get(recipe_link).text,"lxml")

    nutrition = {}
    if soup.find("div",class_="nfbox") == None:
        return nutrition

    # each p gives a piece of information about recipe
    for p in soup.find("div",class_="nfbox").children:
        if type(p) == element.NavigableString:
            continue

        if "nftitle" in p["class"] or "nfdvhdr" in p["class"] or "nfvitbar" in p["class"]:
            continue

        #serving_size
        if "nfserv" in p["class"]:
            nutrition["serving_size"] = p.string.strip()
        #Fat_Cal.
        elif "nfcal" in p["class"]:
            nutrition["Calories"] = get_next_sibling(p.find("span",class_="nfcaltxt")).string.strip()
            arr = p.find("span",class_="nffatcal").string.strip().split()
            if len(arr) != 3:
                nutrition["Fat_Cal."] = "-1"
            else:
                nutrition["Fat_Cal."] = arr[-1]
        #nutrient
        elif "nfnutrient" in p["class"]:
            # get the nutrition_name
            nutrition_name = "_".join(p.find("span",class_="nfmajornutrient").string.strip().split())
            nutrition[nutrition_name] = []
            # the mass
            nutrition[nutrition_name].append(get_next_sibling(p.find("span",class_="nfmajornutrient")).string.strip())
            # percentage
            if p.find("span",class_="nfdvvalnum") != None:
                nutrition[nutrition_name].append(p.find("span",class_="nfdvvalnum").string.strip() + "%")
            else:
                nutrition[nutrition_name].append("-1")
        elif "nfindent" in p["class"]:
            for p_nfnutrient in p.find_all("p",class_="nfnutrient"):
                # means we have a percentage
                if p_nfnutrient.find("span",class_="nfdvvalnum") != None:
                    # get the text that's under p_nfnutrient tag
                    nutrition_name = "_".join(get_prev_sibling(p_nfnutrient.find("span",class_="nfdvval")).string.strip().split()[:-1])
                    nutrition[nutrition_name] = []
                    # the mass
                    nutrition[nutrition_name].append(get_prev_sibling(p_nfnutrient.find("span",class_="nfdvval")).string.strip().split()[-1])
                    # percentage
                    nutrition[nutrition_name].append(p_nfnutrient.find("span",class_="nfdvvalnum").string.strip() + "%")
                else:
                    # means we do not have a percentage
                    nutrition_name = "_".join(p_nfnutrient.string.strip().split()[:-1])
                    nutrition[nutrition_name] = []
                    # the mass
                    nutrition[nutrition_name].append(p_nfnutrient.string.strip().split()[-1])
                    # the percentage
                    nutrition[nutrition_name].append("-1")
        elif "nfvit" in p["class"]:
            for vitamin_name_span in p.find_all("span",class_="nfvitname"):
                vitamin_name = vitamin_name_span.string.strip()
                next_span = get_next_sibling(vitamin_name_span)
                if next_span != None and next_span.has_attr("class") and "nfvitpct" in next_span["class"]:
                    nutrition[vitamin_name] = next_span.string.strip()
                else:
                    nutrition[vitamin_name] = "-1"

    # for ingredients and allergens
    if soup.find("div",class_="ingred_allergen") != None:
        for p in soup.find("div",class_="ingred_allergen").children:
            if type(p) != element.NavigableString and get_next_sibling(p.find("strong")) != None:
                name = p.find("strong").string.strip().lower().split(":")[0]
                text = get_next_sibling(p.find("strong")).string.strip()
                nutrition[name] = text
    else:
        nutrition["ingredients"] = ""
        nutrition["allergens"] = ""

    return nutrition

def get_nutrition(recipe_link, update_recipes):
    if update_recipes:
        try:
            nutrition = scrape_nutrition(recipe_link)
            Recipe.insert_or_update(recipe_link, nutrition)
        except Exception as e:
            print("**********ERROR AT RECIPLE LINK********: " + recipe_link)
            print(e)
            nutrition = Recipe.getByRecipeLink(recipe_link)      
    else:
        nutrition = Recipe.getByRecipeLink(recipe_link)
        if not nutrition:
            try:
                nutrition = scrape_nutrition(recipe_link)
                Recipe.insert_or_update(recipe_link, nutrition)
            except Exception as e:
                print("**********ERROR AT RECIPLE LINK********: " + recipe_link)
                print(e)            

    return nutrition

def parse_dining_hall_section(dining_hall_section_block, itemcode_dict, update_recipes):
    menu_items = []

    for li_menu_item in dining_hall_section_block.find("ul",class_="item-list").children:
        if type(li_menu_item) == element.NavigableString:
            continue

        item_name = li_menu_item.find("a").string.strip()

        itemcodes = {}
        for img_icon in li_menu_item.find_all("img"):
            itemcodes[img_icon["alt"]] = itemcode_dict[img_icon["alt"]]

        recipe_link = li_menu_item.find("a")["href"]

        if(update_recipes):
            time.sleep(1)

        nutrition = get_nutrition(recipe_link, update_recipes)

        menu_items.append({
            "name": item_name,
            "recipe_link": recipe_link,
            "itemcodes": itemcodes,
            "nutrition": nutrition
        })

    return menu_items

def parse_menu(menu_block_div, itemcode_dict, update_recipes):

    dining_hall_menu = {}

    # dining_hall_section_block is <li class="sect-item"></li>
    for dining_hall_section_block in menu_block_div.find("ul",class_="sect-list").children:
        if type(dining_hall_section_block) == element.NavigableString:
            continue

        # get section name
        dining_hall_section_name = ""
        for s in dining_hall_section_block.stripped_strings:
            if s.strip() != "":
                dining_hall_section_name = s.strip()
                break

        dining_hall_menu[dining_hall_section_name] = parse_dining_hall_section(dining_hall_section_block, itemcode_dict, update_recipes)

    return dining_hall_menu

def parse_meal_header(meal_header, is_weekend=False):
    meal_name_list = meal_header.string.lower().strip().split(" ")
    if len(meal_name_list) == 0:
        return None
    elif meal_name_list[0] != "breakfast" and meal_name_list[0] != "brunch" \
            and meal_name_list[0] != "lunch" and meal_name_list[0] != "dinner":
        return None
    elif meal_name_list[0] == "lunch" and is_weekend:
        return "brunch"
    else:
        #meal_name: breakfast, brunch, lunch, etc
        return meal_name_list[0]

def scraper_for_day_overview(menu_date, update_recipes):

    menu_dict = {
        "menuDate": menu_date.strip(),
        "overviewMenu": {}
    }

    overview_menu = {}

    url = "http://menu.dining.ucla.edu/Menus/" + menu_date
    soup = BeautifulSoup(requests.get(url).text,"lxml")

    # matches the itemcode to sentence description
    # ex: V: vegetarian menu option
    itemcode_dict = legend_to_sentence(soup)

    for meal_header in soup.find_all("h2",id="page-header"):
        meal_name = parse_meal_header(meal_header)

        if not meal_name:
            return menu_dict

        overview_menu[meal_name] = {}

        menu_block_div = get_next_sibling(meal_header)

        while get_next_sibling(menu_block_div).has_attr("class") and "menu-block" in get_next_sibling(menu_block_div)["class"]:
            # menu-block div
            menu_block_div = get_next_sibling(menu_block_div)
            # dining_hall_name
            dining_hall_name = menu_block_div.find("h3").string
            #print(dining_hall_name)

            overview_menu[meal_name][dining_hall_name] = parse_menu(menu_block_div, itemcode_dict, update_recipes)

    menu_dict["overviewMenu"] = overview_menu
    return menu_dict

def scraper_for_day_detail(menu_date, update_recipes):
    menu_dict = {
        "menuDate": menu_date.strip(), # date is a string like 2018-04-21
        "detailedMenu": {}
    }

    # date.weekday() returns number from 0 - 6, 5 and 6 are sat/sunday
    is_weekend = datetime.datetime.strptime(menu_date, '%Y-%m-%d').date().weekday() > 4

    detailed_menu = {}

    meal_list = ["Breakfast","Lunch","Dinner"]

    for meal in meal_list:
        url = "http://menu.dining.ucla.edu/Menus/" + menu_date + "/" + meal
        soup = BeautifulSoup(requests.get(url).text,"lxml")

        # matches the itemcode to sentence description
        # ex: V: vegetarian menu option
        itemcode_dict = legend_to_sentence(soup)

        #ex: BREAKFAST MENU FOR TODAY, NOVEMBER 15, 2018
        for meal_header in soup.find_all("h2",id="page-header"):

            meal_name = parse_meal_header(meal_header, is_weekend)

            if not meal_name:
                return menu_dict

            detailed_menu[meal_name] = {}

            menu_block_div = meal_header

            while get_next_sibling(menu_block_div).has_attr("class") and "menu-block" in get_next_sibling(menu_block_div)["class"]:
                # one menu-block per dining hall
                menu_block_div = get_next_sibling(menu_block_div)

                dining_hall_name = menu_block_div.find("h3").string
                #print(dining_hall_name)

                detailed_menu[meal_name][dining_hall_name] = parse_menu(menu_block_div, itemcode_dict, update_recipes)

    menu_dict["detailedMenu"] = detailed_menu

    return menu_dict

def slow_scrape():
    date_str = (date.today() + timedelta(7)).isoformat()
    menu_dict = {}
    menu_dict['detailed'] = scraper_for_day_detail(date_str, update_recipes=True)
    menu_dict['overview'] = scraper_for_day_overview(date_str, update_recipes=True)
    return menu_dict

def hourly_scrape():
    menu_dict = {
        'detailed': [],
        'overview': []
    }

    for days in range(7):
        date_str = (date.today() + timedelta(days)).isoformat()
        menu_dict['detailed'].append(scraper_for_day_detail(date_str, update_recipes=False))
        menu_dict['overview'].append(scraper_for_day_overview(date_str, update_recipes=False))

    return menu_dict

"""
def multi_thread_menu_scraper(days,scraper_func):

    #days is the number of days you want to scrape starting from today
    #scraper_func is the function you want the thread to run
    menu_dict = {"menus":[]}
    thread_list = []
    for i in range(0,days):
        date_str = (date.today() + timedelta(i)).isoformat()
        thread_list.append(Scraper_thread(i,scraper_func,date_str,menu_dict))

    for t in thread_list:
        t.start()

    for t in thread_list:
        t.join()

    return menu_dict
"""
