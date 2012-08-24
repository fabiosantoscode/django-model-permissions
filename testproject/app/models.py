from django.db import models

# Create your models here.
from modelpermissions import locks
from modelpermissions.models import LockingMixin


class Example(models.Model, LockingMixin):
    class Meta:
        permissions = [
            ('example_can_get_id', 'Can get ID')
        ]
    
    name = models.CharField(max_length=33)
    
    @locks.permission('app.example_can_get_id')
    def get_id(self):
        return self.id
    
    def name_conditional_lock(self):
        return not self.name.startswith('hidden-')
    
    @locks.conditional(name_conditional_lock)
    def get_name(self):
        return self.name
    


