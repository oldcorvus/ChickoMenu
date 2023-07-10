from rest_framework import permissions

class IsUserPlanOwner(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        # Check if the user making the request owns the user plan associated with the order
        return obj.user_plan.user == request.user