import os
import sys
import re
import yaml
import shutil
import json
import glob
import time
import subprocess

from subprocess import call
from subprocess import check_output

loadrule_integrity=sys.argv[1]
YamlFile = sys.argv[2]
Variant = sys.argv[3]
print YamlFile

from xml.dom import minidom
xmldoc = minidom.parse(loadrule_integrity)
print xmldoc

YamlData = "" 
YamlBunsList=[] 
BunsToBeRemovedList=[] 
TempBun=""
ProductSpace = "ProductSpace"
InterSpace = "InterSpace"
DeliSpace = "DeliSpace"
SourceSpace = "SourceSpace"

#SCM = '/home/visteon/jazz_4.0.2.1/scmtools/eclipse/fec'
#SCM = '/opt/RTC602_eclipse452_Linux64/scmtools/eclipse/scm'
SCM = '~/jazz_4.0.2.1/scmtools/eclipse/scm'
JAZZ_SERVER = 'https://jazz.visteon.com:9443/ccm2'
CREDENTIALS = '/opt/credentials/rtc.yaml'
username = ""
password = ""
JName_list = []
JBunId_list = []

workspace = os.path.dirname(os.path.realpath(sys.argv[0])) + "/../../"
#try:
#    workspace = os.environ['WORKSPACE']+"/"+os.environ["AdditionalFolderName"]
#    workspace = workspace.replace("(","\\(").replace(")","\\)").replace(" ","\\ ")
#except KeyError:
#    print("Please set the WORKSPACE Environment variable requared for Jenkins build \n")
#    sys.exit(2)
print ("Workspace : " + workspace)
os.chdir(workspace)
#print os.getcwd()

# interface to get the .yaml file content
def read_pipe(p):
    out = ""
    b = 1
    n = 0
    while b == 1:
        s = p.read()
        if s == '':
            b = 0
        try:
            out += s
            n = n + 1
        except:
            b = 0
    return out

def load_yaml(path):
    try:
        stream = open(path, 'r')
    except:
        print("cannot open file '"+path+"'")
        sys.exit(2)
    try:
        data = yaml.load(stream, Loader=yaml.Loader)
    except:
        print("cannot load yaml file '"+path+"'")
        sys.exit(2)
    return data

# interface to get credentials from rtc.yaml file
def get_credentials(dic_data, cred_field):
    cred_data = dic_data[cred_field]
    if cred_data == None:
        print "\nEmpty "+cred_field+"! Check the configuration rtc.yaml file!\n"
        sys.exit(2)
    return cred_data

with open(YamlFile,'r') as intgrty:
    data_intgrty = intgrty.read()
    print ("Data: " + data_intgrty)

YamlData = yaml.load(data_intgrty)

YamlComponentsString=YamlData["Components"]
print "YAML Buns:" + YamlComponentsString

cred_data = load_yaml(CREDENTIALS)
print cred_data
username = get_credentials(cred_data, 'username')
print ("Username : " + username)
password = get_credentials(cred_data, 'password')
print ("Password : " + password)

p = os.popen(SCM + " list components -r "+ JAZZ_SERVER + " -u  "+ username + " -P " + password + " -m 5000 -j  ")
print p
out = read_pipe(p)
print out
r = p.close()
if r == None:
    r = 0

j_file = json.loads(out)
#print j_file
JComponentString= j_file["components"]
#print JComponentString


for jitem in j_file["components"]:
    JName = jitem['name']
    JBunId = jitem['uuid']
    if JName in YamlData["Components"].split():
        JName_list.append(JName)
        print ("JNAME : " + JName)
        JBunId_list.append(JBunId)
        print JBunId

itemlist = xmldoc.getElementsByTagName('parentLoadRule')

