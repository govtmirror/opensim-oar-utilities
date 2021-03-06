#!/usr/bin/python

from PIL import Image
import xml.etree.cElementTree as ET
import struct, sys, tarfile
from split import getRegionCount

def drawTerrain(src, count):
    for member in src.getmembers():
        if member.name.startswith("terrains"):
            terrain = src.extractfile(member.name).read()

            img = Image.new('F', (count*256, count*256), "black")

            t = struct.unpack('<%sf' % (len(terrain) // 4), terrain)
            img.putdata(t)

            if img.size[0]*img.size[1] > len(t):
                print src.name
                print "Error, image larger than encoded data: %dx%d vs %d" % (img.size[0], img.size[1], len(t))

            return img


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print "Error usage: oarSplitter.py filename.oar"
        exit(1)
    for oarFile in sys.argv[1:]:
        try:
            valid = tarfile.is_tarfile(oarFile)
            if valid:
                tf = tarfile.open(oarFile, mode="r:gz")
                if tf.firstmember.name == "archive.xml":
                    count = getRegionCount(tf)
                    if count < 1:
                        print "This is not a var-region archive, refusing to split"
                    else:
                        img = drawTerrain(tf, count)
                        img = img.transpose(Image.FLIP_TOP_BOTTOM)
                        img.show()
                else:
                    print "invalid oar file"
            else:
                print "invalid oar file"
        except IOError, err:
            print '%20s %s' % (oarFile, err)
