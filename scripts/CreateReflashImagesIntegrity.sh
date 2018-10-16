#!/bin/sh
# zchiflis@visteon.com, apetkov@visteon.com, evelikov@visteon.com preslavpugev@visteon.com
# This script creates reflash images, but should not be used as an entry point.
# Use $SCRIPT_ROOT/plugins/MRA2/create_images.py.
# set -e

visteon=`echo 'visteon' | sudo -S mktemp -d -p /media`
parentdir="$(dirname ${SCRIPT_ROOT})"
NANDNAME="8GB_fat32.img"
DEVICE=""

checkForErrors(){
    prevResult=$?
    if [ $prevResult != 0 ]; then
        echo "Error encountered by mk-common.sh. ABORTING..."
        exit 1
    fi
}

#***************************#
#***************************#
#         DEPLOYMENT        #
#***************************#
#***************************#

checkEmmcSize()
{
    local status=0

    SIZE=`fdisk -l $DRIVE | grep Disk | grep bytes | awk '{print $5}'`
    if [ "$SIZE" -lt "104857600" ]; then
        echo ""
        echo "The size of drive $DRIVE is $SIZE bytes."
        echo "This is too small for an eMMC device (NAND flash). "
        echo "Perhaps you accidentally mounted the SPI-flash device (NOR flash)."
        echo "Please rerun the <Autogrator deploy> command supplying the eMMC device as parameter."
        echo "ABORTING..."
        echo ""
        status=1
    else
        echo ""
        echo "The size of drive $DRIVE is $SIZE bytes."
        echo ""
    fi

    return $status
}

check_if_mounted()
{
    mount | grep "^$DRIVE"
    [ "$?" = "0" ] && echo "++ ERROR: Umount any partition on $DRIVE ++" && exit 1
}

getAutoGuessFileName()
{
    fname="";
    for entry in "$FILESPATH"/$1
    do
        if [ -f $entry ] && [ ! -h $entry ]; then
            if [ -z $fname ]; then
                fname=$entry;
            else
                if [ $entry -nt $fname ]; then
                    fname=$entry;
                fi
            fi
        fi
    done

    eval $2=$fname
}

getFileName()
{
    local rd=""
    echo -n "$1: "
    read rd
    if [ ! $rd = "" ]; then
        eval $2=$rd
    fi
}

getFileNames()
{
    if [ ! -d ${FILESPATH} ]; then
        echo "Invalid path specified: ${FILESPATH}"
        exit 1;
    fi
}

makePartitions()
{
    #make partitions

    local status=0

    {
        echo o          # Create empty DOS partition table.
        echo n          # New
        echo p          #   primary partition
        echo 1          #   #1
        echo            #   follows (at next 1 MiB border after MBR)
        echo +32M       #   with 32 MiB size.
        echo t          # Type (of partition #1)
        echo da         #   is 0xDA (non-FS data).
        echo n          # New
        echo e          #   extended partition
        echo 2          #   #2
        echo            #   follows (directly, at 1 MiB border)
        echo +7652M     #   with 7652 MiB size. (Adjust when changing logical partitions!)
        echo n          # New
        echo l          #   logical partition (#5)
        echo            #   follows (at next 1 MiB border after first EBR in extended partition)
        echo +2328M     #   with 2328 MiB size.
        echo t          # Type
        echo 5          #   of partition #5
        echo c          #   is 0x0C (FAT32).
        echo n          # New
        echo l          #   logical partition (#6)
        echo            #   follows (at next 1 MiB border after another EBR)
        echo +8M        #   with 32 MiB size.
        echo t          # Type
        echo 6          #   of partition #6
        echo da         #   is 0xDA (non-FS data).
        echo n          # New
        echo l          #   logical partition (#7)
        echo            #   follows (at next 1 MiB border after another EBR)
        echo +128M      #   with 128 MiB size.
        echo t          # Type
        echo 7          #   of partition #7
        echo c          #   is 0x0C (FAT32).
        echo n          # New
        echo l          #   logical partition (#8)
        echo            #   follows (at next 1 MiB border after another EBR)
        echo +256M      #   with 256 MiB size.
        echo t          # Type
        echo 8          #   of partition #8
        echo c          #   is 0x0C (FAT32).
        echo n          # New
        echo l          #   logical partition (#9)
        echo            #   follows (at next 1 MiB border after another EBR)
        echo +64M       #   with 64 MiB size.
        echo t          # Type
        echo 9          #   of partition #9
        echo da         #   is 0xDA (non-FS data).
        echo n          # New
        echo l          #   logical partition (#10)
        echo            #   follows (at next 1 MiB border after another EBR)
        echo +64M       #   with 64 MiB size.
        echo t          # Type
        echo 10         #   of partition #10
        echo c          #   is 0x0C (FAT32).
        echo n          # New
        echo l          #   logical partition (#11)
        echo            #   follows (at next 1 MiB border after another EBR)
        echo +2424M     #   with 2424 MiB size.
        echo t          # Type
        echo 11         #   of partition #11
        echo c          #   is 0x0C (FAT32).
        echo n          # New
        echo l          #   logical partition (#11)
        echo            #   follows (at next 1 MiB border after another EBR)
        echo +32M       #   with 32 MiB size.
        echo t          # Type
        echo 12         #   of partition #12
        echo da         #   is 0xDA (non-FS data).
        echo n          # New
        echo l          #   logical partition (#13)
        echo            #   follows (at next 1 MiB border after first EBR in extended partition)
        echo +2328M     #   with 2328 MiB size.
        echo t          # Type
        echo 13         #   of partition #13
        echo c          #   is 0x0C (FAT32).
        echo n          # New
        echo l          #   logical partition (#14)
        echo            #   follows (at next 1 MiB border after first EBR in extended partition)
        echo +8M        #   with 8 MiB size.
        echo t          # Type
        echo 14         #   of partition #14
        echo da         #   is 0xDA (non-FS data).
        echo p          # Print partition table.
        echo w          # Write partition table.
    } | fdisk $NANDNAME

    status=$?

    # sleep 1

    # # ignore partition reread warning only for virtual block devices (loop)
    # if [[ $status == 1 ]] && [[ $DRIVE == *loop* ]]; then
    #     status=0
    #     echo "Ignoring reread warning on virtual block device!"
    # fi

    # # actively scan the partitions inside the virtual block device
    # partprobe $DRIVE

    return $status
}

