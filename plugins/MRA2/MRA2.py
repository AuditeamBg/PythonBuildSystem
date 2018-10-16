#!/usr/bin/python

import sys
import os
import os.path
import json
import errno
import re
import time
import subprocess

from subprocess import call
from subprocess import check_output

# Local module includes
from bspos_build import bspos


class MRA2(bspos):
    '''
        The main class which is responsible for MRA2 builds
    '''
    # The absolute path to the workspace directory
    __WORKSPACE_DIR = None
    __BUILD_ID = None
    # Jenkins build ID
    
    def __init__(self, system, build_id, sdk_type):
        super(MRA2,self).__init__(system, build_id, sdk_type)
        try:
            print "BUILD_NAME:", os.environ.get("BUILD_NAME")
            self.__BUILD_ID = build_id
            self.__WORKSPACE_DIR = os.environ['WORKSPACE']+"/"+os.environ["AdditionalFolderName"]
            self.__WORKSPACE_DIR = self.sh_escape(self.__WORKSPACE_DIR)

            if any( ["Build" in self.__WORKSPACE_DIR,
                     "STABLE" in self.__WORKSPACE_DIR, 
                     "UNSTABLE" in self.__WORKSPACE_DIR] ):

                if os.path.isdir(self.__WORKSPACE_DIR+"/Tools/Autogrator"):
                    os.environ["IS_PRODUCT_BUILD"] = "True"
                    os.environ["HAS_REALLY"] = "True"
                else:
                    os.environ["IS_PRODUCT_BUILD"] = "False"
                    os.environ["HAS_REALLY"] = "False"

                if any( ["Release_Build" in self.__WORKSPACE_DIR,
                         "Daily_Build" in self.__WORKSPACE_DIR,
                         "Nightly_Build" in self.__WORKSPACE_DIR] ):
                    os.environ["IS_RELEASE_BUILD"] = "True"
                    os.environ["IS_DAILY_BUILD"] = "True"
                else:
                    os.environ["IS_RELEASE_BUILD"] = "False"
                os.environ["IS_DAILY_BUILD"] = "False"

                if "TegraP1Integrity.Rel" in os.environ.get("Variant", None):
                    os.environ["IS_INTEGRITY_BUILD"] = "True"
                else:
                    os.environ["IS_INTEGRITY_BUILD"] = "False"
            
                if "TegraP1Lin.Rel" in os.environ.get("Variant", None):
                    os.environ["IS_LINUX_BUILD"] = "True"
                else:
                    os.environ["IS_LINUX_BUILD"] = "False"

                if "TegraP1Lin.Dbg" in os.environ.get("Variant", None):
                    os.environ["IS_REFLASH_LINUX_Build"] = "True"
                else:
                    os.environ["IS_REFLASH_LINUX_Build"] = "False"

        except KeyError:
            print("Please set the WORKSPACE Environment variable requared for Jenkins build \n")
            sys.exit(2)

        #setting the version somehow, currently manually
        reg = re.compile("^[a-zA-Z\-._0-9]*-(?P<version>[0-9]{0,3}[_.][0-9]{0,3}[_.][0-9]{0,5}[_.[0-9]{0,5}]?)$")
        try:
            os.environ["CARD_VERSION"] = reg.match(os.environ["BUILD_NAME"]).group('version')
        except:
            os.environ["CARD_VERSION"] = "5.0.0"

    @staticmethod
    def run_command(command):
        return check_output(command, shell=True)

    def workspace_init (self):
        try:
            print "workspace_init"
            path_to_env_conf = self.__WORKSPACE_DIR + "/CI.BuildSystem/scripts/env_conf.sh"
            env_conf_content = ""
            for env_var in os.environ:
                    env_conf_content = env_conf_content + "export " + env_var + "=\"" + os.environ[env_var] + "\"\n"
            env_conf_file = open(path_to_env_conf,'w+')
            env_conf_file.write(env_conf_content)
            super(MRA2,self).system_or_die("chmod 777 "+path_to_env_conf)
        except KeyError:
            print "Error 1"
            print "workspace_init for MRA2 FAILED!!!"


    def prebuild (self):
        #component_build.py
        try:
            print "# prebuild for MRA2"
            super(MRA2,self).system_or_die("python " + os.environ["SCRIPT_ROOT"] + "/plugins/MRA2/prebuild.py")
        except KeyError:
            print "Error 1"
            print "prebuild for MRA2 FAILED!!!"

    def build (self):
        #TopLevelBuns=run find top levels
        try:
            print "# build for MRA2"
            super(MRA2,self).system_or_die("python " + os.environ["SCRIPT_ROOT"] + "/plugins/MRA2/perform_build.py")
        except KeyError:
            print "Error 1"
            print "build for MRA2 FAILED!!!"

    def populate_results(self):
        try:
            print "#TODO: add populate_results for MRA2 !!!"
            super(MRA2,self).system_or_die("python " + os.environ["SCRIPT_ROOT"] + "/plugins/MRA2/populate_results.py")
        except KeyError:
            print "Error 1"
            print "populate_results for MRA2 FAILED!!!"
         
    def create_images(self):
        try:
            print "# create_images for MRA2 !!!"
            super(MRA2,self).system_or_die("echo 'visteon' | sudo -S rm -rf ${WORKSPACE}/${AdditionalFolderName}/resources/dependencies/sdcard/*")
            super(MRA2,self).system_or_die("python " + os.environ["SCRIPT_ROOT"] + "/plugins/MRA2/create_images.py")
        except KeyError:
            print "Error 1"
            print "create_images for MRA2 FAILED!!!"

    def post_processes (self):
        try:
            start = time.time()
            if(os.environ["IS_PRODUCT_BUILD"] == "True"):
                if "IC_E.MRA2" in os.environ["Variant"]:
                    super(MRA2,self).system_or_die("cd ${WORKSPACE}/${AdditionalFolderName} ; sudo 7zr u -m0=lzma2:d=1m:mt=12 -mx=0  -ms=100f512m -y -x!*.cpp -x!*.hpp -x!*.h -x!*.c -x!*.a  artifacts/${BUILD_NAME}_Images.7z ./cards")
                    super(MRA2,self).system_or_die("cd ${SCRIPT_ROOT}/scripts; echo 'visteon' | sudo -S -E ./PostbuildUPG.sh ${Variant}-hud")
                    super(MRA2,self).system_or_die("cd ${WORKSPACE}/${AdditionalFolderName} ; sudo 7zr u -m0=lzma2:d=1m:mt=12 -mx=0  -ms=100f512m -y artifacts/${BUILD_NAME}_HUD_Reflash.7z ./UPG_Output-${Variant}-hud > /dev/null")                 
                
                elif "IC_H.MRA2" in os.environ["Variant"]:
                    super(MRA2,self).system_or_die("cd ${WORKSPACE}/${AdditionalFolderName} ; sudo 7zr u -m0=lzma2:d=1m:mt=12 -mx=0  -ms=100f512m -y -x!*.cpp -x!*.hpp -x!*.h -x!*.c -x!*.a  artifacts/${BUILD_NAME}_Images.7z ./cards")
                    super(MRA2,self).system_or_die("cd ${SCRIPT_ROOT}/scripts; echo 'visteon' | sudo -S -E ./PostbuildUPG.sh")
                    super(MRA2,self).system_or_die("cd ${WORKSPACE}/${AdditionalFolderName} ; sudo 7zr u -m0=lzma2:d=1m:mt=12 -mx=0  -ms=100f512m -y artifacts/${BUILD_NAME}_Reflash.7z ./UPG_Output-${Variant} > /dev/null")           
                
                elif "C5.MRA2" in os.environ["Variant"]:
                    super(MRA2,self).system_or_die("cd ${WORKSPACE}/${AdditionalFolderName} ; sudo 7zr u -m0=lzma2:d=1m:mt=12 -mx=0  -ms=100f512m -y -x!*.cpp -x!*.hpp -x!*.h -x!*.c -x!*.a  artifacts/${BUILD_NAME}_Images.7z ./cards ./LIN_DBG")
                    super(MRA2,self).system_or_die("cd ${SCRIPT_ROOT}/scripts ; echo 'visteon' | sudo -S -E ./PostbuildUPG.sh")
                    super(MRA2,self).system_or_die("cd ${WORKSPACE}/${AdditionalFolderName} ; sudo 7zr u -m0=lzma2:d=1m:mt=12 -mx=0  -ms=100f512m -y artifacts/${BUILD_NAME}_Reflash.7z ./UPG_Output-${Variant} > /dev/null")

                else:
                    super(MRA2,self).system_or_die('echo "Unknown Variant:${Variant}"')
                    
                super(MRA2,self).system_or_die("cd ${SCRIPT_ROOT}/scripts ; echo 'visteon' | sudo -S -E ./CreateReadmeDaily.sh ")
            else:
                super(MRA2,self).system_or_die("cp ${WORKSPACE}/${AdditionalFolderName}/SourceSpace/buns_included_log.txt ${WORKSPACE}/${AdditionalFolderName}/artifacts/")
                
            end = time.time() - start
            print "Post process step took : ", end

        except KeyError:
            print "Error 1"
            print "post_processes for MRA2 FAILED!!!"
