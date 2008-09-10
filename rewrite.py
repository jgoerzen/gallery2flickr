import simplejson
import re

import sys, os

scandir = sys.argv[1]
csvpaths = sys.argv[2]
topalbum = "7"

albums = simplejson.loads(open(scandir + "/albums.info", "r").read())

csv = {}

for line in open(csvpaths, "rt").readlines():
    line = line.strip()
    r = re.search(r"^(\d+),(.+)$", line).groups()
    csv[r[0]] = r[1]

for (album, albuminfo) in albums.items():
    print "\n\n######## Album %s: %s" % (album, albuminfo['title'])
    albumlink = "##FIXME"
    if 'flickrurl' in albuminfo:
        if album in csv:
            albumlink = csv[album]
            albumfind = albums[albuminfo['parent']]
            while albumfind['name'] != '7':
                albumlink = csv[albumfind['name']] + '/' + albumlink
                albumfind = albums[albumfind['parent']]
            print "RewriteRule ^/v/%s($|/$) %sdetail/ [R=permanent,L]" % \
                (albumlink, albuminfo['flickrurl'])
        else:
            print "## FIXME: No CSV for album %s: %s" % \
                (album, albuminfo['title'])
    else:
        print "## FIXME: No Flickr URL for album!"

    images = simplejson.loads(open("%s/%s/images.info" % (scandir, album), "r").read())
    for image in images:
        if image['name'] in csv:
            print "RewriteRule ^/v/%s/%s.html$ %s [R=permanent,L]" % \
                (albumlink, csv[image['name']], image['flickrpage'])
            print "RewriteRule ^/main.php?g2_view=core%%3AShowItem&g2_itemId=%s(&|$) %s [R=permanent,L]" % \
                (image['name'], image['flickrpage'])
            print "RewriteRule ^/d/%s-([0-9]+)/%s$ %s [R=permanent,L]" % \
                (image['name'], csv[image['name']], image['flickrimg'])
            print "RewriteRule ^/main.php?g2_view=core%%3ADownloadItem&g2_itemId=%s(&|$) %s [R=permanent,L]" % \
                (image['name'], image['flickrimg'])
            print ""
        else:
            print "# FIXME: no entry in CSV for image %s" % image['name']

