#!/usr/bin/python

import os
import sys
from local_incremental_build import print_failure
from local_incremental_build import change_the_linker_options

#-------------------------------#
#------------ MAIN -------------#
#-------------------------------#
def main(argv):
    #----------- Pre os build steps -----------#
    workspace_with_additional_folder = os.environ["WORKSPACE"] + '/' + os.environ["AdditionalFolderName"]
    if os.path.isdir(workspace_with_additional_folder + '/artifacts'):
        os.system("rm -rf %s" % (workspace_with_additional_folder + '/artifacts/*'))
    else:
        os.mkdir(workspace_with_additional_folder + '/artifacts')
    if os.path.isdir(workspace_with_additional_folder + '/Tools'):
        os.system("sudo chmod -R 777 " + workspace_with_additional_folder + '/Tools/*')
    else:
        print_failure("Folder Tools is mandatory in workspace : " + workspace_with_additional_folder)
        os._exit(313)
    change_the_linker_options(workspace_with_additional_folder)

    #----------- Build os -----------#
    os.system('bash %s/scripts/VersionReplacer.sh "resources"' % (os.getenv("SCRIPT_ROOT")))
    os.system('bash %s/perform_build.sh "false" "BSP"' % (os.getenv("SCRIPT_ROOT")))
    os.system('bash %s/perform_build.sh "true"' % (os.getenv("SCRIPT_ROOT")))

if __name__ == "__main__":
    main(sys.argv)