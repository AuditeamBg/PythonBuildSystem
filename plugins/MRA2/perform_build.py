#!/usr/bin/python
import sys
import os
import json
import errno
import subprocess
from code_bunnies import code_bunnies
from subprocess import call
from subprocess import check_output
import pprint

#setting the script root
try:
    os.environ["SCRIPT_ROOT"]
    sys.path.append( os.environ['SCRIPT_ROOT'] + "/plugins/MRA2")
except:
    os.environ["SCRIPT_ROOT"] = os.path.dirname(sys.argv[0]) + "/../.."
    sys.path.append(os.environ['SCRIPT_ROOT'] + "/plugins/MRA2")


def perform_build(self, variant):
    code_bunnie = code_bunnies()
    perform_build_script_path   = os.environ["SCRIPT_ROOT"] + "/scripts/perform_build_cmp.sh"
    perform_build_monolith_path = os.environ["SCRIPT_ROOT"] + "/scripts/mra2_perform_build_monolith.sh"
    current_workspace        = os.environ["WORKSPACE"] + "/" + os.environ["AdditionalFolderName"]
    monolith_path            = os.environ["WORKSPACE"] + "/" + os.environ["AdditionalFolderName"] + "/resources/dependencies/MRA2/MRA2_monolith"
    IntegrityBSP_path        = os.environ["WORKSPACE"] + "/" + os.environ["AdditionalFolderName"] + "/Tools/IntegrityBSP"
    platform_bin_path        = os.environ["WORKSPACE"] + "/" + os.environ["AdditionalFolderName"] + "/resources/dependencies/MRA2/BSP/KernelIntegrity/MRA2H2/bin"
    platform_update_bin_path = os.environ["WORKSPACE"] + "/" + os.environ["AdditionalFolderName"] + "/resources/dependencies/MRA2/BSP/KernelIntegrityUpdate/MRA2H2/bin"    
    code_bunnie.inject_bunnies(os.environ["WORKSPACE"] + "/"  +os.environ["AdditionalFolderName"] + "/SourceSpace") #injects the defines in integrity builds
    top_buns = code_bunnie.get_top_buns(os.environ["WORKSPACE"] + "/" + os.environ["AdditionalFolderName"] + "/SourceSpace")
    top_buns_string = " ".join(top_buns)
    top_buns_string = ' '.join(top_buns_string.split("Infrastructure.Websockets"))

    ###### Additional Buns ######
    ###### TODO #################
    ###### Verify ###############
    #top_buns_string = ' '.join(top_buns_string.split("NFC.NFCServiceUnitTest"))
    if os.path.isdir(os.environ["WORKSPACE"] + "/" + os.environ["AdditionalFolderName"]+"/SourceSpace/Media/PlayerIF1Service"):
        top_buns_string += " Media.PlayerIF1Service Media.PlayerIF1TestService Media.PlayerIF1UnitTest"
    if os.path.isdir(os.environ["WORKSPACE"] + "/" + os.environ["AdditionalFolderName"]+"/SourceSpace/TunerIF1/TunerIF1Service"):
        top_buns_string += " TunerIF1.TunerIF1Service"

    print "[perform_build]:The top buns are: "
    pprint.pprint(top_buns_string)

    print "[perform_build]:The Variant is: " 
    pprint.pprint(variant)

    #perform the build
    try :
        if "monolith" not in sys.argv:
            if call(". " + perform_build_script_path + " " + top_buns_string,shell=True) != 0:
                print "[perform_build]:Error:something went wrong with the build shell script"
                print "[perform_build]:Exiting"
                exit(2)
    
        if os.environ["IS_INTEGRITY_BUILD"] == "True":
            if call(". " + perform_build_monolith_path + " " + variant + " " + monolith_path + " " + IntegrityBSP_path + " " +  current_workspace + " " + platform_bin_path + " " + platform_update_bin_path,shell=True) != 0:
                print "[perform_monolith]:Error:something went wrong with the build monolith shell script"
                print "[perform_monolith]:Total Fatals: 1"
                exit(2) 
                #Temporary exits without error. Once all variant are covered, adds exit(2)
                
    except KeyError:
        print "Error 2"
        print "perform_build for MRA2 FAILED!!!"
        exit(2)


if __name__ == '__main__':
    print "[perform_build]:Starting"
    pprint.pprint(dict(os.environ), width=1)
        
    if len(sys.argv) > 2:
        exit(1)

    elif len(sys.argv) == 2:
        perform_build(sys.argv[1], sys.srgv[2])

    elif len(sys.argv) == 1:
        try: 
            variant_env = os.environ["Variant"]
        except:
            print "[perform_build]: Error: the number of arguments is insufficient or 'Variant' is missing"
            exit(1)
        perform_build(sys.argv, variant_env)