#!/usr/bin/python

import sys
import os
import json
import errno
import subprocess

#setting the script root
try:
    os.environ["SCRIPT_ROOT"]
    sys.path.append( os.environ['SCRIPT_ROOT'] + "/plugins/MRA2")
except:
    os.environ["SCRIPT_ROOT"] = os.path.dirname(sys.argv[0]) + "/../.."
    sys.path.append( os.environ['SCRIPT_ROOT'] + "/plugins/MRA2")

from code_bunnies import code_bunnies
from subprocess import call
from subprocess import check_output

def getBuildVariants():
    '''
    TODO: add more Variants
    '''
    variants=[]
    variants.append("TegraP1Integrity.Rel")
    variants.append("TegraP1Lin.Rel")

    return variants

def perform_build_APIBuns(self, variant):
    #keep this method for future
    workspace = os.getenv("WORKSPACE", None)
    dirpath =workspace+"/IncrementalBuild"
    os.chdir(dirpath)
    os.system("sudo chmod 777 "+dirpath+"/Tools/Bunny/Bunny/bin/BunnyBuild")
    os.system("ll Tools/Bunny/Bunny/bin/BunnyBuild")
    print ("Directory changed successfully %s" % dirpath)
    localVariants = getBuildVariants()
    for lVar in localVariants:
        os.system("./Tools/Bunny/Bunny/bin/BunnyBuild %s %s" % ("IF1.TopBun", lVar))


    print "[perform_build for APIBuns]:Exiting with success!!!"
    exit(0)



def main():
#     variant_env = os.environ["Variant"]
#     perform_build_APIBuns(sys.argv, variant_env)
    workspace = os.getenv("WORKSPACE", None)
    dirpath =workspace+"/IncrementalBuild"
    os.chdir(dirpath)
    os.system("sudo -s")
    os.system("sudo chmod 777 "+dirpath+"/CI.BuildSystem/scripts/MRA2_APIBuns_build.sh")
    os.system("su visteon")
    os.system("./CI.BuildSystem/scripts/MRA2_APIBuns_build.sh")



if __name__ == '__main__':
    main()