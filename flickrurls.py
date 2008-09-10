import simplejson, flickrapi

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
    print "\n *** Processing album %s" % album
    images = simplejson.loads(open("%s/%s/images.info" % (scandir, album), "r").read())
    print "%d total images" % len(images)
    for imageidx in range(0, len(images)):
        image = images[imageidx]
        print "Image %s" % image['caption']
        r = flickr.photos_getInfo(photo_id = image['flickrid'])
        images[imageidx]['flickrpage'] = r.photo[0].urls[0].url[0].text

        r = flickr.photos_getSizes(photo_id = image['flickrid'])
        for item in r.sizes[0].size:
            if item['label'] == 'Original':
                images[imageidx]['flickrimg'] = item['source']
        if not (flickrimg in images[imageidx]):
            print "No original URL found for image!"
            sys.exit(1)
    open("%s/%s/images.info" % (scandir, album), "wt").write(simplejson.dumps(images, indent = 4))
    
