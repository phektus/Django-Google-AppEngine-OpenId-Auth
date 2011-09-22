"""Glue between OpenID and django.contrib.auth."""

from google.appengine import api as gae_api
import os

from django.conf import settings
from django.contrib.auth.models import User, check_password
from django.shortcuts import redirect
from django.contrib.auth import authenticate as p_authenticate


class OpenIDBackend(object):
    """A django.contrib.auth backend that authenticates the user based on
    an OpenID response."""
    
    supports_anonymous_user = False
    supports_inactive_user = False
    supports_object_permissions = False
    request = None

    def authenticate(self, **kwargs):
        """Authenticate the user based on an OpenID response."""
        
        if kwargs.has_key('username'):
            username = kwargs.get('username')
            # check for admin login 
            if username == settings.ADMIN_LOGIN:
                password = kwargs.get('password')
                return self.auth_admin(username, password)            
            else:
                try:
                    user = User.objects.get(username=username)
                except User.DoesNotExist:
                    user = User(username=username)
                    user.is_staff = False
                    user.is_superuser = False
                    user.save()
                        
                return user

        return None


    def get_user(self, user_id):
        try:
            return User.objects.get(pk=user_id)
        except User.DoesNotExist:
            return None


    def auth_admin(self, username=None, password=None):
        """Handles authentication for admin"""
        login_valid = (settings.ADMIN_LOGIN == username)
        pwd_valid = check_password(password, settings.ADMIN_PASSWORD)
        if login_valid and pwd_valid:
            try:
                user = User.objects.get(username=username)
            except User.DoesNotExist:
                # Create a new user. Note that we can set password
                # to anything, because it won't be checked; the password
                # from settings.py will.
                user = User(username=username, password=settings.ADMIN_PASSWORD)
                user.is_staff = True
                user.is_superuser = True
                user.save()
            return user
        return None
