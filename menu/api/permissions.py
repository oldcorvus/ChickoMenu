from rest_framework import permissions

from plan.models import UserPlan
from ..models import Menu, Category,MenuItem
from django.utils.translation import gettext as _
from django.utils.timezone import timedelta

class IsOwnerOrReadOnly(permissions.BasePermission):
  
  def has_object_permission(self, request, view, obj):
    # Read permissions are allowed to any request,
    # so we'll always allow GET, HEAD or OPTIONS requests.
    if request.method in permissions.SAFE_METHODS:
        return True

    # Write permissions are only allowed to the owner of the place.
    return obj.owner == request.user


class MenuLimitPermission(permissions.BasePermission):
    message = _("You have exceeded your menu limit for this plan.")

    def has_permission(self, request, view):
        # Check if the request is a POST request
        if request.method == 'POST':
            # Get the user's active plan
            # Get the active UserPlan object for the current user
            active_plan = UserPlan.objects.filter(user=request.user, is_active=True).first()
            if active_plan is not  None:
                duration_plan_item = active_plan.plan.features.get(name='duration')
                menu_limit = active_plan.plan.features.get(name='menu_limit').description
                # Get the duration in days
                duration_in_days = int(duration_plan_item.description)
                # Get the number of menus the user has created
                end_date = active_plan.start_date + timedelta(days=duration_in_days * 30)
                menus_in_period = Menu.objects.filter(owner= request.user, created_at__range=[active_plan.start_date, end_date]).count()

                # Check if the user's menu count is less than their plan's menu limit
                if menus_in_period < int(menu_limit) :
                    return True

            # If the user has exceeded their menu limit, return False
            return False

        # For other request methods, allow access
        return True


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