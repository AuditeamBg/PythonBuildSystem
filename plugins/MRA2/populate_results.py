#!/usr/bin/python

import sys
import os
import json
import errno

#setting the script root
try:
    os.environ["SCRIPT_ROOT"]
    sys.path.append( os.environ['SCRIPT_ROOT'] + "/plugins/MRA2")
except:
    os.environ["SCRIPT_ROOT"] = os.path.dirname(sys.argv[0]) + "/../.."
    sys.path.append( os.environ['SCRIPT_ROOT'] + "/plugins/MRA2")

from code_bunnies import code_bunnies
from subprocess import call

if __name__ == '__main__':
    os.environ["WORKSPACE"] = os.environ["SCRIPT_ROOT"] + "/../../../"
    code_bunnie = code_bunnies()
    is_release_build = os.environ.get("DEPLOY_PATH",None)
    
    is_linux_build = "False"
    is_integrity_build = "False"
    
    if "Linux" in os.environ["WORKSPACE"]:
        is_linux_build = "True"
        
    if "Integrity" in os.environ["WORKSPACE"]:
        is_integrity_build = "True"



    if is_release_build:
        if is_linux_build == "True":
            if call("ln -s $SCRIPT_ROOT/../resources $DEPLOY_PATH/resourcesLinux",shell=True) == 0:
                print "Symlink resourcesLinux is created"
            else:
                print "Symlink resourcesLinux is NOT created"
            if call("ln -s $SCRIPT_ROOT/../SourceSpace $DEPLOY_PATH/SourceSpaceLinux",shell=True) == 0:
                print "Symlink SourceSpaceLinux is created"
            else:
                print "Symlink SourceSpaceLinux is NOT created"
            if call("ln -s $SCRIPT_ROOT/../DeliSpace $DEPLOY_PATH/DeliSpaceLinux",shell=True) == 0:
                print "Symlink DeliSpaceLinux is created"
            else:
                print "Symlink DeliSpaceLinux is NOT created"
            if call("ln -s $SCRIPT_ROOT/../ProductSpace $DEPLOY_PATH/ProductSpaceLinux",shell=True) == 0:
                print "Symlink ProductSpaceLinux is created"
            else:
                print "Symlink ProductSpaceLinux is NOT created"
        if is_integrity_build == "True":
            if call("ln -s $SCRIPT_ROOT/../SourceSpace $DEPLOY_PATH/SourceSpaceIntegrity",shell=True) == 0:
                print "Symlink SourceSpaceIntegrity is created "
            else:
                print "Symlink SourceSpaceIntegrity is NOT created"
            if call("ln -s $SCRIPT_ROOT/../DeliSpace $DEPLOY_PATH/DeliSpaceIntegrity",shell=True) == 0:
                print "Symlink DeliSpaceIntegrity is created "
            else:
                print "Symlink DeliSpaceIntegrity is NOT created"
            if call("ln -s $SCRIPT_ROOT/../resources $DEPLOY_PATH/resourcesIntegrity",shell=True) == 0:
                print "Symlink resourcesIntegrity is created "
            else:
                print "Symlink resourcesIntegrity is NOT created"
            if call("ln -s $SCRIPT_ROOT/../ProductSpace $DEPLOY_PATH/ProductSpaceIntegrity",shell=True) == 0:
                print "Symlink ProductSpaceIntegrity is created "
            else:
                print "Symlink ProductSpaceIntegrity is NOT created"

    populate_results_script_path = os.environ["SCRIPT_ROOT"] + "/scripts/mra2_populate_results.sh"
