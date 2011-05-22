from django.conf.urls.defaults import *
from django.contrib import admin
from settings import FAVMEAL_MEDIA_ROOT
from django.contrib import databrowse
from users.models import UserProfile
from restaurants.models import FoodItem,FoodItemTag,Restaurant,RestaurantMenuItem

from django.contrib.syndication.feeds import Feed

admin.autodiscover()
databrowse.site.register(UserProfile)
databrowse.site.register(FoodItem)
databrowse.site.register(FoodItemTag)
databrowse.site.register(Restaurant)
databrowse.site.register(RestaurantMenuItem)

handler404 = 'utils.views.handle404'

from utils.sitemaps import sitemaps

class RestaurantFeed(Feed):
	title = "All New Restaurants"
	link = "/restaurantnews/"
	description = "Updates on changes and additions to chicagocrime.org."
	
	def item_link(self,rest_item):
		return 'http://127.0.0.1:8000/restfeeds/%s/' % rest_item.id
	
	def items(self):
		return Restaurant.objects.order_by('-created_on')[:5]

restaurants_feeds = {'latest':RestaurantFeed}

urlpatterns = patterns('',
		       (r'^djangoadmin/(.*)', admin.site.root),
		       (r'^databrowse/(.*)', databrowse.site.root),
		       (r'^site_media/(?P<path>.*)$', 'django.views.static.serve', {'document_root': FAVMEAL_MEDIA_ROOT}),
		       (r'^sitemaps.xml$', 'django.contrib.sitemaps.views.sitemap', {'sitemaps': sitemaps}),
		       (r'^restfeeds/(?P<url>.*)/$', 'django.contrib.syndication.views.feed', {'feed_dict': restaurants_feeds}),
)
urlpatterns += patterns('common.common_views',
					    (r'^contactus/$','view_contactus',{'homepage_template':'homepage.html','contactus_template':'contactus.html'},'contactus'),
					    (r'^invite/$','view_refer_friend',{'referfriend_template':'referfriend.html'},'referfriend'),
)

urlpatterns += patterns('users.registration_views',
					    (r'^register/$','view_register',{'homefood_registration_template':'homefood/homefood_registration.html','restaurantfood_registration_template':'restaurants/restaurants_registration.html','messfood_registration_template':'messfood/messfood_registration.html'},'register'),
					    (r'^checkemail/$', 'view_checkemail',{},'checkemail'),
)
urlpatterns += patterns('users.authentication_views',
					    (r'^login/$','view_login',{'login_template':'users/login.html'},'login'),
					    (r'^logout/$', 'view_logout',{},'logout'),
)

urlpatterns += patterns('users.users_views',
                       (r'^$', 'view_homepage',{'homepage_template':'homepage.html'},'homepage'),
                       (r'^account/$', 'view_account',{'account_template':'users/account.html'},'account'),
                       (r'^passwordreset/$', 'view_reset_password',{'passwordreset_template':'users/passwordreset.html'},'passwordreset'),                       
                       (r'^savetodaysfood/$','view_save_todaysfood',{},'save_todaysfood'),
                       (r'^allusers/$','view_show_registeredusers',{'userslist_template':'users/allusers.html'},'allusers'),
                       (r'^myorders/$','view_myorders',{'userorders_template':'users/myorders.html'},'myorders'),
                       (r'^allorders/$','view_allorders',{'allorders_template':'users/allorders.html'},'allorders'),
                       (r'^orderdetails/$','view_orderdetails',{'orderdetails_template':'users/orderdetails.html'},'orderdetails')
)
urlpatterns += patterns('homefood.views',
                       (r'^homefood/$', 'view_homefood',{'homefood_registration_template':'homefood/homefood_registration.html','homefood_template':'homefood/homefood.html'},'homefood'),
)
urlpatterns += patterns('restaurants.views',
					    (r'^restaurants/$','view_restaurants',{'restaurants_registration_template':'restaurants/restaurants_registration.html','restaurants_template':'restaurants/restaurants.html'},'restaurantfood'),
					    (r'^restaurants/(?P<ralias>([a-zA-Z0-9-])+)/$','view_restaurantmenu',{'restaurantmenu_template':'restaurants/restaurantmenu.html'}),
					    (r'^orderconfirm/$','view_orderconfirm',{'ordercofirm_template':'restaurants/orderconfirm.html'}),
					    (r'^orderdelete/$','view_orderdelete',{},'orderdelete'),
					    (r'^computedeliverytime/$','view_computedeliverytime',{'deliverytime_template':'restaurants/deliverytime.html'},'computedeliverytime'),
					    (r'^makeorder/$','view_makeorder',{},'makeorder'),
					    (r'^ordersummary/$','view_ordersummary',{'orderdone_template':'restaurants/ordersummary.html'},'ordersummary'),
)
urlpatterns += patterns('messfood.views',
                       (r'^messfood/$', 'view_messfood',{'messfood_registration_template':'messfood/messfood_registration.html','messfood_template':'messfood/messfood.html'},'messfood'),
                       (r'^messfood/createmess/$', 'view_createmess',{},'createmess'),
)
urlpatterns += patterns('django.views.generic.simple',
    ('^checkout/$', 'redirect_to', {'url': '/restaurants/checkout/'}),
)
urlpatterns += patterns('users.views',
					    (r'^dashboard/$','view_userdashboard',{'userdashboard_template':'users/dashboard.html'},'userdashboard'),
)
urlpatterns += patterns('tracks.views',
					    (r'^routes/$','view_routes',{'routes_template':'tracks/routes.html'},'routesdashboard'),
)