for bun in itemlist:	
    for comp in bun.getElementsByTagName('component'):
        if comp.attributes['itemId'].value in JBunId_list:
            for Bun1 in bun.getElementsByTagName('sandboxRelativePath'):
                BunToAppend = Bun1.attributes['pathPrefix'].value
                if BunToAppend not in BunsToBeRemovedList:
                    BunsToBeRemovedList.append(BunToAppend)
print "Found BUNS to be Removed from SourceSpace"
print BunsToBeRemovedList

def system_or_die(command):
    print "Running : "+command+"\n"
    tar_res = os.system(command)
    if tar_res != 0:
        print "\n\nERROR:\nExecution of : ( ", command, " ) failed with error code :", tar_res, "\n\n"

if [Variant == "TegraP1Lin.Rel.B0hw.C5.MRA2"]:
    SystemCommand = "cd "+ workspace +"; "+ workspace +"/Tools/Really/Really/really.sh "+ workspace +"./CI.BuildSystem/source_code/LinuxRelease.py ReleaseSpace/ -f" 
    system_or_die(SystemCommand)
    ReleaseSpace = "ReleaseSpace"
else:
    SystemCommand = "cd "+ workspace +"; "+ workspace +"/Tools/Really/Really/really.sh "+ workspace +"./CI.BuildSystem/source_code/IntegrityRelease.py ReleaseSpace/ -f" 
    system_or_die(SystemCommand)
    ReleaseSpace = "ReleaseSpace"

print os.getcwd()

for line in BunsToBeRemovedList:
    if "SourceSpace" in line:
        
        #get Domain from line after the last "/"
        Domain = line[len("/" + SourceSpace):line.rfind("/")]
        print ("Domain :" + Domain)
        
        #get bunion(bin folder) 
        Bun = line[line.rfind("/"):]
        print ("Bun :" + Bun)
        
        ReleaseSrc = workspace  +  ReleaseSpace + "/" + Variant +  Domain + Bun
        print ("ReleaseSource :" + ReleaseSrc)

        DstCopy = workspace + DeliSpace + "/" + Variant + Domain + Bun
        print ("DstCopy :" + DstCopy)
        #Dest= DstCopy + Bun  #workspace + DeliSpace + "/" + Variant + Domain + Bun
        #print ("Dest :" + Dest)
        
        if os.path.exists(ReleaseSrc):
            shutil.move(ReleaseSrc,DstCopy)
            time.sleep(5)

        #variable for folder that should be deleted from SourceSpace after build folder was moved in DeliSpace
        ScrDirDelete = workspace + SourceSpace + Domain + Bun
        print ("SourceDirDelete : " + ScrDirDelete)

        if os.path.isdir(ScrDirDelete):
            shutil.rmtree(ScrDirDelete)  

InterSpaceDstDlt = workspace + InterSpace #+ "/" + Variant #+ Domain + Bun
print ("InterSpace Destination : " + InterSpaceDstDlt)
if os.path.isdir(InterSpaceDstDlt):
    shutil.rmtree(InterSpaceDstDlt)
cd ..
ProductSpaceDstDlt= workspace + ProductSpace
print ("ProductSpace Delete: " + ProductSpaceDstDlt)
if os.path.isdir(ProductSpaceDstDlt):
    shutil.rmtree(ProductSpaceDstDlt)

#make archive of SourceSpace and DeliSpace
if os.path.isdir(workspace + SourceSpace):
    print "adding SourceSpace"
    os.chdir(workspace)
    system_or_die("sudo 7zr a -m0=lzma2:d=1m:mt=12 -mx=0  -ms=100f512m -y  artifacts/SourceSpace.7z    SourceSpace")
else:
    print "not found" + workspace + SourceSpace

if os.path.isdir(workspace + DeliSpace):
    print "adding DeliSpace"
    os.chdir(workspace)
    system_or_die("sudo 7zr a -m0=lzma2:d=1m:mt=12 -mx=0  -ms=100f512m -y  artifacts/DeliSpace.7z    DeliSpace")
else:
    print "not found" + workspace + DeliSpace