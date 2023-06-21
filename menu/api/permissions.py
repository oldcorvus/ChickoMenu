from rest_framework import permissions
from ..models import Menu, Category,MenuItem

class IsOwnerOrReadOnly(permissions.BasePermission):
  
  def has_object_permission(self, request, view, obj):
    # Read permissions are allowed to any request,
    # so we'll always allow GET, HEAD or OPTIONS requests.
    if request.method in permissions.SAFE_METHODS:
        return True

    # Write permissions are only allowed to the owner of the place.
    return obj.owner == request.user


class MenuOwnerOrReadOnly(permissions.BasePermission):
      
  def has_object_permission(self, request, view, obj):
    # Read permissions are allowed to any request,
    # so we'll always allow GET, HEAD or OPTIONS requests.
    if request.method in [permissions.SAFE_METHODS]:
        return True

    # Write permissions are only allowed to the owner of the place.
    return obj.menu.owner == request.user


  def has_permission(self, request, view):
        if request.method in ['POST', 'PATCH', 'DELETE']:
            if 'category_pk' in request.data:
                category = Category.objects.filter(pk=request.data['category_pk']).first()
                if category and category.menu.owner == request.user:
                    return True
            elif 'menu_item_pk' in request.data:
                menu_item = MenuItem.objects.filter(pk=request.data['menu_item_pk']).first()
                if menu_item and menu_item.menu.owner == request.user:
                    return True
            elif 'menu' in request.data:
                menu = Menu.objects.filter(pk=request.data['menu']).first()
                if menu and menu.owner == request.user:
                    return True
            return False
        return True