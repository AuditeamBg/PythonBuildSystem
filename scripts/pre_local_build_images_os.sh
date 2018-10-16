#!/bin/sh

Variant=''
filename="environment_vars_for_os.txt"

cd $SCRIPT_ROOT/scripts

while read -r line

do
    IN="$line"
    source ./$filename
    export $(cut -d= -f1 ./$filename)
done < "./$filename"

export WORKSPACE=$(dirname $(dirname $(dirname "$PWD")))
export BUILD_NUMBER=$(basename $(dirname $(dirname "$PWD")))
export SCRIPT_ROOT="$WORKSPACE/$BUILD_NUMBER/CI.BuildSystem"
export PLUGINS_MRA2_ROOT="$SCRIPT_ROOT/plugins/MRA2/"
export AdditionalFolderName=$BUILD_NUMBER
export LOCAL_IMAGE_CREATE=True

pushd `dirname $0` > /dev/null
SCRIPTPATH=`pwd`
popd > /dev/null

if [ -z $Variant ]; then
	if [ -d ${SCRIPTPATH}/../../SourceSpace/MRA2/IVINode ]; then
		echo "Variant=TegraP1Integrity.Rel.B0hw.C5.MRA2" > ${SCRIPTPATH}/${filename}
		if [ -d ${SCRIPTPATH}/../../SourceSpace/Tuner ]; then
			echo "Variant=TegraP1Lin.Rel.B0hw.C5.MRA2" > ${SCRIPTPATH}/${filename}
		fi
	else
		echo "Variant=TegraP1Integrity.Rel.B0hw.IC_E.MRA2" > ${SCRIPTPATH}/${filename}
		if [ -d ${SCRIPTPATH}/../../SourceSpace/AR ]; then
			echo "Variant=TegraP1Integrity.Rel.B0hw.IC_H.MRA2" > ${SCRIPTPATH}/${filename}
		fi
	fi
else
	if [ $1 == "1" ]; then
		echo "Variant=TegraP1Integrity.Rel.B0hw.C5.MRA2"
		Variant=TegraP1Integrity.Rel.B0hw.C5.MRA2
		echo "Variant=TegraP1Integrity.Rel.B0hw.C5.MRA2" > ${SCRIPTPATH}/${filename}
	elif [ $1 == "2" ]; then
		echo "Variant=TegraP1Integrity.Rel.B0hw.IC_E.MRA2"
		Variant=TegraP1Integrity.Rel.B0hw.IC_E.MRA2
		echo "Variant=TegraP1Integrity.Rel.B0hw.IC_E.MRA2" > ${SCRIPTPATH}/${filename}
	elif [ $1 == "3" ]; then
		echo "Variant=TegraP1Integrity.Rel.B0hw.IC_H.MRA2"
		Variant=TegraP1Integrity.Rel.B0hw.IC_H.MRA2
		echo "Variant=TegraP1Integrity.Rel.B0hw.IC_H.MRA2" > ${SCRIPTPATH}/${filename}
	elif [ $1 == "4" ]; then
		echo "Variant=TegraP1Integrity.Rel.B0hw.C5.MRA2"
		Variant=TegraP1Lin.Rel.B0hw.C5.MRA2
		echo "Variant=TegraP1Integrity.Rel.B0hw.C5.MRA2" > ${SCRIPTPATH}/${filename}
	else
		echo "Illegal variant choice!"
		echo "Add parameter:"
		echo "\"1\" for Variant=TegraP1Integrity.Rel.B0hw.C5.MRA2"
		echo "\"2\" for Variant=TegraP1Integrity.Rel.B0hw.IC_E.MRA2"
		echo "\"3\" for Variant=TegraP1Integrity.Rel.B0hw.IC_H.MRA2"
		echo "\"4\" for Variant=TegraP1Lin.Rel.B0hw.C5.MRA2"
	fi
fi
echo "Variant is $Variant"

DATE=`date +%Y%m%d`
BOARD=''
case $Variant in
	TegraP1Integrity.Rel.B0hw.C5.MRA2|TegraP1Lin.Rel.B0hw.C5.MRA2)  BOARD="C5";;
	TegraP1Integrity.Rel.B0hw.IC_H.MRA2) BOARD="IC-H";;
	TegraP1Integrity.Rel.B0hw.IC_E.MRA2) BOARD="IC-E";;
	*) echo "please add board type(C5,IC-H,IC-E) to variant variable";;
esac

OSType=''
case $Variant in
	TegraP1Lin.Rel.B0hw.C5.MRA2)
		OSType="Linux"
		echo "IS_DAILY_Integrity_BUILD=False" >> ${SCRIPTPATH}/${filename}
		echo "IS_DAILY_Linux_BUILD=True" >> ${SCRIPTPATH}/${filename}
	;;
	TegraP1Integrity.Rel.B0hw.C5.MRA2|TegraP1Integrity.Rel.B0hw.IC_H.MRA2|TegraP1Integrity.Rel.B0hw.IC_E.MRA2)
		OSType="Integrity"
		echo "IS_DAILY_Integrity_BUILD=True" >> ${SCRIPTPATH}/${filename}
	    echo "IS_DAILY_Linux_BUILD=False" >> ${SCRIPTPATH}/${filename}
	;;
	*) echo "Invalid OS type(Lin, integrity) to variant variable"
esac	


python pre_local_build_images_os.py