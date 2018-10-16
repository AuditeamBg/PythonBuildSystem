#!/usr/bin/python

import os
import shutil

variant = str(os.getenv('Variant'))
workspace = str(os.getenv('WORKSPACE'))
build_name = str(os.getenv('BUILD_NAME'))
additionalFolderName = str(os.getenv('AdditionalFolderName'))
product_excludes_root = additionalFolderName + '/ProductSpace/' + variant + '/'
product_excludes = []
resources_excludes_root = additionalFolderName + '/resources/dependencies/'
resources_excludes = []
tools_excludes_root = additionalFolderName + '/Tools/'
tools_excludes = []

os.chdir(workspace)
for item in os.listdir(product_excludes_root):
    if os.path.isdir(product_excludes_root + item) and item not in('HMI', 'UICockpit', 'DI', 'HMISDK', 'PlatformOnOff', 'SharedConfig', 'SharedLIBs'):
        product_excludes.append("--exclude='" + product_excludes_root + item + "'")
#if os.path.isdir(product_excludes_root + "UICockpit/UIServerProcess"):
    #product_excludes.append("--exclude='" + product_excludes_root + "UICockpit/UIServerProcess'")

for item in os.listdir(resources_excludes_root):
    if os.path.isdir(resources_excludes_root + item) and not item == 'MRA2':
        resources_excludes.append("--exclude='" + resources_excludes_root + item + "'")
if "INTEGRITY" in variant.upper():
    for item in os.listdir(tools_excludes_root+ "IntegrityBSP/"):
        if os.path.isdir(tools_excludes_root + "IntegrityBSP/" + item) and item not in ('ghs.comp_201416', 'ghs.comp_201416_linux', 'ghs.int1124-P2', '.settings'):
            tools_excludes.append("--exclude='" + tools_excludes_root + "IntegrityBSP/" + item + "'")
tools_excludes.append("--exclude='" + tools_excludes_root + "Autogrator/resources'")

excludes_string = " ".join(product_excludes) + " " + " ".join(resources_excludes) + " " + " ".join(tools_excludes)
os.system("tar --atime-preserve -zcpf %s_Workspace.tar.gz %s %s" % (build_name, additionalFolderName, excludes_string))
shutil.move(build_name + "_Workspace.tar.gz", additionalFolderName + "/artifacts")
