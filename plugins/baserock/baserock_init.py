'''
Created on Sep 9, 2014

@author: jenkins
'''

# System level includes
import sys
import os

# Local module includes
sys.path.append("../../")
import bspos_build
from bspos_build import bspos

class baserock_init(bspos):
    '''
    classdocs
    '''
    
    # TODO: chroot location should be parametrized
    chroot_location = "/opt/baserock/chroots/14-20"
    
    # bsp os build system folder
    build_system_name = "BSPOS_BS1.0"
    
    # Jenkins build ID
    __BUILD_ID = None
    
    # The script name, which is entry point for the baserock build
    __ENTRY_POINT_SCRIPT = "execute-baserock-build.sh"
    

    def __init__(self, system, build_id, sdk_type):

        '''
            Init the parent class (bspos)
        '''
        super(baserock_init,self).__init__(system, build_id, sdk_type)
        
        # Set build id
        self.__BUILD_ID = build_id
        
        # Set the workspace dir, it is equal to Jenkins workspace + Jenkins Build ID
        try:            
            self.__WORKSPACE_DIR = os.environ['WORKSPACE']+"/"+self.__BUILD_ID
            self.__WORKSPACE_DIR = self.sh_escape(self.__WORKSPACE_DIR)
        except KeyError:
            print("Please set the WORKSPACE Environment variable requared for Jenkins build \n")
            sys.exit(2)
        
    
        
    def workspace_init (self):
        
        # 1. Copy Build system files to the proper location
        command = "cd "+self.__WORKSPACE_DIR+" && "
        command += "rm -rf "+self.chroot_location+"/"+self.build_system_name+"/plugins/baserock/*.pyc && "
        command += "cp -rp "+self.build_system_name+"/* "+self.chroot_location+"/"+self.build_system_name+"/"
        self.system_or_die(command)

    def build (self):        
        
        # 1. Execute the shell script, which is responsible for the baserock build
        command = "cd "+self.__WORKSPACE_DIR+"/"+self.build_system_name+" && "
        command += "chmod +x ./scripts/"+self.__ENTRY_POINT_SCRIPT+" && "
        command += "./scripts/"+self.__ENTRY_POINT_SCRIPT
        self.system_or_die(command)
          
    def post_processes (self):        
        
        # 1. Dummy action as it is not needed for baserock build for now
        print " "
