#!/usr/bin/python

import os
import re
import sys
import subprocess
import os.path as path

######################### VARIABLES ########################################

os.environ["WORKSPACE"] = path.abspath(path.join(os.getcwd(),"../../"))

try:
    os.environ["OBJDUMP"]
except:
    os.environ["OBJDUMP"] = "/opt/nvidia/t168/tegra-5.0.10-nv/sysroots/x86_64-oesdk-linux/usr/libexec/aarch64-gnu-linux/gcc/aarch64-gnu-linux/6.2.0/objdump"

try:
    os.environ["Variant"]
except:
    os.environ["Variant"] = "TegraP1Integrity.Dbg.B1hw.IC-H.MRA2"

try:
    os.environ["pref"]
except:
    if "B1" in Variant:
        if "C5" in os.environ["Variant"]:
            os.environ["pref"] = "-b1"
        elif "IC_H" in os.environ["Variant"]:
            os.environ["pref"] = ""
        else:
            os.environ["pref"] = ""
    else:
        os.environ["pref"] = ""

################################################VIP_BOOTLOADER_UPDATER###################################################################################
try:
    os.environ["VIP_BOOTLOADER"]
except:
    if "C5" in os.environ["Variant"]:
        os.environ["VIP_BOOTLOADER"] = path.abspath(path.join(os.environ["WORKSPACE"],"MRA2.Reflash.ConfigTemplates/Cars_C5/Cars_C5_Bootloader.odx-f"))
    elif "IC_H" in os.environ["Variant"]:
        os.environ["VIP_BOOTLOADER"] = path.abspath(path.join(os.environ["WORKSPACE"],"MRA2.Reflash.ConfigTemplates/Cars_IC-H/Cars_IC-H_Bootloader.odx-f"))
    else:
        os.environ["VIP_BOOTLOADER"] = path.abspath(path.join(os.environ["WORKSPACE"],"MRA2.Reflash.ConfigTemplates/Cars_IC-E/Cars_IC-E_Bootloader.odx-f"))

try:
    os.environ["VIP_BOOTLOADER_CRC"]
except:
    if "C5" in os.environ["Variant"]:
        os.environ["VIP_BOOTLOADER_CRC"] = path.abspath(path.join(os.environ["WORKSPACE"],"cards/Mra2-VIP-C5v" + os.environ["BS_VERSION"] + "/VIP/bin/bootloader_b1/MRA2Fbl-B1_Updater.crc"))
    elif "IC_H" in os.environ["Variant"]:
        os.environ["VIP_BOOTLOADER_CRC"] = path.abspath(path.join(os.environ["WORKSPACE"],"cards/Mra2-VIP-IC-Hv" + os.environ["BS_VERSION"] + "/VIP/bin/bootloader/MRA2Fbl_Updater.crc"))
    else:
        os.environ["VIP_BOOTLOADER_CRC"] = path.abspath(path.join(os.environ["WORKSPACE"],"cards/Mra2-VIP-IC-Ev" + os.environ["BS_VERSION"] + "/VIP/bin/bootloader/MRA2Fbl_Updater.crc"))

try:
    os.environ["VIP_BOOTLOADER_SIG"]
except:
    if "C5" in os.environ["Variant"]:
        os.environ["VIP_BOOTLOADER_SIG"] = path.abspath(path.join(os.environ["WORKSPACE"],"cards/Mra2-VIP-C5v" + os.environ["BS_VERSION"] + "/VIP/bin/bootloader_b1/MRA2Fbl-B1_Updater_cccv2.sig"))
    elif "IC_H" in os.environ["Variant"]:
        os.environ["VIP_BOOTLOADER_SIG"] = path.abspath(path.join(os.environ["WORKSPACE"],"cards/Mra2-VIP-IC-Hv" + os.environ["BS_VERSION"] + "/VIP/bin/bootloader/MRA2Fbl_Updater_cccv2.sig"))
    else:
        os.environ["VIP_BOOTLOADER_SIG"] = path.abspath(path.join(os.environ["WORKSPACE"],"cards/Mra2-VIP-IC-Ev" + os.environ["BS_VERSION"] + "/VIP/bin/bootloader/MRA2Fbl_Updater_cccv2.sig"))

