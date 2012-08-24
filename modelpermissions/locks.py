from functools import update_wrapper

from django.core.exceptions import PermissionDenied
from django.contrib.auth.models import Permission

def _get_function_wrapper(f, lock_test):
    def wrapper(self, *args, **kwargs):
        if not lock_test(self):
            raise PermissionDenied('%s is a locked method.' % f)
        else:
            return f(self, *args, **kwargs)
    
    wrapper = update_wrapper(wrapper,f)
    wrapper.lock_test = lock_test
    return wrapper

def permission(*permissions):
    def permission_test(model_instance):
        unlocker = model_instance.get_unlocker()
        absolute_unlock = model_instance.has_absolute_unlock()
        
        if absolute_unlock:
            return True
        elif not unlocker:
            return False
        else:
            return unlocker.has_perms(permissions)
    
    def permission_decorator(f):
        return _get_function_wrapper(f, lock_test=permission_test)
    
    return permission_decorator

def conditional(test):
    def conditional_test(model_instance):
        if model_instance.has_absolute_unlock():
            return True
        else:
            return test(model_instance)
    
    def conditional_decorator(f):
        return _get_function_wrapper(f, lock_test=conditional_test)
    
    return conditional_decorator

