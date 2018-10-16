#!/usr/bin/python

import sys
import os
import time
import errno


class txtColors:
    # Green color
    TAG_OK = '\033[92m'
    # Yellow color
    TAG_WARNING = '\033[93m'
    # Red color
    TAG_FAIL = '\033[91m'
    # End for each color
    TAG_END = '\033[0m'


#------------------------------------#
def get_monolith_variant(variant_name):
    '''
     Input: This function takes one string:
     - variant_name(string) : variant name of the current build.
     Returns :
     - monolith_variant(string) : string which contains the variant name of the given sources
     Summary :
     - This method is used to get the variant of the monolith according to the variant_name of the given sources.
     '''

    variant_name_to_lower = variant_name.lower()
    monolith_variant = ""
    if variant_name_to_lower == "vans" or variant_name_to_lower == "van":
        monolith_variant = "TegraP1Integrity.Dbg.B1hw.C5_VANS.MFA2"
    elif variant_name_to_lower == "trucks" or variant_name_to_lower == "truck":
        monolith_variant = "TegraP1Integrity.Dbg.B1hw.C5_TRUCKS.MFA2"
    elif variant_name_to_lower == "c5":
        monolith_variant = "TegraP1Integrity.Dbg.B1hw.C5.MFA2"
    elif variant_name_to_lower in "ic-h":
        monolith_variant = "TegraP1Integrity.Dbg.B1hw.IC_H.MFA2"
    elif variant_name_to_lower == "ic-e":
        monolith_variant = "TegraP1Integrity.Dbg.B1hw.IC_E.MFA2"
    elif variant_name_to_lower == "c5-se":
        monolith_variant = "TegraP1Integrity.Dbg.B1hw.C5_SE.MFA2"
    else:
        print_failure(
            "ERROR : Variant of build (C5, IC-E, IC-H, C5-SE, Vans, Trucks)"
            " is missing in the name of the sources archive/folder."
            "\nMonolith wasn't created.")
        os._exit(313)
    return monolith_variant


#------------------------------------#
def get_variant(sources):
    '''
     Input: This function takes one string:
     - sources(string) : sources name as string.
     Returns :
     - variant_name(string) : string which contains the variant name of the given sources
     Summary :
     - This method is used to extract the variant name from the given sources.
     '''

    sources_to_lower = sources.lower()
    variant_name = ""
    if "vans" in sources_to_lower or "van" in sources_to_lower:
        variant_name = "Vans"
    elif "truck" in sources_to_lower or "trucks" in sources_to_lower:
        variant_name = "Trucks"
    elif "c5." in sources_to_lower or "c5_" in sources_to_lower:
        variant_name = "C5"
    elif "ic-h" in sources_to_lower:
        variant_name = "IC-H"
    elif "ic-e" in sources_to_lower:
        variant_name = "IC-E"
    elif "c5-se" in sources_to_lower:
        variant_name = "C5-SE"
    else:
        print_failure(
            "ERROR : Variant of build (C5, IC-E, IC-H, C5-SE, Vans, Trucks)"
            " is missing in the name of the sources archive/folder."
            "\nSources name : %s" % (sources))
        os._exit(313)
    return variant_name


#------------------------------------#
def get_type(sources):
    '''
     Input: This function takes one string:
     - sources(string) : sources name as string.
     Returns :
     - type_src(string) : string which contains the type(Daily, Nightly, Release) of the given sources
     Summary :
     - This method is used to extract the type(Daily, Nightly, Release) from the given sources.
     '''
     
    sources_to_lower = sources.lower()
    type_src = ""
    if "daily" in sources_to_lower:
        type_src = "Daily"
    elif "release" in sources_to_lower:
        type_src = "Release"
    elif "nightly" in sources_to_lower:
        type_src = "Nightly"
    else:
        print_failure(
            "ERROR : Type of build (Daily, Nightly, Release) is missing in the name of the sources archive/folder."
            "\nSources name : %s" % (sources))
        os._exit(313)
    return type_src


#------------------------------------#
def get_os(sources):
    '''
     Input: This function takes one string:
     - sources(string) : sources name as string.
     Returns :
     - os_src(string) : string which contains the operating system name of the given sources
     Summary :
     - This method is used to extract the OS type from the given sources.
     '''
    sources_to_lower = sources.lower()
    os_src = ""
    if "integrity" in sources_to_lower:
        os_src = "Integrity"
    elif "linux" in sources_to_lower:
        os_src = "Linux"
    else:
        print_failure("ERROR : OS of build (Integrity, Linux) is missing in the name of the sources archive/folder.")
        os._exit(313)
    return os_src


