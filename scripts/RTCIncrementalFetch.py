#!/usr/bin/env python

import os
import sys
import yaml
import time

JAZZ_SERVER = "https://jazz.visteon.com:9443/ccm2"
LSCM = '/home/visteon/jazz_4.0.2.1/scmtools/eclipse'
CREDENTIALS = '/opt/credentials/rtc.yaml'
JAZZ_USER = "KARLSRCI"

REPOSITORY_WORKSPACE = sys.argv[1]
STREAM = sys.argv[2]
LOAD_RULES = sys.argv[3]

WORKSPACE = os.getenv("WORKSPACE", None)
AdditionalFolderName = os.getenv("AdditionalFolderName", None)
BUILD_NAME = os.getenv("BUILD_NAME", None)

#WORKSPACE='/home/visteon/workspace/Test/Test_RTC_IncrementalFetch'
#AdditionalFolderName='IncrementalBuild'
#BUILD_NAME='20170309-DAG.MFA2.MY18.E008.IC-C5.Linux.Daily-8.2.104'


CHANGES_AVAILABLE = 0
FETCH_FAILED = 1
ACCEPT_FAILED = 1


# Public interface to get the .yaml file content
def load_yaml(path):
    try:
        stream = open(path, 'r')
        data = yaml.load(stream, Loader=yaml.Loader)
    except:
        print("'" + path + "' can not be found!\n")
        sys.exit(2)
    return data


# Public interface to get credentials from rtc.yaml file
def get_credentials(dic_data, cred_field):
    cred_data = dic_data[cred_field]
    if cred_data == None:
        print "\nEmpty " + cred_field + " ! Check the configuration rtc.yaml file!\n"
        sys.exit(2)
    return cred_data


# Create a Bash file set property for execution
def openBashFile(command_fileL):
    try:
        command_file_strL = open(command_fileL, 'w+')
    except:
        print("\n " + command_fileL + " file can not be opened!!!\n")
        sys.exit(2)
    command = "chmod +x " + command_fileL
    os.system(command)
    return command_file_strL


# Execute a Bash file and delete it after that
def executeBashFile(command_file_streamL, command_fileL, commandL):
    command_file_streamL.write(commandL)
    command_file_streamL.close()
    exit_codeL = os.system('./' + command_fileL)
    os.remove('./' + command_fileL)
    if exit_codeL != 0:
        print "Command execution failed. \n"
        sys.exit(2)


# Remove proxy
def proxy_remove():
    os.system("unset FTP_PROXY")
    os.system("unset HTTPS_PROXY")
    os.system("unset NO_PROXY")
    os.system("unset ftp_proxy")
    os.system("unset https_proxy")
    os.system("unset http_proxy")
    os.system("unset no_proxy")
    os.system("unset HTTP_PROXY")


def print_help():
    print "\n RTCIncrementalFetch.py"


def KillRTCDaemon(RTCDaemon):
    ###############################################################################################
    DAEMON_PORT = os.system("`egrep -o ' [0-9]+' <<< \"%s\" | sed -e 's/^[[:space:]]*//'`" % RTCDaemon)
    ###############################################################################################
    os.system("lsof -i | grep %s | awk '{print $2}' | xargs kill -9" % DAEMON_PORT)


def Load_Result_Command():
    load_result = os.system(
        'cat %s/%s/LOAD_RESULT.TXT | grep -e "Problem running " || LOAD_RESULT=1' % (WORKSPACE, AdditionalFolderName))

    return load_result


def SCM_Download():
    ##################################################################################################################################
    os.system('echo "%s/lscm load -r local -R %s -d %s/%s/ "%s" -f"' % (
    LSCM,LOAD_RULES, WORKSPACE, AdditionalFolderName, REPOSITORY_WORKSPACE))
    ##################################################################################################################################
    os.system('time %s/lscm load -r local -R %s -d %s/%s/ "%s" -f 2>%s/%s/LOAD_RESULT.TXT || true' % (
    LSCM,LOAD_RULES, WORKSPACE, AdditionalFolderName, REPOSITORY_WORKSPACE, WORKSPACE, AdditionalFolderName))
    os.system('cat %s/%s/LOAD_RESULT.TXT'  % (WORKSPACE, AdditionalFolderName))

def Clean_Dir():
    os.chdir(WORKSPACE)
    os.system('echo "visteon" | sudo -S rm -rf %s/.jazz5' % (AdditionalFolderName))
    os.system('echo "visteon" | sudo -S rm -rf %s' % (AdditionalFolderName))
    os.system('echo "visteon" | sudo -S mkdir -p %s/%s/accept' % (os.getcwd(), AdditionalFolderName))
    os.system('echo "visteon" | sudo -S chmod -R 777 %s/%s/accept' % (os.getcwd(), AdditionalFolderName))
    os.chdir("%s/%s/accept" % (os.getcwd(), AdditionalFolderName))

