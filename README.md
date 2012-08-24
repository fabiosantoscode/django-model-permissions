django-model-permissions
========================

A model-level lock paradigm applied to Django Auth Permissions.


Usage
=====

First, apply locks to some model methods:


```python
class Example(models.Model, LockingMixin):
    class Meta:
        permissions = [
            ('example_can_get_id', 'Can get ID')
        ]
    
    name = models.CharField(max_length=33)
    
    @locks.permission('app.example_can_get_id')
    def get_id(self):
        return self.id
```

Then, instance it and use it. When you try to access a locked method,
modelpermissions will throw an exception.

```python
model = Example.objects.create(name='name')

try:
    model.get_id()
    assert False #remove this
except PermissionDenied:
    'django.core.exceptions.PermissionDenied was thrown'
```

But now let's unlock this model instance and try again

```python
model.unlock(user)

model.get_id()
'no exception thrown'
```


Checks
------
You can use the above idiom, or you may want to check whether a method is locked beforehand.
    
```python
from modelpermissions import checks

get_id_is_locked = checks.is_locked(model,'get_id')
```

Beyond The Obvious
==================

You can apply tricks such as securing a model's `save` method and thus greatly reduce the number of permission-related testing work on your hands.

You can turn a RelatedManager (ex: `ExampleModel.posts`) into a property with a method which decides whether you get back every `post`, or just `post`s that are visible to `request.user`. The user is always available in `model.get_unlocker()`. Beware that the model may be absolutely unlocked instead, though. You can check using `model.has_absolute_unlock()`

Roadmap
=======

1. Create the reverse of LockingMixin, a mixin that makes the model start out as unlocked, and be locked afterwards, to embrace more access control strategies.

Installing
==========

1. Install django-model-permissions so that the `modelpermissions` module is somewhere in your python path.
2. Add `modelpermissions` to your `INSTALLED_APPS` setting


Reason
======

This library was created out of a need to help ease the pain of access control in a complex application. Together with a middleware which catches the PermissionDenied exception it raises, it can help you forget about access control as you create your views.

You can easily assign permissions to views using the decorators found in `django.contrib.auth.decorators`, but it's rather tedious to do that to every single view in your project, remember permission names, etc.

Since there are usually less models than there are views, it may be a better idea to apply permissions to your models.