#------------------------------------#
def get_extract_command(sources, correct_workspace_path):
    '''
     Input: This function takes two strings:
     - sources(string) : sources name as string (format .tar.gz).
     - correct_workspace_path(string) : correct_workspace_path (The same path to the workspace as that on the server).
     Returns :
     - command(string) : string which contains the command for extracting the archive in the correct_workspace_path
     Summary :
     - This method is used to get the command for extracting the sources in the correct_workspace_path..
     '''
    command = ""
    if ".tar.gz" in sources:
        command = "echo 'visteon' | sudo -S  tar -xpvf " + sources + " -C " + correct_workspace_path
    else:
        print_failure("ERROR : The sources archive must be in '.tar.gz' format.")
        os._exit(313)
    return command


#------------------------------------#
def get_correct_workspace_for_current_variant(os_name, variant_name):
    '''
    Input: This function takes two strings:
    - os_name(string) : Operating system name of the current build.
    - variant_name(string) : Project variant name of the current build.
    Returns :
    - none
    Summary :
    - This method is used to generate the correct path to the workspace by os and variant
    '''
    os_name_to_lower = os_name.lower()
    variant_name_to_lower = variant_name.lower()
    
    correct_path_to_workspace = ''
    if os_name_to_lower == "linux":
        if variant_name_to_lower == "c5":
            correct_path_to_workspace = "/workspace/JenkinsWorkspace/DAG_MRA2_MY20_STABLE/C5_Linux/Build"
        elif variant_name_to_lower == "c5-se":
            correct_path_to_workspace = "/workspace/JenkinsWorkspace/DAG_MRA2_MY20_STABLE/C5-SE_Linux/Build"
        elif variant_name_to_lower == "trucks" or variant_name_to_lower == "truck":
            correct_path_to_workspace = "/workspace/JenkinsWorkspace/DAG_MRA2_MY20_STABLE/TRUCK-C5_Linux/Build"
        elif variant_name_to_lower == "vans" or variant_name_to_lower == "van":
            correct_path_to_workspace = "/workspace/JenkinsWorkspace/DAG_MRA2_MY20_STABLE/C5-Vans_Linux/Build"
        else:
            print_failure("ERROR : Variant name in the archive name is missing or wrong please check it and try again.")
            os._exit(313)
    elif os_name_to_lower == "integrity":
        if variant_name_to_lower == "c5":
            correct_path_to_workspace = "/workspace/JenkinsWorkspace/DAG_MRA2_MY20_STABLE/C5_Integrity/Build"
        elif variant_name_to_lower == "c5-se":
            correct_path_to_workspace = "/workspace/JenkinsWorkspace/DAG_MRA2_MY20_STABLE/C5-SE_Integrity/Build/"
        elif variant_name_to_lower == "trucks" or variant_name_to_lower == "truck":
            correct_path_to_workspace = "/workspace/JenkinsWorkspace/DAG_MRA2_MY20_STABLE/TRUCK-C5_Integrity/Build"
        elif variant_name_to_lower == "vans" or variant_name_to_lower == "van":
            correct_path_to_workspace = "/workspace/JenkinsWorkspace/DAG_MRA2_MY20_STABLE/C5-Vans_Integrity/Build"
        elif variant_name_to_lower == "ic-e":
            correct_path_to_workspace = "/workspace/JenkinsWorkspace/DAG_MRA2_MY20_STABLE/IC-E_Integrity/Build"
        elif variant_name_to_lower == "ic-h":
            correct_path_to_workspace = "/workspace/JenkinsWorkspace/DAG_MRA2_MY20_STABLE/IC-H_Integrity/Build"
        else:
            print_failure("ERROR : Variant name in the archive name is missing or wrong please check it and try again.")
            os._exit(313)
    else:
        print_failure("ERROR : Os type in the archive name is missing or wrong please check it and try again.")
        os._exit(313)

    return correct_path_to_workspace


