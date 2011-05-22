from django.db import models
from common.models import BaseModel
from common.models import Address

RESTAURANT_STATUS_CHOICES = (
                             ('0','Premium'),
                             ('1','Regular'),
                             ('2','Blocked')
                             )

class RestaurantManager(models.Manager):
    def create_restaurant(self, name, address,status='0'):
        from utils import name_for_linking
        try:
            alias = name_for_linking('%s' % name.lower())
            return self.get(alias=alias)
        except Restaurant.DoesNotExist:
            restaurant = Restaurant(name=name, alias=alias, address=address,status=status)
            restaurant.save()
            return restaurant

class PremiumRestaurantsManager(models.Manager):
    def get_query_set(self):
        return super(PremiumRestaurantsManager,self).get_query_set().filter(status='0')    

class RegularRestaurantsManager(models.Manager):
    def get_query_set(self):
        return super(RegularRestaurantsManager,self).get_query_set().filter(status='1')
    
class BlockedRestaurantsManager(models.Manager):
    def get_query_set(self):
        return super(BlockedRestaurantsManager,self).get_query_set().filter(status='2')    

class Restaurant(BaseModel):
    name = models.CharField(max_length=100,blank=False)
    alias = models.CharField(max_length=100,blank=False,unique=True,db_index=True)
    address = models.ForeignKey(Address)
    status = models.CharField(max_length=1,blank=False,choices=RESTAURANT_STATUS_CHOICES)
    objects = RestaurantManager()
    premiumobjects = PremiumRestaurantsManager()
    regularobjects = RegularRestaurantsManager()
    blockedobjects = BlockedRestaurantsManager()
    
    def get_status(self):
        for rest_status in RESTAURANT_STATUS_CHOICES:
            if rest_status[0] == self.status:
                return rest_status[1]
        return None
    
    def make_premium(self):
        self.status = '0'
        self.save()
        return self
    
    def menuitems(self):
        return RestaurantMenuItem.objects.filter(restaurant=self).order_by('item__name')
    
    def __unicode__(self):
        return '%(name)s:%(alias)s' % {'name':self.name, 'alias':self.alias}

class FoodItemTagManager(models.Manager):
    def create_fooditemtag(self,name):
        try:
            tag = self.get(name = name.strip().lower())
        except FoodItemTag.DoesNotExist:
            tag = FoodItemTag(name = name.strip().lower())
            tag.save()
        return tag

class FoodItemTag(BaseModel):
    name = models.CharField(max_length=30,blank=False,unique=True,db_index=True)
    objects = FoodItemTagManager()
    
    def __unicode__(self):
        return '%(name)s' % {'name':self.name}

class FoodItemManager(models.Manager):
    def create_fooditem(self,name,type='Veg',tags=[]):
        from utils import name_for_linking
        alias = name_for_linking('%s' % name.lower()) 
        fooditem = self._check_exists(alias = alias)
        if not fooditem:
            fooditem = FoodItem(name=name,type=type,alias=alias)
            fooditem.save()
        if tags:
            for tag in tags:
                fooditem.tags.add(tag)
        return fooditem
    
    def _check_exists(self,alias):
        try:
            exist = self.get(alias=alias)
            print '=====\nAlready Exists:%s\n=====' % exist
            return exist
        except FoodItem.DoesNotExist:
            return None

class FoodItem(BaseModel):
    name = models.CharField(max_length=50,blank=False)
    type = models.CharField(max_length=20,blank=False)
    alias = models.CharField(max_length=100,blank=False,unique=True,db_index=True)
    tags = models.ManyToManyField(FoodItemTag)
    objects = FoodItemManager()
    
    def __unicode__(self):
        return '%(name)s:%(alias)s' % {'name':self.name,'alias':self.alias}
    
class RestaurantMenuItemManager(models.Manager):
    def create_restaurant_menuitem(self,restaurant,item,cost=None):
        existing_menuitem = self._check_exists(restaurant=restaurant,item=item)
        if existing_menuitem:
            return existing_menuitem
        restaurant_menu_item = RestaurantMenuItem(restaurant=restaurant,item=item,cost=cost)
        restaurant_menu_item.save()
        return restaurant_menu_item
        
    def _check_exists(self,restaurant,item):
        try:
            return self.get(restaurant=restaurant,item=item)
        except RestaurantMenuItem.DoesNotExist:
            return False
    
class RestaurantMenuItem(BaseModel):
    restaurant = models.ForeignKey(Restaurant)
    item = models.ForeignKey(FoodItem)
    cost = models.DecimalField(max_digits=6,decimal_places=2,blank=True,null=True)
    objects = RestaurantMenuItemManager()
    
    def __unicode__(self):
        return '%s' % self.item       