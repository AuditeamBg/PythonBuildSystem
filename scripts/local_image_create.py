#!/usr/bin/python

import errno
import os
import sys
import time
import webbrowser

from local_incremental_build import get_variant
from local_incremental_build import get_correct_workspace_for_current_variant
from local_incremental_build import path_existence_safe_check
from local_incremental_build import print_failure
from local_incremental_build import print_success
from local_incremental_build import print_warning
from local_incremental_build import unexpected_error_handling
from local_incremental_build import txtColors
from export_workspace_path import WORKSPACE_TXT_FILE_NAME_EXTENSION

NAME_OF_FILE_TO_INDICATE_ALREADY_MOVED_FILES = "files_moved"
NAME_OF_FILE_FOR_RETURN_CODE = "return_code_of_last_build.txt"
POSSIBLE_OS_NAMES = ["Linux", "Integrity"]
VARIANTS_WITHOUT_LINUX = ["IC-E", "IC-H"]
ADDITIONAL_FOLDER_NAME = "IncrementalBuild"
NECESSARY_FOLDERS_FOR_BUILD = ["SourceSpace",
                               "ProductSpace",
                               "DeliSpace",
                               "resources"]
SCRIPTS_ROOT = os.getcwd()
BSP_BUILD_WORKSPACE_PATH = os.path.dirname(os.path.dirname(SCRIPTS_ROOT))
PATH_TO_ARTIFACTS_OF_BSP_BUILD = BSP_BUILD_WORKSPACE_PATH + '/artifacts'

#-----------------------------------#
#------------ COMMANDS -------------#
#-----------------------------------#

