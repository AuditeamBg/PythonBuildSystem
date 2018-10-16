#!/usr/bin/python

import os
import sys

from local_incremental_build import get_os

WORKSPACE_TXT_FILE_NAME_EXTENSION = "_Workspace.txt"

def first_letter_capital(value):
    return value[0].upper() + value[1:].lower()

def main(argv):

    build_name = os.getenv("BUILD_NAME", None).strip()
    workspace = os.getenv("WORKSPACE", None).strip()
    additional_folder_name = os.getenv("AdditionalFolderName", None)
    path_to_artifacts = os.path.join(workspace, additional_folder_name + "/artifacts")
    current_os = first_letter_capital(get_os(build_name))

    if current_os == "Linux":
        workspace_file_name = "Linux" + WORKSPACE_TXT_FILE_NAME_EXTENSION
    elif current_os == "Integrity":
        workspace_file_name = "Integrity" + WORKSPACE_TXT_FILE_NAME_EXTENSION
    else:
        print "------------------------------------------------------------------------------"
        print "<!> Error <!> The os type is missing in the environment variable - BUILD_NAME."
        print "------------------------------------------------------------------------------"
        sys.exit(1)

    if not os.path.exists(path_to_artifacts):
        os.makedirs(path_to_artifacts)

    with open(os.path.join(path_to_artifacts, workspace_file_name), "w") as file:
        full_workspace_path = os.path.join(workspace, additional_folder_name)
        file.write(full_workspace_path)
        file.close()

if __name__ == "__main__":
    main(sys.argv)