#------------------------------------#
def change_the_linker_options(correct_workspace_path_with_additional_folder):
    '''
    Input: This function takes one string:
    - correct_workspace_path_with_additional_folder(string) : correct workspace path to the current variant and os
                                                                                                with additional folder.
    Returns :
    - none
    Summary :
    - This method is used to change the linker options of the bunny to save additional 15 minutes from the build time
    '''
    integrity_bunion_paths = [
        correct_workspace_path_with_additional_folder + '/SourceSpace/HMI/ClusterEntry/build/variants/',
        correct_workspace_path_with_additional_folder + '/SourceSpace/HMI/ClusterHigh/build/variants/',
        correct_workspace_path_with_additional_folder + '/SourceSpace/HMI/HUD/build/variants/',
        correct_workspace_path_with_additional_folder + '/SourceSpace/UICockpit/UIServerProcess/build/variants/'
    ]
    input_name = 'Integrity.bunion'
    output_name = 'Integrity2.bunion'

    for path in integrity_bunion_paths:
        input_name_with_path = path + input_name
        output_name_with_path = path + output_name

        if os.path.isfile(input_name_with_path):
            with open(input_name_with_path, 'r') as input_file, open(output_name_with_path, 'w') as output_file:
                for line in input_file:
                    if "bunAndDependers.addLinkerOptions('-delete', '-uvfd', '-Olink', '-Osize', '-Omax')" == line.strip():
                        output_file.write("bunAndDependers.addLinkerOptions('-delete', '-uvfd')\n")
                    else:
                        output_file.write(line)

            os.system("echo 'visteon' | sudo -S  rm %s" % (input_name_with_path))
            os.rename(output_name_with_path, input_name_with_path)


#-------------------------------------#
#------------ EXTENSIONS -------------#
#-------------------------------------#

def print_success(message, add_dashes=True):
    """
    Input : This function takes one string :
    - message(string) : message to print
    - add_dashes(boolean) : is necessary to add dashes before and after the message (by default is true)
    Returns :
    - none
    Summary :
    - This method is used to print success messages
    """
    if add_dashes == True:
        count_of_dashes = len(message)

        if '\n' in message:
            message_to_list = message.split('\n')
            count_of_dashes = len(max(message_to_list, key=len))
        dashes = "-" * count_of_dashes

        print(txtColors.TAG_OK + dashes + txtColors.TAG_END)
        print(txtColors.TAG_OK + message + txtColors.TAG_END)
        print(txtColors.TAG_OK + dashes + txtColors.TAG_END)
    else:
        print(txtColors.TAG_OK + message + txtColors.TAG_END)


#------------------------------------#
def print_warning(message, add_dashes=True):
    """
    Input : This function takes one string and one boolean :
    - message(string) : message to print
    - add_dashes(boolean) : is necessary to add dashes before and after the message (by default is true)
    Returns :
    - none
    Summary :
    - This method is used to print warning messages
    """
    if add_dashes == True:
        count_of_dashes = len(message)
        if '\n' in message:
            message_to_list = message.split('\n')
            count_of_dashes = len(max(message_to_list, key=len))
        dashes = "-" * count_of_dashes

        print(txtColors.TAG_WARNING + dashes + txtColors.TAG_END)
        print(txtColors.TAG_WARNING + message + txtColors.TAG_END)
        print(txtColors.TAG_WARNING + dashes + txtColors.TAG_END)
    else:
        print(txtColors.TAG_WARNING + message + txtColors.TAG_END)


#------------------------------------#
def print_failure(message, add_asterisks=True):
    """
    Input : This function takes one string :
    - message(string) : message to print
    - add_asterisks(boolean) : is necessary to add asterisks before and after the message (by default is true)
    Returns :
    - none
    Summary :
    - This method is used to print fail messages
    """
    if add_asterisks == True:
        count_of_asterisks = len(message)
        if '\n' in message:
            message_to_list = message.split('\n')
            count_of_asterisks = len(max(message_to_list, key=len))
        asterisks = "-" * count_of_asterisks

        print(txtColors.TAG_FAIL + asterisks + txtColors.TAG_END)
        print(txtColors.TAG_FAIL + message + txtColors.TAG_END)
        print(txtColors.TAG_FAIL + asterisks + txtColors.TAG_END)
    else:
        print(txtColors.TAG_FAIL + message + txtColors.TAG_END)


#------------------------------------#
#------------ UTILITIES -------------#
#------------------------------------#