def execute_move_files(is_current_variant_having_linux, current_variant_name):
    """
     Input : This function takes one boolean and two strings :
     - is_current_variant_having_linux(boolean) : boolean which will be used to know,
        if the current variant have linux part (IVI)
     - current_variant_name(string) : current variant name;
     - os_name(string) : current os name;
     Returns :
     - None
     Summary :
     - This function will be used do all the necessary steps to
        move the workspace files for all os types for current variant.
    """
    os_names_for_current_variant = [ "Integrity" ]

    if is_current_variant_having_linux == True:
        os_names_for_current_variant = POSSIBLE_OS_NAMES

    for os_name in os_names_for_current_variant:

        correct_workspace_path = get_correct_workspace_for_current_variant(os_name, current_variant_name)
        full_path_to_text_file_with_workspace_path = os_name + WORKSPACE_TXT_FILE_NAME_EXTENSION

        # Check if exists the text file with correct workspace path for the current os and it is not empty.
        # If exists and it is not empty will get the content as correct workspace path value
        # Otherwise will use the hardcoded value from the method of script local_incremental_build.py.
        # The hardcoded values from that method are automatically updated by the script -
        # 'automatic_update_paths_to_correct_workspace.py', so don't worry it will be correct ! :)

        if os.path.exists(full_path_to_text_file_with_workspace_path):
            with open(full_path_to_text_file_with_workspace_path, "r") as file_with_workspace_path:
                content_of_file_with_workspace_path = file_with_workspace_path.read().strip("\n").strip()
                file_with_workspace_path.close()
            if is_none_or_empty_string(content_of_file_with_workspace_path) == False:
                correct_workspace_path = content_of_file_with_workspace_path

        full_correct_workspace_path = os.path.join(correct_workspace_path, ADDITIONAL_FOLDER_NAME)

        # Getting path from which to get workspace files for current os
        path_to_workspace_files_for_current_os = os.path.join(PATH_TO_ARTIFACTS_OF_BSP_BUILD, os_name + "Workspace")

        # If the exists the file used to indicate that the workspace files for current os are moved.
        # It will skip the moving step for that os.
        full_path_to_indicating_file = path_to_workspace_files_for_current_os + '/' + NAME_OF_FILE_TO_INDICATE_ALREADY_MOVED_FILES
        if os.path.exists(full_path_to_indicating_file):
            print_warning(
                "WARNING : The files for current variant for OS %s were already moved! Skipping this step." % os_name)
            continue

        if check_already_moved_workspace_files(full_correct_workspace_path):
            handle_already_moved_files(full_correct_workspace_path,
                                       current_variant_name,
                                       os_name,
                                       path_to_workspace_files_for_current_os)

        if os.path.exists(full_correct_workspace_path) == False:
            try:
                print("\n------------------------------------")
                print("Creating path tree to correct workspace for OS : %s" % os_name)
                print("...")
                result = os.system("mkdir -p " + full_correct_workspace_path)
                if os.WEXITSTATUS(result) > 0:
                    print_failure("<!> ERROR <!> Unsuccessful creating path to correct workspace for OS : %s" % os_name)
                    os._exit(313)
                folder_from_which_to_change_permissions = os.path.dirname(
                                                                os.path.dirname(
                                                                    full_correct_workspace_path))
                os.system("chmod -R 777 %s" % folder_from_which_to_change_permissions)

            except OSError as e:
                if e.errno == errno.EPERM:
                    print_failure("<!> ERROR <!> You do not have permission for operation mkdir. Try to start the script with 'sudo'.")
                    os._exit(313)
                elif e.errno == errno.EACCES:
                    print_failure("<!> ERROR <!> You do not have permission to create the path tree. Try to start the script with 'sudo'.l")
                    os._exit(313)
                else:
                    unexpected_error_handling(3, "Creating the path tree failed!")
            except BaseException as e:
                unexpected_error_handling(3, e.message)


        if os.path.exists(path_to_workspace_files_for_current_os) == False:
            print_warning("WARNING : The folder with the files for current variant for OS %s are missing."
                          "\nSkipping moving files for that os.", os_name)
            #wait_answer_to_continue()

        result_of_moving_files = move_files_to_correct_workspace_path(os_name, path_to_workspace_files_for_current_os, full_correct_workspace_path)

        if result_of_moving_files > 0:
            print_failure("<!> ERROR <!> Unsuccessful moving of the workspace files.")
            os._exit(313)

        create_symlinks_for_builds_in_bsp_build_workspace_path(os_name,
                                                               current_variant_name,
                                                               full_correct_workspace_path)

        # If there aren't any remaining files in the path to the workspace files for current os.
        # Will create file which indicates that they were moved.
        count_of_remaining_files = len(listdir_not_hidden(path_to_workspace_files_for_current_os))

        if count_of_remaining_files < 1:
            os.system("touch %s" % (full_path_to_indicating_file))

