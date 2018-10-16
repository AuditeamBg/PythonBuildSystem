#!/usr/bin/python

import os
import urllib2
import urlparse
import sys

def nonblank_lines(f):
    for l in f:
        line = l.rstrip()
        if line:
            yield line
def main():
    try:
        buildUrl = os.environ["BUILD_URL"]
        buildId = os.environ["SOURCE_BUILD_NUMBER"]
        envFile = "injectedEnvVars/export"
        envUrl = buildUrl + envFile
        url = urlparse.urlparse(envUrl)
        path = url.path
        p = path.split(os.sep)
        l = len(p)
        p[l-3] = buildId
        first = '/'
        newlist = [first] + p
        d = os.path.join(*newlist)
        newUrl = url._replace(path=d)
        print(newUrl)
        newBuildUrl = newUrl.geturl()
    except KeyError:
        print("Missing environment variables. Old environment variables could not be set")
        sys.exit()

    try:
        u = urllib2.urlopen(newBuildUrl)

        for lines in nonblank_lines(u):
            x = lines.split("=")
            print("Setting %s variable to %s value" % ( x[0],x[1]))
            os.environ[x[0]] = x[1]
            print(x[0])
    except urllib2.URLError:
        print("File does not exists using the new environment")
    del os.environ["BUILD_ID"]

if __name__ == '__main__':
    main()

