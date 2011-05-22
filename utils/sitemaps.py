from django.contrib.sitemaps import Sitemap
from django.core import urlresolvers
from datetime import datetime

URLMAP = {
          'homepage':'/',
          'homefood':'/homefood/',
          'restaurants':'/restaurants/',
          'messfood':'/messfood/',
          'aboutus':'/site_media/flat/aboutus.html',
          'contactus':'/contactus/',
          'terms':'/site_media/flat/terms.html',
          'privacy':'/site_media/flat/privacy.html'
          }

class ServicesSitemap(Sitemap):
    priority = 0.8
    lastmod = datetime(day=11,month=11,year=2008)
    changefreq = 'weekly'
    
    def items(self):
        return ['homefood','restaurants','messfood']
    
    def location(self,key):
        return URLMAP[key]

class HomepageSitemap(Sitemap):
    priority = 0.9
    lastmod = datetime(day=11,month=11,year=2008)
    changefreq = 'daily'
    
    def items(self):
        return ['homepage',]
    
    def location(self,key):
        return URLMAP[key]
    
class StaticPageSitemap(Sitemap):    
    priority = 0.6
    lastmod = datetime(day=11,month=11,year=2008)
    changefreq = 'weekly'
    
    def items(self):
        return ['aboutus','contactus','terms','privacy']
    
    def location(self,key):
        return URLMAP[key]

sitemaps ={
          'services':ServicesSitemap,
          'home':HomepageSitemap,
          'staticpages':StaticPageSitemap,
          }