#--------------------------------------#
def execute_build(argv, current_variant_name, is_current_variant_having_linux, is_rebuild):
    """
     Input : This function takes one list, one string and one boolean :
     - argv(list) : contains the passed arguments to the script without the script name
     - current_variant_name(string) : current variant name;
     - is_current_variant_having_linux(boolean) : boolean which will be used to know,
        if the current variant have linux part (IVI)
     Returns :
     - None
     Summary :
     - This function will be used do all the necessary steps to build the wanted os types.
    """

    build_or_rebuild_string = "build"
    if is_rebuild == True:
        build_or_rebuild_string = "rebuild"
    else:
        if os.getenv("LOCAL_CLEAN_REBUILD", None) != None:
            del os.environ["LOCAL_CLEAN_REBUILD"]
        
    arguments_without_option = filter(lambda x: x != build_or_rebuild_string, argv)

    results_of_the_builds = {}
    if len(arguments_without_option) == 0:
        if is_current_variant_having_linux == True:
            arguments_without_option = POSSIBLE_OS_NAMES
        else:
            arguments_without_option = ["Integrity"]

    
    for current_os_name in arguments_without_option:
        current_os_name = current_os_name[0].upper() + current_os_name[1:].lower()
        
        if current_os_name not in POSSIBLE_OS_NAMES:
            print_failure("<!> ERROR <!> : The passed os - %s is invalid.\nPlease choose one of the following : %s" %
                          (current_os_name, ", ".join(POSSIBLE_OS_NAMES)))
            os._exit(313)
            

        elif current_os_name == "Linux" and is_current_variant_having_linux == False:
            print_warning(
                "WARNING : The current variant name %s doesn't have Linux part. Skipping build for Linux!"
                % current_variant_name)

        print("\n------------------------------------")
        print("Starting %s on %s.%s" % (build_or_rebuild_string, current_variant_name, current_os_name))
        print("...")

        correct_workspace_path_for_current_os = get_correct_workspace_for_current_variant(current_os_name,
                                                                                          current_variant_name)
        
        correct_workspace_full_path = os.path.join(correct_workspace_path_for_current_os, ADDITIONAL_FOLDER_NAME)

        # If is rebuild delete the InterSpace and the ProductSpace. And export environment var LOCAL_CLEAN_REBUILD
        if is_rebuild == True:
            command_for_deleting_interspace = "echo 'visteon' | sudo -S rm -rf %s/InterSpace" % correct_workspace_full_path
            command_for_deleting_productspace = "echo 'visteon' | sudo -S rm -rf %s/ProductSpace" % correct_workspace_full_path
            os.system(command_for_deleting_interspace)
            os.system(command_for_deleting_productspace)
            os.environ["LOCAL_CLEAN_REBUILD"] = "True"

        path_existence_safe_check(correct_workspace_path_for_current_os,
                                  "The files for variant %s.%s are missing."
                                  % (current_variant_name, current_os_name)
                                  + "\nPlease move with script 'local_image_create.py' them and try again.")


        path_to_build_system_scripts_for_current_os_variant = os.path.join(correct_workspace_full_path,
                                                                           "CI.BuildSystem/scripts")
        os.chdir(path_to_build_system_scripts_for_current_os_variant)
        
        command = "./pre_local_build_images_os.sh"
        result = os.system(command)
        
        result_of_current_build = get_build_result_by_os_and_variant(current_os_name, current_variant_name)
        
        if is_none_or_empty_string(str(result_of_current_build)) == False:
            results_of_the_builds[current_os_name] = result_of_current_build
            
        check_necessary_files_and_create_symlinks(current_os_name, correct_workspace_full_path)

    # If any build has failed print error and don't ask for create images.
    is_any_build_failed = False
    for os_name, result_of_build in results_of_the_builds.iteritems():
        if result_of_build > 0:
            is_any_build_failed = True
            print_failure("<!> ERROR <!> The %s for %s.%s wasn't successful."% (build_or_rebuild_string, current_variant_name, os_name))
        else:        
            print_success("<!> SUCCESS <!> The %s for %s.%s was successful." % (build_or_rebuild_string, current_variant_name, os_name))
    
    #if is_any_build_failed == False:
    #    print_warning("Do you want to create images ? (y/n)")
    #    answer = raw_input()
    #    
    #    if is_none_or_empty_string(answer) == False:
    #        if answer[0].lower() == 'y':
    execute_create_images(is_current_variant_having_linux, current_variant_name)