makeFilesystems()
{
    #make filesystems

    # handle various device names.
    # note something like fdisk -l /dev/loop0 | egrep -E '^/dev' | cut -d' ' -f1
    # won't work due to https://bugzilla.redhat.com/show_bug.cgi?id=649572

    local status=0
    DRIVE=$DEVICE
    DRIVE_NAME=`basename $DRIVE`
    DEV_DIR=`dirname $DRIVE`

    echo "DRIVE:$DRIVE"

    PARTITION1=${DRIVE}1
    if [ ! -b ${PARTITION1} ]; then
        PARTITION1=${DRIVE}p1
    fi
    if [ ! -b ${PARTITION1} ]; then
        PARTITION1=$DEV_DIR/${DRIVE_NAME}p1
    fi

    PARTITION5=${DRIVE}5
    if [ ! -b ${PARTITION5} ]; then
        PARTITION5=${DRIVE}p5
    fi
    if [ ! -b ${PARTITION5} ]; then
        PARTITION5=$DEV_DIR/${DRIVE_NAME}p5
    fi

    PARTITION6=${DRIVE}6
    if [ ! -b ${PARTITION6} ]; then
        PARTITION6=${DRIVE}p6
    fi
    if [ ! -b ${PARTITION6} ]; then
        PARTITION6=$DEV_DIR/${DRIVE_NAME}p6
    fi

    PARTITION7=${DRIVE}7
    if [ ! -b ${PARTITION7} ]; then
        PARTITION7=${DRIVE}p7
    fi
    if [ ! -b ${PARTITION7} ]; then
        PARTITION7=$DEV_DIR/${DRIVE_NAME}p7
    fi

    PARTITION8=${DRIVE}8
    if [ ! -b ${PARTITION8} ]; then
        PARTITION8=${DRIVE}p8
    fi
    if [ ! -b ${PARTITION8} ]; then
        PARTITION8=$DEV_DIR/${DRIVE_NAME}p8
    fi

    PARTITION9=${DRIVE}9
    if [ ! -b ${PARTITION9} ]; then
        PARTITION9=${DRIVE}p9
    fi
    if [ ! -b ${PARTITION9} ]; then
        PARTITION9=$DEV_DIR/${DRIVE_NAME}p9
    fi

    PARTITION10=${DRIVE}10
    if [ ! -b ${PARTITION10} ]; then
        PARTITION10=${DRIVE}p10
    fi
    if [ ! -b ${PARTITION10} ]; then
        PARTITION10=$DEV_DIR/${DRIVE_NAME}p10
    fi

    PARTITION11=${DRIVE}11
    if [ ! -b ${PARTITION11} ]; then
        PARTITION11=${DRIVE}p11
    fi
    if [ ! -b ${PARTITION11} ]; then
        PARTITION11=$DEV_DIR/${DRIVE_NAME}p11
    fi

    PARTITION12=${DRIVE}12
    if [ ! -b ${PARTITION12} ]; then
        PARTITION12=${DRIVE}p12
    fi
    if [ ! -b ${PARTITION12} ]; then
        PARTITION12=$DEV_DIR/${DRIVE_NAME}p12
    fi

    PARTITION13=${DRIVE}13
    if [ ! -b ${PARTITION13} ]; then
        PARTITION13=${DRIVE}p13
    fi
    if [ ! -b ${PARTITION13} ]; then
        PARTITION13=$DEV_DIR/${DRIVE_NAME}p13
    fi

    PARTITION14=${DRIVE}14
    if [ ! -b ${PARTITION14} ]; then
        PARTITION14=${DRIVE}p14
    fi
    if [ ! -b ${PARTITION14} ]; then
        PARTITION14=$DEV_DIR/${DRIVE_NAME}p14
    fi

    # FAT16
    if [ -b ${PARTITION1} ]; then
        echo "visteon" | sudo -S dd if=/dev/zero of=${PARTITION1} bs=4096 count=8192
        checkForErrors
    else
        echo "Cannot find ${PARTITION1} partition in /dev"
        status=1
    fi

     # FAT32
     if [ -b ${PARTITION5} ]; then
         echo "visteon" | sudo -S umount ${PARTITION5}
         echo "visteon" | sudo -S mkfs.vfat -s 128 -F 32 -n "int_opt" ${PARTITION5}
         checkForErrors
     else
         echo "Cannot find ${PARTITION5} partition in /dev"
         status=1
     fi

    # FAT32
     if [ -b ${PARTITION7} ]; then
         echo "visteon" | sudo -S umount ${PARTITION7}
         echo "visteon" | sudo -S mkfs.vfat -s 128 -F 32 -n "int_var" ${PARTITION7}
         checkForErrors
     else
         echo "Cannot find ${PARTITION7} partition in /dev"
         status=1
     fi

     # FAT32
     if [ -b ${PARTITION8} ]; then
         echo "visteon" | sudo -S umount ${PARTITION8}
         echo "visteon" | sudo -S mkfs.vfat -s 128 -F 32 -n "int_log" ${PARTITION8}
         checkForErrors
     else
         echo "Cannot find ${PARTITION8} partition in /dev"
         status=1
     fi

     # Secure storage - Erase
     if [ -b ${PARTITION9} ]; then
         echo "visteon" | sudo -S dd if=/dev/zero of=${PARTITION9} bs=4096 count=16384
         checkForErrors
     else
         echo "Cannot find ${PARTITION9} partition in /dev"
         status=1
     fi

     # FAT32
     if [ -b ${PARTITION10} ]; then
         echo "visteon" | sudo -S umount ${PARTITION10}
         echo "visteon" | sudo -S mkfs.vfat -s 128 -F 32 -n "int_cores" ${PARTITION10}
         checkForErrors
     else
         echo "Cannot find ${PARTITION10} partition in /dev"
         status=1
     fi

     # FAT32
     if [ -b ${PARTITION11} ]; then
         echo "visteon" | sudo -S umount ${PARTITION11}
         echo "visteon" | sudo -S mkfs.vfat -s 128 -F 32 -n "int_upd" ${PARTITION11}
         checkForErrors
     else
         echo "Cannot find ${PARTITION11} partition in /dev"
         status=1
     fi

     # FAT16 
     if [ -b ${PARTITION13} ]; then
         echo "visteon" | sudo -S umount ${PARTITION13}
         echo "visteon" | sudo -S mkfs.vfat -s 128 -F 32 -n "int_opt_2" ${PARTITION13}
         checkForErrors
     else
         echo "Cannot find ${PARTITION13} partition in /dev"
         status=1
     fi

     # RAW - fill with zeros
     if [ -b ${PARTITION14} ]; then
         echo "visteon" | sudo -S dd if=/dev/zero of=${PARTITION14} bs=4096 count=2048
         checkForErrors
     else
         echo "Cannot find ${PARTITION14} partition in /dev"
         status=1
     fi

    return $status
}

