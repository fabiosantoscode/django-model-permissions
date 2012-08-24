from django.test import TestCase
from django.db import models
from django.core.exceptions import PermissionDenied
from django.contrib.auth.models import User, Permission, ContentType

import locks

from checks import is_locked, is_unlocked

from models import LockingMixin

class SomeModel(models.Model, LockingMixin):
    name = models.CharField(max_length=32)
    
    @locks.permission('.permission')
    def get_name(self):
        return self.name
    
    def always_true(self):
        return True
        
    def always_false(self):
        return False
    
    @locks.conditional(always_true)
    def get_real_name(self):
        pass
    
    @locks.conditional(always_false)
    def destroy_world(self):
        pass
        
        
    
class ModelPermissionTests(TestCase):
    def setUp(self):
        ct = ContentType.objects.create()
        permission = Permission.objects.create(
            codename='permission', name='permission', content_type=ct)
        
        self.loser = User.objects.create(username='loser')
        self.user = User.objects.create(username='user')
        
        self.user.user_permissions.add(permission)
        
        self.user.save()
        
        assert self.user.has_perm('.permission')
        
        self.model = self.m = SomeModel.objects.create(name='name')
    
    def test_unlock(self):
        'test unlocking a model'
        
        m = SomeModel.objects.get(name='name')
        
        try:
            m.get_name()
        except PermissionDenied:
            pass
        
        m.unlock(absolute=True)
        self.assertEqual(m.get_name(),'name')
        
        m.unlock(self.user)
        self.assertEqual(m.get_name(),'name')
        
        m.unlock(self.loser)
        try:
            m.get_name()
            self.assertFalse(throw_permission_denied)
        except PermissionDenied:
            pass
    
    def test_exception_thrown(self):
        'test correct exception is thrown'
        
        throw_permission_denied = 'Should have thrown PermissionDenied'
        
        self.m.lock()
        
        try:
            self.m.get_name()
            
            self.assertFalse(throw_permission_denied)
        except PermissionDenied as e:
            self.assertTrue('is a locked method' in str(e))
    
    def test_permission_locks(self):
        self.assertTrue(is_locked(self.m,'get_name'))
        self.assertTrue(is_locked(self.m,'get_name', self.loser))
        self.assertTrue(is_unlocked(self.m,'get_name', self.user))
    
    def test_conditional_locks(self):
        self.assertTrue(is_unlocked(self.m,'get_real_name'))
        self.assertTrue(is_locked(self.m,'destroy_world'))
        
        self.assertTrue(is_unlocked(self.m,'get_real_name'), self.user)
        self.assertTrue(is_locked(self.m,'destroy_world'), self.user)
        
        self.assertTrue(is_unlocked(self.m, 'get_real_name'), self.loser)
        self.assertTrue(is_locked(self.m, 'destroy_world'), self.loser)
        



