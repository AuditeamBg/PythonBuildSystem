'''
Created on Sep 8, 2014

@author: Zhivko Zapryanov
'''

# System level includes
from abc import ABCMeta, abstractmethod
import os
import sys
import json

class bspos(object):
    '''
        This module define the main interfaces for bsp os build,
        it is template module, which should be inherit from all bsp os plugins
    '''

    __metaclass__ = ABCMeta

    # System to build
    __SYSTEM = None

    '''
        Select the kind of SDK you want. The options are:
        BSP for simple rootf, that you can flash to the target
        full SDK for generated filesystem, which as the name implies, gives you an SDK that contains all the libraries and headers for the things you selected to be put in the filesystem narcissus will generate.
    '''
    __SDK_TYPE = None

    # Build ID, which is uniq for every Jenkins build
    __JENKINS_BUILD_ID = None

    def __init__(self, system, build_id, sdk_type):
        '''
            Main variable init
        '''

        self.__SYSTEM = system
        self.__SDK_TYPE = sdk_type
        self.__JENKINS_BUILD_ID = build_id

    # Public interface to get the system to build
    def get_system(self):
        return self.__SYSTEM

    # Public interface to get the SDK Type
    def get_sdk_type(self):
        return self.__SDK_TYPE

    # Public interface to get the Build ID
    def get_build_id(self):
        return self.__JENKINS_BUILD_ID

    '''
        Method : system_or_die

        Description : Method to call shell scripts
    '''
    def system_or_die(self, command):
        print command
        #call_params = shlex.split(command)
        #res = subprocess.call(call_params, shell=True)
        res = os.system(command)
        if res != 0:
            print "ERROR: Execution of (", command, ") failed with error code ", res, "\n"
            #sys.exit(2)

    '''
        Method : sh_escape

        Description : Escape symbols from directory path
    '''
    def sh_escape(self,s):
        return s.replace("(","\\(").replace(")","\\)").replace(" ","\\ ")

    '''
        Method : parse_system_config

        Description : parse system config json file
    '''
    def get_system_config_file(self):
        with open("plugins/conf/systems.json", 'r') as fd:
            return json.load(fd)



    '''
        The abstract methods should be defined in every subclass, which
        is inheriting the current one. These are the main interfaces, which the
        build system will call during it's work
    '''


    '''
        Method : workspace_init

        Description : The responsible of this method is to
                    prepare the build workspace for the build.
                    It needs to copy all needed build scripts before proceed
    '''
    @abstractmethod
    def workspace_init (self):
        # If we call this method, then something is wrong return error
        print "Something is wrong! You have called workspace_init from the parent class"
        sys.exit(2)


    '''
        Method : build

        Description : This method is an entry point for the build
                   it needs to do all build related tasks
    '''
    @abstractmethod
    def build (self):
        # If we call this method, then something is wrong return error
        print "Something is wrong! You have called build from the parent class"
        sys.exit(2)


    '''
        Method : post_processes

        Description : This method is called after the build is done
                    it should make post build tasks eg. create symbolic links
    '''
    @abstractmethod
    def post_processes (self):
        # If we call this method, then something is wrong return error
        print "Something is wrong! You have called post_processes from the parent class"
        sys.exit(2)

    '''
        Method : create_images

        Description : This method is called after the create_images is done
                    it create images
    '''
    @abstractmethod
    def create_images (self):
        # If we call this method, then something is wrong return error
        print "Something is wrong! You have called create_images from the parent class"
        sys.exit(2)

    '''
        Method : populate_results

        Description : This method is called after the populate_results is done
                    it populates results
    '''
    @abstractmethod
    def populate_results (self):
        # If we call this method, then something is wrong return error
        print "Something is wrong! You have called create_images from the parent class"
        sys.exit(2)

    '''
        Method : prebuild

        Description : This method is called after the workspace_init is done
                    it does prebuild stuff
    '''
    @abstractmethod
    def prebuild (self):
        # If we call this method, then something is wrong return error
        print "Something is wrong! You have called prebuild from the parent class"
        sys.exit(2)



