"""
This file demonstrates writing tests using the unittest module. These will pass
when you run "manage.py test".

Replace this with more appropriate tests for your application.
"""

from django.test import TestCase
from django.contrib.auth.models import User, Permission
from django.core.exceptions import PermissionDenied

from models import Example


class SimpleTest(TestCase):
    def test_code_example(self):
        'test the code example in README.md'
        
        permission = Permission.objects.get(
            codename='example_can_get_id')
        
        user = User.objects.create(
            username='user')
        user_without_permissions = User.objects.create(
            username='without_permissions')
        user.user_permissions.add(permission)
        
        assert user.has_perm('app.example_can_get_id')
        
        '''
        Basic Example
        '''
        
        """
        <model code here>
        
        Then, instance it and use it. When you try to access a locked
        method, modelpermissions will throw an exception.
        """
        
        model = Example.objects.create(name='hidden-name')
        
        try:
            model.get_id()
            assert False #remove this
        except PermissionDenied:
            'django.core.exceptions.PermissionDenied was thrown'
        
        "But now let's unlock this model instance and try again"
        model.unlock(user)
        
        model.get_id()
        'no exception thrown'
        
        
        '''
        Checks example
        '''
        
        from modelpermissions import checks
        
        get_id_locked = checks.is_locked(model,'get_id')
        
        
