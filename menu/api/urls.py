from django.urls import path
from .views import ListOfAllActiveMenus, MenuDetail, UserMenus

app_name = "menu"

urlpatterns = [
    path('menus/active/', ListOfAllActiveMenus.as_view(), name='list_active_menus'),
    path('menus/user/', UserMenus.as_view(), name='user_menus'),
    path('menus/<str:pk>', MenuDetail.as_view(),name='menu_detail'),

]