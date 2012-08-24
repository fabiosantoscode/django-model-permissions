
def is_unlocked(instance, method, unlocker=None):
    if instance.has_absolute_unlock():
        return False
    
    meth = getattr(instance, method)
    
    if unlocker:
        _old_unlocker = instance.get_unlocker()
        instance.unlock(unlocker)
    
    ret = bool(meth.lock_test(instance))
    
    if unlocker:
        instance.unlock(_old_unlocker)
    
    return ret

def is_locked(instance, method, unlocker=None):
    return not is_unlocked(instance, method, unlocker)