def Accept_Result_Command():
    #accept_result_print = 'time %s/lscm accept -r local -s %s -t "%s" --no-merge --flow-components --overwrite-uncommitted --verbose || true' % (LSCM, STREAM, REPOSITORY_WORKSPACE)
    #print "accept_result_print=",accept_result_print
    accept_result = os.system('time %s/lscm accept -r local -s %s -t "%s" --no-merge --flow-components --overwrite-uncommitted --verbose || true' % (LSCM, STREAM, REPOSITORY_WORKSPACE))
    
    return accept_result

def Accept_Result_And_Write_In_File_Command():
    accept_result = os.system(
        '%s/lscm accept -r local -s %s --no-merge --flow-components --overwrite-uncommitted --verbose 2>%s/ACCEPT_RESULT_FAULT.TXT || true' % (
            LSCM, STREAM, FullPath))

    return accept_result

def Check_Daemon_Command():
    check_daemon = os.system('`cat %s/%s/LOAD_RESULT.TXT | grep -e "already owned by daemon running on port"` || CHECK_DAEMON=1' % (
    WORKSPACE, AdditionalFolderName))

    return check_daemon

def RTC_Update(Stream):
    WORKSPACE = os.getenv("WORKSPACE", None)
    AdditionalFolderName = os.getenv("AdditionalFolderName", None)
    os.chdir("%s/%s/CI.Repository/RTC" % (WORKSPACE, AdditionalFolderName))
    os.system("python ./RTC_update.py -r -n -c -o -t stream %s" % Stream)

username = ""
password = ""

if __name__ == '__main__':
    if (('RTCIncrementalFetch.py' in sys.argv[0]) and (len(sys.argv) > 2)):
        cred_data = load_yaml(CREDENTIALS)
        username = get_credentials(cred_data, 'username')
        password = get_credentials(cred_data, 'password')
    else:
        print_help()
        sys.exit(2)

print "WORKSPACE=",WORKSPACE
print "AdditionalFolderName=",AdditionalFolderName

################################JAZZ LOGIN################################################
##########################################################################################
os.system("%s/lscm login -r %s -n local -u %s -P %s" % (LSCM, JAZZ_SERVER, username, password))
##########################################################################################

FullPath = "%s/%s" % (WORKSPACE, AdditionalFolderName)
if not (os.path.exists(FullPath)):
    os.system('echo "visteon" | sudo -S mkdir -p %s' % FullPath)
    os.system('echo "visteon" | sudo -S chmod -R 777 %s' % FullPath)
   
print "FullPath=",FullPath

FullPathWithAccept = FullPath + "/accept"
if not (os.path.exists(FullPathWithAccept)):
    os.system('echo "visteon" | sudo -S mkdir -p %s' % FullPathWithAccept)
    os.system('echo "visteon" | sudo -S chmod -R 777 %s' % FullPathWithAccept)

print "FullPathWithAccept=",FullPathWithAccept

############################################################################################
FullPathWithJazz = FullPath + "/.jazz5"
if not (os.path.exists(FullPathWithJazz)):
    print "jazz folder does not exist"
    os.chdir(FullPathWithAccept)
    os.system(
        'echo "%s/lscm accept -r local -s %s -t "%s" --no-merge --flow-components --overwrite-uncommitted --verbose"' % (
        LSCM, STREAM, REPOSITORY_WORKSPACE))
    ACCEPT_RESULT = Accept_Result_Command()
    os.chdir(FullPath)
    SCM_Download()
    LOAD_RESULT = Load_Result_Command()
    CHECK_DAEMON = Check_Daemon_Command()

    if (CHECK_DAEMON != 1):
        KillRTCDaemon(CHECK_DAEMON)
        SCM_Download()
        LOAD_RESULT = Load_Result_Command()

    if (LOAD_RESULT != 1):
        print "Loading failed......"
        os.system('cat %s/LOAD_RESULT.TXT' % FullPath)
        sys.exit(3)

    CHANGES_AVAILABLE = 1
    print "CHANGES_AVAILABLE=", CHANGES_AVAILABLE

