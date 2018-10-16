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

    print "[prebuild]:Starting"

    generic_prebuild_script = os.environ["SCRIPT_ROOT"] + "/scripts/prebuild.sh"

    # Call generic prebuild script
    if call(". "+generic_prebuild_script,shell=True) == 0:
        print "[prebuild_generic]:Exiting with success"
    else:
        print "[prebuild_generic]:Error:Something went wrong with the prebuild shell script"
        print "[prebuild_generic]:Error 1"
        print "[prebuild_generic]:Exiting"
        exit(2)
