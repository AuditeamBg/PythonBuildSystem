#!/bin/bash
echo '[perform_build]:CreateReflashImagesReflashLinux.sh START'
U='visteon'
G='visteon'
WORKSPACE="$(dirname "${SCRIPT_ROOT}")"
strip_linux_binaries="${SCRIPT_ROOT}/scripts/extractsymbols.py"
cards_path="${SCRIPT_ROOT}/../cards/"
dest_path="${SCRIPT_ROOT}/../LIN_DBG/"
native_ramdisk_cpio_binaries="${WORKSPACE}/resources/dependencies/drive-t186ref-foundation/native-linux-os/visteon/"
native_ramdisk_cpio_folder="${WORKSPACE}/resources/dependencies/drive-t186ref-foundation/native-linux-os/tmp-cpio/"
native_ramdisk_cpio="${WORKSPACE}/Tools/drive-t186ref-foundation/native-linux-os/native-ramdisk.cpio"
shared_libs="${WORKSPACE}/Doc/IntegrationMra2H2/doc/etc/lib/"
mra_exports="${WORKSPACE}/Doc/IntegrationMra2H2/doc/etc/profile.d/"
swupdate="${WORKSPACE}/Doc/IntegrationMra2H2/doc/etc/swupdate/"
rclocal="${WORKSPACE}/Doc/IntegrationMra2H2/doc/etc/"
rcnetworkconf="${WORKSPACE}/Doc/IntegrationMra2H2/doc/etc/rc.d/"
stripCommandLinux="/opt/nvidia/t168/tegra-5.0.4-nv/sysroots/x86_64-oesdk-linux/usr/libexec/aarch64-gnu-linux/gcc/aarch64-gnu-linux/6.2.0/strip -s "

if [ -d "${native_ramdisk_cpio_binaries}" ]; then
    echo "${native_ramdisk_cpio_binaries}:EXIST"
else
	echo "${native_ramdisk_cpio_binaries}:Something went wrong"
fi

if [ -d "${native_ramdisk_cpio_folder}" ]; then
    sudo rm -rf ${native_ramdisk_cpio_folder}
    if [ $? -eq 0 ]; then
    	echo "OLD ${native_ramdisk_cpio_folder} was deleted"
    	mkdir -p ${native_ramdisk_cpio_folder}
	    if [ $? -eq 0 ]; then
	    	echo "mkdir -p ${native_ramdisk_cpio_folder}:SUCCESS"
	    else
	    	echo "mkdir -p ${native_ramdisk_cpio_folder}:FAILED"
	    fi
    else
    	echo "OLD ${native_ramdisk_cpio_folder} was NOT deleted"
    fi
else
	mkdir -p ${native_ramdisk_cpio_folder}
	if [ $? -eq 0 ]; then
	     echo "mkdir -p ${native_ramdisk_cpio_folder}:SUCCESS"
    else 
    	echo "mkdir -p ${native_ramdisk_cpio_folder}:FAILED"
	fi
fi

if [ -f "${native_ramdisk_cpio}" ]; then
    echo "${native_ramdisk_cpio}:EXIST"
else
	echo "${native_ramdisk_cpio}:Something went wrong"
fi

if [ -f ${WORKSPACE}/resources/dependencies/drive-t186ref-foundation/native-linux-os/native-ramdisk.updated.cpio ]; then
    sudo rm -rf ${WORKSPACE}/resources/dependencies/drive-t186ref-foundation/native-linux-os/native-ramdisk.updated.cpio
    if [ $? -eq 0 ]; then
        echo "Last native-ramdisk.updated.cpio was deleted"
    else
        echo "Last native-ramdisk.updated.cpio was NOT deleted"
    fi
fi

