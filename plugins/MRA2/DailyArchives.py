#!/usr/bin/python

import sys
import os
import time

#import shlex
#import subprocess

'''
    Method : system_or_die

    Description : Method to call shell scripts
'''
def system_or_die(command):
    print command
    #call_params = shlex.split(command)
    #res = subprocess.call(call_params, shell=True)
    res = os.system(command)
    if res != 0:
        print "ERROR: Execution of (", command, ") failed with error code ", res, "\n"
        #sys.exit(2)

try:
    WORKSPACE_DIR = os.environ["WORKSPACE"]
    try:
        s = os.environ["AdditionalFolderName"]
        WORKSPACE_DIR = WORKSPACE_DIR + "/" + os.environ["AdditionalFolderName"]
    except:
        pass
    WORKSPACE_DIR = WORKSPACE_DIR.replace("(","\\(").replace(")","\\)").replace(" ","\\ ")
    os.chdir(WORKSPACE_DIR)
    if WORKSPACE_DIR[-1] != '/' and WORKSPACE_DIR[-1] != '\\':
        WORKSPACE_DIR = WORKSPACE_DIR + "/"
except KeyError:
    print "WORKSPACE environment variable is not set"
    WORKSPACE_DIR = ""

try:
    BUILD_NAME = os.environ["BUILD_NAME"]
except KeyError:
    print "BUILD_NAME environment variable is not set"
    BUILD_NAME = ""


if os.path.isdir("resources/dependencies/MRA2/MRA2_monolith"):
    system_or_die("sudo 7zr u -m0=lzma2:d=1m:mt=12 -mx=0  -ms=100f512m -y artifacts/" + BUILD_NAME + "_Sources.7z resources/dependencies/MRA2/MRA2_monolith > /dev/null")
else:
    print "not found", WORKSPACE_DIR, "resources/dependencies/MRA2/MRA2_monolith"

if os.path.isdir("resources/dependencies/MRA2/BSP"):
    system_or_die("sudo 7zr u -m0=lzma2:d=1m:mt=12 -mx=0  -ms=100f512m -y artifacts/" + BUILD_NAME + "_Sources.7z resources/dependencies/MRA2/BSP > /dev/null")
else:
    print "not found", WORKSPACE_DIR, "resources/dependencies/MRA2/BSP"

if os.path.isdir("resources/configuration"):
    system_or_die("sudo 7zr u -m0=lzma2:d=1m:mt=12 -mx=0  -ms=100f512m -y artifacts/" + BUILD_NAME + "_Sources.7z resources/configuration > /dev/null")
else:
    print "not found", WORKSPACE_DIR, "resources/configuration"

if os.path.isdir("resources/dependencies/drive-t186ref-linux/out"):
    system_or_die("sudo 7zr u -m0=lzma2:d=1m:mt=12 -mx=0  -ms=100f512m -y artifacts/" + BUILD_NAME + "_Sources.7z resources/dependencies/drive-t186ref-linux/out > /dev/null")
else:
    print "not found", WORKSPACE_DIR, "resources/dependencies/drive-t186ref-linux/out"
system_or_die("cp -rf")
system_or_die("sudo 7zr u -m0=lzma2:d=1m:mt=12 -mx=0  -ms=100f512m -y   -x\!Tools/Autogrator/resources/ -x\!Tools/ComaTestGen/ artifacts/" + BUILD_NAME + "_Sources.7z ./SourceSpace ./DeliSpace ./Tools ./CI.BuildSystem ./BunnyBuildingWorkspace ./WorkspaceSettings.set ./UserSettings.txt > /dev/null")

system_or_die("sudo tar -czf artifacts/IF1.tar.gz SourceSpace/IF1/*")
system_or_die("sudo tar -czf artifacts/MRA2.tar.gz SourceSpace/MRA2/*")
system_or_die("sudo tar -czf artifacts/PlatformOnOff.tar.gz SourceSpace/PlatformOnOff/*")
