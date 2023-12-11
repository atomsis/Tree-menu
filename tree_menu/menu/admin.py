from django.contrib import admin
from .models import MenuItem

# Register your models here.
class MenuItemAdmin(admin.ModelAdmin):
    list_display = ('name', 'url', 'parent','named_url')
    list_filter = ('parent',)
    search_fields = ('name', 'url')

admin.site.register(MenuItem, MenuItemAdmin)

