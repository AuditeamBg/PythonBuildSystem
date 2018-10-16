'''
Created on Sep 8, 2014

@author: Zhivko Zapryanov
'''

# System level includes
import sys
import os
import json
import errno

# Local module includes
sys.path.append("../../")
import bspos_build
from bspos_build import bspos


class bitbake(bspos):
    '''
        The main class which is responsible for bitbake builds
    '''
    
    # The absolute path to the workspace directory
    __WORKSPACE_DIR = None
    
    # eagle config file
    __EAGLE_CONFIG_FILE = None
    
    # eagle artifacts folder
    __EAGLE_ARTIFACTS_DIR = "build/tmp/deploy/images"
    
    # Jenkins build ID
    __BUILD_ID = None

    def __init__(self, system, build_id, sdk_type):
        '''
            Init the parent class (bspos)
        '''
        super(bitbake,self).__init__(system, build_id, sdk_type)
        
        # Set build id
        self.__BUILD_ID = build_id
        
        # Set the workspace dir, it is equal to Jenkins workspace + Jenkins Build ID
        try:            
            self.__WORKSPACE_DIR = os.environ['WORKSPACE']+"/"+self.__BUILD_ID
            self.__WORKSPACE_DIR = self.sh_escape(self.__WORKSPACE_DIR)
        except KeyError:
            print("Please set the WORKSPACE Environment variable requared for Jenkins build \n")
            sys.exit(2)
            
        self.__EAGLE_CONFIG_FILE = self.__WORKSPACE_DIR+"/plugins/conf/bitbake_local.conf"
              
    def workspace_init (self):
        
        print self.__WORKSPACE_DIR
        
        # 1. Create the new workspce dir
        try:
            os.makedirs(self.__WORKSPACE_DIR)
        except OSError as e:
            if e.errno != errno.EEXIST:
                raise # handle the errors different from directory already exist
            else:
                print self.__WORKSPACE_DIR+" directory already exist.\n"
        
        # Parse system config file to get the init command
        system_config = self.get_system_config_file()
        
        # Get the system, which we are building currently
        system = self.get_system()
        
        # Get the fetch command for this system
        fetch_command = system_config[system]["fetch_command"]
        
        # Get build config dir, it should be copy to the new workspace
        build_config_dir = system_config[system]["build_config_dir"]
        
        # Get the enter env command
        build_env_command = system_config[system]["build_env_command"]
                    
        # 2. Fetch needed repositories for the build
        command  = "cd "+self.__WORKSPACE_DIR+" && "
        command += fetch_command+" && "
        command += "repo sync"
        self.system_or_die(command)
        
        # 3. Check if we have optional packages and add them if we have
        if 'AdditionalPackages' in os.environ:
            command  = "python "+self.__WORKSPACE_DIR+"/BSPOS_BS1.0/plugins/bitbake/add_optionals.py "+self.__WORKSPACE_DIR
            self.system_or_die(command)
        
        # 4. Prepare workspace configuration
        command  = "cd "+self.__WORKSPACE_DIR+" && "
        command += build_env_command+" && "
        command += "cp -p "+self.__WORKSPACE_DIR+"/"+build_config_dir+"/* ./conf/"
        self.system_or_die(command)
         
    def build (self):       
        
        # Parse system config file to get the init command
        system_config = self.get_system_config_file()
        
        # Get the system, which we are building currently
        system = self.get_system()
        
        # Get the fetch command for this system
        build_env_command = system_config[system]["build_env_command"]
        build_command = system_config[system]["build_command"]
        
        # 1. Initialize build variables and execute the build
        command = "cd "+self.__WORKSPACE_DIR+" && "
        command += build_env_command+" && "
        command += build_command
        self.system_or_die(command)
          
    def post_processes (self):
        
        # Get the system, which we are building currently
        system = self.get_system()
        
        # 1. Create symlink to the artifact directory
        command = "cd "+self.__WORKSPACE_DIR+" && "
        command += "ln -s ../"+self.__BUILD_ID+"/"+self.__EAGLE_ARTIFACTS_DIR+"/"+system+" ../artifacts/"+self.__BUILD_ID
        self.system_or_die(command)
        
        
        
        