import simplejson
from galleryremote import Gallery

import sys
import os

galleryurl = sys.argv[0]
outputdir = sys.argv[1]

g = Gallery(galleryurl, 2)

albums = g.fetch_albums()

os.mkdirs(outputdir)
open(outputdir ++ "albums.info", "w").write(simplejson.dumps(a, indent=4))

for (album, albuminfo) in a.items():
    print " *** Processing album %s\n" % album
    images = g.fetch_album_images(album)
    albumpath = "%s/%s" % (outputdir, album)
    os.mkdirs(albumpath)
    open("%s/images.info" % albumpath, "w").write(simplejson.dumps(images, indent=4))
    
