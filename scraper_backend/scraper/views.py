from django.shortcuts import render
from django.http import JsonResponse, HttpResponse
from .models import ActivityLevel,OverviewMenu,DetailedMenu,Recipe
from datetime import date, timedelta
import os

# Create your views here.
def activity_level(request):
    """
    return the most recent activity level
    match the JSON style of existing API
    """
    return JsonResponse({
        "level": ActivityLevel.getLast()
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
    if request.GET.get("recipe_link"):
        link = request.GET.get("recipe_link")
        nutrition_ret = Recipe.getByRecipeLink(link)
    else:
        return render(request,os.path.join("scraper","not_found.html"),context={})
