from django.contrib import admin
from .models import   Menu,  MenuItem, Category
# Register your models here.
admin.site.register(Menu)
admin.site.register(Category)
admin.site.register(MenuItem)