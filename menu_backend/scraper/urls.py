from django.urls import re_path

from . import views

urlpatterns = [
    re_path(r'^(?i)ActivityLevels/', views.activity_level, name='activity_level'),
    re_path(r'^(?i)overviewMenu/', views.overview_menu, name='overview_menu'),
    re_path(r'^(?i)detailedMenu/', views.detailed_menu, name="detailed_menu"),
    re_path(r'^(?i)nutritionbox/', views.nutrition_box, name='nutrition_box'),
    re_path(r'^(?i)Hours/', views.hour, name="hour"),
    re_path(r'^(?i)test/',views.test, name="test")
]