from django.contrib import admin
from restaurants.models import Restaurant,FoodItem

class RestaurantAdmin(admin.ModelAdmin):
    pass
class FoodItemAdmin(admin.ModelAdmin):
    pass

admin.site.register(Restaurant, RestaurantAdmin)
admin.site.register(FoodItem, FoodItemAdmin)