else:
    os.system('time %s/lscm compare -f b -r local workspace "%s" stream %s -j > %s/COMPARE_RESULT.TXT || true' % (
    LSCM, REPOSITORY_WORKSPACE, STREAM, FullPath))
    NEW_COMPONENT_AVAILABLE = os.system(
        "NEW_COMPONENT_AVAILABLE=`cat %s/COMPARE_RESULT.TXT | grep '\"added\": true'` || NEW_COMPONENT_AVAILABLE=1" % (
        FullPath))

    if (NEW_COMPONENT_AVAILABLE != 1):
        print "\n\n\n----- New component available -----\n"
        print "----- Cleaning workspace -----\n\n\n"

        os.system(
            'echo "%s/lscm accept -r local -s %s -t "%s" --no-merge --flow-components --overwrite-uncommitted --verbose"' % (
            LSCM, STREAM, REPOSITORY_WORKSPACE))

        ACCEPT_RESULT = Accept_Result_Command()
        Clean_Dir()
        SCM_Download()
        LOAD_RESULT = Load_Result_Command()
        CHECK_DAEMON = Check_Daemon_Command()

        if (CHECK_DAEMON != 1):
            KillRTCDaemon(CHECK_DAEMON)
            Clean_Dir()
            SCM_Download()
            LOAD_RESULT = os.system('`cat %s/%s/LOAD_RESULT.TXT | grep -e "Problem running "` || LOAD_RESULT=1' % (
            WORKSPACE, AdditionalFolderName))

        if (LOAD_RESULT != 1):
            print "Loading failed"
            os.system('cat %s/LOAD_RESULT.txt' % FullPath)
            sys.exit(3)

        CHANGES_AVAILABLE = 1
        print "CHANGES_AVAILABLE=", CHANGES_AVAILABLE

    else:
        os.chdir(FullPath)
        os.system(
            'echo "%s/lscm accept -r local -s %s --no-merge --flow-components --overwrite-uncommitted --verbose "' % (
            LSCM, STREAM))
        ACCEPT_RESULT = os.system(
            '`%s/lscm accept -r local -s %s --no-merge --flow-components --overwrite-uncommitted --verbose 2>%s/ACCEPT_RESULT_FAULT.TXT || true`' % (
            LSCM, STREAM, FullPath))
        CHANGES_AVAILABLE = os.system(
            '`echo -e "%s" | grep -e "Workspace unchanged."` || CHANGES_AVAILABLE=1' % (ACCEPT_RESULT))
        print "CHANGES_AVAILABLE=", CHANGES_AVAILABLE
        ACCEPT_FAILED = os.system(
            '`cat %s/ACCEPT_RESULT_FAULT.TXT | grep -e "Update failed" -e "Problem running "` || ACCEPT_FAILED=1' % (
            FullPath))
        CHECK_DAEMON = os.system(
            '`cat %s/ACCEPT_RESULT_FAULT.TXT | grep -e "already owned by daemon running on port"` || CHECK_DAEMON=1' % (
            FullPath))

        PROBLEM_ACCEPT = os.system("`cat %s/%s/ACCEPT_RESULT_FAULT.TXT | grep -e \"Problem running 'accept':\"` || PROBLEM_ACCEPT=1" % (WORKSPACE, AdditionalFolderName))
        if PROBLEM_ACCEPT != "1":
            RTC_Update(STREAM)


        if (CHECK_DAEMON != 1):
            KillRTCDaemon(CHECK_DAEMON)
            Clean_Dir()

if (ACCEPT_FAILED != 1):
    print "Accept failed:"
    os.system('cat %s/ACCEPT_RESULT_FAULT.TXT' % (FullPath))
    Clean_Dir()

    os.system(
        'echo "%s/lscm accept -r local -s %s -t "%s" --no-merge --flow-components --overwrite-uncommitted --verbose"' % (
        LSCM, STREAM, REPOSITORY_WORKSPACE))
    ACCEPT_RESULT = Accept_Result_Command()

    os.chdir('..')
    SCM_Download()
    LOAD_RESULT = Load_Result_Command()
    CHECK_DAEMON = Check_Daemon_Command()

    if (CHECK_DAEMON != 1):
        KillRTCDaemon(CHECK_DAEMON)
        Clean_Dir()
        SCM_Download()
        LOAD_RESULT = os.system('`cat %s/%s/LOAD_RESULT.TXT | grep -e "Problem running "` || LOAD_RESULT=1' % (
            WORKSPACE, AdditionalFolderName))

    if (LOAD_RESULT != 1):
        print "Loading failed ... "
        os.system('cat %s/LOAD_RESULT.TXT' % (FullPath))
        sys.exit(3)

    CHANGES_AVAILABLE = 1
    print "CHANGES_AVAILABLE=", CHANGES_AVAILABLE

if (CHANGES_AVAILABLE == 1):
    os.system('echo "%s/lscm create snapshot -r local -n %s %s" > SNAPSHOT_CREATE.txt' % (LSCM, BUILD_NAME, STREAM))
    os.system('%s/lscm create snapshot -r local -n %s %s > SNAPSHOT_CREATE.txt' % (LSCM, BUILD_NAME, STREAM))

    os.system('echo -e "\n\nSNAPSHOT : %s" > %s/RTC_FETCH_RESULT.txt' % (BUILD_NAME, FullPath))

os.system('echo -e "%s" >> %s/RTC_FETCH_RESULT.txt' % (ACCEPT_RESULT, FullPath))
print "ACCEPT_RESULT=", ACCEPT_RESULT

os.system('echo "CHANGES_AVAILABLE=%s" > %s/env_config' % (CHANGES_AVAILABLE, FullPath))
os.system('cat %s/env_config' % (FullPath))