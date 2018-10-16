#!/usr/bin/python

import os
import sys

WORKSPACE = os.getenv("WORKSPACE", None)
BUILD_NUMBER = os.getenv("BUILD_NUMBER", None)
FULL_WORKSPACE_PATH = os.path.join(WORKSPACE, BUILD_NUMBER)
PATH_TO_HMI_DAIMLER_BIN_ARCHIVE = os.path.join(FULL_WORKSPACE_PATH,"resourcesLinux/dependencies/HMI-IVI-Daimler-bin")
PATH_TO_ROOTFS_ARCHIVE = os.path.join(FULL_WORKSPACE_PATH,"resourcesLinux/dependencies/drive-t186ref-linux/out/targetfs")
STARTING_NAME_OF_HMI_DAIMLER_BIN_ARCHIVE = "carbon_ui"
STARTING_NAME_OF_ROOTFS_ARCHIVE = "tegra-genivi-7-image-tegra-t18x.ta"
PATH_TO_TARGETFS = '{}/resourcesLinux/dependencies/drive-t186ref-linux/out/targetfs/'.format(FULL_WORKSPACE_PATH)

def getNameOfRootFSIfExists():
    startingNameOfArchive = STARTING_NAME_OF_ROOTFS_ARCHIVE
    fullNameOfArchive = ''
    isFound = False
    os.chdir(PATH_TO_ROOTFS_ARCHIVE)

    for fileSystemObj in os.listdir(PATH_TO_ROOTFS_ARCHIVE):
        if startingNameOfArchive in fileSystemObj:
            fullNameOfArchive = fileSystemObj
            isFound = True
            break

    if isFound == False:
        print("Error : Not found archive starting with {} in directory {}.".format(startingNameOfArchive,
                                                                                   PATH_TO_ROOTFS_ARCHIVE))
    else:
        print("Found archive - {}".format(fullNameOfArchive))

    os.system("cd -")

    return fullNameOfArchive

def getNameOfDaimlerArchiveIfExists():
    startingNameOfArchive = STARTING_NAME_OF_HMI_DAIMLER_BIN_ARCHIVE
    fullNameOfArchive = ''
    isFound = False
    os.chdir(PATH_TO_HMI_DAIMLER_BIN_ARCHIVE)

    for fileSystemObj in os.listdir(PATH_TO_HMI_DAIMLER_BIN_ARCHIVE):
        if startingNameOfArchive in fileSystemObj:
            fullNameOfArchive = fileSystemObj
            isFound = True
            break

    if isFound == False:
        print("Error : Not found archive starting with {} in directory {}.".format(startingNameOfArchive,
                                                                                   PATH_TO_HMI_DAIMLER_BIN_ARCHIVE))
    else:
        print("Found archive - {}".format(fullNameOfArchive))

    os.system("cd -")

    return fullNameOfArchive


def extractDaimlerArchive(fullPathToArchive, pathToExtractIn):
    if os.path.exists(pathToExtractIn) == False:
        os.system('mkdir -p {}'.format(pathToExtractIn))
    commandForExtract = "echo 'visteon' | sudo -S  tar -xpvf {} -C {}".format(fullPathToArchive, pathToExtractIn)

    result = os.system(commandForExtract)

    commandToExecute = "echo 'visteon' | sudo -S rm {}".format(fullPathToArchive)
    os.system(commandToExecute)

    if os.WEXITSTATUS(result) > 0:
        return ''
    return pathToExtractIn


def copyFilesToTargetFs(nameOfArchive, pathToExtractedFiles):

    os.chdir(pathToExtractedFiles)

    ## Copy outer configuration files ##
    pathToOuterConfigFiles = '{}/etc'.format(PATH_TO_HMI_DAIMLER_BIN_ARCHIVE)
    nameOfInnerExtractedFolder = ''
    dirsInExtractedDir = os.listdir(pathToExtractedFiles)
    if len(dirsInExtractedDir) > 0:
        nameOfInnerExtractedFolder = dirsInExtractedDir[0]
    else:
        print("<!> Warning <!> Nothing found in extracted folder. Exiting ...")
        sys.exit(313)

    pathToExtractedFiles = os.path.join(pathToExtractedFiles, nameOfInnerExtractedFolder)
    commandForCopyingOuterConfigFiles = 'cp -rn {} {}'.format(pathToOuterConfigFiles, pathToExtractedFiles)
    resultOfCopyOuterCfg = os.WEXITSTATUS(os.system(commandForCopyingOuterConfigFiles))
    if resultOfCopyOuterCfg > 0:
        print("<!> Warning <!> Unsuccessful move of outer config files.")

    os.chdir(pathToExtractedFiles)

    for fileSystemObj in os.listdir(pathToExtractedFiles):
        commandForCopyingCurrentFolder = ''

        if os.path.isdir(fileSystemObj):
            print("--- Copying dir : {}".format(fileSystemObj))
            commandForCopyingCurrentFolder = 'cp -rn {} {}'.format(fileSystemObj, PATH_TO_TARGETFS)
        else:
            print("--- Copying file : {}".format(fileSystemObj))
            commandForCopyingCurrentFolder = 'cp -n {} {}'.format(fileSystemObj, PATH_TO_TARGETFS)

        os.system(commandForCopyingCurrentFolder)

    print("<!> Notify <!> Deleting folder with extracted files.")
    os.system('rm -rf {}'.format(os.path.dirname(pathToExtractedFiles)))

def main(argv):
    print("[copying_files_hmi_daimler_bin_to_targerfs] Starting ...")

    nameOfArchive = getNameOfRootFSIfExists()
    if nameOfArchive == '':
        sys.exit(313)

    print("------------- Starting extracting Root FS Archive -------------")
    fullPathToArchive = os.path.join(PATH_TO_ROOTFS_ARCHIVE, nameOfArchive)
    pathToExtractedFiles = extractDaimlerArchive(fullPathToArchive, PATH_TO_ROOTFS_ARCHIVE)
    if pathToExtractedFiles == '':
        print("<!> Warning <!> The extract wasn't successful!")
    print("<!> Success <!> The extract was successful!")

   nameOfArchive = getNameOfDaimlerArchiveIfExists()
    if nameOfArchive == '':
        sys.exit(313)

    print("------------- Starting extracting of Daimler IVI HMI Bin Archive -------------")
    fullPathToArchive = os.path.join(PATH_TO_HMI_DAIMLER_BIN_ARCHIVE, nameOfArchive)
    pathToExtractIn = os.path.join(PATH_TO_HMI_DAIMLER_BIN_ARCHIVE, "carbonui")
    pathToExtractedFiles = extractDaimlerArchive(fullPathToArchive, pathToExtractIn)
    if pathToExtractedFiles == '':
        print("<!> Warning <!> The extract wasn't successful!")
    print("<!> Success <!> The extract was successful!")
    '''
    print("---------------- Starting copying of Daimler IVI HMI Bin ----------------")
    copyFilesToTargetFs(nameOfArchive, pathToExtractedFiles)

    print("[copying_files_hmi_daimler_bin_to_targerfs] Finished.")
    '''
if __name__ == "__main__":
    main(sys.argv)
