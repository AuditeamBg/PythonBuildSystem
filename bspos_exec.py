#!/usr/bin/python

# System level includes
import os
import sys
from subprocess import call

#setting the script root

try:
    os.environ[SCRIPT_ROOT]
except:
    os.environ["SCRIPT_ROOT"] = os.path.dirname(os.path.abspath(sys.argv[0]))

# Local module includes
import bspos_build
from bspos_build import bspos

#import bitbake
sys.path.append( os.environ['SCRIPT_ROOT'] + "/plugins/bitbake")
import bitbake
from bitbake import bitbake

#import baserock
sys.path.append( os.environ['SCRIPT_ROOT'] + "/plugins/baserock")
from baserock import Baserock

#import MRA2
sys.path.append( os.environ['SCRIPT_ROOT'] + "/plugins/MRA2")
import MRA2
from MRA2 import MRA2

os.environ["ARCHIVING"] = sys.argv[1]

import MRA2_APIBuns
from MRA2_APIBuns import MRA2_APIBuns


'''
Created on Sep 8, 2014

@author: Zhivko Zapryanov; Georgi Zahariev

This is an entry point for the bsp os jenkins build
'''

def main():

    try:
        system = os.environ['Machine']
    except KeyError:
        print("Please set the 'Machine' variable requared for Jenkins build \n")
        system = " Error:variable_not_found_in_environment "
        #sys.exit(2)
    try:
        build_id = os.environ['BUILD_ID']
    except KeyError:
        print("Please set the 'BUILD_ID' variable requared for Jenkins build \n")
        build_id = " Error:variable_not_found_in_environment "
        #sys.exit(2)
    try:
        node_label = os.environ['NODE_LABELS']
    except KeyError:
        print("Please set the 'NODE_LABELS' variable requared for Jenkins build \n")
        node_label = " Error:variable_not_found_in_environment "
        #sys.exit(2)
    try:
        sdk_type = os.environ['SDKType']
    except KeyError:
        print("Please set the 'SDKType' variable requared for Jenkins build \n")
        sdk_type = " Error:variable_not_found_in_environment "
        #sys.exit(2)

    # We need to determinate the build type here for now we have only Baserock, MFA2 and Bitbake
    if "bitbake" in node_label:
        # If we have bitbake build init the bitbake object
        print "Starting Bitbake build\n"
        # TODO: handle the error properly
        BSP_OS = bitbake(system, build_id, sdk_type)

    elif "MRA2" in node_label:
        # If we have MFA2 build init the MFA2 object
        print "Starting MRA2 build\n"
        # TODO: handle the error properly
        BSP_OS = MRA2(system, build_id, sdk_type)



    # 1. Init the build workspace
    # TODO: handle the error properly
    if os.environ["ARCHIVING"] == "initialiazation":
        print "Workspace initialiazation\n"
        BSP_OS.workspace_init()

    # 1.1.0 prep the build workspace
    # TODO: handle the error properly
    #print "Workspace prep \n"
    if os.environ["ARCHIVING"] == "initialiazation":
        BSP_OS.prebuild()

    # 2. Start the build
    # TODO: handle the error properly
    if os.environ["ARCHIVING"] == "false":
        BSP_OS.build()


    # 2.1 populate_results
    # TODO: handle the error properly
    if os.environ["ARCHIVING"] == "true":
        print "Starting bsp os populate_results\n"
        BSP_OS.populate_results()

    # 2.2 Start the build
    # TODO: handle the error properly
    if os.environ["ARCHIVING"] == "true":
        print "Starting bsp os create_images\n"
        BSP_OS.create_images()


    # 3. Perform post processing
    # TODO: handle the error properly
    if os.environ["ARCHIVING"] == "true":
        print "Performing post processing\n"
        BSP_OS.post_processes()

if __name__ == '__main__':
    main()