def actions_before_exit(os_type, path_to_workspace_of_current_build, variant_name, path_to_workspace_of_bsp_build, is_extracted, is_built):
    """
    Input : This function takes four string and 2 booleans:
    - os_type(string) : operating system type of the current variant
    - path_to_workspace_of_current_build(string) : workspace path to the current variant with the current os type
    - variant_name(string) : name of the current variant
    - path_to_workspace_of_bsp_build(string) : path to workspace of bsp build of the current variant
    - is_extracted(boolean) : variable to tell if the current variant was extracted during the usage of the script
    - is_built(boolean) : variable to tell if the current variant was built during the usage of the script
    Returns :
    - none
    Summary :
    - This method is used to do necessary actions before exit
    """
    output_string = ""
    if is_extracted and is_built:
        output_string = " Part has been extracted and built in the directory : "
    elif is_extracted and not is_built:
        output_string = " Part has been extracted in the directory : "
    else:
        output_string = " Part has been built in the directory : "

    name_of_symlink = variant_name + "." + os_type + "Build"
    if not os.path.isdir(name_of_symlink):
        os.system("ln -s " + path_to_workspace_of_current_build + " " + name_of_symlink)

    output_string = os_type + output_string + path_to_workspace_of_current_build
    output_string += "\nSymlink with name " + name_of_symlink + " for this part is created in : " + path_to_workspace_of_bsp_build
    print_warning(output_string)


#-----------------------------------------#
#------------ ERROR HANDLING -------------#
#-----------------------------------------#
def unexpected_error_handling(exit_code, additional_message=""):
    """
    Input : This function takes one int and one string :
    - exit_code(int) : exit code which we use to check if the error is already handled
    - additional_message(string) [optional] : message to append when print the error
    Returns :
    - none
    Summary :
    - This method is used to handle unexpected errors.
    """
    if exit_code == 313:
        # if the exit code is 313 the error is already handled
        os._exit(1)
    else:
        print_failure(txtColors.TAG_FAIL + "ERROR : An unexpected error occurred." + additional_message)
        os._exit(exit_code)


#------------------------------------#
def path_existence_safe_check(file_system_object, additional_message=""):
    """
     Input : This function takes two strings :
     - file_system_object(string) : name of the path to check;
     - additional_message(string) [optional] : message to append when print the error
     Returns :
     - none
     Summary :
     - This method will check if path exists. And if the path doesn't exists will throw exception.
    """
    if not os.path.exists(file_system_object):
        if ".7z" in file_system_object or ".tar" in file_system_object:
            print_failure("ERROR : Archive " + file_system_object + " doesn't exist." + additional_message)
        else:
            print_failure("ERROR : File system object " + file_system_object + " doesn't exist." + additional_message)

        os._exit(313)


#-------------------------------#
#------------ MAIN -------------#
#-------------------------------#

