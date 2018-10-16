#!/bin/sh

# This script creates reflash images, 
# but should not be used as an entry point,
# use /plugins/MRA2/create_images.py

echo '[perform_build]:CreateReflashImagesLinux.sh'
parentdir="$(dirname "${SCRIPT_ROOT}")"

#strip="/opt/nvidia/t168/tegra-5.0.4-nv/sysroots/x86_64-oesdk-linux/usr/libexec/aarch64-gnu-linux/gcc/aarch64-gnu-linux/6.2.0/strip -s"
# Create boot images for reflashing
if [ -d "${parentdir}/artifacts" ]; then
    echo 'visteon' | sudo -S rm -rf ${parentdir}/artifacts/*_Images.7z || true
else
    mkdir -p ${parentdir}/artifacts
fi

# Create reflash dir
if [ ! -d "${parentdir}/ReflashImages" ]; then
    mkdir -p ${parentdir}/ReflashImages
fi

cd ${parentdir}


if [ -d resourcesLinux ]; then
rm -fr resourcesLinux
fi

if [ ! -d ${parentdir}/resources/dependencies/drive-t186ref-linux/out/targetfs/var/visteon/cinemo ]; then
	mkdir -p ${parentdir}/resources/dependencies/drive-t186ref-linux/out/targetfs/var/visteon/cinemo
fi

ln -s resources resourcesLinux

echo "Building the artifacts.. "
/usr/bin/time -v sudo -S 7zr a -l -r ${BUILD_NAME}_Images.7z resourcesLinux -m0=lzma2:d=1m:mt=12 -mx=0  -ms=100f512m -y -xr\@$SCRIPT_ROOT/scripts/symlinks-excludes-linux.txt -x!*.a -x!*.h -x!*.cpp -x!*.hpp -x!*.bunion -x!*.o \
        -x!*.cdl -x!*.fidl -x!*.sdf -x!*.sd -x!*.siz -x!*.Template -x!*.user -x!*.vcxproj -x!*.vsd -x!*.xlsx -x!*.sbs -x!*.bunion -x!*.kzproj  -x!*.sln  -x!*.psd -x!*.dnm -x!*.dep -x!*.ael -x!*/inc/* -x!*.template  -x!*.glsl  -x!*.cc  -x!*/Images/*

unlink resourcesLinux

mv ${BUILD_NAME}_Images.7z ${parentdir}/artifacts/ | true
