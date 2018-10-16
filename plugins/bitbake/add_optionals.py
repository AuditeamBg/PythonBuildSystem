#!/usr/bin/python
import sys
import os

PROJECT_FOLDER = str(sys.argv[1])+'/Eagle-Distribution'
META_FILE = PROJECT_FOLDER + '/conf/bblayers.conf.sample'
PACKAGE_FILE = PROJECT_FOLDER + '/meta-visteon-core/recipes-core/images/dev-image.bb'
OPTIONALS_FILE = PROJECT_FOLDER + '/meta-visteon-optionals/packagegroup-visteon-optionals.bb'

META_ADD = '  ##COREBASE##/../meta-visteon-optionals \\\n  "\n'
PACKAGE_ADD = '    packagegroup-visteon-optionals \\\n    "\n'


def addMeta():
    with open(META_FILE, 'r') as fd:
        lines = fd.readlines()
    pass_line = False
    for i, line in enumerate(lines):
        if 'BBLAYERS ?=' in line:
            pass_line = True
        if pass_line:
            if '  "' in line:
                lines[i] = META_ADD
                break
    with open(META_FILE, 'w') as fd:
        for line in lines:
            fd.write(line)


def addPackageGroup():
    with open(PACKAGE_FILE, 'r') as fd:
        lines = fd.readlines()
    pass_line = False
    for i, line in enumerate(lines):
        if 'IMAGE_INSTALL_append =' in line:
            pass_line = True
        if pass_line:
            if '    "' in line:
                lines[i] = PACKAGE_ADD
                break
    with open(PACKAGE_FILE, 'w') as fd:
        for line in lines:
            fd.write(line)


def addOptionals():
    if 'AdditionalPackages' in os.environ:
        OPTIONALS_ADD = os.environ['AdditionalPackages']
    optionals = OPTIONALS_ADD.split(',')
    for i, o in enumerate(optionals):
        if 'bluez' in o:
            optionals[i] = 'bluez4'
        if 'lua' in o:
            optionals[i] = 'lua'
        optionals[i] = optionals[i].lstrip(" ")
        optionals[i] = optionals[i].rstrip(" ")
        optionals[i] = "    " + optionals[i]
    with open(OPTIONALS_FILE, 'r') as fd:
        lines = fd.readlines()
    pass_line = False
    for i, line in enumerate(lines):
        if 'RDEPENDS_${PN} =' in line:
            pass_line = True
        if pass_line:
            if '    "' in line:
                lines[i] = optionals[0] + " \\\n"
                lines = lines[:i + 1]
                break
    if len(optionals) > 1:
        for i in range(1, len(optionals)):
                lines.append(optionals[i] + " \\\n")
    lines.append('    "\n')
    with open(OPTIONALS_FILE, 'w') as fd:
        for line in lines:
            fd.write(line)
    # for line in lines:
    #     print line

def main():
    addMeta()
    addPackageGroup()
    addOptionals()


if __name__ == '__main__':
    main()