def main(argv):
    start = time.time()
    total_args = len(argv)
    os.chdir("../../")
    is_only_build = False
    os_src = ""
    variant_src = ""
    main_dir = ""
    os_builds_with_workspaces = {}
    additional_folder_name = "/IncrementalBuild"
    correct_workspace_path_with_additional_folder = ""
    is_high_or_entry_variant = False
    is_called_for_local_image_create = False

    # Exiting if the sources or the variant for build aren't passed as argument
    if total_args < 2:
        print_failure("ERROR : Please pass the sources archive or the variant which you want to build as argument.")
        os._exit(313)

    # If on of the parameters is extract that means that this script is called for image create.
    # And it will use only the functionality for extracting the files in the correct workspace path.
    # The build will be processed by script pre_local_build_images_os.py.
    if "extract" in argv:
        is_called_for_local_image_create = True
        argv = filter(lambda arg: arg != "extract", argv)
        total_args = len(argv)

    if main_dir == "":
        main_dir = os.getcwd()

    for i in range(1, total_args):
        sources = str(argv[i])

        # You need to pass combination of Variant + OsType Example: C5.Integrity to make only build without extracting archive #
        if ".tar.gz" in argv[i]:
            is_only_build = False
        else:
            is_only_build = True

        ##---------------------- Initialization of commonly needed variables ----------------------##


        os_src = get_os(sources)
        variant_src = get_variant(sources)

        # We skip the steps for building if the variant is IC-E or IC-H and the os type is Linux.
        # Because they don't have Linux ^.^
        if variant_src == "IC-E" or variant_src == "IC-H":
            is_high_or_entry_variant = True

        if is_high_or_entry_variant == True and os_src == "Linux":
            continue

        correct_workspace_path = get_correct_workspace_for_current_variant(os_src, variant_src)
        os_builds_with_workspaces[os_src] = correct_workspace_path
        correct_workspace_path_with_additional_folder = correct_workspace_path + additional_folder_name
        ##---------------------- Initialization of commonly needed variables ----------------------##


        ##---------------------- Safe check for already extracted variant in the correct_workspace_path ----------------------##
        answer = ""
        if os.path.isdir(correct_workspace_path) \
                and (os.path.isdir(correct_workspace_path_with_additional_folder + "/SourceSpace")
                     or os.path.isdir(correct_workspace_path_with_additional_folder + "/DeliSpace")
                     or os.path.isdir(correct_workspace_path_with_additional_folder + "/InterSpace")
                     or os.path.isdir(correct_workspace_path_with_additional_folder + "/ProductSpace")):

            answer = ""
            if is_only_build == False and is_called_for_local_image_create == False:
                print_warning(
                    "There is already extracted archive for this variant and os type in " + correct_workspace_path +
                    "\nChoose one of the following by writing the number in front :" +
                    "\n1.Delete the already extracted archive and then extract and build passed one" +
                    "\n2.Build the already extracted archive without extracting the passed one" +
                    "\n3.Exit")
                answer = raw_input()

                while answer not in ('1', '2', '3'):
                    print_failure("ERROR : You must choose option 1, 2 or 3. Try Again")
                    print_warning(
                        "There is already extracted archive for this variant and os type in " + correct_workspace_path +
                        "\nChoose one of the following by writing the number in front :" +
                        "\n1.Delete the already extracted archive and then extract and build passed one" +
                        "\n2.Build the already extracted archive without extracting the passed one" +
                        "\n3.Exit")
                    answer = raw_input()
                if answer == '3':
                    os._exit(313)
                elif answer == '1':
                    print("------------------------------------")
                    print("Deleting the extracted archive from:")
                    print("'" + correct_workspace_path + "'")
                    print("...")

                    path_existence_safe_check(correct_workspace_path)
                    os.system("echo 'visteon' | sudo -S  rm -rf " + (correct_workspace_path + additional_folder_name))
                    os.system("echo 'visteon' | sudo -S  rm -rf " + (main_dir + variant_src + '.' + os_src))

            elif is_called_for_local_image_create == True:
                print_warning(
                    "There is already extracted archive for this variant and os type in " + correct_workspace_path +
                    "\nChoose one of the following by writing the number in front :" +
                    "\n1.Delete the already extracted archive and then extract the passed one" +
                    "\n2.Exit")
                answer = raw_input()

                while answer not in ('1', '2'):
                    print_failure("ERROR : You must choose option 1 or 2. Try Again")
                    print_warning(
                        "There is already extracted archive for this variant and os type in " + correct_workspace_path +
                        "\nChoose one of the following by writing the number in front :" +
                        "\n1.Delete the already extracted archive and then extract the passed one" +
                        "\n2.Exit")

                    answer = raw_input()
                if answer == '2':
                    os._exit(313)
                elif answer == '1':
                    print("------------------------------------")
                    print("Deleting the extracted archive from:")
                    print("'" + correct_workspace_path + "'")
                    print("...")

                    path_existence_safe_check(correct_workspace_path)
                    os.system("echo 'visteon' | sudo -S  rm -rf " + (correct_workspace_path + additional_folder_name))
                    os.system("echo 'visteon' | sudo -S  rm -rf " + (main_dir + variant_src + '.' + os_src))
            else:
                is_only_build = True
        ##------------------- Safe check for already extracted variant in the correct_workspace_path ----------------------##


        ##---------------------- Necessary steps for incremental build start ----------------------##
        if is_only_build == False:
            try:
                print("------------------------------------")
                print("Creating the path tree to correct workspace:")
                print("'" + correct_workspace_path + "'")
                print("...")
                os.system("echo 'visteon' | sudo -S  mkdir -p " + correct_workspace_path)
                os.system("echo 'visteon' | sudo -S  chmod -R 777 " + os.path.dirname(correct_workspace_path))
            except OSError as e:
                if e.errno == errno.EPERM:
                    print_failure("ERROR : You do not have permission for operation mkdir.")
                    os._exit(313)
                elif e.errno == errno.EACCES:
                    print_failure("ERROR : You do not have access to create the path tree.")
                    os._exit(313)
                else:
                    unexpected_error_handling(e.message, "Creating the path tree failed!")
            except BaseException as e:
                unexpected_error_handling(e.message, "Creating the path tree failed!")

            print("\n------------------------------------")
            print("Extracting the archive '" + sources + "'")
            print("...")
            try:
                os.chdir("artifacts")
                path_existence_safe_check(correct_workspace_path)
                path_existence_safe_check(sources)
                command_extract = get_extract_command(sources, correct_workspace_path)
                os.system(command_extract)
                print_success("Extracted the archive '" + sources + "'.")
                os.chdir("../")
            except OSError as e:
                if e.errno == errno.EACCES:
                    non_accessible_folder = ""
                    if correct_workspace_path in str(e):
                        non_accessible_folder = correct_workspace_path
                    elif main_dir in str(e):
                        non_accessible_folder = main_dir
                    print_failure("ERROR : You do not have access change the directory to " + non_accessible_folder + ".")
                    os._exit(313)
                else:
                    unexpected_error_handling(e.message, "Extracting archive failed!")
            except BaseException as e:
                unexpected_error_handling(e.message, "Extracting archive failed!")
        ##---------------------- End of steps for incremental build ----------------------##

        # If is called for local image create continue because we don't need The local build
        if is_called_for_local_image_create == True:
            continue

        ##---------------------- Building Steps Start ----------------------##
        print("\n------------------------------------")
        print("Starting build on " + os_src)
        print("...")
        try:
            if os_src == "Integrity":
                change_the_linker_options(correct_workspace_path_with_additional_folder)
            folder_ci_build_system = correct_workspace_path_with_additional_folder + "/CI.BuildSystem"
            path_existence_safe_check(folder_ci_build_system)
            os.chdir(folder_ci_build_system)
            command = "echo 'visteon' | sudo -S  chmod -R 777 %s" % correct_workspace_path_with_additional_folder
            os.system(command)
            command = "echo 'visteon' | sudo -S  ./perform_build.sh local"
            os.system(command)
            os.chdir(main_dir)
            print_success("Finished build on " + os_src + ".")

        except OSError as e:
            if e.errno == errno.EACCES:
                non_accessible_folder = correct_workspace_path_with_additional_folder
                print_failure("ERROR : You do not have access change the directory to " + non_accessible_folder + ".")
                actions_before_exit(os_src, correct_workspace_path, variant_src, main_dir, True, False)
                os._exit(313)
            else:
                unexpected_error_handling(e.message, "Build failed!")
                actions_before_exit(os_src, correct_workspace_path, variant_src, main_dir, True, False)
        except BaseException as e:
            unexpected_error_handling(e.message, "Build failed!")
            actions_before_exit(os_src, correct_workspace_path, variant_src, main_dir, True, False)

        if os_src == "Integrity":
            print("\n------------------------------------")
            print("Recreating monolith for " + os_src)
            print("...")
            try:
                path_existence_safe_check(correct_workspace_path_with_additional_folder)
                command = "echo 'visteon' | sudo -S  chmod -R 777 " \
                          + correct_workspace_path_with_additional_folder \
                          + "/resources/"
                os.system(command)
                folder_monolith = correct_workspace_path_with_additional_folder \
                                  + "/resources/dependencies/MRA2/mra2_monolith/"
                path_existence_safe_check(folder_monolith, "Monolith folder is mandatory!")
                os.chdir(folder_monolith)
                monolith_variant = get_monolith_variant(variant_src)
                command = "echo 'visteon' | sudo -S  ./recreate_monolith.sh TegraP1Integrity.Dbg.B0hw.C5.MRA2" \
                          + monolith_variant
                os.system(command)
                print_success("Monolith recreated.")

            except OSError as e:
                if e.errno == errno.EACCES:
                    non_accessible_folder = correct_workspace_path_with_additional_folder
                    print_failure("ERROR : You do not have access change the directory to " + non_accessible_folder + ".")
                    os._exit(313)
                else:
                    unexpected_error_handling(e.message, "Recreating of the monolith failed!")
            except BaseException as e:
                unexpected_error_handling(e.message, "Recreating of the monolith failed!")

                ##---------------------- End of Building Steps ----------------------##

    print_success("Passed time: " + time.strftime("%H:%M:%S", time.gmtime(time.time() - start)) + ".")
    for os_type in os_builds_with_workspaces:
        if is_only_build == False:
            actions_before_exit(os_type, os_builds_with_workspaces[os_type], variant_src, main_dir, False, True)
        else:
            actions_before_exit(os_type, os_builds_with_workspaces[os_type], variant_src, main_dir, True, True)


if __name__ == "__main__":
    main(sys.argv)
