import simplejson
import re

import sys, os

scandir = sys.argv[1]
csvpaths = sys.argv[2]

albums = simplejson.loads(open(scandir + "/albums.info", "r").read())

csv = {}
for line in open(csvpaths, "rt").readlines():
    line = line.strip()
    r = re.search(r"^(\d+),(.+)$", line).groups()
    csv[r[0]] = r[1]

for (album, albuminfo) in albums.items():
    print "\n\n# Album %s: %s" % (album, albuminfo['title'])
    if ['flickrurl'] in albuminfo:
        if album in csv:
            print "RewriteRule ^/v/%s($|/$) %s" % \
                (csv[album], albuminfo['flickrurl'])
        else:
            print "## FIXME: No CSV for album %s: %s" % \
                (album, albuminfo['title'])
    else:
        print "## FIXME: No Flickr URL for album!"

