from django.utils.translation import gettext_lazy as _
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.generics import (
ListAPIView, ListCreateAPIView, RetrieveUpdateDestroyAPIView,
CreateAPIView, UpdateAPIView, DestroyAPIView,
)
from menu.models import Menu, Category, MenuItem
from .serializers import (
    CategorySerializer,
    MenuDetailSerializer,
    MenuItemSerializer,
    MenuSerializer,
)
from .permissions import IsOwnerOrReadOnly, MenuOwnerOrReadOnly
from .utils import get_code

class ListOfAllActiveMenus(ListAPIView):
    serializer_class = MenuSerializer
    permission_classes = [AllowAny]


    def get_queryset(self):
        return Menu.active_menus.all()

class UserMenus(ListCreateAPIView):
    serializer_class = MenuSerializer
    permission_classes = [IsAuthenticated,IsOwnerOrReadOnly]


    def get_queryset(self):
        return Menu.objects.filter(owner=self.request.user)

    def perform_create(self, serializer):
        code = get_code()
        serializer.save(owner=self.request.user, code=code)