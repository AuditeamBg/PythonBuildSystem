#!/bin/sh

if [ -d Tools/IntegrityBSP ]; then
  d=`ls -d Tools/IntegrityBSP/ghs.nvidia.int*/drive-t*ref-integrity/integrity*`
  if [ -d $d ]; then
    basename $d | sed 's/-/ /g'
  fi
  if [ -f Tools/IntegrityBSP/version.txt ]; then
    echo -n "BSP "
    cat Tools/IntegrityBSP/version.txt
  fi
fi
if [ -f Tools/drive-t*ref-linux/KernelLinux/doc/ReleaseNotes.txt ]; then
  sed -n -e 's/#//g;s/.*Kernel/Kernel/g;/VERSION/{p;q}' Tools/drive-t*ref-linux/KernelLinux/doc/ReleaseNotes.txt
fi
if [ -d HMI ]; then
  cd HMI
  ls *.7z | sed 's/.7z//;s/_/ /g'
fi
if [ -f HMI/hmi/dihmi.info ]; then
  sed -n -e 's/-Kanzi version\(.*\)/Kanzi version\1/p' HMI/hmi/dihmi.info
fi
if [ -f SourceSpace/IF1ThriftMe/ReleaseNotes.txt ]; then
  sed -n -e 's/#//g;s/.*IF1/IF1/g;/VERSION/{p;q}' SourceSpace/IF1ThriftMe/ReleaseNotes.txt
  sed -n -e '/Changes/{n;p;n;p;n;p}' SourceSpace/IF1ThriftMe/ReleaseNotes.txt | sed 3q
fi
if [ -f SourceSpace/Reflash/CoreReflash/doc/RevisionHistory.txt ]; then
  sed -n 's/,.*//;/CoreReflash \([0-9]*\.[0-9]*[\.0-9]*\)/{p;q}' SourceSpace/Reflash/CoreReflash/doc/RevisionHistory.txt
fi
if [ -f SourceSpace/Reflash/UPG/doc/RevisionHistory.txt ]; then
  sed -n 's/,.*//;/UPG \([0-9]*\.[0-9]*[\.0-9]*\)/{p;q}' SourceSpace/Reflash/UPG/doc/RevisionHistory.txt
fi
if [ -f SourceSpace/Reflash/Inireader/doc/RevisionHistory.txt ]; then
  sed -n 's/,.*//;/Inireader \([0-9]*\.[0-9]*[\.0-9]*\)/{p;q}' SourceSpace/Reflash/Inireader/doc/RevisionHistory.txt
fi