#--------------------------------------#
def execute_create_images(is_current_variant_having_linux, current_variant_name):
    """
     Input : This function takes one boolean and one string :
     - is_current_variant_having_linux(boolean) : boolean which will be used to know,
        if the current variant have linux part (IVI)
     - current_variant_name(string) : current variant name;
     Returns :
     - None
     Summary :
     - This function will be used do all the necessary steps to create local images.
    """

    os.chdir(SCRIPTS_ROOT)

    for os_name in POSSIBLE_OS_NAMES:
        if is_current_variant_having_linux == False and os_name == 'Linux':
            continue

        full_correct_workspace_path_for_current_os = get_correct_workspace_for_current_variant(
            os_name, current_variant_name) + "/" + ADDITIONAL_FOLDER_NAME

        # Check if the necessary folders to make a build are moved in the correct directory for current variant and os
        path_existence_safe_check(full_correct_workspace_path_for_current_os,
                                  "The moving of workspace fiels and build for all OS types is mandatory!")
        for necessary_folder_for_build in NECESSARY_FOLDERS_FOR_BUILD:
            path_existence_safe_check(
                full_correct_workspace_path_for_current_os + "/" + necessary_folder_for_build,
                "The moving of workspace files and build of all possible OS types for the current variant."
                "\nIs mandatory to create images!")

        for symlink_root_name in NECESSARY_FOLDERS_FOR_BUILD:
            full_symlink_name = symlink_root_name + os_name
            path_to_current_necessary_symlink_for_current_os_type = os.path.join(BSP_BUILD_WORKSPACE_PATH,
                                                                                 full_symlink_name)

            path_existence_safe_check(path_to_current_necessary_symlink_for_current_os_type,
                                      ("Symlink %s is mandatory to create images." % full_symlink_name)
                                      + "\nPlease move all necessary workspace files for all possible"
                                        "os types with script local_image_create.py .")

    result = os.system("echo 'visteon' | sudo -S bash %s/pre_local_build_images_product.sh" % SCRIPTS_ROOT)

    result_of_creating_images = os.WEXITSTATUS(result)
    if result_of_creating_images > 0:
        print_failure("<!> ERROR <!> : The creation of images was unsuccessful.")
        os._exit(313)

    #ask_to_open_folder(PATH_TO_ARTIFACTS_OF_BSP_BUILD, txtColors.TAG_OK + "Enter 'y' to open the folder with the image." + txtColors.TAG_END)
#------------------------------------#
#------------ UTILITIES -------------#
#------------------------------------#
def get_build_result_by_os_and_variant(os_name, variant_name):
    """
     Input : This function takes two strings :
     - os_type(string) : operation system type of the symlink name;
     - variant_name(string) : variant name of the symlink name;
     Returns :
     - int - return code of given build
     Summary :
     - This function will be used to get the return code. 
        Of the latest build for the given os and variant name.
    """
    full_workspace_path = os.path.join(get_correct_workspace_for_current_variant(os_name, variant_name), ADDITIONAL_FOLDER_NAME)
    path_existence_safe_check(full_workspace_path, "The workspace for %s %s is missing." % (variant_name, os_name))
    full_path_to_file_with_return_code = os.path.join(full_workspace_path, NAME_OF_FILE_FOR_RETURN_CODE)
    
    if os.path.exists(full_path_to_file_with_return_code):
        with open(full_path_to_file_with_return_code, 'r') as f:
            file_content = f.read().strip()
            if file_content != "":
                return int(file_content)
                
    return 0
#--------------------------------------#
def is_none_or_empty_string(string_value):
    """
     Input : This function takes one string :
     - string_value(string) : value to check if it is none or empty string;
     Returns :
     - boolean - result of the check
     Summary :
     - This function will be used to check if the passed value is none or empty string.
    """
    if string_value != None and string_value != "":
        return False

    return True

#--------------------------------------#
def open_folder(path):
    """
     Input : This function takes one string :
     - path(string) : path to the folder which will be open in folder manager;
     Returns :
     - None
     Summary :
     - This function will be used open folder in file manager.
    """
    if os.path.exists(path):
        webbrowser.open(path)
    else:
        print_warning("Warning <!> Path which you tried to open doesn't exists.")