try:
    os.environ["VIP_BOOTLOADER_SREC"]
except:
    if "C5" in os.environ["Variant"]:
        os.environ["VIP_BOOTLOADER_SREC"] = path.abspath(path.join(os.environ["WORKSPACE"],"cards/Mra2-VIP-C5v" + os.environ["BS_VERSION"] + "/VIP/bin/bootloader_b1/MRA2Fbl-B1_Updater.srec"))
    elif "IC_H" in os.environ["Variant"]:
        os.environ["VIP_BOOTLOADER_SREC"] = path.abspath(path.join(os.environ["WORKSPACE"],"cards/Mra2-VIP-IC-Hv" + os.environ["BS_VERSION"] + "/VIP/bin/bootloader/MRA2Fbl_Updater.srec"))
    else:
        os.environ["VIP_BOOTLOADER_SREC"] = path.abspath(path.join(os.environ["WORKSPACE"],"cards/Mra2-VIP-IC-Ev" + os.environ["BS_VERSION"] + "/VIP/bin/bootloader/MRA2Fbl_Updater.srec"))

################################################VIP_BOOTLOADER_UPDATER###################################################################################


################################################VIP_APPLICATION###################################################################################
try:
    os.environ["VIP_ODX"]
except:
    if "C5" in os.environ["Variant"]:
        os.environ["VIP_ODX"] = path.abspath(path.join(os.environ["WORKSPACE"],"MRA2.Reflash.ConfigTemplates/Cars_C5/Cars_C5_VIP_Application.odx-f"))
    elif "IC_H" in os.environ["Variant"]:
        os.environ["VIP_ODX"] = path.abspath(path.join(os.environ["WORKSPACE"],"MRA2.Reflash.ConfigTemplates/Cars_IC-H/Cars_IC-H_VIP_Application.odx-f"))
    else:
        os.environ["VIP_ODX"] = path.abspath(path.join(os.environ["WORKSPACE"],"MRA2.Reflash.ConfigTemplates/Cars_IC-E/Cars_IC-E_VIP_Application.odx-f"))

try:
    os.environ["VIP_CRC"]
except:
    if "C5" in os.environ["Variant"]:
        os.environ["VIP_CRC"] = path.abspath(path.join(os.environ["WORKSPACE"],"cards/Mra2-VIP-C5v" + os.environ["BS_VERSION"] + "/VIP/bin/rel-mra2_c5" + os.environ["pref"] + "-default/rel-mra2_c5" + os.environ["pref"] + "-default_app_only.crc"))
    elif "IC_H" in os.environ["Variant"]:
        os.environ["VIP_CRC"] = path.abspath(path.join(os.environ["WORKSPACE"],"cards/Mra2-VIP-IC-Hv" + os.environ["BS_VERSION"] + "/VIP/bin/rel-mra2_ic" + os.environ["pref"] + "-default/rel-mra2_ic" + os.environ["pref"] + "-default_app_only.crc"))
    else:
        os.environ["VIP_CRC"] = path.abspath(path.join(os.environ["WORKSPACE"],"cards/Mra2-VIP-IC-Ev" + os.environ["BS_VERSION"] + "/VIP/bin/rel-mra2_ic" + os.environ["pref"] + "-default/rel-mra2_ic" + os.environ["pref"] + "-default_app_only.crc"))

try:
    os.environ["VIP_SIG"]
except:
    if "C5" in os.environ["Variant"]:
        os.environ["VIP_SIG"] = path.abspath(path.join(os.environ["WORKSPACE"],"cards/Mra2-VIP-C5v" + os.environ["BS_VERSION"] + "/VIP/bin/rel-mra2_c5" + os.environ["pref"] + "-default/rel-mra2_c5" + os.environ["pref"] + "-default_app_only_cccv2.sig"))
    elif "IC_H" in os.environ["Variant"]:
        os.environ["VIP_SIG"] = path.abspath(path.join(os.environ["WORKSPACE"],"cards/Mra2-VIP-IC-Hv" + os.environ["BS_VERSION"] + "/VIP/bin/rel-mra2_ic" + os.environ["pref"] + "-default/rel-mra2_ic" + os.environ["pref"] + "-default_app_only_cccv2.sig"))
    else:
        os.environ["VIP_SIG"] = path.abspath(path.join(os.environ["WORKSPACE"],"cards/Mra2-VIP-IC-Ev" + os.environ["BS_VERSION"] + "/VIP/bin/rel-mra2_ic" + os.environ["pref"] + "-default/rel-mra2_ic" + os.environ["pref"] + "-default_app_only_cccv2.sig"))

