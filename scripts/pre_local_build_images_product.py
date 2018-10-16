#!/usr/bin/python

import os
import sys
from local_incremental_build import print_failure

#-------------------------------#
#------------ MAIN -------------#
#-------------------------------#
def main(args):
    #----------- Do pre local create images steps -----------#
    workspace_with_additional_folder = os.environ["WORKSPACE"] + '/' + os.environ["AdditionalFolderName"]
    if os.path.isdir(workspace_with_additional_folder + '/artifacts'):
        os.system("mv %s %s" % ((workspace_with_additional_folder + '/artifacts/*FULL.zip'),
                                workspace_with_additional_folder + '/VIP_resources/DI-Cluster-IntEng/'))
        os.system("mv %s %s" % ((workspace_with_additional_folder + '/artifacts/*Sources.txt'),
                                workspace_with_additional_folder + '/VIP_resources/DI-Cluster-IntEng/'))
        os.system("find %s -type f ! -name '*.tar.gz' -delete" % (workspace_with_additional_folder + '/artifacts/*'))
    else:
        os.mkdir(workspace_with_additional_folder + '/artifacts')
    if os.path.isdir(workspace_with_additional_folder + '/Tools'):
        os.system("sudo chmod -R 777 " + workspace_with_additional_folder + '/Tools/*')
    else:
        print_failure("Folder Tools is mandatory in workspace : " + workspace_with_additional_folder)
        os._exit(313)

    #----------- Create local images -----------#
    os.system('bash %s/perform_build.sh "product"' % (os.getenv("SCRIPT_ROOT")))

if __name__ == "__main__":
    main(sys.argv)