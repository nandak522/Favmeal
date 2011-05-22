from libs.html_filter import html_filter

_filter = html_filter()
# BEGIN : configure Favmeal supported tags
#flash objects
#_filter.allowed['object'] = ('type','data','width', 'height',)
#_filter.allowed['param'] = ('name', 'value',)
#_filter.allowed['embed'] = ('src', 'type', 'wmode', 'width', 'height',)
##images
#_filter.allowed['img'] = ('src','height','width','border','alt')
## line breaks
#_filter.allowed['br'] = ()
## hyperlinks
#_filter.allowed['a'] = ('href')
## list tags
#_filter.allowed['ol'] = ()
#_filter.allowed['ul'] = ()
#_filter.allowed['li'] = ()
##paragraph
#_filter.allowed['p']  = ('align')
##bold
#_filter.allowed['b'] = ()
#_filter.allowed['strong'] = ()
#_filter.allowed['u'] =()
#_filter.allowed['i'] =()
#_filter.allowed['strike']= ()
#_filter.allowed['blockquote']=()
##table
#_filter.allowed['table']  = ('align','width','height','border','valign','bgcolor')
#_filter.allowed['tbody'] = ()
#_filter.allowed['tr'] = ('width','height','bgcolor')
#_filter.allowed['td'] = ('width','height','colspan','rowspan','bgcolor')

_filter.allowed={}
#_filter.no_close += ('br',)

#_filter.protocol_attributes += ('value',)


#_filter.make_clickable_urls= True
# END : configure Orglex supported tags
#_filter.break_words_longer_than = 30



def break_text(text):
    return _filter.break_words(text)

def clean(input,foremail=False):
    cleaned_text= _filter.go(input)
    if foremail:
        cleaned_text = clean_entities(cleaned_text)
    return cleaned_text

def clean_entities(cleaned_text):
    cleaned_text = cleaned_text.replace('&nbsp;',' ')
    cleaned_text = cleaned_text.replace('&quot;','"')
    cleaned_text = cleaned_text.replace('&lt;','<')
    cleaned_text = cleaned_text.replace('&gt;','>')
    cleaned_text = cleaned_text.replace('&gt;','>')
    cleaned_text = cleaned_text.replace('&gt;','>')
    cleaned_text = cleaned_text.replace('&#8722;','-')
    cleaned_text = cleaned_text.replace('&#8217;','\'')
    cleaned_text = cleaned_text.replace('&#8216;','\'')
    cleaned_text = cleaned_text.replace('&#8220;','"')
    cleaned_text = cleaned_text.replace('&#8221;','"')
    numens={'&#32;':' ','&#33;':'!','&#34;':'\"','&#35;':'#','&#36;':'$','&#37;':'%','&#38;':'&','&#39;':'\'','&#40;':'(','&#41;':')','&#42;':'*','&#43;':'+','&#44;':',','&#45;':'-','&#46;':'.','&#47;':'/','&#48;':'0','&#49;':'1','&#50;':'2','&#51;':'3','&#52;':'4','&#53;':'5','&#54;':'6','&#55;':'7','&#56;':'8','&#57;':'9','&#58;':':','&#59;':';','&#60;':'<','&#61;':'=','&#62;':'>','&#63;':'?','&#64;':'@',}
    for nentity in numens.keys():
        cleaned_text = cleaned_text.replace(nentity,numens[nentity])
    ignoreentities=['&OElig;','&#338;','&oelig;','&#339;','&Scaron;','&#352;','&scaron;','&#353;','&Yuml;','&#376;','&circ;','&#710;','&tilde;','&#732;','&ensp;','&#8194;','&emsp;','&#8195;','&thinsp;','&#8201;','&zwnj;','&#8204;','&zwj;','&#8205;','&lrm;','&#8206;','&ndash;','&#8211;','&mdash;','&#8212;','&lsquo;','&#8216;','&rsquo;','&#8217;','&sbquo;','&#8218;','&ldquo;','&#8220;','&rdquo;','&#8221;','&bdquo;','&#8222;','&dagger;','&#8224;','&Dagger;','&#8225;','&hellip;','&#8230;','&permil;','&#8240;','&lsaquo;','&#8249;','&rsaquo;','&#8250;','&euro;','&#8364;']
    for entity in ignoreentities:
        cleaned_text = cleaned_text.replace(nentity,'')
    return cleaned_text


def clean_html_tags(input):
    from HTMLParser import HTMLParseError
    try:
        return _filter.strip_tags(input)
        print 'Problem in Stripping Tags'
    except HTMLParseError,e:
        return _filter.strip_tags(_filter.go(input))