try:
    os.environ["VIP_SRC"]
except:
    if "C5" in os.environ["Variant"]:
        os.environ["VIP_SRC"] = path.abspath(path.join(os.environ["WORKSPACE"],"cards/Mra2-VIP-C5v" + os.environ["BS_VERSION"] + "/VIP/bin/rel-mra2_c5" + os.environ["pref"] + "-default/rel-mra2_c5" + os.environ["pref"] + "-default_app_only.srec"))
    elif "IC_H" in os.environ["Variant"]:
        os.environ["VIP_SRC"] = path.abspath(path.join(os.environ["WORKSPACE"],"cards/Mra2-VIP-IC-Hv" + os.environ["BS_VERSION"] + "/VIP/bin/rel-mra2_ic" + os.environ["pref"] + "-default/rel-mra2_ic" + os.environ["pref"] + "-default_app_only.srec"))
    else:
        os.environ["VIP_SRC"] = path.abspath(path.join(os.environ["WORKSPACE"],"cards/Mra2-VIP-IC-Ev" + os.environ["BS_VERSION"] + "/VIP/bin/rel-mra2_ic" + os.environ["pref"] + "-default/rel-mra2_ic" + os.environ["pref"] + "-default_app_only.srec"))
################################################VIP_APPLICATION###################################################################################


########################### FUNCTIONS #########################################

def dump_an_object(path_to_srec):
    if os.environ["OBJDUMP"] is not None:
        command = "%s%s%s" % (os.environ["OBJDUMP"]," -h ",path_to_srec)
        parsed = subprocess.Popen(command,stdout=subprocess.PIPE,shell=True)
        (out,err) = parsed.communicate()
        return out

def cat_CRC_and_turn_to_hex_without_0x(path_to_CRC):
    crc_elements = []

    with open(path_to_CRC, 'r') as f:
        content = f.read()

    newArray = content.replace('0x','').replace(',','').replace(' ','')
        #newArray = list(filter(lambda x : x != ',', list(filter(lambda item: item.strip(), [element.strip('0x') for element in crc_elements])))) 

    if newArray != None:
        return newArray
    else:
        print "Something went wrong .."
        exit(2)

def cat_SIG_and_turn_to_hex_without_0x(path_to_SIG):
    sig_elements = []
 
    with open(path_to_SIG, 'r') as f:
        content = f.read()
       
    newArray = content.replace('0x','').replace(',','').replace(' ','')
    #newArray = list(filter(lambda x : x != ',', list(filter(lambda item: item.strip(), [element.strip('0x') for element in crc_elements])))) 
    if newArray != None:
        return newArray
    else:
        print "Something went wrong .."
        exit(2)

#############################====MAIN====######################################

if __name__ == '__main__':
    print "Starting Generation of VIP_ODX...."
    if "C5" in os.environ["Variant"]:
        vip_bootloader = "MRA2Fbl-B1_Updater.srec"
    else:
        vip_bootloader = "MRA2Fbl_Updater.srec"
    if "C5" in os.environ["Variant"]:
        vip_srec      = "rel-mra2_c5" + os.environ["pref"] + "-default_app_only.srec"
    else:
        vip_srec      = "rel-mra2_ic" + os.environ["pref"] + "-default_app_only.srec"

    obj_dumped     = dump_an_object(os.environ["VIP_SRC"])
    crc_address    = cat_CRC_and_turn_to_hex_without_0x(os.environ["VIP_CRC"])
    sig_address    = cat_SIG_and_turn_to_hex_without_0x(os.environ["VIP_SIG"])
    sig_address   = "".join(sig_address)
    crc_address   = "".join(crc_address)

    obj2_dumped    = dump_an_object(os.environ["VIP_BOOTLOADER_SREC"])
    crc2_address    = cat_CRC_and_turn_to_hex_without_0x(os.environ["VIP_BOOTLOADER_CRC"])  
    sig2_address    = cat_SIG_and_turn_to_hex_without_0x(os.environ["VIP_BOOTLOADER_SIG"])
    sig2_address   = "".join(sig2_address)
    crc2_address   = "".join(crc2_address)

