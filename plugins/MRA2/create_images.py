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
    os.environ["SCRIPT_ROOT"] = os.path.dirname(os.path.dirname(os.path.dirname(sys.argv[0])))
    sys.path.append( os.environ['SCRIPT_ROOT'] + "/plugins/MRA2")

from code_bunnies import code_bunnies
from subprocess import call

if __name__ == '__main__':
    #Write versioning information to Integrity and Linux streams
    try:
        f = open(os.environ["SCRIPT_ROOT"]+"/../SourceSpace/ver" ,'w')
        f.write(os.environ['BUILD_NAME'])
        f.close()
    
        current_build_variant = os.environ.get("Variant", None)
        symlink_for_systemd_path = os.environ["SCRIPT_ROOT"] + "/scripts/symlinkforsystemd.py"
        strip_linux_binaries = os.environ["SCRIPT_ROOT"] + "/scripts/extractsymbols.py"
        
        cards_path = os.environ["SCRIPT_ROOT"] + "/../cards/"
        dest_path = os.environ["SCRIPT_ROOT"] + "/../LIN_DBG/"
    
        additional_copy_script_path = os.environ["SCRIPT_ROOT"] + "/plugins/MRA2/copy_to_card.py " + os.environ["SCRIPT_ROOT"] + "/../Doc/IntegrationMra2H2/doc/Autogrator/IntegrationMra2H2/additional_copy.yaml"
        cards_indexes_autogrator = ["Mra2-SOC-IC-Hv","Mra2-VIP-IC-Hv","Mra2-SOC-C5v","Mra2-VIP-C5v","Mra2-SOC-IC-Ev","Mra2-VIP-IC-Ev"]  # cards by name, edit to add
    
        if os.environ["IS_INTEGRITY_BUILD"] == "True":
            cards_indexes_additional = ["additionalIntegrity"]
            create_images_flash_script_path = os.environ["SCRIPT_ROOT"] + "/scripts/CreateReflashImagesIntegrity.sh"
    
        if os.environ["IS_LINUX_BUILD"] == "True":
            cards_indexes_additional = ["additionalLinux"]
            create_images_flash_script_path = os.environ["SCRIPT_ROOT"] + "/scripts/CreateReflashImagesLinux.sh"
    
        if os.environ["IS_REFLASH_LINUX_Build"] == "True":
            cards_indexes_additional = ["additionalReflashLinux"]
            create_images_flash_script_path = os.environ["SCRIPT_ROOT"] + "/scripts/CreateReflashImagesReflashLinux.sh"
     
    
        if 'cards_indexes_additional' in locals():
            if call("python "+additional_copy_script_path + " " + ' '.join(cards_indexes_additional),shell=True) != 0:
                print "[populate_results]:Additional copy scripts failed"
    
        if 'create_images_flash_script_path' in locals():
            if call(". "+create_images_flash_script_path,shell=True) != 0:
                print "[populate_results]:Additional flash images scripts failed"
    
        if 'cards_indexes_autogrator' in locals():
            if os.environ["IS_RELEASE_BUILD"] == "True" or os.environ["IS_DAILY_BUILD"] == "True":
                if call("python "+additional_copy_script_path + " " + ' '.join(cards_indexes_autogrator),shell=True) != 0:
                    print "[populate_results]:Additional copy Autogrator failed"
            
                if "C5" in current_build_variant:
                    if call("python " + symlink_for_systemd_path + " ",shell=True) != 0:
                        print"[populate_results]:symlinks for systemd script Failed"
    
                    if call("python " + strip_linux_binaries + " " + cards_path + " " + dest_path, shell=True) != 0:
                        print "[populate_results]:stripping binaries script Failed"
    
        print "[create_images]:Exiting"
        exit(0)
        
    except KeyError:
        print "Error 1"
        print "create_images for MRA2 FAILED!!!"
