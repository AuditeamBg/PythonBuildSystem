'''
@author: Georgi Zahariev
'''

# System level includesssss
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
from MRA2 import MRA2


class MRA2_APIBuns(MRA2):
    '''
        The class which is responsible for MRA2 builds for APIBuns stream
    '''


    # The absolute path to the workspace directory

    __WORKSPACE_DIR = None
    # Jenkins build ID
    __BUILD_ID = None

    def __init__(self, system, build_id, sdk_type):
        '''
            Init the parent class (mra2)
        '''
        super(MRA2_APIBuns,self).__init__(system, build_id, sdk_type)
#         Set build id
        self.__BUILD_ID = build_id
#
#         # Set the workspace dir, it is equal to Jenkins workspace + Jenkins Build ID
        try:
            self.__WORKSPACE_DIR = os.environ['WORKSPACE']+"/"+os.environ["AdditionalFolderName"]
            self.__WORKSPACE_DIR = self.sh_escape(self.__WORKSPACE_DIR)
        except KeyError:
            print("Please set the WORKSPACE Environment variable requared for Jenkins build \n")
            sys.exit(2)

#         #determine if this is a product build
        if os.path.isdir(self.__WORKSPACE_DIR+"/Tools/Autogrator"):
            os.environ["IS_PRODUCT_BUILD"] = "True"

        else:
            os.environ["IS_PRODUCT_BUILD"] = "False"
            build_name = os.getenv("BUILD_NAME", None)
            if build_name != None:
                if (not "Integrity" in build_name) and (not "Linux" in build_name):
                    os.environ["IS_DOMAIN_BUILD"] = "True"
                else:
                    os.environ["IS_DOMAIN_BUILD"] = "False"

#         # Separate on comma.
#         #determine if this is a Release/Nightly build
        if os.getenv("IS_RELEASE_BUILD") == None:
            if any( ["Release_Build" in self.__WORKSPACE_DIR,
                      "Nightly_Build" in self.__WORKSPACE_DIR,
                      "IC-H_Rebuild" in self.__WORKSPACE_DIR,
                      "IC-E_Rebuild" in self.__WORKSPACE_DIR,
                      "TRUCK-C5_Rebuild" in self.__WORKSPACE_DIR,
                      "Vans_Rebuild" in self.__WORKSPACE_DIR,
                      "C5_Rebuild" in self.__WORKSPACE_DIR] ):
                os.environ["IS_RELEASE_BUILD"] = "True"
            else:
                os.environ["IS_RELEASE_BUILD"] = "False"
            if "Daily_Build" not in self.__WORKSPACE_DIR:
                os.environ["IS_DAILY_BUILD"] = "False"
            else:
                os.environ["IS_DAILY_BUILD"] = "True"
                os.environ["IS_RELEASE_BUILD"] = "True"

        #determine if this is a Daily Integrity build
        if "UNSTABLE" in self.__WORKSPACE_DIR and "Integrity" in os.environ.get("Variant", None):
            os.environ["IS_DAILY_Integrity_BUILD"] = "True"
        else:
            os.environ["IS_DAILY_Integrity_BUILD"] = "False"

        #determine if this is a Daily Integrity build
        if "SmartCore" in self.__WORKSPACE_DIR and "Integrity" in os.environ.get("Variant", None):
            os.environ["IS_DAILY_Integrity_BUILD"] = "True"

        #determine if this is a Daily Integrity build
        if "Diagnostic" in self.__WORKSPACE_DIR:
            os.environ["IS_Domain_BUILD"] = "True"
        else:
            os.environ["IS_Domain_BUILD"] = "False"

        #determine if this is a Daily Linux build
        if "UNSTABLE" in self.__WORKSPACE_DIR and "Lin" in os.environ.get("Variant", None):
            os.environ["IS_DAILY_Linux_BUILD"] = "True"
        else:
            os.environ["IS_DAILY_Linux_BUILD"] = "False"

        #determine if this is a Daily Linux build
        if "SmartCore" in self.__WORKSPACE_DIR and "Lin" in os.environ.get("Variant", None):
            os.environ["IS_DAILY_Linux_BUILD"] = "True"

        #determine if this is a Nightly Integrity build
        if any( ["_STABLE" in self.__WORKSPACE_DIR,
                 "_REBUILD" in self.__WORKSPACE_DIR] ):

            #determine if this is a Nightly Integrity build
            if "Integrity" in os.environ.get("Variant", None):
                os.environ["IS_Nightly_Integrity_BUILD"] = "True"
            else:
                os.environ["IS_Nightly_Integrity_BUILD"] = "False"

            #determine if this is a Nightly Linux build
            if "Lin" in os.environ.get("Variant", None):
                os.environ["IS_Nightly_Linux_BUILD"] = "True"
            else:
                os.environ["IS_Nightly_Linux_BUILD"] = "False"
        else:
            os.environ["IS_Nightly_Integrity_BUILD"] = "False"
            os.environ["IS_Nightly_Linux_BUILD"] = "False"

        if os.path.isdir(self.__WORKSPACE_DIR+"/Tools/Autogrator"):
            os.environ["HAS_REALLY"] = "True"
        else:
            os.environ["HAS_REALLY"] = "False"

        #setting the version somehow, currently manually
        #reg = re.compile("^[a-zA-Z\-._0-9]*-(?P<version>[0-9]{0,5}[_.][0-9]{0,5}[_.][0-9]{0,5}[_.[0-9]{0,5}])$")
        reg = re.compile("^[a-zA-Z\-._0-9]*-(?P<version>[0-9]{0,3}[_.][0-9]{0,3}[_.][0-9]{0,5}[_.[0-9]{0,5}]?)$")
        print "BUILD_NAME", os.environ.get("BUILD_NAME")
        try:
            os.environ["CARD_VERSION"] = reg.match(os.environ["BUILD_NAME"]).group('version')
        except:
            os.environ["CARD_VERSION"] = "0.1.0"

    @staticmethod
    def run_command(command):
        return check_output(command, shell=True)
