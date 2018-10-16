#!/usr/bin/python

import yaml
import sys
import os
from subprocess import call
from glob import glob


def generate_dest_path (card_kind, comand1, workspace, card_path):

    if "additional" in card_kind:
        dest_path = workspace + "/" + comand1
        do_sudo = ""

    else:
        dest_path = workspace+card_path+card_kind+os.environ["CARD_VERSION"]+"/"+comand1
        do_sudo = "sudo "

    return dest_path, do_sudo


if __name__ == '__main__':
    #if os.geteuid() != 0:
    #        exit("You need to be root to copy files, try running this script with sudo.")
    #if len(sys.argv) != 2:
    #    exit("This script requires one argument! \n The relative path to the yaml it has to read.")
    try:
        if os.path.dirname(sys.argv[0]) == "":
            workspace = "./../../../"
        else:
            workspace = os.path.dirname(sys.argv[0]) + "/../../../"
        cards = sys.argv[2:]
        card_path = "cards/"
        yaml_data = ""  # yaml data
        #cards = ["additionalLinux","additionalIntegrity","MRA2H2Sdv","MRA2H2MicroSdv","MRA2H2RH850Firmwarev","MRA2H2SpiFlashv","MRA2M2Emmcv","MRA2M2Usbv","coboldv","primaryv"]  # cards by name, edit to add
        with open(sys.argv[1], 'r') as f:
            yaml_data = yaml.load(f, Loader=yaml.Loader)
        for card_kind in cards:
            if yaml_data.get(card_kind, 0):
                for comand in yaml_data[card_kind]:
                    comands = comand.split(',')
                    comands[1] = comands[1].strip()
                    comands[0] = comands[0].strip()
                    # dest_path = workspace+card_path+current_card+os.environ["CARD_VERSION"]+"/"+comands[1]
                    path_sudo = generate_dest_path (card_kind, comands[1], workspace, card_path)
                    dest_path = path_sudo[0]
                    do_sudo = path_sudo[1]
                    if '/' == dest_path[-1]:
                        call(do_sudo + 'mkdir -vp '+dest_path,shell=True)
                    else:
                        slash_ind = dest_path.rfind('/')
                        call(do_sudo + 'mkdir -vp '+dest_path[:slash_ind],shell=True)
                    if call(do_sudo + 'cp -vrp '+workspace+comands[0]+' '+dest_path,shell=True) != 0 :
                        print "[copy_to_card]:Copying files failed!"
        print "[copy_to_card]:Exiting with success!"
        exit(0)
    except KeyError:
        print "Error 1"
        print "copy_to_card for MRA2 FAILED!!!"
