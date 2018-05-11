from django.shortcuts import render
from django.http import JsonResponse, HttpResponse
from .models import ActivityLevel,OverviewMenu,DetailedMenu,Recipe
from datetime import date, timedelta
import os
from .db_insertion import *

# Create your views here.
def activity_level(request):
    """
    return the most recent activity level
    match the JSON style of existing API
    """
    return JsonResponse({
        "level": ActivityLevel.getLast()
    })

def hour(request):
    """
    return hours starting from yesterday, with length 8
    """
    return JsonResponse({
        "hours": Hour.getByDateRange(date.today()-timedelta(days=1),date.today()+timedelta(days=6))
    })

def overview_menu(request):
    """
    return the overmenu starting from yesterday, with length 8
    """
    return JsonResponse({
        "menus": OverviewMenu.getByDateRange(date.today()-timedelta(days=1),date.today()+timedelta(days=6))
    })

def detailed_menu(request):
    """
    return the detailedmenu starting from yesterday, with length 8
    """
    return JsonResponse({
        "menus": DetailedMenu.getByDateRange(date.today()-timedelta(days=1),date.today()+timedelta(days=6))
    })    

def nutrition_box(request):
    """
    render the nutrition box
    """
    def helper(value):
        """
        value is string;
        This is a helper function to check whether value contains -1; if so, returns --; else, return original value
        """
        if "-1" in value:
            return "--"
        else:
            return value


    if request.GET.get("recipe_link"):
        link = request.GET.get("recipe_link")
        nutrition_ret = Recipe.getByRecipeLink(link)

        # if not find recipe_link
        if len(nutrition_ret) == 0:
            return render(request,os.path.join("scraper","not_found.html"),context={})
        else:    
            # build the context for template
            nutrition_dict = {}
            nutrition_dict["serving_size"] = helper(nutrition_ret["serving_size"])
            nutrition_dict["Calories"] = helper(nutrition_ret["Calories"])
            nutrition_dict["Fat_Cal"] = helper(nutrition_ret["Fat_Cal."])
            nutrition_dict["Total_Fat_g"] = helper(nutrition_ret["Total_Fat"][0])
            nutrition_dict["Total_Fat_p"] = helper(nutrition_ret["Total_Fat"][1])
            nutrition_dict["Saturated_Fat_g"] = helper(nutrition_ret["Saturated_Fat"][0])
            nutrition_dict["Saturated_Fat_p"] = helper(nutrition_ret["Saturated_Fat"][1])
            nutrition_dict["Trans_Fat_g"] = helper(nutrition_ret["Trans_Fat"][0])
            nutrition_dict["Cholesterol_g"] = helper(nutrition_ret["Cholesterol"][0])
            nutrition_dict["Cholesterol_p"] = helper(nutrition_ret["Cholesterol"][1])
            nutrition_dict["Sodium_g"] = helper(nutrition_ret["Sodium"][0])
            nutrition_dict["Sodium_p"] = helper(nutrition_ret["Sodium"][1])
            nutrition_dict["Total_Carbohydrate_g"] = helper(nutrition_ret["Total_Carbohydrate"][0])
            nutrition_dict["Total_Carbohydrate_p"] = helper(nutrition_ret["Total_Carbohydrate"][1])
            nutrition_dict["Dietary_Fiber_g"] = helper(nutrition_ret["Dietary_Fiber"][0])
            nutrition_dict["Dietary_Fiber_p"] = helper(nutrition_ret["Dietary_Fiber"][1])
            nutrition_dict["Sugars_g"] = helper(nutrition_ret["Sugars"][0])
            nutrition_dict["Protein_g"] = helper(nutrition_ret["Protein"][0])
            nutrition_dict["VA_p"] = helper(nutrition_ret["Vitamin A"])
            nutrition_dict["VC_p"] = helper(nutrition_ret["Vitamin C"])
            nutrition_dict["Cal_p"] = helper(nutrition_ret["Calcium"])
            nutrition_dict["Iron_p"] = helper(nutrition_ret["Iron"])

            return render(request,os.path.join("scraper","nutritionbox.html"),context=nutrition_dict)

    else:
        return render(request,os.path.join("scraper","not_found.html"),context={})


def test(request):
    # insert_activity_level()
    # return HttpResponse("yes")
    insert_hours()
    return HttpResponse("yes3")
