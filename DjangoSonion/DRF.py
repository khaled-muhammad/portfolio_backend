from rest_framework import permissions
from django.contrib.auth.models import User
from rest_framework import authentication
from rest_framework import exceptions
from django.conf import settings

class AnonymousPermissionOnly(permissions.BasePermission):
    message = "You are already authenticated. please signout to use this method!"
    def has_permission(self, request, view):
        return not request.user.is_authenticated

class isAdminOrPostOnly(permissions.BasePermission):
    message = "Nehoon!" #"You Don't have permissions to see the admin messages!"

    def has_permission(self, request, view):
        return bool(request.user and request.user.is_staff) or request.method == 'POST'


def exact(val, form):
    form = form.split('_')

    for splitN in form:
        returned = val.find(splitN)
        if returned == -1 or val[returned+1] == form[1]:
            return False
        
        else:
            print(val[returned+2])
            print(form[1])
            return True
