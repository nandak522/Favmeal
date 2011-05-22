from django.db import models
from django.contrib.auth.models import User
from common.models import BaseModel
from common.models import Address
from restaurants.models import FoodItem
from restaurants.models import RestaurantMenuItem
from utils.fields import CustomMenuItemsField

class InvalidServiceTypeException(Exception):
    pass

class UserProfileManager(models.Manager):
    def create_userprofile(self,email,password,service_type,mobile,source_place,source_area,destination_place,destination_area,source_landmark,destination_landmark,city='Hyderabad',source_zip=None,destination_zip=None,dateofbirth=None,favdish=None,organization=None,source_latitude=None,source_longitude=None,destination_latitude=None,destination_longitude=None):
        user = self.djangouser_exists(email)
        if not user:
            user = User.objects.create_user(self._compute_username(email),email,password)
            if service_type == 'restaurantfood':
                source = Address.objects.get(place='Dummy Place')
            else:
                source = Address.objects.create_address(place=source_place, landmark=source_landmark, area=source_area, city=city, zip=source_zip,latitude=source_latitude, longitude=source_longitude)
            destination = Address.objects.create_address(place=destination_place, landmark=destination_landmark, area=destination_area, city=city, zip=destination_zip,latitude=destination_latitude, longitude=destination_longitude)
            userprofile = UserProfile(user=user,name=user.username,email=email,organization=organization,dateofbirth=dateofbirth,favdish=favdish,source=source,destination=destination,mobile=mobile,service_type=service_type)
            userprofile.save()
            return userprofile
        return user.get_profile()
    
    def djangouser_exists(self,email):
        try:
            return User.objects.get(email=email)
        except User.DoesNotExist:
            return None
    
    def _compute_username(self,email):
        import sha,random
        salt = sha.new(str(random.random())).hexdigest()[:5]
        code = sha.new(salt+ email).hexdigest()
        return code[:30]

class UserProfile(BaseModel):
    SERVICE_CHOICES = (('homefood','homefood'),
                   ('restaurantfood','restaurantfood'),
                   ('messfood','messfood'),
                   )
    user = models.OneToOneField(User,unique=True)
    name = models.CharField(max_length=50, blank=True)
    email = models.EmailField(blank=False,db_index=True)
    service_type = models.CharField(max_length=50,blank=False,choices=SERVICE_CHOICES)
    organization = models.CharField(max_length=50, null=True,blank=True,db_index=True)#FIXME:when we scale, we need to replace this with a ForeignKey(Organization)
    dateofbirth = models.DateField(blank=True,null=True)
    favdish = models.CharField(max_length=50,blank=True,null=True)
    source = models.ForeignKey(Address,related_name='src')
    destination = models.ForeignKey(Address,related_name='dest')
    mobile = models.CharField(max_length=10,blank=False,db_index=True)
    objects = UserProfileManager()
    
    def __unicode__(self):
        return self.email
    
    def source_address_text(self):
        return "%s, %s, %s, %s India" % (self.source.place,self.source.landmark,self.source.area,self.source.city)
    
    def destination_address_text(self):
        return "%s, %s, %s, %s India" % (self.destination.place,self.destination.landmark,self.destination.area,self.destination.city)

    def set_password(self,newpassword):
        user = self.user
        user.set_password(newpassword)
        user.save()
        return self
    
    def reset_password(self):
        newpassword = User.objects.make_random_password()
        self.user.set_password(newpassword)
        self.user.save()
        return newpassword
    
    def get_service_type(self):
        return self.service_type
    
    def mark_homefood_service(self):
        self.service_type = 'homefood'
        self.save()
        return self
    
    def mark_restaurantfood_service(self):
        self.service_type = 'restaurantfood'
        self.save()
        return self
    
    def mark_messfood_service(self):
        self.service_type = 'messfood'
        self.save()
        return self
    
    def get_subscribed_mess(self):
        if self.service_type == 'messfood':
            from messfood.models import Mess
            for mess in Mess.objects.all():
                if self.source.place == mess.address.place:
                    return mess
        return None
    
    def set_source_address(self,source_place,source_area,source_landmark,city='Hyderabad',source_zip=None,source_latitude=None,source_longitude=None):
        source = Address.objects.create_address(place=source_place, landmark=source_landmark, area=source_area, city=city, zip=source_zip,latitude=source_latitude, longitude=source_longitude)
        self.source = source
        self.save()
        return self
        
    def set_destination_address(self,destination_place,destination_area,destination_landmark,city='Hyderabad',destination_zip=None,destination_latitude=None,destination_longitude=None):
        destination = Address.objects.create_address(place=destination_place, landmark=destination_landmark, area=destination_area, city=city, zip=destination_zip,latitude=destination_latitude, longitude=destination_longitude)
        self.destination = destination
        self.save()
        return self

class UserHomeFoodManager(models.Manager):
    def create_userfood(self,fooditem,userprofile):
        food_for_today = self.get_todays_food(userprofile)
        if food_for_today:
            food_for_today.fooditem = fooditem
            food_for_today.save()
        else:
            food_for_today = UserHomeFood(fooditem=fooditem,userprofile=userprofile)
            food_for_today.save()
        return food_for_today
    
    def get_todays_food(self,userprofile):
        from datetime import datetime
        today = datetime.date(datetime.now())
        try:
            return self.get(userprofile=userprofile,created_on__day=today.day,created_on__month=today.month,created_on__year=today.year)
        except UserHomeFood.DoesNotExist:
            return None
        
class UserHomeFood(BaseModel):
    fooditem = models.ForeignKey(FoodItem)
    userprofile = models.ForeignKey(UserProfile)
    objects = UserHomeFoodManager()
    
    def __unicode__(self):
        return '%s|%s' % (self.fooditem.alias,self.userprofile)        

class UserOrderManager(models.Manager):
    def create_userorder(self,userprofile,deliverytime,menuitems,totalcost,status=0,is_amountpaid=False):
        import time
        unique_timestamp = str(int(time.time()))
        order = self.exists(code=unique_timestamp)
        if order:
            return order
        order = UserOrder(userprofile=userprofile,code=unique_timestamp,status=status,deliverytime=deliverytime,items=menuitems,totalcost=str(round(float(totalcost))),is_amountpaid=is_amountpaid)
        order.save()
        return order
    
    def exists(self,code):
        try:
            return self.get(code=code)
        except UserOrder.DoesNotExist:
            return None

class UserOrder(BaseModel):
    ORDER_STATUS_CHOICES = ((0,'Yet to be Start'),
                            (1,'Under Process'),
                            (2,'Done'),
                            (3,'Cancelled'),
                            )
    userprofile = models.ForeignKey(UserProfile)
    code = models.CharField(max_length=20,blank=False,unique=True,db_index=True)
    status = models.CharField(max_length=50,blank=False,choices=ORDER_STATUS_CHOICES)
    deliverytime = models.DateTimeField(blank=False)
    items = CustomMenuItemsField(blank=False)
    totalcost = models.DecimalField(max_digits=6,decimal_places=2,blank=False)
    is_amountpaid = models.BooleanField(default=False,blank=False)
    objects = UserOrderManager()

    #FIXME:currently retrieves only the restaurant of latest item. If the order spans across multiple restaurants, the following method need to be corrected
    def get_restaurant(self):
        menuitem_id = self.items.split(',')[0]
        from restaurants.models import RestaurantMenuItem
        return RestaurantMenuItem.objects.get(id=menuitem_id).restaurant
        
    def __unicode__(self):
        return '%s|%s' % (self.userprofile,self.code)