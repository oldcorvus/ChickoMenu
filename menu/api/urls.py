from django.urls import path
from .views import ListOfAllActiveMenus, UserMenus

app_name = "menu"

urlpatterns = [
    path('menus/active/', ListOfAllActiveMenus.as_view(), name='list_active_menus'),
    path('menus/user/', UserMenus.as_view(), name='user_menus'),

]