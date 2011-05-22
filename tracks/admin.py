from django.contrib import admin
from tracks.models import Halt

class HaltAdmin(admin.ModelAdmin):
    list_display = ('name','latitude','longitude')
    ordering = ('-created_on',)
    search_fields = ('name',)
    list_filter = ['name','latitude','longitude']
    
    
admin.site.register(Halt,HaltAdmin)