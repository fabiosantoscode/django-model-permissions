django-model-permissions
========================

A lock paradigm applied to Django Models.


Usage
=====

First, apply locks to some model methods:

    class Example(models.Model, LockingMixin):
        class Meta:
            permissions = [
                ('example_can_get_id', 'Can get ID')
            ]
        
        name = models.CharField(max_length=33)
        
        @locks.permission('app.example_can_get_id')
        def get_id(self):
            return self.id
    
Then, instance it and use it. When you try to access a locked method,
modelpermissions will throw an exception.

    model = Example.objects.create(name='name')
    
    try:
        model.get_id()
        assert False #remove this
    except PermissionDenied:
        'django.core.exceptions.PermissionDenied was thrown'

But now let's unlock this model instance and try again

    model.unlock(user)
    
    model.get_id()
    'no exception thrown'


Checks
------
You can use the above idiom, or you may want to check whether a method is locked beforehand.

    from modelpermissions import checks
    
    get_id_is_locked = checks.is_locked(model,'get_id')


Installing
==========

1. Install django-model-permissions so that the `modelpermissions` module is somewhere in your python path.
2. Add `modelpermissions` to your `INSTALLED_APPS` setting