#--------------------------------------#
def create_symlinks_for_builds_in_bsp_build_workspace_path(os_type,
                                                            variant_name,
                                                            path_to_workspace_of_current_build):
    """
     Input : This function takes three strings :
     - os_type(string) : operation system type of the symlink name;
     - variant_name(string) : variant name of the symlink name;
     - path_to_workspace_of_current_build(string) : path to the target of the symlink;
     Returns :
     - None
     Summary :
     - This function will be used to create symlinks in bsp build dir.
       Which will point to the workspace path of the passed variant and os type.
    """

    name_of_symlink = variant_name + "." + os_type + "Build"
    full_path_to_symlink = BSP_BUILD_WORKSPACE_PATH + '/' + name_of_symlink
    if os.path.isdir(full_path_to_symlink):
        os.system("rm %s" % full_path_to_symlink)

    os.system("ln -s " + path_to_workspace_of_current_build + " " + (full_path_to_symlink))
    print_success("Symlink %s created in %s" % (name_of_symlink, BSP_BUILD_WORKSPACE_PATH))

#--------------------------------------#
def ask_to_open_folder(path, message="Do you want to open the path in File Manager ? (y/n)"):
    """
     Input : This function takes one string :
     - path(string) : path to the folder which will be open in folder manager;
     Returns :
     - None
     Summary :
     - This function will be used to ask if the user wants to open folder in file manager.
       And if the user write 'y' or word starting with this character (case insensitive) will open the folder.
    """
    answer_for_open_folder = raw_input(message).lower()
    if is_none_or_empty_string(answer_for_open_folder) == False:
        if answer_for_open_folder[0] == 'y':
            open_folder(path)

#--------------------------------------#
def handle_already_moved_files(full_correct_workspace_path, current_variant_name, os_name, path_to_workspace_files_for_current_os):
    """
     Input : This function takes three strings :
     - full_correct_workspace_path(string) : full path to the correct workspace path (including 'AdditionalFolderName');
     - current_variant_name(string) : current variant name;
     - os_name(string) : current os name;
     Returns :
     - None
     Summary :
     - This function will be used to handle the answer from method get_answer_for_already_moved_files.
    """
    answer = '1'
    while answer not in ('1', '2', '3'):
        print_failure("<!> ERROR <!> You must choose option 1, 2 or 3. Try Again")
        answer = get_answer_for_already_moved_files(full_correct_workspace_path)

    if answer == '3':
        # Exiting
        os._exit(313)
    elif answer == '2':
        # Opening the workspace path
        open_folder(full_correct_workspace_path)
        os._exit(313)
    elif answer == '1':
        # Deleting the already moved files
        delete_already_moved_files_and_move_the_new(full_correct_workspace_path, current_variant_name, os_name, path_to_workspace_files_for_current_os)
        os._exit(313)

#--------------------------------------#
def wait_answer_to_continue():
    """
     Input :
     - None
     Returns :
     - None
     Summary :
     - This function will be used to wait answer from the user to continue forward.
    """
    answer_for_skipping = raw_input("Enter 'ok' to continue.")
    while (answer_for_skipping.lower() != "ok"):
        answer_for_skipping = raw_input("Enter 'ok' to continue.")

#--------------------------------------#
def check_already_moved_workspace_files(full_correct_workspace_path):
    correct_workspace_path = os.path.dirname(full_correct_workspace_path)

    path_to_source_space_for_current_variant_and_os = os.path.isdir(full_correct_workspace_path + "/SourceSpace")
    path_to_deli_space_for_current_variant_and_os = os.path.isdir(full_correct_workspace_path + "/DeliSpace")
    path_to_inter_space_for_current_variant_and_os = os.path.isdir(full_correct_workspace_path + "/InterSpace")
    path_to_product_space_for_current_variant_and_os = os.path.isdir(full_correct_workspace_path + "/ProductSpace")

    result = os.path.isdir(correct_workspace_path) \
             and (path_to_source_space_for_current_variant_and_os
                  or path_to_deli_space_for_current_variant_and_os
                  or path_to_inter_space_for_current_variant_and_os
                  or path_to_product_space_for_current_variant_and_os)

    return result