def clean_restrictions(input):
    return _plainfilter.go(input)


##############
# Custom method not fool proof
###############
def clean_html(description):
    import re
    description = re.sub('<([^!>]([^>]|\n)*)>', '', description)
    description = description.replace('&nbsp;',' ')
    description = description.replace('&quot;','"')
    description = description.replace('&lt;','<')
    description = description.replace('&gt;','>')
    description = description.replace('&gt;','>')
    description = description.replace('&gt;','>')
    description = re.sub('&#[a-zA-Z0-9]+;','',description)
    return description
 



def make_video_links(text_with_newlines_as_br,conversation):
    import re
    video_link='<div class="share-video"><br><a href="/conversations/email/%s/%s/">Share this video</a></div>' % (str(conversation.id),conversation.alias)
    pattern = re.compile(r'(<embed (.*?)>(.*?)</embed>)')
    text_with_share_link = re.sub(pattern,'\g<0>'+video_link,text_with_newlines_as_br)
    if text_with_newlines_as_br == text_with_share_link:
        pattern = re.compile(r'(<embed (.*?)>(.*?)</embed>)')
        text_with_share_link = re.sub(pattern,'<span style="display:block;">'+'\g<0>'+video_link+'</span>',text_with_newlines_as_br)
    return text_with_share_link

#Fetches full feed entry from the url and looks for external links
#
def process_links(fe,ignorelist=[]):
    from urllib import urlopen
    from re import findall
    alinks=[]
    content = fe.description #urlopen(url).read()
    domain = get_domain(fe.link)
    ignorelist.append(domain)
    pattern = re.compile('<a href=.*?([hH][tT][tT][pP][:][/][/].*?)[ "\'].*?>.*?</a>',re.IGNORECASE|re.MULTILINE|re.DOTALL)
    links = findall(pattern,content)
    for link in links:
            if not match_domain(get_domain(link),domain) and (len(link) < 2500):
                        alinks.append(link)
    return alinks

def plain_url(url):
    if url[0:7] == "http://":
        url = url[7:]
    pairs = url.split('/')
    totaldomain=pairs[0]
    if len(pairs)>1:
        rest = url.split('/')[1]
        if rest:
            return False
    return True

def match_domain(domain1,domain2):
    domain1frags=domain1.split('.')
    domain2frags=domain2.split('.')
    domain1frags.reverse()
    domain2frags.reverse()
    if len(domain1frags) < len(domain2frags):
        length = len(domain1frags)
    else:
        length = len(domain2frags)
    matches = 0
    for i in range(length):
        if domain1frags[i].lower() != domain2frags[i].lower():
            break
        matches+=1
    if matches > 1:
        return True
    return False

def get_domain(url):
    if url[0:7] == "http://":
        url = url[7:]
    totaldomain=url.split('/')[0]
    return totaldomain

#####
# Retrieves all the input type textfields with names like keyprefix1,keyprefix2 and returns their values in list.
######
def process_input_boxes(request,keyprefix,min,max):
    return_list=[]
    for i in range(min,max):
        if _request_param_post(request,keyprefix+str(i)):
            id = _request_param_post(request,keyprefix+str(i)).strip()
            return_list.append(int(id))
    return return_list

from sgmllib import SGMLParser
class HTMLLinkFinder(SGMLParser):
    def reset(self):
        SGMLParser.reset(self)
        self.urls=[]
        self.insideatag=False
        
    def start_a(self,attrs):
        href = [v for (k,v) in attrs if k == 'href']
        if href:
            self.insideatag=True
            self.text=''
            self.link = href[0]
            
    def end_a(self):
        if self.insideatag:
            self.urls.append((self.text,self.link))
            self.insideatag=False
        
    def handle_data(self,text):
        if self.insideatag:
            self.text = text
            
def linkfinder(feedentry):
    import re
    content = feedentry.description+' '+ feedentry.title
    parser = HTMLLinkFinder()
    parser.feed(content)
    parser.close()
    return parser.urls
    
#####################################################
def popular_urls():
    from datetime import datetime,timedelta
    from feeds.models import FeedEntryLink,FeedEntry
    urls={}
    sdays = datetime.now()-timedelta(days=7)
    fes = FeedEntry.objects.filter(created_on__gt=sdays)
    for fe in fes:
        fel=FeedEntryLink.objects.update(fe)
        if fel.forwardlinks.all():
            for link in fel.forwardlinks.all():
                if urls.has_key(link.link):
                    urls[link.link]+=1
                else:
                    urls[link.link] = 1
    items = urls.items()
    items = [(v,k) for (k,v) in items]
    items.sort()
    items.reverse()
    items = [(k,v) for (v,k) in items]
    return items

