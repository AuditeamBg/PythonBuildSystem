#!/usr/bin/python

import os
import shutil
import sys

workspace = str(os.getenv("WORKSPACE", None))
build_name = str(os.getenv("BUILD_NAME", None))
build_number = str(os.getenv("BUILD_NUMBER", None))
workspace_with_build_number = os.path.join(workspace, build_number)
path_to_artifacts = os.path.join(workspace_with_build_number, "artifacts")

os.chdir(workspace_with_build_number)

if workspace == None:
    print("Environment variable is missing : WORKSPACE")
    sys.exit(313)
    
if build_name == None:
    print("Environment variable is missing : BUILD_NAME")
    sys.exit(313)
    
if build_number == None:
    print("Environment variable is missing : BUILD_NUMBER")
    sys.exit(313)


full_name_of_the_archive = "%s_Workspace.tar.gz" % build_name
is_having_linux = True
excludes_string = ""
possible_os_types = [ 'Linux',
                      'Integrity']
root_names_of_folders_to_exclude = [ 'DeliSpace',
                                     'ProductSpace',
                                     'SourceSpace',
                                     'resources']

if "IC-H" in build_name or "IC-E" in build_name:
    is_having_linux = False

for root_name in root_names_of_folders_to_exclude:
    for os_type in possible_os_types:
        if is_having_linux == False and os_type == "Linux":
            continue
        excludes_string += (" --exclude='%s'" % (root_name + os_type))

archive_workspace_command = "echo 'visteon' | sudo -S tar -czpvf %s * %s" % (full_name_of_the_archive, excludes_string)
os.system(archive_workspace_command)

path_to_moved_integrity_workspace = os.path.join(path_to_artifacts, "IntegrityWorkspace")
path_to_moved_linux_workspace = os.path.join(path_to_artifacts, "LinuxWorkspace")

if os.path.exists(path_to_moved_integrity_workspace):
    os.system("rm -rf %s" % path_to_moved_integrity_workspace)
if os.path.exists(path_to_moved_linux_workspace):
    os.system("rm -rf %s" % path_to_moved_linux_workspace)

if os.path.exists(path_to_moved_integrity_workspace):
    print("Error <!> 'IntegrityWorkspace' isn't deleted.")
else:
    print("Notify <!> 'IntegrityWorkspace' is deleted successfully")

if os.path.exists(path_to_moved_linux_workspace):
    print("Error <!> 'LinuxWorkspace' isn't deleted.")
else:
    print("Notify <!> 'LinuxWorkspace' is deleted successfully")

if os.path.exists(full_name_of_the_archive):
    shutil.move(full_name_of_the_archive, "artifacts")
else:
    print("Error <!> WORKSPACE archive doesn't exists.")