#--------------------------------------#
def move_files_to_correct_workspace_path(os_name,
                                         path_to_workspace_files_for_current_os,
                                         full_correct_workspace_path):
    """
     Input : This function takes three strings :
     - os_name(string) : current os name;
     - path_to_workspace_files_for_current_os(string) : full path to the directory with the workspace files for current os;
     - full_correct_workspace_path(string) : full path to the correct workspace path (including 'AdditionalFolderName');
     Returns :
     - None
     Summary :
     - This function will be used to move the workspace file from bsp build workspace to the correct workspace path
        for the current os type and os name.
    """

    try:
        print("\n------------------------------------")
        print("Moving files to path : " + full_correct_workspace_path)
        print("...")

        command_for_move = "echo 'visteon' | sudo -S mv %s/* %s" % (path_to_workspace_files_for_current_os,
                                                                    full_correct_workspace_path)
        result = os.system(command_for_move)
        print_success("The files for os %s are successfully moved." % os_name)
        #ask_to_open_folder(full_correct_workspace_path)
        return os.WEXITSTATUS(result)
    except OSError as e:
        if e.errno == errno.EPERM:
            print_failure("<!> ERROR <!> You do not have permission for operation mv."
                                    "\nTry to change permissions in directory : %s"
                          % full_correct_workspace_path)
            os._exit(313)
        elif e.errno == errno.EACCES:
            print_failure("<!> ERROR <!> You do not have access to move files in %s."
                          % full_correct_workspace_path)
            os._exit(313)
        else:
            unexpected_error_handling(3,
                                      "Moving files failed. Current OS is : %s" % os_name)
    except BaseException as e:
        unexpected_error_handling(3, ("Moving files failed. Current OS is : %s" % os_name) + e.message)

#--------------------------------------#
def delete_already_moved_files_and_move_the_new(full_correct_workspace_path,
                                                current_variant_name,
                                                os_name,
                                                path_to_workspace_files_for_current_os):
    """
     Input : This function takes three strings :
     - full_correct_workspace_path(string) : full path to the correct workspace path (including 'AdditionalFolderName');
     - current_variant_name(string) : current variant name;
     - os_name(string) : current os name;
     Returns :
     - None
     Summary :
     - This function will be used to delete the already moved files for the current os type and os name.
    """

    print("------------------------------------")
    print("Deleting the already moved files from:")
    print("'" + full_correct_workspace_path + "'")
    print("...")

    path_existence_safe_check(full_correct_workspace_path)
    os.system(
        "echo 'visteon' | sudo -S  rm -rf " + (full_correct_workspace_path))
    symlink_name_for_current_os = (current_variant_name + '.' + os_name)
    result = os.system("echo 'visteon' | sudo -S  rm -rf " +
              (os.path.join(
                  BSP_BUILD_WORKSPACE_PATH,
                  symlink_name_for_current_os)))
    result_of_deleting_already_moved_files = os.WEXITSTATUS(result)

    if result_of_deleting_already_moved_files > 0:
        print_failure("<!> ERROR <!> The deleting of the already moved files was unsuccessful.")
        os._exit(313)

    result_of_moving_files = move_files_to_correct_workspace_path(os_name,
                                                                 path_to_workspace_files_for_current_os,
                                                                 full_correct_workspace_path)
    if result_of_moving_files > 0:
        print_failure("<!> ERROR <!> Unsuccessful moving of the workspace files.")
        os._exit(313)

#--------------------------------------#
def listdir_not_hidden(path):
    """
     Input : This function takes one string :
     - path(string) : path in which to get the not hidden file system objects;
     Returns :
     - None
     Summary :
     - This function will be used to get the file system objects without the hidden ones in the passed path.
    """

    result = []

    for f in os.listdir(path):
        if not f.startswith('.'):
            result.append(f)

    return result