mountPartitions()
{
    local status=0

    sleep 3 # just in case, influence of automount on some VMs

    echo "visteon" | sudo -S umount ${PARTITION5}
    echo "visteon" | sudo -S umount ${PARTITION7}
    echo "visteon" | sudo -S umount ${PARTITION8}
    echo "visteon" | sudo -S umount ${PARTITION10}
    echo "visteon" | sudo -S umount ${PARTITION11}
    echo "visteon" | sudo -S umount ${PARTITION13}

    echo "visteon" | sudo -S rm -Rf $visteon/int_opt
    echo "visteon" | sudo -S rm -Rf $visteon/int_var
    echo "visteon" | sudo -S rm -Rf $visteon/int_log
    echo "visteon" | sudo -S rm -Rf $visteon/int_cores
    echo "visteon" | sudo -S rm -Rf $visteon/int_upd
    echo "visteon" | sudo -S rm -Rf $visteon/int_opt2

    sync
    sleep 2

    echo "visteon" | sudo -S mkdir $visteon/int_opt
    echo "visteon" | sudo -S mkdir $visteon/int_var
    echo "visteon" | sudo -S mkdir $visteon/int_log
    echo "visteon" | sudo -S mkdir $visteon/int_cores
    echo "visteon" | sudo -S mkdir $visteon/int_upd
    echo "visteon" | sudo -S mkdir $visteon/int_opt2

    sleep 2

    #####################################

    echo "visteon" | sudo -S mount -t vfat -o quiet ${PARTITION5} $visteon/int_opt
    if [ $? -ne 0 ]; then
        echo "Mount ${PARTITION5} error - exiting"
        status=1
    fi
    echo "visteon" | sudo -S mount -t vfat -o quiet ${PARTITION7} $visteon/int_var
    if [ $? -ne 0 ]; then
        echo "Mount ${PARTITION7} error - exiting"
        status=1
    fi
    echo "visteon" | sudo -S mount -t vfat -o quiet ${PARTITION8} $visteon/int_log
    if [ $? -ne 0 ]; then
        echo "Mount ${PARTITION8} error - exiting"
        status=1
    fi
    echo "visteon" | sudo -S mount -t vfat -o quiet ${PARTITION10} $visteon/int_cores
    if [ $? -ne 0 ]; then
        echo "Mount ${PARTITION10} error - exiting"
        status=1
    fi
    echo "visteon" | sudo -S mount -t vfat -o quiet ${PARTITION11} $visteon/int_upd
    if [ $? -ne 0 ]; then
        echo "Mount ${PARTITION11} error - exiting"
        status=1
    fi
    echo "visteon" | sudo -S mount -t vfat -o quiet ${PARTITION13} $visteon/int_opt2
    if [ $? -ne 0 ]; then
        echo "Mount ${PARTITION13} error - exiting"
        status=1
    fi

    #check if mount is fine before carrying on
    if [ $status -ne 0 ]; then
        #cleanup and exit
        sleep 1
        echo "visteon" | sudo -S umount ${PARTITION1}
        echo "visteon" | sudo -S umount ${PARTITION5}
        echo "visteon" | sudo -S umount ${PARTITION7}
        echo "visteon" | sudo -S umount ${PARTITION8}
        echo "visteon" | sudo -S umount ${PARTITION10}
        echo "visteon" | sudo -S umount ${PARTITION11}
        echo "visteon" | sudo -S umount ${PARTITION13}

        echo "visteon" | sudo -S rm -Rf $visteon/int_opt
        echo "visteon" | sudo -S rm -Rf $visteon/int_var
        echo "visteon" | sudo -S rm -Rf $visteon/int_log
        echo "visteon" | sudo -S rm -Rf $visteon/int_cores
        echo "visteon" | sudo -S rm -Rf $visteon/int_upd
        echo "visteon" | sudo -S rm -Rf $visteon/int_opt2
    fi

    return $status
}


