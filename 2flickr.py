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
    print "\n *** Processing album %s" % album
    images = simplejson.loads(open("%s/%s/images.info" % (scandir, album), "r").read())
    print "%d total images" % len(images)
    for imageidx in range(0, len(images)):
        image = images[imageidx]
        if 'flickrid' in image:
            print "Image %s already uploaded with id %s" % \
                (image['name'], image['flickrid'])
        else:
            print image['title']
            print image['caption'] + ' ' + image['description']
            print "%s/%s/%s.data" % (scandir, album, image['name'])
            print 'fromgallery galleryid:%s gallerylbumid:%s' % (image['name'], album)
            r = flickr.upload(filename = ("%s/%s/%s.data" % (scandir, album,
                                                            image['name'])).encode('utf-8'),
                              title = image['title'],
                              description = image['caption'] + ' ' + 
                                            image['description'],
                              tags = 'fromgallery galleryid:%s galleryalbumid:%s' %
                                     (image['name'], album))
            image['flickrid'] = r.photoid[0].text
            images[imageidx] = image
            print "Image %s uploaded with id %s" % \
                (image['name'], image['flickrid'])
            writefd = open("%s/%s/images.info" % (scandir, album), "wt")
            writefd.write(simplejson.dumps(images, indent = 4))
            writefd.close()
        # uploaded image
        
    r = flickr.photosets_create(title=album['title'],
                                description=album['summary'])
    