#####################################################
def clean_ampersands(text):
    if '&' not in text:
        return text
    text = text.replace("&lt;", "<")
    text = text.replace("&gt;", ">")
    text = text.replace("&raquo;", "")
    text = text.replace("&laquo;", "")
    text = text.replace("&apos;", "'")
    text = text.replace("&quot;", '"')
    text = text.replace("&amp;", "&")
    text = text.replace("&nbsp;", " ")
    text = text.replace("&#8217;", "'")
    text = text.replace("&#8212;", "-")
    text = text.replace("&#8211;", "-")
    text = text.replace("&#47;",'/')
    return text

def ripscript(text):
    import re
    pattern = re.compile(r'<script .*?>.*?</script>',re.IGNORECASE|re.MULTILINE|re.DOTALL)
    text=re.sub(pattern,'',text)
    pattern = re.compile(r'<script>.*?</script>',re.IGNORECASE|re.MULTILINE|re.DOTALL)
    text=re.sub(pattern,'',text)
    pattern = re.compile(r'<style .*?>.*?</style>',re.IGNORECASE|re.MULTILINE|re.DOTALL)
    text=re.sub(pattern,'',text)
    pattern = re.compile(r'<style>.*?</style>',re.IGNORECASE|re.MULTILINE|re.DOTALL)
    text=re.sub(pattern,'',text)
    return text

def full_article(feedentry):
    uncleanhtml = ripscript(fetch_article(feedentry))
    #clean_html = clean(uncleanhtml)
    #clean_text = clean_ampersands(clean_html)
    return uncleanhtml

def fetch_article(feedentry):
    import urllib2
    (url,title,description) = (feedentry.link,feedentry.title,feedentry.description[:30])
    content=urllib2.urlopen(url).read()
    block = find_block(content,url,title,description)
    block = clean_block(block)
    return block

def clean_block(content):
    return content

def _unicode(content):
    try:
        content = content.decode('ascii')
        content = unicode(content)
    except UnicodeDecodeError:
        try:
            content = content.decode('latin1')
            content = unicode(content)
        except UnicodeDecodeError,e:
                print e
    return content

def _remove(title):
    els=title.split(' ')
    return " ".join(els[1:])


def find_block(content,url,title,description):
    ucontent = _unicode(content)
    result= _handle_case1(content,url,title,description)
    if result:
        return str(result)
    i=0
    while i<3:
        result= _handle_case1(content,url,_remove(title),description)
        if result:
            return str(result)
        i+=1
    return result

def clean_title(title):
    import re
    words = title.split(' ')
    wordlists=[]
    for word in words:
        alphas = re.findall('[a-z0-9]+',word) 
        if len(alphas)>1:
            break
        else:
            wordlists.append(word)
    return " ".join(wordlists)

def _handle_case1(content,url,title,description):
    from libs.BeautifulSoup import BeautifulSoup as BS
    import re
    parser = BS(content)
    title = clean_title(title)
    locations = parser.body.findAll(text=re.compile(title))
    location = None
    max = 0
    if locations:
        location = _pickup_the_best(locations)
        return str(len(locations))+'::'+str(len(location.fetchParents()))+'::'+str(location.fetchParents()[1])
    return str(len(locations))+'::'+str(location)

def _pickup_the_best(locations):
    filter1=[]
    filter2=[]
    for location in locations:
        filter1=[]
        print '-----------------------------------------------'
        for parent in location.fetchParents():
            print parent.name
            if parent.name in ['td','tr','table','div','p','h1','h2','h3','font','a']:
                if filter1.count(location) ==0 :
                    filter1.append(location)
    if len(filter1):
        return filter1[len(filter1)/2]
    return locations[len(locations)/2]

def addbrs(text):
    return text.replace('\n','<br>')

def _request_param_post(request,key):
    return request.POST.get(key)

def _request_param_get(request,key):
    return request.GET.get(key)

def _extract_params(request,keys):
    from utils.html import _request_param_post,_request_param_get
    params={}
    for key in keys:
        params[key]=''
        if _request_param_post(request,key):
          value = _request_param_post(request,key)
          value = value.strip()
          params[key]=value
    return [params.get(key,'') for key in keys]
