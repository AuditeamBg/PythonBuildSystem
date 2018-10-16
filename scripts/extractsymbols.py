#!/usr/bin/python
import os
import time
import sys

def extractSymbols():
    extractSymbolsStartTime = time.time()

    cards_path = sys.argv[1]
    linuxSymbolsDBG = sys.argv[2]

    stripCommandLinux = "/opt/nvidia/t168/tegra-5.0.10-nv/sysroots/x86_64-oesdk-linux/usr/libexec/aarch64-gnu-linux/gcc/aarch64-gnu-linux/6.2.0/strip -s"
    extractDebugSymbols = "/opt/nvidia/t168/tegra-5.0.10-nv/sysroots/x86_64-oesdk-linux/usr/libexec/aarch64-gnu-linux/gcc/aarch64-gnu-linux/6.2.0/objcopy --only-keep-debug"
    linkDebugFile = "/opt/nvidia/t168/tegra-5.0.10-nv/sysroots/x86_64-oesdk-linux/usr/libexec/aarch64-gnu-linux/gcc/aarch64-gnu-linux/6.2.0/objcopy --add-gnu-debuglink="
    os.system(" echo 'before strip' ; /usr/bin/du -hcs " + cards_path + " ; echo 'stripping...'")

    originalBinariesSize = {}
    for dirpath, dirnames, filenames in os.walk(cards_path):
        for filename in [f for f in filenames if "-linux/out/targetfs/opt/" in dirpath]:
            filePath = os.path.join(dirpath, filename)
            if (filePath.endswith(".so") or (('.' not in filename) and os.access(filePath, os.X_OK))) and False == os.path.islink(filePath):
                pass
            else:
                continue
            
            symbolFilePath = filePath + ".dbg"
            cmdExtractSymbols = extractDebugSymbols + " " + filePath + " " + symbolFilePath
            cmdStripCmd = stripCommandLinux + " " + os.path.join(dirpath, filename)
            cmdLinkSymbols = linkDebugFile + symbolFilePath + " " + filePath
            
            if True == os.path.isfile(filePath):
                os.system(cmdExtractSymbols)
            else:
                continue
            
            if False ==  os.path.isfile(filePath):
                exit(1)

            if True == os.path.isfile(symbolFilePath) and True ==  os.path.isfile(filePath):
                os.system(cmdStripCmd)
                if ( False == os.path.isfile(filePath)):
                        print "ERROR file disapear"
                        exit(1)
                originalBinariesSize[ filename] =  (os.path.getsize(filePath),dirpath)
                os.system(cmdLinkSymbols)
                os.system("mkdir -p " + linuxSymbolsDBG)
                os.system("mv " + symbolFilePath + " " + linuxSymbolsDBG)

    os.system(" echo 'after strip' ; /usr/bin/du -hcs " + cards_path + " ; echo 'stripping finished ....'")

if __name__ == '__main__':
    extractSymbols()
        