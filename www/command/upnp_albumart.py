#!/usr/bin/python3
# Copyright (C) 2021 J.F.Dockes. License: MIT

#
# Retrieve the album art URI from an openhome or UPnP/AV renderer.
#
# 2021-01-16 Tim Curtis:
# - Change 0S._exit() to sys.exit()
#

import sys
import os
import upnpp
import urllib.parse

def debug(x):
    print("%s" % x, file = sys.stderr)

def usage():
    prog = os.path.basename(__file__)
    debug("Usage: %s devname" % prog)
    sys.exit(1)


def artFromMeta(metadata):
    dirc = upnpp.UPnPDirContent()
    dirc.parse(metadata)
    if dirc.m_items.size():
        dirobj = dirc.m_items[0]
        if "upnp:albumArtURI" in dirobj.m_props:
            o = urllib.parse.urlsplit(dirobj.m_props["upnp:albumArtURI"])
            url_escaped = urllib.parse.ParseResult(o.scheme, o.netloc, urllib.parse.quote(o.path), "", "", "").geturl()
            print("%s" % url_escaped)
            sys.exit(0)


def artFromOHInfo(service):
    # Prefer metatext as this will get the dynamic art if a radio is playing
    retdata = upnpp.runaction(service, "Metatext", [])
    if retdata and "Value" in retdata:
        artFromMeta(retdata["Value"])
    # Else try Track which will yield current playlist track or static radio data
    retdata = upnpp.runaction(service, "Track", [])
    if retdata and "Metadata" in retdata:
        artFromMeta(retdata["Metadata"])


def artFromAVTransport(service):
    retdata = upnpp.runaction(service, "GetPositionInfo", ["0"])
    if retdata and "TrackMetaData" in retdata:
        artFromMeta(retdata["TrackMetaData"])


if len(sys.argv) != 2:
    usage()
devname = sys.argv[1]

log = upnpp.Logger_getTheLog("stderr")
log.setLogLevel(0)

service = upnpp.findTypedService(devname, "Info", True)
if service:
    artFromOHInfo(service)
service = upnpp.findTypedService(devname, "AVTransport", True)
if service:
    artFromAVTransport(service)

sys.exit(0)

