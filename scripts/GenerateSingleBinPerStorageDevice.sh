#!/bin/bash

###############################################################################
#
# Copyright (c) 2018 NVIDIA Corporation.  All rights reserved.
#
# NVIDIA Corporation and its licensors retain all intellectual property
# and proprietary rights in and to this software, related documentation
# and any modifications thereto.  Any use, reproduction, disclosure or
# distribution of this software and related documentation without an express
# license agreement from NVIDIA Corporation is strictly prohibited.
#
###############################################################################
#
# Factory flashing script(GenSingleBinaryPerStorageDevice.sh).
#
# This script generates one single binary for each storage device. It concatenates all the
# partition binaries on that storage device into a single binary based on sequence given in
# FileToFlash.txt.
#
# Usage: ./GenSingleBinaryPerStorageDevice.sh <input-binaries-location> <output-binaries-location>
#
# Input: It reads FileToFlash.txt file created during generation of binaries.
#        It parses the FileToFile.txt and appends the binaries in same order
#        as given in FileToFlash.txt.
#        Argument1: Location where FileToFlash.txt and input binaries are present.
#        Argument2: Output location, where output binaries are stored. In absence
#                   of this argument home directory is chosen as output directory.
#
# Output: Generates a binary for each storage device. Output binary name is
#         derived from storage device controller name given in FileToFlash.txt.
#
# Assumptions: Script assumes that FileToFlash.txt and input binaries are all
#         present at the location passed. It does not explicitly checks for presence
#         of those files.
#         It also assumes that start offset of all partitions on a storage device is in
#         ascending order.
#         It also assumes that user's system already have umount, losetup, e2fsck
#         and resize2fs utilities. If not present, install them.
#
###############################################################################

# Declare an array to save FileToFlash.txt.
declare -a FileToFlash

# Declare an array to store all storage devices controller names.
declare -a StorageControllers

# Declare an array to store output binary names.
declare -a OutputBinaryNames

declare -a CurrentOffset

NumPartitions=0
NumStorageController=0
InputBinariesPath=$1
OutputBinariesPath=$2

#
# Read the FileToFlash.txt and save in a global array.
#
function ReadFileToFlash {
	local FileName=$InputBinariesPath/FileToFlash.txt
	local Line
	local i=0

	#mv $FileName ${FileName}.orig && grep "^[^[:blank:]]* [^B_]" ${FileName}.orig > $FileName

	while IFS='' read -r Line
	do
		FileToFlash[$i]=$Line
		i=$((i+1))
	done < $FileName

	NumPartitions=$i
}

#
# Searches whether a storage controller is already present in StorageControllers array.
# Argument1: Storage device name to be searched.
#
function ContainsStorageControllerString {
	local String1=$1
	local i
	local c=0

	for i in ${StorageControllers[*]}
	do
		if [ $i = $String1 ]
		then
			return $c
		fi
		c=$((c+1))
	done

	return 255
}

#
# Calculates the total number of storage device controllers and save them in an array.
#
function CountStorageControllers {
	local c=0
	local i=0
	local String

	for ((c=1; c<$NumPartitions; c++))
	do
		String=( ${FileToFlash[$c]} )
		ContainsStorageControllerString ${String[0]}
		if [ $? -eq 255 ]
		then
			StorageControllers[$i]=${String[0]}
			i=$((i+1))
		fi
	done

	NumStorageController=$i
}

#
# Creates the output binary name string for each device controller
# depending upon device controller name and saves them in an array.
#
function SetOutputBinaryName {
	local c

	for ((c=0; c<$NumStorageController; c++))
	do
		OutputBinaryNames[$c]=`echo $((c+1))${StorageControllers[$c]} | tr '/' '-' | tr '\.' '-'`
		OutputBinaryNames[$c]=${OutputBinaryNames[$c]}.bin
		CurrentOffset[$c]=0
	done		
}	

function GetAvailableLoopDevice {
    export DEVICE=`echo 'visteon' | sudo -S losetup -f`
}

#
# Creates the output binary for each storage device controllera and saves them in already
# specified location.
#
function CreateOutputBinaries {
	local c
	local String
	local Index
	local Start
	local OutputBinary
	local InputBinary
	local PartitionSize
	local Diff=0
	local Resize
	local LoopDevice

	for ((c=0; c<NumStorageController; c++))
	do
		rm -rf $OutputBinariesPath/${OutputBinaryNames[$c]}
	done

	for ((c=1; c<NumPartitions; c++))
	do
		String=( ${FileToFlash[$c]} )
        
        if [[ ${String[1]} = *"B_"* ]]; then
            echo "Skipping partition ${String[1]} "
        	continue
        fi

		echo "Processing partition ${String[1]}."

		ContainsStorageControllerString ${String[0]}
		Index=$?
		if [ $Index -eq 255 ]
		then
			echo "Error: Not able to find the storage device controller."
			exit
		fi

		Start=${String[3]}
		PartitionSize=${String[4]}
		InputBinary=${String[2]}
		OutputBinary=${OutputBinaryNames[$Index]}
		Resize=${String[6]}

		rm -rf /tmp/binary1.bin
		if [ $Start -ne ${CurrentOffset[$Index]} ]
		then
			Diff=$((Start-CurrentOffset[$Index]))
			truncate -s $Diff /tmp/binary1.bin	
			cat /tmp/binary1.bin >> $OutputBinariesPath/$OutputBinary
		fi

		rm -rf /tmp/binary2.bin
		cp $InputBinariesPath/$InputBinary /tmp/binary2.bin
		truncate -s $PartitionSize /tmp/binary2.bin

		if [ $Resize -eq 1 ]
		then
			LoopDevice=${DEVICE}
			sudo umount ${LoopDevice}
			sudo losetup -d ${LoopDevice}
			sudo losetup ${LoopDevice} /tmp/binary2.bin
			sudo e2fsck -yfFt ${LoopDevice}
			sudo resize2fs -fFp $LoopDevice && sync
			sudo losetup -d ${LoopDevice}
		fi

		cat /tmp/binary2.bin >> $OutputBinariesPath/$OutputBinary

		CurrentOffset[$Index]=$((CurrentOffset[$Index]+PartitionSize+Diff))
		Diff=0
	done

	rm -rf /tmp/binary2.bin
	rm -rf /tmp/binary1.bin
}

# Start executing.
if [ $# -eq 0 ]
then
	echo "Error: Please provide input binaries location."
	echo "It is assumed that FileToFlash.txt and input binaries are present at same location."
	echo
	echo "Usage:"
	echo "./$0 <input-binaries-location> <output-binaries-location>"
	exit
fi

if [ $# -eq 1 ]
then
	echo "Info: Output location for storing out binaries is not provided."
	echo "Info: Output binaries will be stored in home directory."
	OutputBinariesPath=~
fi

ReadFileToFlash
CountStorageControllers
SetOutputBinaryName
GetAvailableLoopDevice
CreateOutputBinaries
echo "Completed."
