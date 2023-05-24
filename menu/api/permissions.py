from rest_framework import permissions
from ..models import Menu

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
    if request.method in permissions.SAFE_METHODS:
        return True

    # Write permissions are only allowed to the owner of the place.
    return obj.menu.owner == request.user

  def has_permission(self, request, view):
    if request.method == "POST":
        # For create action
        try:
            menu_id = request.data["menu"]
            menu = Menu.objects.get(pk=menu_id, owner=request.user)
            return True
        except:
            return False
    return True