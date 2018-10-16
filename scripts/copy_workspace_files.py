#!/usr/bin/python

import os
import sys
#from export_workspace_path import WORKSPACE_TXT_FILE_NAME_EXTENSION

POSSIBLE_OS_NAMES = [ "Linux", "Integrity" ]
BUILD_NUMBER = os.getenv("BUILD_NUMBER", None)
Variant = os.getenv("Variant", None)
main_dir_path = os.getenv("WORKSPACE", None)
Minor_Variant = Variant.split('.')[1]

if "IC" in Minor_Variant:
    Minor_Variant = Minor_Variant.replace("_","-")

def main(argv):

    if (BUILD_NUMBER == None):
        print("Error <!> Environment variable BUILD_NUMBER is missing.")
        os._exit(313)

    if main_dir_path == None:
        print("Error <!> Environment variable WORKSPACE is missing.")
        os._exit(313)
        
    main_dir_path_with_additional_folder_name = os.path.join(main_dir_path, BUILD_NUMBER)
    artifacts_path = os.path.join(main_dir_path_with_additional_folder_name, "artifacts")
    
    for current_os in POSSIBLE_OS_NAMES:                
        workspace_path = "/home/visteon/workspace/DAG_MRA2_MY20_STABLE/" + Minor_Variant + "_" + current_os + "/Build/IncrementalBuild"        
        print "workspace_path",workspace_path
        if os.path.exists(workspace_path) == False:
            print("Warning <!> Wrong workspace was passed or the file with workspace path is deleted.")
            continue
            
        path_to_copy_workspace_for_current_os = os.path.join(artifacts_path, current_os + "Workspace")
        command_for_copying_files = 'cp -rv %s %s' % (workspace_path,path_to_copy_workspace_for_current_os)
        os.system(command_for_copying_files)
        
        
        command_for_permissions = 'echo "visteon" | sudo -S chmod -R 777 %s' % path_to_copy_workspace_for_current_os
        os.system(command_for_permissions)

if __name__ == "__main__":
    main(sys.argv)