import simplejson
from galleryremote import Gallery

import sys
import os
import urllib

galleryurl = sys.argv[1]
outputdir = sys.argv[2]

print galleryurl

g = Gallery(galleryurl, 2)

albums = g.fetch_albums()

os.mkdir(outputdir)
open(outputdir + "albums.info", "w").write(simplejson.dumps(albums, indent=4))

for (album, albuminfo) in albums.items():
    print " *** Processing album %s\n" % album
    images = g.fetch_album_images(album)
    albumpath = "%s/%s" % (outputdir, album)
    os.mkdir(albumpath)
    open("%s/images.info" % albumpath, "w").write(simplejson.dumps(images, indent=4))
    for image in images:
        print "Downloading image " + image['name']
        urllib.urlretrieve(galleryurl +
                           "/main.php?g2_view=core%3ADownloadItem&g2_itemId=" +
                           image['name'],
                           albumpath + "/" + image['name'] + ".data")
