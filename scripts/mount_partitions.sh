#!/bin/sh

if [ -z "$1" ]; then
echo image not specified
exit 1
fi

if [ -z "$2" ]; then
echo mount directory not specified
exit 1
fi

DIR="$2"

if [ ! -d "$DIR" ]; then
mkdir -p "$DIR"
fi

IMAGE="$1"

PTAB=`mktemp -p .`
TMP=`mktemp -p .`
fdisk -u -l "$IMAGE" > $PTAB
awk -v image="$IMAGE" -v mnt="$DIR" 'BEGIN{sector_size=512}/Sector size/{sector_size=$7}$6$7 ~ /FAT32/{system("echo mkdir -p "mnt"/"$1"\;mount -o loop,offset=\`expr " sector_size " \\\* "$2"\` "image" "mnt"/"$1)}' $PTAB > $TMP

awk -v mnt="$DIR" '$6$7 ~ /FAT32/{system("echo umount "mnt"/"$1)}END{system("echo rm -f -r "mnt)}' $PTAB > umount_partitions.sh

sh $TMP
sync

rm -f $TMP
rm -f $PTAB

