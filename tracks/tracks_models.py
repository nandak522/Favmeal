from django.db import models
from common.models import BaseModel
from utils import name_for_linking

class HaltManager(models.Manager):
    def create_halt(self,name,latitude=None,longitude=None,zip=None):
        alias = name_for_linking(name)
        halt = self.exists(alias=alias)
        if halt:
            return halt
        halt = Halt(name=name,alias=alias,latitude=latitude,longitude=longitude,zip=zip)
        halt.save()
        return halt
    
    def exists(self,alias):
        try:
            return self.get(alias=alias)
        except Halt.DoesNotExist:
            return None
    
class Halt(BaseModel):
    name = models.CharField(max_length=40, blank=False)
    alias = models.CharField(max_length=40,blank=False,unique=True,db_index=True)
    latitude = models.DecimalField(max_digits=12, decimal_places=5,blank=True,null=True)
    longitude = models.DecimalField(max_digits=12, decimal_places=5,blank=True,null=True)
    zip = models.IntegerField(max_length=6, blank=True, null=True) 
    objects = HaltManager()

    def __unicode__(self):
        return self.alias
    
    def position_wrt_route(self,route):
        route = self.route_set.all().get(code=route.code)
        try:
            halt_position = route.routehaltmembership_set.all().get(halt=self).halt_position
        except Exception:
            return None
        return halt_position

class RouteManager(models.Manager):
    def create_route(self,code,halts):
        route = self.exists(code=code)
        if route:
            return route
        route = Route(code=code)
        route.save()
        latest_halt_position = 0
        for halt in halts:
            latest_halt_position += 1
            membership = RouteHaltMembership.objects.create_routehaltmembership(route=route,halt=halt,halt_position=latest_halt_position)
        return route

    def exists(self,code):
        try:
            return self.get(code=code)
        except Route.DoesNotExist:
            return None

class Route(BaseModel):
    code = models.CharField(max_length=4,blank=False,db_index=True)
    halts = models.ManyToManyField(Halt,through='RouteHaltMembership')
    objects = RouteManager()
    
    def latest_halt_position(self):
        route_halts = RouteHaltMembership.objects.filter(route=self).order_by('-halt_position')
        if route_halts:
            return route_halts[0].halt_position
        return 0
    
    def append_halt(self,halt):
        halt_position = self.latest_halt_position() + 1
        try:
            return RouteHaltMembership.objects.create_routehaltmembership(route=self, halt=halt, halt_position=halt_position)
        except Exception,e:
            print 'Exception while appending Halt:%s to Route:%s' % (halt,self)
            return None
    
    def __unicode__(self):
        return self.code
    
    #FIXME:def get_halts_sorted_by_position(self):
#        return []

class RouteHaltMembershipManager(models.Manager):
    def create_routehaltmembership(self,route,halt,halt_position):
        routehalt = self.exists(route=route,halt=halt)
        if routehalt:
            return routehalt
        routehalt = RouteHaltMembership(route=route,halt=halt,halt_position=halt_position)
        routehalt.save()
        return routehalt
    
    def exists(self,route,halt):
        try:
            return self.get(route=route,halt=halt)
        except RouteHaltMembership.DoesNotExist:
            return None
    
class RouteHaltMembership(BaseModel):
    route = models.ForeignKey(Route)
    halt = models.ForeignKey(Halt)
    halt_position = models.IntegerField(default=1,blank=False,max_length=2)
    objects = RouteHaltMembershipManager()
    
    def __unicode__(self):
        return '%s:%s:%s' % (self.route.code,self.halt.alias,self.halt_position)

class VehicleManager(models.Manager):
    def create_vehicle(self,number):
        vehicle = self.exists(number=number)
        if not vehicle:
            vehicle = Vehicle(number=number)
            vehicle.save()
        return vehicle
    
    def exists(self,number):
        try:
            return self.get(number=number)
        except Vehicle.DoesNotExist:
            return None

class Vehicle(BaseModel):
    number = models.CharField(max_length=10,blank=False,unique=True,db_index=True)
    objects = VehicleManager()

    def __unicode__(self):
        return self.number    

class VehicleMeterReadingManager(models.Manager):
    def record_vehiclereading(self,vehicle,start,end):
        reading = self.exists(vehicle=vehicle,start=start,end=end)
        if not reading:
            reading = VehicleMeterReading(vehicle=vehicle,start=start,end=end)
            reading.save()
        return reading
    
    def exists(self,vehicle,start,end):
        try:
            return self.get(vehicle=vehicle,start=start,end=end)
        except VehicleMeterReading.DoesNotExist:
            return None
        
class VehicleMeterReading(BaseModel):
    vehicle = models.ForeignKey(Vehicle)
    start = models.DecimalField(max_digits=10, decimal_places=2,blank=False)
    end = models.DecimalField(max_digits=10, decimal_places=2,blank=False)
    objects = VehicleMeterReadingManager()

    def __unicode__(self):
        return '%s:%s Kms on:%s' % (self.vehicle,self.end-self.start,self.created_on)

class VehicleRouteMembershipManager(models.Manager):
    def create_vehicleroutemembership(self,vehicle,route):
        vehicleroutemembership = self.exists(vehicle=vehicle,route=route)
        if vehicleroutemembership:
            return vehicleroutemembership
        vehicleroutemembership = VehicleRouteMembership(vehicle=vehicle,route=route)
        vehicleroutemembership.save()
        return vehicleroutemembership
    
    def exists(self,vehicle,route):
        try:
            return self.get(vehicle=vehicle,route=route)
        except VehicleRouteMembership.DoesNotExist:
            return None
        
class VehicleRouteMembership(BaseModel):
    vehicle = models.ForeignKey(Vehicle)
    route = models.ForeignKey(Route)
    objects = VehicleRouteMembershipManager()

    def __unicode__(self):
        return '%s:%s' % (self.vehicle,self.route)
