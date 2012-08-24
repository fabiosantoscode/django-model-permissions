from django.db import models



class LockingMixin(object):
    def __init__(self):
        self._unlocker = None
        self._temp_unlocker = None
    
    def unlock(self, unlocker=None, absolute=False):
        self._unlocker = 'absolute' if absolute else unlocker
    
    def lock(self):
        self._unlocker = None
    
    def get_unlocker(self):
        return self._temp_unlocker or self._unlocker
    
    def has_absolute_unlock(self):
        return self._unlocker == 'absolute'



