from django.contrib import admin
from .models import ActivityLevel,OverviewMenu,DetailedMenu,Recipe

# Register your models here.
class ActivityLevelModelAdmin(admin.ModelAdmin):
    list_display = ["__str__","createdAt"]

    class Meta:
        model = ActivityLevel

class OverviewMenuModelAdmin(admin.ModelAdmin):
    list_display = ["__str__","createdAt","updatedAt","menuDate"]

    class Meta:
        model = OverviewMenu

class DetailedMenuModelAdmin(admin.ModelAdmin):
    list_display = ["__str__","createdAt","updatedAt","menuDate"]

    class Meta:
        model = DetailedMenu

class RecipeModelAdmin(admin.ModelAdmin):
    list_display = ["__str__","createdAt","updatedAt"]

    class Meta:
        model = Recipe

admin.site.register(ActivityLevel, ActivityLevelModelAdmin)
admin.site.register(OverviewMenu, OverviewMenuModelAdmin)
admin.site.register(DetailedMenu, DetailedMenuModelAdmin)
admin.site.register(Recipe, RecipeModelAdmin)