# Create boot images for reflashing
if [ -d ${WORKSPACE}/artifacts ]; then
    sudo rm -rf ${WORKSPACE}/artifacts/*_Images.7z || true
else
    mkdir -p ${WORKSPACE}/artifacts

fi

# Create reflash dir
if [ ! -d "${WORKSPACE}/ReflashImages" ]; then
    mkdir -p ${WORKSPACE}/ReflashImages
fi

if [ ! -d ${WORKSPACE}/resources/dependencies/drive-t186ref-foundation/native-linux-os/tmp-cpio/opt/visteon/bin/ ]; then
    mkdir -p ${WORKSPACE}/resources/dependencies/drive-t186ref-foundation/native-linux-os/tmp-cpio/opt/visteon/bin/
fi

if [ ! -d ${WORKSPACE}/resources/dependencies/drive-t186ref-foundation/native-linux-os/tmp-cpio/opt/visteon/lib/ ]; then
    mkdir -p ${WORKSPACE}/resources/dependencies/drive-t186ref-foundation/native-linux-os/tmp-cpio/opt/visteon/lib/
fi

if [ ! -d ${WORKSPACE}/resources/dependencies/drive-t186ref-foundation/native-linux-os/tmp-cpio/lib/ReflashLib ]; then
    mkdir -p ${WORKSPACE}/resources/dependencies/drive-t186ref-foundation/native-linux-os/tmp-cpio/lib/ReflashLib 
fi

if [ ! -d ${WORKSPACE}/resources/dependencies/drive-t186ref-foundation/native-linux-os/tmp-cpio/etc/profile.d ]; then
    mkdir -p ${WORKSPACE}/resources/dependencies/drive-t186ref-foundation/native-linux-os/tmp-cpio/etc/profile.d 
fi

if [ ! -d ${WORKSPACE}/resources/dependencies/drive-t186ref-foundation/native-linux-os/tmp-cpio/opt/visteon/etc/swupdate ]; then
    mkdir -p ${WORKSPACE}/resources/dependencies/drive-t186ref-foundation/native-linux-os/tmp-cpio/opt/visteon/etc/swupdate
fi

if [ ! -d ${WORKSPACE}/resources/dependencies/drive-t186ref-foundation/native-linux-os/tmp-cpio/opt/visteon/etc/trace ]; then
    mkdir -p ${WORKSPACE}/resources/dependencies/drive-t186ref-foundation/native-linux-os/tmp-cpio/opt/visteon/etc/trace
fi

cd ${native_ramdisk_cpio_folder}

echo "visteon" | sudo -S cpio -i -d -H newc -F ${native_ramdisk_cpio}
echo "visteon" | sudo -S uuidgen >zfile.txt
echo "visteon" | sudo -S cp -vrp ${native_ramdisk_cpio_binaries}* ${native_ramdisk_cpio_folder}/opt/visteon/
echo "visteon" | sudo -S cp -vrp ${shared_libs}* ${native_ramdisk_cpio_folder}/opt/visteon/lib/
echo "visteon" | sudo -S cp -vrp ${mra_exports}* ${native_ramdisk_cpio_folder}/etc/profile.d/
echo "visteon" | sudo -S cp -vrp ${swupdate}* ${native_ramdisk_cpio_folder}/opt/visteon/etc/swupdate
echo "visteon" | sudo -S cp -vrp ${rcnetworkconf}* ${native_ramdisk_cpio_folder}/etc/rc.d/
echo "visteon" | sudo -S cp -vrp ${rclocal}/rc.local ${native_ramdisk_cpio_folder}/etc/rc.local
echo "visteon" | sudo -S cp -vrp ${rclocal}/default.sco ${native_ramdisk_cpio_folder}/opt/visteon/etc/trace

echo "Stripping Reflash Linux Binaries..........START"

${stripCommandLinux} ${native_ramdisk_cpio_folder}/opt/

echo "Stripping Reflash Linux Binaries..........END" 

echo "visteon" | sudo -S find . -print0 | sudo cpio -0 -H newc -o >../../../../../ReflashImages/native-ramdisk.updated.cpio
echo "visteon" | sudo -S chown -R $U:$G ${WORKSPACE}/ReflashImages/native-ramdisk.updated.cpio

cd ${WORKSPACE}

echo "Building the artifacts.. "
/usr/bin/time -v 7zr a ${BUILD_NAME}_Images.7z ReflashImages
sync

mv ${BUILD_NAME}_Images.7z ${WORKSPACE}/artifacts/

# Temporary hack
echo '[perform_build]:CreateReflashImagesReflashLinux.sh FINISH'

