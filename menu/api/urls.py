from django.urls import path
from .views import ListOfAllActiveMenus

app_name = "menus"

urlpatterns = [
    path('menus/active/', ListOfAllActiveMenus.as_view(), name='list_active_menus'),
]