#!/usr/bin/python

from subprocess import call
import os
import re
import pprint
class code_bunnies: #I don't know yet what else the class will be used for so I picked a unique sounding name with no meaning

    #name: inject_bunnies
    #input:  the root directory from where to search for bunnies
    #returns: none
    def inject_bunnies(self,root):


        inject_dict =            {"IC-C5_SE":{
                                          "private/build/HAL_RUI.bunion":"bun.addDefines('VARIANT_IC');",
                                          "private/build/HAL_WLAN.bunion":"bun.addDefines('VARIANT_IC');",
                                          "private/build/HAL_Media.bunion":"bun.addDefines('VARIANT_IC');"
                                          },
                                  "IC-E":{
                                          "private/build/UIServerProcess.bunion":"bun.addDefines('VARIANT_IC');",
                                          "private/build/HAL_cluster.bunion":"bun.addDefines('VARIANT_IC');",
                                          "private/build/HAL_AM.bunion":"bun.addDefines('VARIANT_IC');",
                                          "private/build/HAL_BT.bunion":"bun.addDefines('VARIANT_IC');",
                                          "private/build/HAL_Contacts.bunion":"bun.addDefines('VARIANT_IC');",
                                          "private/build/HAL_Phone.bunion":"bun.addDefines('VARIANT_IC');",
                                          "private/build/HAL_Settings.bunion":"bun.addDefines('VARIANT_IC');",
                                          "private/build/HAL_Tuner.bunion":"bun.addDefines('VARIANT_IC');",
                                          "private/build/HAL_Media.bunion":"bun.addDefines('VARIANT_IC');",
                                          "private/build/ClusterEntry.bunion":"bun.addDefines('VARIANT_IC');"
                                          },
                                  "IC-H":{
                                          "private/build/UIServerProcess.bunion":"bun.addDefines('VARIANT_IC');",
                                          "private/build/HAL_cluster.bunion":"bun.addDefines('VARIANT_IC');",
                                          "private/build/HAL_AM.bunion":"bun.addDefines('VARIANT_IC');",
                                          "private/build/HAL_BT.bunion":"bun.addDefines('VARIANT_IC');",
                                          "private/build/HAL_Contacts.bunion":"bun.addDefines('VARIANT_IC');",
                                          "private/build/HAL_Phone.bunion":"bun.addDefines('VARIANT_IC');",
                                          "private/build/HAL_Settings.bunion":"bun.addDefines('VARIANT_IC');",
                                          "private/build/HAL_Tuner.bunion":"bun.addDefines('VARIANT_IC');",
                                          "private/build/HAL_Media.bunion":"bun.addDefines('VARIANT_IC');"
                                          }
                                  }

        build_type = "empty"
        reg_hmi = re.compile("Integrity/Build")
        for btype in inject_dict:
            reg = re.compile(btype)
            if reg.search(os.environ["JOB_NAME"]) and reg_hmi.search(os.environ["JOB_NAME"]):
                build_type = btype
                break
            else:
                build_type = "empty"
        if build_type == "empty":
            return
        for dirname, dirnames, filenames in os.walk(root):
            for filename in filenames:
                for partial_edit_path in inject_dict[build_type]:
                    if partial_edit_path in dirname+'/'+filename:
                        with open(dirname+'/'+filename,'a') as f:
                            f.write("\n"+inject_dict[build_type][partial_edit_path]+"\n")


    #name: get_banned_bunns
    #input: the root directory from where to search for banned domains
    #returns: array of the banned domains
    def get_banned_bunns(self,root,script_name):

        list_of_banned_domains = []
        #we must detect which of the domains we must parse
        for level_one_dir in os.listdir(root):
            #checking if they have the script
            try:  #in case we try to open a file instead of a directory
                for level_one_dir_element in os.listdir(os.path.join(root,level_one_dir,"scripts")):
                    if level_one_dir_element == script_name:
                        list_of_banned_domains.append(level_one_dir)
            except:
                print level_one_dir
        return list_of_banned_domains

    #name: get_top_buns
    #input: the root directory from where to search for bunion files
    #returns: array of the top level buns - the buns that aren't required by other buns
    def get_top_buns(self,root):

        list_of_components = [] #all components who's bunion files were found
        list_of_dependancies = [] #all components named as required in said bunion files
        list_of_top_buns = [] #result of checking which components don't appear as required
        list_of_binaries = []


        list_of_banned_domains = self.get_banned_bunns(root,"Build.sh")
        #list_of_banned_domains.append(self.get_banned_bunns(root,"Build.H2Lin.sh"))

        for dirname, dirnames, filenames in os.walk(root):
            #parse path to all filenames.
            for filename in filenames:
                if filename.endswith('bunion') and dirname.split('/')[-2] == filename.split('.bunion')[0]:  #skip all that is not bunion and where requirements are not kept
                    f = open(os.path.join(dirname, filename), 'r+')
                    contents = f.read()
                    component_name = dirname.split('/')[-3] + '.' + dirname.split('/')[-2]
                    level_one_dir_specific = dirname.split(root)[1].split('/')[1]
                    list_of_components.append([component_name,level_one_dir_specific])
                    parse_now = 0 #bool that checks if we're in the deps lines
                    contents_array = contents.split("\n")
                    for line in contents_array: #parse the contents of the bunion file line by line
                        if "bun.setType(EXE)" in line:
                            list_of_binaries.append(component_name)
                        
                        line = line.strip() #last line of deps
                        if ')' in line and parse_now == 1:
                            parse_now = 0
                            if "'" in line: #case when the ')' isn't on a new line
                                split_line = line.split(',')
                                for splitling in split_line:
                                    if "'" in splitling:
                                        line = splitling.strip()
                                        prefix = line.split("'")[0]
                                        line = line.split("'")[1]
                                        if line not in list_of_dependancies and '#' not in prefix:
                                            list_of_dependancies.append(line)
                        if parse_now == 1 and line != '': #deps
                            split_line = line.split(',')
                            for splitling in split_line:
                                if "'" in splitling:
                                    line = splitling.strip()
                                    prefix = line.split("'")[0]
                                    line = line.split("'")[1]
                                    if line not in list_of_dependancies and '#' not in prefix:
                                        list_of_dependancies.append(line)
                        elif line.find("bun.requires") != -1 and parse_now == 0: #fist line of deps
                            parse_now = 1
                            if "'" in line: #case when the "bun.requires(" doesn't end with a new line
                                split_line = line.split(',')
                                for splitling in split_line:
                                    if "'" in splitling:
                                        line = splitling.strip()
                                        prefix = line.split("'")[0]
                                        line = line.split("'")[1]
                                        if line not in list_of_dependancies and '#' not in prefix :
                                            list_of_dependancies.append(line)
                    f.close()
        print "[code_bunnies]:Banned domains:"
        pprint.pprint(list_of_banned_domains)

        print "[code_bunnies]:List_of_components:"
        pprint.pprint(list_of_components)

        print "[code_bunnies]:List_of_binaries"
        pprint.pprint(list_of_binaries)
        
        bun_log_content = ""
        for single_component in list_of_components: #check which components don't appear as requirements of others
            if single_component[0] not in list_of_dependancies and not single_component[1] in list_of_banned_domains and single_component[0] in list_of_binaries:
                list_of_top_buns.append(single_component[0])
                bun_log_content += "\n"+single_component[0]
#             if "IF1" not in single_component[1]:#APIBuns
#                 #Exclude all ThriftMe and IF1 Components
#                 #Exclude non-buildable Audio bunions
#                 if single_component[0] not in list_of_dependancies and not single_component[1] in list_of_banned_domains:
#                     list_of_top_buns.append(single_component[0])
#             elif "MediaIF1" in single_component[1]:
#                 if single_component[0] not in list_of_dependancies and not single_component[1] in list_of_banned_domains:
#                     list_of_top_buns.append(single_component[0])
#         for binaryItem in list_of_binaries:
#             list_of_top_buns.append(binaryItem)

         #printing a log of the buns present in the build
        path_to_bun_log = root + "/buns_included_log.txt"
        bun_log_file = open(path_to_bun_log,'w+')
        bun_log_file.write(bun_log_content)
        call("chmod 777 "+path_to_bun_log,shell=True)
        return list_of_top_buns