#--------------------------------------#
def check_necessary_files_and_create_symlinks(current_os_name, full_correct_workspace_path):
    """
     Input : This function takes one string :
     - path(string) : path in which to get the not hidden file system objects;
     Returns :
     - None
     Summary :
     - This function will be used to get the file system objects without the hidden ones in the passed path.
    """

    # Paths to necessary folders from current os for creating images
    path_to_source_space_for_current_os = os.path.join(full_correct_workspace_path, "SourceSpace")
    path_to_product_space_for_current_os = os.path.join(full_correct_workspace_path, "ProductSpace")
    path_to_deli_space_for_current_os = os.path.join(full_correct_workspace_path, "DeliSpace")
    path_to_resources_for_current_os = os.path.join(full_correct_workspace_path, "resources")

    # Destinations for symlinks to necessary folders from current os for creating images
    destination_for_symlink_to_source_space_for_current_os = os.path.join(BSP_BUILD_WORKSPACE_PATH,
                                                                          "SourceSpace%s" % current_os_name)
    destination_for_symlink_to_deli_space_for_current_os = os.path.join(BSP_BUILD_WORKSPACE_PATH,
                                                                        "DeliSpace%s" % current_os_name)
    destination_for_symlink_to_product_space_for_current_os = os.path.join(BSP_BUILD_WORKSPACE_PATH,
                                                                           "ProductSpace%s" % current_os_name)
    destination_for_symlink_to_resources_for_current_os = os.path.join(BSP_BUILD_WORKSPACE_PATH,
                                                                        "resources%s" % current_os_name)

    # Safe checks for each path to necessary folders from current os for creating images and creation of the symlinks
    path_existence_safe_check(path_to_source_space_for_current_os,
                              "SourceSpace for os %s is mandatory." % current_os_name)
    if os.path.islink(destination_for_symlink_to_source_space_for_current_os):
        os.system("rm %s" % destination_for_symlink_to_source_space_for_current_os)
    os.system("ln -s %s %s" %
              (path_to_source_space_for_current_os, destination_for_symlink_to_source_space_for_current_os))

    path_existence_safe_check(path_to_deli_space_for_current_os,
                              "DeliSpace for os %s is mandatory." % current_os_name)
    if os.path.islink(destination_for_symlink_to_deli_space_for_current_os):
        os.system("rm %s" % destination_for_symlink_to_deli_space_for_current_os)
    os.system("ln -s %s %s" %
              (path_to_deli_space_for_current_os, destination_for_symlink_to_deli_space_for_current_os))

    path_existence_safe_check(path_to_product_space_for_current_os,
                              "ProductSpace for os %s is mandatory." % current_os_name)
    if os.path.islink(destination_for_symlink_to_product_space_for_current_os):
        os.system("rm %s" % destination_for_symlink_to_product_space_for_current_os)
    os.system("ln -s %s %s" %
              (path_to_product_space_for_current_os, destination_for_symlink_to_product_space_for_current_os))

    path_existence_safe_check(path_to_resources_for_current_os,
                              "resources for os %s is mandatory." % current_os_name)
    if os.path.islink(destination_for_symlink_to_resources_for_current_os):
        os.system("rm %s" % destination_for_symlink_to_resources_for_current_os)
    os.system("ln -s %s %s" %
              (path_to_resources_for_current_os, destination_for_symlink_to_resources_for_current_os))

#--------------------------------------#
def get_answer_for_already_moved_files(correct_workspace_path):
    """
     Input : This function takes one string :
     - correct_workspace_path(string) : correct_workspace_path to the current variant and os type;
     Returns :
     - answer(string) : value containing the chosen by the user option
     Summary :
     - This function will be used to get answer from the user which option he wants to
    """

    print_warning("There is already moved files for this variant and os type in %s" % correct_workspace_path
                  +"\nChoose one of the following by writing the number in front :"
                  + "\n1.Delete the already moved files and then move the new ones."
                  + "\n2.Open workspace path to the already moved files."
                  + "\n3.Exit")

    answer = raw_input()

    return answer

