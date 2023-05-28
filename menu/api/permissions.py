from rest_framework import permissions
from ..models import Menu, Category

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
      if request.method in ["POST", "PATCH", "DELETE"]:
          # For create or update actions, find the menu by the category pk and check that it belongs to the user
          try:
              category_pk = view.kwargs['pk']
              category = Category.objects.get(pk=category_pk)
              menu = Menu.objects.get(pk=category.menu.pk, owner=request.user)
              return True
          except:
              return False
      else:
          # For all other actions, allow access
          return True