############################Parse-to-Temp-Files#################################

    with open('temp.srec', 'w') as tmp_file:
        tmp_file.write('<DATAFILE LATEBOUND-DATAFILE="true">')
        tmp_file.write(vip_srec)
        tmp_file.write('</DATAFILE>')

    with open('temp.sig', 'w') as sig_file:
        sig_file.write('<FW-SIGNATURE TYPE="A_BYTEFIELD">')
        sig_file.write(sig_address)
        sig_file.write('</FW-SIGNATURE>')

    with open('temp.crc', 'w') as crc_file:
        crc_file.write('<FW-CHECKSUM TYPE="A_BYTEFIELD">')
        crc_file.write(crc_address)
        crc_file.write('</FW-CHECKSUM>')

    with open('temp.odx', 'w') as segment_file:
        segment_file.write('<SEGMENTS>\n')

        for line in obj_dumped.split('\n'):
            if 'sec' in line:
                index, name, size, VMA, LMA, FILE_OFF, Algn = line.split()
                var=int(VMA,16)+int(size,16)-1
                var=format(var,"08X")
                segment_file.write(' <SEGMENT ID="MRA2-BSP-Segment-' + str(int(index)+1).zfill(2) + '">\n')
                segment_file.write('   <SHORT-NAME>' + name.strip('.').title() + '</SHORT-NAME>\n')
                segment_file.write('   <LONG-NAME>MRA2-BSP-Segment-' + str(int(index)+1).zfill(2) + '</LONG-NAME>\n')
                segment_file.write('   <SOURCE-START-ADDRESS>' + str(format(int(VMA,16),"08X")) + '</SOURCE-START-ADDRESS>\n')
                segment_file.write('   <SOURCE-END-ADDRESS>' + str(var)+ '</SOURCE-END-ADDRESS>\n')
                segment_file.write(' </SEGMENT>\n')

        segment_file.write('</SEGMENTS>')

    with open(os.environ["VIP_ODX"], 'r') as s:
        s_content = s.read()

    pre,  signature = s_content.split('<FW-SIGNATURE TYPE="A_BYTEFIELD">')
    signature, post = signature.split('</FW-SIGNATURE>')

    with open(os.environ["VIP_ODX"], 'w') as s:
        s.write(pre)
        s.write(open('temp.sig', 'r').read().replace('\n','\n\t\t'))
        s.write(post)

    with open(os.environ["VIP_ODX"], 'r') as c:
        c_content = c.read()

    pre,  checksum = c_content.split('<FW-CHECKSUM TYPE="A_BYTEFIELD">')
    checksum, post = checksum.split('</FW-CHECKSUM>')

    with open(os.environ["VIP_ODX"], 'w') as c:
        c.write(pre)
        c.write(open('temp.crc', 'r').read().replace('\n','\n\t\t'))
        c.write(post)

    with open(os.environ["VIP_ODX"], 'r') as f:
        f_content = f.read()

    pre,  segments = f_content.split('<SEGMENTS>')
    segments, post = segments.split('</SEGMENTS>')

    with open(os.environ["VIP_ODX"], 'w') as f:
        f.write(pre)
        f.write(open('temp.odx', 'r').read().replace('\n','\n\t\t'))
        f.write(post)


    with open(os.environ["VIP_ODX"], 'r') as f:
        f_content = f.read()

    pre,  datafile = f_content.split('<DATAFILE LATEBOUND-DATAFILE="true">')
    datafile, post = datafile.split('</DATAFILE>')

    with open(os.environ["VIP_ODX"], 'w') as f:
        f.write(pre)
        f.write(open('temp.srec', 'r').read().replace('\n','\n\t\t'))
        f.write(post)

