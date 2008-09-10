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
        
    if 'flickrid' in albums[album]:
        print "Using existing photoset with id %s" % albums[album]['flickrid']
    else:
        r = flickr.photosets_create(title=albums[album]['title'],
                                    description=albums[album]['summary'],
                                    primary_photo_id=images[0]['flickrid'])
        albums[album]['flickrid'] = r.photoset[0]['id']
        albums[album]['flickrurl'] = r.photoset[0]['url']
        writefd = open("%s/albums.info" % scandir, "w")
        writefd.write(simplejson.dumps(albums, indent=4))
        writefd.close()
        print "Created photoset for album %s at %s" % (albums[album]['title'], albums[album]['flickrurl'])
        
    print "len(images) = %d" % len(images)

    for image in images[1:]:
        flickr.photosets_addPhoto(photoset_id = albums[album]['flickrid'],
                                  photo_id = image['flickrid'])
        print "Added image %s to set" % image['name']
