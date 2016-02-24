#!/usr/bin/env python

import scraperwiki
import requests
import lxml.html
import re

#Copy and paste a column from excel within the ''' markers to create a variable
pastedfromexcel = '''https://instagram.com/explore/locations/268366
https://instagram.com/explore/locations/214928
https://instagram.com/explore/locations/227381507
https://instagram.com/explore/locations/215120477
https://instagram.com/explore/locations/211441764
https://instagram.com/explore/locations/1005550884
https://instagram.com/explore/locations/219234043
https://instagram.com/explore/locations/213057678
https://instagram.com/explore/locations/216982612
https://instagram.com/explore/locations/227939512
https://instagram.com/explore/locations/241481920
https://instagram.com/explore/locations/1606049
https://instagram.com/explore/locations/130684996
https://instagram.com/explore/locations/223282394
https://instagram.com/explore/locations/250447165
https://instagram.com/explore/locations/399873
https://instagram.com/explore/locations/5026
https://instagram.com/explore/locations/4635724
https://instagram.com/explore/locations/213023829
https://instagram.com/explore/locations/215088470
https://instagram.com/explore/locations/116160'''

#This then splits that variable on each carriage return, to create a list of usernames
picurllist = pastedfromexcel.split('\n')
baseurl = 'https://www.instagram.com/explore/locations/'

#Here we define a function which uses the username as an argument
def grabfollows(userurl):
    #create the full URL by joining the username to the baseurl
    #userurl = baseurl+picurl
    print "SCRAPING", userurl
    #scrape it into 'html'
    #THIS GENERATES AN ERROR IF THE URL HAS DISAPPEARED
    html = scraperwiki.scrape(userurl)
    #convert it to an lxml object
    root = lxml.html.fromstring(html)
    print root
    #grab meta tag with name attribute as specified
    meta = root.cssselect('meta[name="description"]')
    #grab content= value
    print "META", meta[0].attrib.get('content')
    description = meta[0].attrib.get('content')
    #grab anything in <script> tags
    headers = root.cssselect('script')
    #the 7th one (index 6) has what we need
    profiledata = headers[6].text
    print profiledata
    #split the contents of that tag in three, grab the second part (after the first mention of nodes)
    recentposts = profiledata.split('"nodes":')[1]
    print "nodes", len(recentposts)
    pics = recentposts.split('"code":"')
    latlng = profiledata.split('"lat":')
    print "pics", len(pics)
    print "geo", latlng[1]
    lat = latlng[1].split(',')[0]
    lng = latlng[1].split('"lng":')[1].split(',')[0]
    print "LATLNG", lat, lng
    record['lat'] = lat
    record['lng'] = lng
    record['userurl'] = userurl
    print record
    #save the whole thing, with username as the unique key
    scraperwiki.sql.save(['userurl'], record)
    '''for pic in pics[1:-1]:
        print "PIC", pic
        picurlid = pic.split('"')[0]
        print picurlid
        ownerid = pic.split('"owner":{"id":"')[1].split('"}')[0]
        if len(pic.split('"owner":{"id":"'))>1:
            comments = pic.split('comments":{"count":')[1].split('}')[0]
        else:
            comments = "NO COMMENTS"
        if len(pic.split('caption":'))>1:
            caption = pic.split('caption":')[1].split('}')[0]
            likes = caption.split('likes":')[1].split('}')[0].replace('{"count":','')
        else:
            caption = "NO CAPTION"
            likes = pic.split('likes":')[1].split('}')[0].replace('{"count":','')
        date = pic.split('date":')[1].split(',')[0]
        isvideo = pic.split('is_video":')[1].split(',')[0]
        print ownerid, comments, caption, likes, date, isvideo
        #create the fields in our dictionary, and assign variables to those
        record['ownerid'] = ownerid
        record['comments'] = comments
        record['likes'] = likes
        record['caption'] = caption
        record['date'] = date
        record['isvideo'] = isvideo
        record['picurlid'] = picurlid
        record['description'] = description
        record['userurl'] = userurl
        print record
        #save the whole thing, with username as the unique key
        scraperwiki.sql.save(['picurlid'], record)'''

#create an empty record (this will be filled when the function runs above)
record = {}
#loop through our username list
for picurl in picurllist:
    #run the function defined above on each username
    grabfollows(picurl)

#picurl = '-0ICf6gPdN/'
#grabfollows(picurl)
#html = requests.get(picurl)
#print html.content

# Saving data:



