from django.urls import path
from .views import ListOfAllActiveMenus, MenuDetail, MenuItemDetail, UserMenus, CategoryDetail

app_name = "menu"

urlpatterns = [
    path('menus/active/', ListOfAllActiveMenus.as_view(), name='list_active_menus'),
    path('menus/user/', UserMenus.as_view(), name='user_menus'),
    path('menus/<str:pk>', MenuDetail.as_view(),name='menu_detail'),
    path('categories/<str:pk>/', CategoryDetail.as_view(), name='category-detail'),
    path('menu-item/<str:pk>/', MenuItemDetail.as_view(), name='menu-item-detail'),

]