if [ ! -d ${parentdir}/IntegrityImages ]; 
then
    mkdir -p ${parentdir}/IntegrityImages
else
    echo "${parentdir}/IntegrityImages exists"
fi

cd ${parentdir}/IntegrityImages

    # Find available device
    export DEVICE=`echo 'visteon' | sudo -S losetup -f`

    if [[ -d "${parentdir}/artifacts" ]]; then
        rm -fr ${parentdir}/artifacts/*_Images.7z || true
    else
        mkdir -p ${parentdir}/artifacts
    fi

    if [[ -f "${parentdir}/IntegrityImages/${NANDNAME}" ]]; then
        echo "visteon" | sudo -S rm -f ${parentdir}/IntegrityImages/${NANDNAME}
    fi

     echo "|====================================================================================|"
     echo "|               [CreateReflashImagesIntegrity]:Create a blank image                  |"
     echo "|====================================================================================|"

     dd if=/dev/zero of=${NANDNAME} iflag=fullblock bs=1M count=8192 && sync 

     echo "|====================================================================================|"
     echo "|      Mount the image on the first available loop device on ${DEVICE}:              |"
     echo "|====================================================================================|"

     echo "visteon" | sudo -S losetup $DEVICE ${NANDNAME}

     echo "|====================================================================================|"
     echo "|                     Format the image using fdisk program                           |"
     echo "|====================================================================================|"

     makePartitions; 
     checkForErrors;

     echo "|====================================================================================|"
     echo "|                     Detach the loop Device : ${DEVICE}                             |"
     echo "|====================================================================================|"

     echo "visteon" | sudo -S losetup -d ${DEVICE} 

     echo "|====================================================================================|"
     echo "|  Mount again the image on loop device ${DEVICE} with offset 1048576                |"
     echo "|====================================================================================|"

     echo "visteon" | sudo -S losetup -f ${NANDNAME} #-o 1048576 

     echo "|====================================================================================|"
     echo "|                      Create vfat file system on image:                             |"
     echo "|====================================================================================|"

     echo "visteon" | sudo -S partx -v --add $DEVICE
     makeFilesystems;
     checkForErrors;

     echo "|====================================================================================|"
     echo "|     Mount partition (with offset) and write files to it: ${PARTITION5}             |"
     echo "|====================================================================================|"

     mountPartitions; 
     checkForErrors;

     echo "|=========================================================================================|"
     echo "|  Write files to the image ${parentdir}/resources/dependencies/sdcard/ to ${PARTITION5}  |"
     echo "|=========================================================================================|"


     echo "visteon" | sudo -S cp -Rdpv ${parentdir}/resources/dependencies/sdcard/* $visteon/int_opt && sync


     echo "|====================================================================================|"
     echo "|     Finally, unmount the image from the loop device : ${DEVICE}                    |"
     echo "|====================================================================================|"

     
     echo "visteon" | sudo -S umount $visteon/int_opt
     echo "visteon" | sudo -S umount $visteon/int_var
     echo "visteon" | sudo -S umount $visteon/int_log
     echo "visteon" | sudo -S umount $visteon/int_cores
     echo "visteon" | sudo -S umount $visteon/int_upd
     echo "visteon" | sudo -S umount $visteon/int_opt2
    
     echo "visteon" | sudo -S partx -d ${DEVICE}
     echo "visteon" | sudo -S losetup -d ${DEVICE} 

     echo "visteon" | sudo -S rm -fr $visteon
     echo "visteon" | sudo -S mv ${parentdir}/IntegrityImages/${NANDNAME} ${parentdir}/resources/dependencies/drive-t186ref-integrity/out
     checkForErrors;
     
     echo "|====================================================================================|"
     echo "|                             ${NANDNAME} was created                                |"
     echo "|====================================================================================|"

sync


if [[ -d resourcesIntegrity ]]; then
    rm -fr resourcesIntegrity
fi

ln -s ${parentdir}/resources ${parentdir}/resourcesIntegrity

mkdir -p ${parentdir}/resources/dependencies/drive-t186ref-integrity/out

echo "Archiving the artifacts.. "
/usr/bin/time -v sudo -S 7zr a -l -r ${parentdir}/artifacts/${BUILD_NAME}_Images.7z ${parentdir}/resourcesIntegrity -m0=lzma2:d=1m:mt=12 -mx=0  -ms=100f512m -xr\@$SCRIPT_ROOT/scripts/symlinks-excludes-integrity.txt -x!*.dba -x!*.map -x!*.dla -y -x!*.a -x!*.h -x!*.cpp -x!*.hpp -x!*.o \
      -x!*.siz -x!*.Template -x!*.user -x!*.vcxproj -x!*.vsd -x!*.xlsx -x!*.sbs -x!*.ipp -x!*.kzproj  -x!*.sln  -x!*.psd -x!*.dnm -x!*.elf -x!*.dep -x!*.ael -x!*/inc/* -x!*/Images/* -x!*.template  -x!*.glsl -x!*.cc

unlink resourcesIntegrity

sync
