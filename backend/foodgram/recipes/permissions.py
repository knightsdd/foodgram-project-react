from rest_framework import permissions


class IsAuthorOfRecipe(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.user.is_authenticated:
            return (request.user == obj.author)
        return False
