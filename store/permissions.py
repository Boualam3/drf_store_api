from rest_framework import permissions


class IsAdminReadOnly(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            return True
        return bool(request.user and request.user.is_staff)


class ViewCustomerHistoryPermissions(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user.has_perm('store.view_history')


"""
this is how to customize django permissions specially DjangoModelPermissions below down 
we dont need in our store its just for learning and make it as reference  about permissions 
"""


class FullDjangoModelPermission(permissions.DjangoModelPermissions):
    def __init__(self) -> None:
        self.perms_map['GET'] = ['%(app_label)s.view_%(model_name)s']
