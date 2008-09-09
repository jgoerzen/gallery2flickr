import simplejson
import flickrapi

import sys, os, urllib

flickrapikey = sys.argv[1]
flickrapisecret = sys.argv[2]
scandir = sys.argv[3]

flickr = flickrapi.FlickrAPI(flickrapikey, flickrapisecret)

(token, frob) = flickr.get_token_part_one(perms='write')
if not token: raw_input("Press ENTER after you authorized this program")
flickr.get_token_part_two((token, frob))

albums = simplejson.loads(open(scandir + "/albums.info", "r").read())
for (album, albuminfo) in albums.items():
    print " *** Processing album %s" % album
    
