from django.urls import path

from . import views

urlpatterns = [
    path('ActivityLevels', views.activity_level, name='activity_level'),
    path('overviewMenu', views.overview_menu, name='overview_menu'),
    path('detailedMenu', views.detailed_menu, name="detailed_menu"),
    path('nutritionbox', views.nutrition_box, name='nutrition_box'),
    # TODO: write the hour route
    path('test',views.test, name="test")
]