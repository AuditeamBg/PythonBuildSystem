#!/usr/bin/python

#####################################################################
#
# This script is designed to clean Jenkins servers based
# on RTC.
# It requires a root directory argument and root access.
# It will delete all folders that are all the following
#     1. Named after a number (12) or a # followed by a number(#11)
#     2. Have not had their contents edited in the last day.
#     3. Contain a .jazz5 folder OR is empty OR contains ONLY
#         a Reports folder.
#
# EXAMPLE: sudo python ./ServerCleaner.py workspace
#
#####################################################################

import os
import sys
from subprocess import call
import re
import time

if __name__ == '__main__':
    if os.geteuid() != 0:
            exit("You need to be root to clean the server, try running this script with sudo.")
    if len(sys.argv) != 2:
        exit("This script requires one argument! \n The relative path to the workspace it has to clean.")
    else:
        call("cd "+os.path.abspath(os.path.dirname(sys.argv[0]))+"; pwd;",shell=True)
    reg = re.compile("^#{0,1}[1,2,3,4,5,6,7,8,9,0]{1,10}$")
    full_log = ""
    not_del_log = ""
    delete_log = ""
    template_common = """_______________________________________________________________________________________________________________________________________
{foldername_str} is a number ({dirname_str})
{foldername_str} contains the folders: {dirnames_str}
{foldername_str} contains the files: {filenames_str}
{foldername_str} {msg}
{foldername_str} will {not_b} be deleted
"""
    template_delete = """{dirname_str} will be deletet ({reason})
"""
    template_not_del = """_______________________________________________________________________________________________________________________________________
{foldername_str} contains the folders: {dirnames_str}
{foldername_str} contains the files: {filenames_str}
{dirname_str} will not be deleted {reason}
"""
    for dirname, dirnames, filenames in os.walk(sys.argv[1]):
        foldername = dirname.split('/')[-1]
        if re.match(reg,foldername):
            if os.stat(dirname).st_mtime + 60*60*12 > time.time():
                full_log+=template_common.format(not_b = "not",msg = "is NOT older than 12 hours",foldername_str = foldername , filenames_str = " ".join(filenames), dirname_str = dirname, dirnames_str = " ".join(dirnames))
                not_del_log+=template_not_del.format(reason = "because it was edited in the last 12 hours", foldername_str = foldername , filenames_str = " ".join(filenames), dirname_str = dirname, dirnames_str = " ".join(dirnames))
            elif os.path.exists(dirname+"/.jazz5"):
                full_log+=template_common.format(not_b = "",msg = "contains a jazz5 folder",foldername_str = foldername , filenames_str = " ".join(filenames), dirname_str = dirname, dirnames_str = " ".join(dirnames))
                delete_log+=template_delete.format(dirname_str = dirname, reason = "jazz5")
                call("rm -rf "+dirname, shell=True)
            elif os.listdir(dirname) == []:
                full_log+=template_common.format(not_b = "",msg = "is empty",foldername_str = foldername , filenames_str = " ".join(filenames), dirname_str = dirname, dirnames_str = " ".join(dirnames))
                delete_log+=template_delete.format(dirname_str = dirname, reason = "empty")
                call("rm -rf "+dirname, shell=True)
            elif os.listdir(dirname) == ['Reports']:
                full_log+=template_common.format(not_b = "",msg = "is a functional test build folder",foldername_str = foldername , filenames_str = " ".join(filenames), dirname_str = dirname, dirnames_str = " ".join(dirnames))
                delete_log+=template_delete.format(dirname_str = dirname, reason = "Reports")
                call("rm -rf "+dirname, shell=True)
            else:
                full_log+=template_common.format(not_b = "not",msg = "lacks any of the features of build folder",foldername_str = foldername , filenames_str = " ".join(filenames), dirname_str = dirname, dirnames_str = " ".join(dirnames))
                not_del_log+=template_not_del.format(reason = "because it lacks any of the features of build folder", foldername_str = foldername , filenames_str = " ".join(filenames), dirname_str = dirname, dirnames_str = " ".join(dirnames))
    with open(os.path.dirname(sys.argv[0])+"/log_ServerCleaner.txt","w+") as f:
        f.write(full_log)
    with open(os.path.dirname(sys.argv[0])+"/log_ServerCleaner_to_delete.txt","w+") as f:
        f.write(delete_log)
    with open(os.path.dirname(sys.argv[0])+"/log_ServerCleaner_not_to_delete.txt","w+") as f:
        f.write(not_del_log)



