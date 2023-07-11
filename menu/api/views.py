from django.utils.translation import gettext_lazy as _
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.generics import (
ListAPIView, ListCreateAPIView, RetrieveUpdateDestroyAPIView,
CreateAPIView
)
from menu.models import Menu, Category, MenuItem
from .serializers import (
    CategorySerializer,
    MenuDetailSerializer,
    MenuItemSerializer,
    MenuSerializer,
    
)
from rest_framework.parsers import MultiPartParser
from django.core.cache import cache
from django.shortcuts import get_object_or_404
from .permissions import IsOwnerOrReadOnly, MenuOwnerOrReadOnly, MenuLimitPermission
from .utils import get_code

class ListOfAllActiveMenus(ListAPIView):
    serializer_class = MenuSerializer
    permission_classes = [AllowAny]

    def get_queryset(self):
        # Check if the response is already cached
        cache_key = 'active_menus_cache_key'
        cached_data = cache.get(cache_key)
        if cached_data:
            return cached_data
    
        # If the response is not cached, compute it and cache it
        queryset = Menu.active_menus.all()
        cache.set(cache_key, queryset, timeout=60)  # cache for 1 minutes
        return queryset


class UserMenus(ListCreateAPIView):
    serializer_class = MenuSerializer
    permission_classes = [IsAuthenticated,IsOwnerOrReadOnly, MenuLimitPermission]


    def get_queryset(self):
        # Check if the response is already cached
        cache_key = f'user_menus_cache_key_{self.request.user.id}'
        cached_data = cache.get(cache_key)
        if cached_data:
            return cached_data

        # If the response is not cached, compute it and cache it
        queryset = Menu.objects.filter(owner=self.request.user)
        cache.set(cache_key, queryset, timeout=60)  # cache for 1 minutes
        return queryset

    def perform_create(self, serializer):

        code = get_code()
        serializer.save(owner=self.request.user, code=code)


class MenuDetail(RetrieveUpdateDestroyAPIView):
    permission_classes = [IsOwnerOrReadOnly]
    serializer_class = MenuDetailSerializer
    def get_object(self):
        # Check if the response is already cached
        cache_key = f'menu_detail_cache_key_{self.kwargs["pk"]}'
        cached_data = cache.get(cache_key)
        if cached_data:
            return cached_data

        # If the response is not cached, compute it and cache it
        menu = get_object_or_404(Menu, pk=self.kwargs['pk'])
        cache.set(cache_key, menu, timeout=10)  # cache for 1 minutes
        return menu
        
class CategoryDetail(RetrieveUpdateDestroyAPIView):
    permission_classes = [IsAuthenticated, MenuOwnerOrReadOnly]
    serializer_class = CategorySerializer

    def get_object(self):
        return get_object_or_404(Category, pk=self.kwargs['pk'])

class MenuItemDetail(RetrieveUpdateDestroyAPIView):
    permission_classes = [IsAuthenticated, MenuOwnerOrReadOnly]
    serializer_class = MenuItemSerializer
    
    def get_object(self):
        return get_object_or_404(MenuItem, pk=self.kwargs['pk'])

class CreateCategory(CreateAPIView):
    """
    Create a new category.
    """
    serializer_class = CategorySerializer
    permission_classes = [IsAuthenticated,MenuOwnerOrReadOnly]

    def perform_create(self, serializer):
        menu = serializer.validated_data['menu']
        menu = get_object_or_404(Menu,pk=menu.id)
        serializer.save(menu=menu)

class CreateMenuItem(CreateAPIView):
    """
    Create a new menu item.
    """
    serializer_class = MenuItemSerializer
    permission_classes = [IsAuthenticated,MenuOwnerOrReadOnly]
    parser_classes = [MultiPartParser]
    
    def perform_create(self, serializer):
        menu = serializer.validated_data['menu']
        category = serializer.validated_data['category']
        menu = get_object_or_404(Menu,pk=menu.id)
        category = get_object_or_404(Category,pk=category.id)

        serializer.save(menu=menu, category= category)