#
    def workspace_init (self):
        #Create env_conf.sh
        path_to_env_conf = self.__WORKSPACE_DIR + "/CI.BuildSystem/scripts/env_conf.sh"
        env_conf_content = ""
        for env_var in os.environ:
            if env_var == "WORKSPACE": #the workspace is set telative to the
                env_conf_content = env_conf_content + "pushd `dirname $0` > /dev/null\n"
                env_conf_content = env_conf_content + "export " + env_var + "=`pwd`/../../..\n"
                env_conf_content = env_conf_content + "popd > /dev/null\n"
            else:
                env_conf_content = env_conf_content + "export " + env_var + "=\"" + os.environ[env_var] + "\"\n"
        env_conf_file = open(path_to_env_conf,'w+')
        env_conf_file.write(env_conf_content)
        super(MRA2_APIBuns,self).system_or_die("chmod 777 "+path_to_env_conf)

        if os.environ["IS_PRODUCT_BUILD"] == "True":
            if os.path.isdir(self.__WORKSPACE_DIR+"/resources"):
                #Writing ver file for each build. It is used in later stage by Release builds
                SW_VERSION_FILE = os.environ["SCRIPT_ROOT"]+"/../resources/dependencies/ver"
                f = open(SW_VERSION_FILE ,'wr+')
                f.write(os.environ['BUILD_NAME'])
                f.close()

    def prebuild (self):
        super(MRA2_APIBuns,self).system_or_die("python " + os.environ["SCRIPT_ROOT"] + "/plugins/MRA2/prebuild.py")

    def build (self):
        #component_build.py
        #TopLevelBuns=run find top levels
        super(MRA2_APIBuns,self).system_or_die("python " + os.environ["SCRIPT_ROOT"] + "/plugins/MRA2/perform_build.py")

    def build_APIBuns (self):
        #component_build.py
        #TopLevelBuns=run find top levels
        super(MRA2_APIBuns,self).system_or_die("python " + os.environ["SCRIPT_ROOT"] + "/plugins/MRA2/perform_build_APIBuns.py")

    def populate_results(self):
        # Writing version file in Daily/Nightly release builds
        print "#TODO: add populate_results for MRA2 !!!"
         #super(MRA2,self).system_or_die("python " + os.environ["SCRIPT_ROOT"] + "/plugins/MRA2/populate_results.py")
    def create_images(self):
        super(MRA2_APIBuns,self).system_or_die("python " + os.environ["SCRIPT_ROOT"] + "/plugins/MRA2/create_images.py")
        print "# create_images for MRA2 !!!"

    def post_processes (self):
        start = time.time()


        #move the buns log to the artifacts folder
        super(MRA2_APIBuns,self).system_or_die("cp ${WORKSPACE}/${AdditionalFolderName}/SourceSpace/buns_included_log.txt ${WORKSPACE}/${AdditionalFolderName}/artifacts/")

        try:
            if(os.environ["IS_PRODUCT_BUILD"] == "True"):
                if os.environ["IS_RELEASE_BUILD"] == "True":

                    super(MRA2_APIBuns,self).system_or_die("cd ${WORKSPACE}/${AdditionalFolderName} ; /usr/bin/time -v sudo 7zr u -m0=lzma2:d=1m:mt=12 -mx=0  -ms=100f512m -y artifacts/${BUILD_NAME}_Images.7z ./cards> /dev/null")
        except:
            print "IS_PRODUCT_BUILD is missing from the environment. Irrelevant outside product builds."

        try:
            if(os.environ["IS_PRODUCT_BUILD"] == "True"):
                if os.environ["IS_RELEASE_BUILD"] == "True":
                    #super(MRA2,self).system_or_die("cd ${WORKSPACE}/${AdditionalFolderName} ; sudo chmod +x ./Tools/Autogrator/resources/cards/Mfa2M2Emmcv"+os.environ["CARD_VERSION"]+"/master/tool/* ; sudo chmod +x ./Tools/Autogrator/resources/cards/Mfa2M2Emmcv"+os.environ["CARD_VERSION"]+"/master/tool/* ; sudo chmod +x ./Tools/Autogrator/resources/cards/Mfa2M2Emmcv"+os.environ["CARD_VERSION"]+"/master/lin_root/etc/udev/linux_dhcp_setup.sh ")
                    #super(MRA2,self).system_or_die("sudo ln -s /opt/visteon/lib/misc/libGLESv2.so ${WORKSPACE}/${AdditionalFolderName}/Tools/Autogrator/resources/cards/Mfa2M2Emmcv"+os.environ["CARD_VERSION"]+"/master/lin_opt/lib/misc/libGLESv2.so.1 ")
                    #super(MRA2,self).system_or_die("sudo ln -s /opt/visteon/lib/misc/libEGL.so ${WORKSPACE}/${AdditionalFolderName}/Tools/Autogrator/resources/cards/Mfa2M2Emmcv"+os.environ["CARD_VERSION"]+"/master/lin_opt/lib/misc/libEGL.so.1 ")
                    #super(MRA2,self).system_or_die("sudo ln -s /opt/visteon/lib/misc/libEGL.so ${WORKSPACE}/${AdditionalFolderName}/Tools/Autogrator/resources/cards/Mfa2M2Emmcv"+os.environ["CARD_VERSION"]+"/master/lin_upd/opt/visteon/lib/misc/libEGL.so.1 ")
                    #super(MRA2,self).system_or_die("sudo ln -s /opt/visteon/lib/misc/libasound_module_pcm_caro.so ${WORKSPACE}/${AdditionalFolderName}/Tools/Autogrator/resources/cards/Mfa2M2Emmcv"+os.environ["CARD_VERSION"]+"/master/lin_root/usr/lib/alsa-lib/libasound_module_pcm_caro.so ")
                    #super(MRA2,self).system_or_die("sudo ln -s /opt/visteon/lib/misc/libasound_module_pcm_carompc.so ${WORKSPACE}/${AdditionalFolderName}/Tools/Autogrator/resources/cards/Mfa2M2Emmcv"+os.environ["CARD_VERSION"]+"/master/lin_root/usr/lib/alsa-lib/libasound_module_pcm_carompc.so ")
                    #super(MRA2,self).system_or_die("cd ${WORKSPACE}/${AdditionalFolderName} ; /usr/bin/time -v sudo tar -czf artifacts/${BUILD_NAME}_Images.tar Tools/Autogrator/*")
                    #super(MRA2,self).system_or_die("cd ${WORKSPACE}/${AdditionalFolderName} ; /usr/bin/time -v sudo 7zr u -m0=lzma2:d=1m:mt=12 -mx=0  -ms=100f512m -y artifacts/${BUILD_NAME}_Images.7z Tools/Autogrator/* > /dev/null")
                    super(MRA2_APIBuns,self).system_or_die("cd ${WORKSPACE}/${AdditionalFolderName} ; /usr/bin/time -v sudo tar -czf artifacts/IF1.tar resourcesIntegrity/dependencies/additionalIntegrity/IF1/*")
                    super(MRA2_APIBuns,self).system_or_die("cd ${WORKSPACE}/${AdditionalFolderName} ; /usr/bin/time -v sudo tar -czf artifacts/MRA2.tar resourcesIntegrity/dependencies/additionalIntegrity/MRA2/*")
                    #super(MRA2,self).system_or_die("/usr/bin/time -v python " + STRIPPED_IMAGE_SCRIPT + " ${WORKSPACE}/${AdditionalFolderName}/artifacts/${BUILD_NAME}_Images.7z ${WORKSPACE}/${AdditionalFolderName}/Tools")
                elif(os.environ["IS_Nightly_Integrity_BUILD"] == "True"):
                    super(MRA2_APIBuns,self).system_or_die("cd ${WORKSPACE}/${AdditionalFolderName} ; mkdir -p artifacts; /usr/bin/time -v sudo tar -czf artifacts/IF1.tar resources/dependencies/additionalIntegrity/IF1/*")
                    super(MRA2_APIBuns,self).system_or_die("cd ${WORKSPACE}/${AdditionalFolderName} ; /usr/bin/time -v sudo tar -czf artifacts/MRA2.tar resources/dependencies/additionalIntegrity/MRA2/*")
        except:
            print "IS_PRODUCT_BUILD is missing from the environment. Irrelevant outside product builds."

        end = time.time() - start

        print "Post process step took", end