#################################################################################

    with open('temp2.sig', 'w') as sig2_file:
        sig2_file.write('<FW-SIGNATURE TYPE="A_BYTEFIELD">')
        sig2_file.write(sig2_address)
        sig2_file.write('</FW-SIGNATURE>')

    with open(os.environ["VIP_BOOTLOADER"], 'r') as s:
        s_content = s.read()

    pre,  signature = s_content.split('<FW-SIGNATURE TYPE="A_BYTEFIELD">')
    signature, post = signature.split('</FW-SIGNATURE>')

    with open(os.environ["VIP_BOOTLOADER"], 'w') as s:
        s.write(pre)
        s.write(open('temp2.sig', 'r').read().replace('\n','\n\t\t'))
        s.write(post)

    with open('temp2.crc', 'w') as crc2_file:
        crc2_file.write('<FW-CHECKSUM TYPE="A_BYTEFIELD">')
        crc2_file.write(crc2_address)
        crc2_file.write('</FW-CHECKSUM>')

    with open(os.environ["VIP_BOOTLOADER"], 'r') as c:
        c_content = c.read()

    pre,  checksum = c_content.split('<FW-CHECKSUM TYPE="A_BYTEFIELD">')
    checksum, post = checksum.split('</FW-CHECKSUM>')

    with open(os.environ["VIP_BOOTLOADER"], 'w') as c:
        c.write(pre)
        c.write(open('temp2.crc', 'r').read().replace('\n','\n\t\t'))
        c.write(post)

    with open('temp2.odx', 'w') as segment2_file:
        segment2_file.write('<SEGMENTS>\n')

        for line in obj2_dumped.split('\n'):
            if 'sec' in line:
                index, name, size, VMA, LMA, FILE_OFF, Algn = line.split()
                var=int(VMA,16)+int(size,16)-1
                var=format(var,"08X")
                segment2_file.write(' <SEGMENT ID="MRA2-BSP-Segment-' + str(int(index)+1).zfill(2) + '">\n')
                segment2_file.write('   <SHORT-NAME>' + name.strip('.').title() + '</SHORT-NAME>\n')
                segment2_file.write('   <LONG-NAME>MRA2-BSP-Segment-' + str(int(index)+1).zfill(2) + '</LONG-NAME>\n')
                segment2_file.write('   <SOURCE-START-ADDRESS>' + str(format(int(VMA,16),"08X")) + '</SOURCE-START-ADDRESS>\n')
                segment2_file.write('   <SOURCE-END-ADDRESS>' + str(var)+ '</SOURCE-END-ADDRESS>\n')
                segment2_file.write(' </SEGMENT>\n')

        segment2_file.write('</SEGMENTS>')

    with open(os.environ["VIP_BOOTLOADER"], 'r') as f:
        f_content = f.read()

    pre,  segments = f_content.split('<SEGMENTS>')
    segments, post = segments.split('</SEGMENTS>')

    with open(os.environ["VIP_BOOTLOADER"], 'w') as f:
        f.write(pre)
        f.write(open('temp2.odx', 'r').read().replace('\n','\n\t\t'))
        f.write(post)

    with open('temp2.srec', 'w') as tmp2_file:
        tmp2_file.write('<DATAFILE LATEBOUND-DATAFILE="true">')
        tmp2_file.write(vip_bootloader)
        tmp2_file.write('</DATAFILE>')

    with open(os.environ["VIP_BOOTLOADER"], 'r') as f:
        f_content = f.read()

    pre,  datafile = f_content.split('<DATAFILE LATEBOUND-DATAFILE="true">')
    datafile, post = datafile.split('</DATAFILE>')

    with open(os.environ["VIP_BOOTLOADER"], 'w') as f:
        f.write(pre)
        f.write(open('temp2.srec', 'r').read().replace('\n','\n\t\t'))
        f.write(post)

#################################################################################
        print "End of Generating VIP_ODX...."