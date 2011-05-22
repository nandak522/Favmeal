from django.core.management.base import NoArgsCommand

from optparse import make_option

class Command(NoArgsCommand):
    option_list = NoArgsCommand.option_list 
    help = "########### Imports the list of food items corresponding to one and only one particular restaurant, from a csv file ##############"
    requires_model_validation = True

    def handle_noargs(self, **options):
        import csv
        csvreader = csv.reader(open('/work/favmeal_trunk/thirty_six_jubilee_hills.csv'))
        currow = csvreader.next()#header should be skipped
        currow = csvreader.next()
        passed = []
        missed = []
        while currow:
            print 'creating:%s' % (str(currow))
            restaurant_name = currow[0]
            from restaurants.models import Restaurant
            restaurant = Restaurant.objects.get(name=restaurant_name.strip())
            item_name= currow[1]
            item_price = currow[2]
            item_type = currow[3]
            item_tags = currow[4]
            fooditem = self._create_fooditem(item_name,item_type,item_tags)
            menuitem = self._assign_fooditem_to_restaurant(restaurant,fooditem,int(item_price))
            print 'created:%s item_type:%s item_tags:%s' % (item_name,item_type,str(item_tags))
            passed.append(menuitem)
            try:
                currow = csvreader.next()
            except Exception,e:
                print 'Exception while importing:%s' % e
                missed.append(item_name)
                break
        print 'passed:%s' % len(passed)
        print 'missed:%s' % len(missed)
        print 'missed:%s' % missed
        return None
    
    def _create_fooditem(self,name,type,tag_names):
        tags = []
        for tag_name in tag_names.split(','):
            from restaurants.models import FoodItemTag
            tag = FoodItemTag.objects.create_fooditemtag(name=tag_name)
            tags.append(tag)
        from restaurants.models import FoodItem
        fooditem = FoodItem.objects.create_fooditem(name=name, type=type,tags=tags)
        return fooditem
    
    def _assign_fooditem_to_restaurant(self,restaurant,item,cost):
        from restaurants.models import RestaurantMenuItem
        restaurant_menuitem = RestaurantMenuItem.objects.create_restaurant_menuitem(restaurant=restaurant, item=item, cost=cost)
        return restaurant_menuitem