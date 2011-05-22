from django.contrib import admin
from users.models import UserProfile

class UserProfileAdmin(admin.ModelAdmin):
    list_display = ('name','email','organization','mobile')
    ordering = ('-created_on',)
    search_fields = ('name','email', 'organization')
    list_filter = ['organization','service_type']
    
admin.site.register(UserProfile,UserProfileAdmin)