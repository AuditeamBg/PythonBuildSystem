#!/usr/bin/python

import os
import shutil

variant = str(os.getenv("Variant"))
workspace = str(os.getenv("WORKSPACE"))
build_name = str(os.getenv("BUILD_NAME"))
additional_folder_name = str(os.getenv('AdditionalFolderName'))

product_excludes_root = additional_folder_name + '/ProductSpace/' + variant + '/'
resources_excludes_root = additional_folder_name + '/resources/dependencies/'
tools_excludes_root = additional_folder_name + '/Tools/'

path_to_folders_to_archive = additional_folder_name + '/ProductSpace/ ' + additional_folder_name + '/resources/ ' + additional_folder_name + '/Tools/ '

additional_folder_name = str(os.getenv("AdditionalFolderName"))

product_space_excludes = ["HMI", "UICockpit", "DI", "HMISDK", "PlatformOnOff", "SharedConfig", "SharedLIBs"]
tools_excludes = ["ghs.comp_201416", "ghs.comp_201416_linux", "ghs.int1124-P2", ".settings"]
resources_excludes = ["MRA2"]

product_space_excludes_with_prefix = " ".join([ ("--exclude='%s" % product_excludes_root) + x + "'" for x in product_space_excludes])
tools_excludes_with_prefix = " ".join([ ("--exclude='%s" % tools_excludes_root) + x + "'" for x in tools_excludes])
resources_excludes_with_prefix = " ".join([ ("--exclude='%s" % resources_excludes_root) + x + "'" for x in resources_excludes])
full_name_of_the_archive = "%s_additional_resources.tar.gz" % build_name
archive_additional_resources_command = "echo 'visteon' | sudo -S tar -czpvf %s %s %s %s %s" % (full_name_of_the_archive, path_to_folders_to_archive, product_space_excludes_with_prefix, tools_excludes_with_prefix, resources_excludes_with_prefix)

os.system(archive_additional_resources_command)
shutil.move(full_name_of_the_archive, "%s/artifacts" % additional_folder_name)