#---------------------------------------#
def print_message_for_wrong_chosen_function_and_exit(current_variant_name):
    """
     Input : This function takes one string :
     - current_variant_name(string) : current variant name;
     Returns :
     - None
     Summary :
     - This function will be used print the message when the user chooses wrong function and after that will exit
        with the default code for this script '313'.
    """

    print_warning("| Please try again by passing one of the following options: |")
    print("move_files - will move all necessary workspace files for all possible os types from directory: %s"
                                                                                                    % PATH_TO_ARTIFACTS_OF_BSP_BUILD)
    print_warning("Note (for build options) : the build options will ask do you want "
                  + "to create images after the build finish.")
    print("build Linux Integrity - this option will build both os types for current variant : %s"
                                                                                            % current_variant_name)
    print("build Linux - this option will build only Linux part for current variant : %s" % current_variant_name)
    print("build Integrity - this option will build only Integrity part for current variant : %s"
                                                                                            % current_variant_name)
    print("rebuild Linux Integrity - this option will make rebuild for both os types for current variant : %s"
                                                                                            % current_variant_name)
    print("rebuild Linux - this option will make rebuild only Linux part for current variant : %s" % current_variant_name)
    print("rebuild Integrity - this option will make rebuild only Integrity part for current variant : %s"
                                                                                            % current_variant_name)
    print("create_images - this option will create images, but only if there are moved and built all possible "
            + "os types for the current variant."
            + "\n  (This must be done with script local_image_create.py)")
    os._exit(313)

#-------------------------------#
#------------ MAIN -------------#
#-------------------------------#

def main(argv):
    start = time.time()
    os.chdir(SCRIPTS_ROOT)
    argv = argv[1:]
    argv = [x.lower() for x in argv]
    total_args = len(argv)
    environment_vars_file_name = "environment_vars_for_product.txt"
    full_path_to_environment_vars_file = os.path.join(SCRIPTS_ROOT, environment_vars_file_name)
    build_name = ""

    # Check if environment_vars_for_product.txt exists and exit if doesn't exists
    path_existence_safe_check(full_path_to_environment_vars_file,
                              "\nYou maybe executed the script from the one of the OS type builds. You need to execute it from the main nightly build!")

    # Get BUILD_NAME which is necessary for next steps
    with open(full_path_to_environment_vars_file) as f:

        lines = f.readlines()
        for line in lines:
            if "BUILD_NAME" in line:
                build_name = map(lambda x: x.rstrip("\n"), line.split("="))[1]
                break

    if  is_none_or_empty_string(build_name):
        print_failure("<!> ERROR <!> : The environment variable BUILD_NAME is missing in file %s."
                                                                                % (full_path_to_environment_vars_file))
        os._exit(313)

    current_variant_name = get_variant(build_name)
    is_current_variant_having_linux = True

    if current_variant_name in VARIANTS_WITHOUT_LINUX:
        is_current_variant_having_linux = False


    if total_args == 0:
        print_message_for_wrong_chosen_function_and_exit(current_variant_name)

    # Check arguments options : ("move_files", "build", "create_images")
    if total_args >= 1:
        if "move_files" in argv:
            execute_move_files(is_current_variant_having_linux, current_variant_name)
        elif "rebuild" in argv:
            execute_build(argv, current_variant_name, is_current_variant_having_linux, True)
            print_success("Passed time for rebuild: "
                                                + time.strftime("%H:%M:%S",time.gmtime(time.time() - start)) + ".")
        elif "build" in argv:
            execute_build(argv, current_variant_name, is_current_variant_having_linux, False)
            print_success("Passed time for build: "
                                                + time.strftime("%H:%M:%S",time.gmtime(time.time() - start)) + ".")
        elif "create_images" in argv:
            execute_create_images(is_current_variant_having_linux, current_variant_name)
            print_success("Passed time for create images: "
                                                + time.strftime("%H:%M:%S", time.gmtime(time.time() - start)) + ".")
        else:
            print_message_for_wrong_chosen_function_and_exit(current_variant_name)


if __name__ == "__main__":
    main(sys.argv)