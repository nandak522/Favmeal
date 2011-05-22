from django.db import models
from common.models import BaseModel
from common.models import Address

MESS_STATUS_CHOICES = (
                             ('0','Premium'),
                             ('1','Regular'),
                             ('2','Blocked')
                             )

class MessManager(models.Manager):
    def create_mess(self, name, address,status='0'):
        from utils import name_for_linking
        alias = name_for_linking('%s' % name.lower())
        try:
            return self.get(alias=alias)
        except Mess.DoesNotExist:
            mess = Mess(name=name, alias=alias, address=address,status=status)
            mess.save()
            return mess

class PremiumMessManager(models.Manager):
    def get_query_set(self):
        return super(PremiumMessManager,self).get_query_set().filter(status='0')    

class RegularMessManager(models.Manager):
    def get_query_set(self):
        return super(RegularMessManager,self).get_query_set().filter(status='1')
    
class BlockedMessManager(models.Manager):
    def get_query_set(self):
        return super(BlockedMessManager,self).get_query_set().filter(status='2')  

class Mess(BaseModel):
    name = models.CharField(max_length=100,blank=False)
    alias = models.CharField(max_length=100,blank=False,unique=True,db_index=True)
    address = models.ForeignKey(Address)
    status = models.CharField(max_length=1,blank=False,choices=MESS_STATUS_CHOICES)
    objects = MessManager()
    premiumobjects = PremiumMessManager()
    regularobjects = RegularMessManager()
    blockedobjects = BlockedMessManager()
    
    def __unicode__(self):
        return '%(name)s:%(alias)s' % {'name':self.name, 'alias':self.alias}