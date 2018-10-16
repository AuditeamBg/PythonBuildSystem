#!/bin/sh

echo "............. Perform Build ............."

if [ -z $WORKSPACE ]; then
    export WORKSPACE=$(dirname $(dirname "$PWD"))
fi

if [ -z $AdditionalFolderName ]; then
    export AdditionalFolderName=$(basename $(dirname "$PWD"))
fi

if [ -z $SCRIPT_ROOT ]; then
    export SCRIPT_ROOT=$(dirname "$PWD")/$(basename "$PWD")
fi

if [ -z $Variant ]; then
    export Variant="TegraP1Integrity.Rel.B0hw.C5.MRA2"
fi

if [[ -z $NODE_LABELS ]]; then
    export NODE_LABELS="MRA2Linux"
fi

if [ -z $Machine ]; then
    export Machine="MRA2Machine"
fi

if [ -z $BUILD_ID ]; then
    export BUILD_ID="5.0.0"
fi

if [ -z $SDKType ]; then
    export SDKType="TegraP1Integrity"
fi

yearnumber=`date +%y`
if [[ `date +"%u"` -gt 2 ]]; 
then
	weeknumber=`date -d "next week" +%V`
else
	weeknumber=`date +%V`
fi

if [ -z $VERSION_PATCH_LEVEL ]; then
    export VERSION_PATCH_LEVEL="$yearnumber.$weeknumber.00"
fi

if [ -z ${BS_WORKSPACE} ]; then
    export BS_WORKSPACE="${WORKSPACE}/${AdditionalFolderName}"
fi

if [ -z $BUILD_NAME ]; then
    export BUILD_NAME="LocalBuild-$yearnumber"
fi

if [ ! -z ${Variant} ]; then
    if [ "*C5*" == ${Variant} ]; then
        export JOB_VARIANT="C5"
    elif [ "*IC-H*" == ${Variant} ]; then
        export JOB_VARIANT="IC-H"
    elif [ "*IC-E*" == ${Variant} ]; then
        export JOB_VARIANT="IC-E"
    else
        #default
        export JOB_VARIANT="C5"
    fi
fi

if [ -z $JOB_NAME ]; then
    export JOB_NAME="DAG_MRA2_MY20_BUILD/${JOB_VARIANT}_Build"
fi

python ${WORKSPACE}/$AdditionalFolderName/CI.BuildSystem/bspos_exec.py "initialiazation" && sync;
if [ $? -ne 0 ]; then
	echo "Something went wrong after bspos_exec.py initialiazation!!!"
	exit 1
fi


if [ ! -d ${WORKSPACE}/${AdditionalFolderName}/artifacts ]; then
    mkdir -p ${WORKSPACE}/${AdditionalFolderName}/artifacts
fi

if [ -d ${WORKSPACE}/${AdditionalFolderName} ]; then
    cd ${WORKSPACE}/${AdditionalFolderName}
fi

if [ "$2" = "BSP" ]; then
    ${WORKSPACE}/${AdditionalFolderName}/CI.BuildSystem/scripts/PrebuildBSPMRA.sh
    sync;
fi


if [ "$1" = "product" ]; then
   
    if [ -d $WORKSPACE/$AdditionalFolderName/Linux_resources/ ]; then
        7zr x $WORKSPACE/$AdditionalFolderName/Linux_resources/*/artifacts/*Linux*_Images.7z -aoa -o$WORKSPACE/$AdditionalFolderName
        if [ $? -ne 0 ]; then
			echo "Something went wrong with extracting Linux image!!!"
			exit 1
		fi
    fi
    
    if [ -d $WORKSPACE/$AdditionalFolderName/Integrity_resources/ ]; then
        7zr x $WORKSPACE/$AdditionalFolderName/Integrity_resources/*/artifacts/*Integrity*_Images.7z -aoa -o$WORKSPACE/$AdditionalFolderName
        if [ $? -ne 0 ]; then
			echo "Something went wrong with extracting Integrity Image!!!"
			exit 1
		fi
    fi
    
    if [ -d $WORKSPACE/$AdditionalFolderName/ReflashLinux_resources/ ]; then
        7zr x $WORKSPACE/$AdditionalFolderName/ReflashLinux_resources/*/artifacts/*Linux*_Images.7z -aoa -o$WORKSPACE/$AdditionalFolderName
        if [ $? -ne 0 ]; then
			echo "Something went wrong with extracting Reflash Linux archive!!!"
			exit 1
		fi
    fi
    
    if [ ! -d $WORKSPACE/$AdditionalFolderName/artifacts ]; then
        mkdir -p $WORKSPACE/$AdditionalFolderName/artifacts
    fi
    
    if [ -d $WORKSPACE/$AdditionalFolderName/VIP_resources/DI-Cluster-IntEng/ ]; then
        mv $WORKSPACE/$AdditionalFolderName/VIP_resources/DI-Cluster-IntEng/*FULL* $WORKSPACE/$AdditionalFolderName/artifacts/
    else
    	echo "VIP FULL archive is missing!!!"
    	exit 1
    fi
    
    if [ -f $WORKSPACE/$AdditionalFolderName/ReflashImages/native-ramdisk.updated.cpio ]; then
        mv $WORKSPACE/$AdditionalFolderName/ReflashImages/native-ramdisk.updated.cpio $WORKSPACE/$AdditionalFolderName/Tools/drive-t186ref-foundation/native-linux-os/native-ramdisk.cpio
    else
    	echo "Reflash Linux is missing!!!"
    	exit 1
    fi
    
    if [ ! -d $WORKSPACE/$AdditionalFolderName/resources/dependencies/Vip/RH850/MRA2/RH850AutosarOS.Dbg/bin ]; then
        mkdir -p $WORKSPACE/$AdditionalFolderName/resources/dependencies/Vip/RH850/MRA2/RH850AutosarOS.Dbg/bin
    fi
    
    if [ -f $WORKSPACE/$AdditionalFolderName/VIP_resources/DI-Cluster-IntEng/*BIN* ]; then
        7zr x $WORKSPACE/$AdditionalFolderName/VIP_resources/DI-Cluster-IntEng/*BIN* -aoa -o$WORKSPACE/$AdditionalFolderName/resources/dependencies/Vip/RH850/MRA2/RH850AutosarOS.Dbg/bin/
        if [ $? -ne 0 ]; then
			echo "Something went wrong with extracting of VIP ARCHIVE!!!"
			exit 1
		fi
	else
		echo "VIP BIN archive is missing!!!"
		exit 1
    fi
    
    if [ ! -d $WORKSPACE/$AdditionalFolderName/Tools/drive-t186ref-linux/RootfsLinux/targetfs/ ]; then
        mkdir -p $WORKSPACE/$AdditionalFolderName/Tools/drive-t186ref-linux/RootfsLinux/targetfs/
    fi
    
    if [ -f $WORKSPACE/$AdditionalFolderName/Tools/drive-t186ref-linux/RootfsLinux/bin/tegra-genivi-12-image-tegra-t18x.tar.gz ]; then
        tar -xpf $WORKSPACE/$AdditionalFolderName/Tools/drive-t186ref-linux/RootfsLinux/bin/tegra-genivi-12-image-tegra-t18x.tar.gz -C $WORKSPACE/$AdditionalFolderName/Tools/drive-t186ref-linux/RootfsLinux/targetfs/
        if [ $? -ne 0 ]; then
			echo "Something went wrong with extracting of tegra-genivi-12-image-tegra-t18x.tar.gz!!!"
			exit 1
		fi
	else
		if [ $Variant = *"C5"* ]; then
			echo "Archive tegra-genivi-12-image-tegra-t18x.tar.gz is probably changed!!!"
			exit 1
		fi
    fi
    
    if [ -f $WORKSPACE/$AdditionalFolderName/Tools/drive-t186ref-linux/RootfsLinux/carbon_ui-release_v*-aarch64-visteon-HMI_SW_COMMON.001 ]; then
        7zr x $WORKSPACE/$AdditionalFolderName/Tools/drive-t186ref-linux/RootfsLinux/carbon_ui-release_v*-aarch64-visteon-HMI_SW_COMMON.001 -aoa -o$WORKSPACE/$AdditionalFolderName/Tools/drive-t186ref-linux/RootfsLinux/targetfs/
        if [ $? -ne 0 ]; then
			echo "Something went wrong with extracting IVI HMI carbon* archive!!!"
			exit 1
		fi
	else
		if [ $Variant = *"C5"* ]; then
			echo "IVI HMI HAS CHANGED NAME PATTERN!!!"
			exit 1
		fi
    fi

    if [ -f $WORKSPACE/$AdditionalFolderName/Tools/drive-t186ref-linux/RootfsLinux/targetfs/opt/hmi/ui/bin/sysui ]; then
        chmod +x $WORKSPACE/$AdditionalFolderName/Tools/drive-t186ref-linux/RootfsLinux/targetfs/opt/hmi/ui/bin/sysui
    fi

    if [ -d $WORKSPACE/$AdditionalFolderName/resources/dependencies/MRA2/BSP/BSP/ApplicationsIntegrity/MRA2H2/bin ]; then
        tar -xvf $WORKSPACE/$AdditionalFolderName/resources/dependencies/MRA2/BSP/BSP/ApplicationsIntegrity/MRA2H2/bin/*tar.gz
        if [ $? -ne 0 ]; then
			echo "Something went wrong with extracting!!!"
			exit 1
		fi
    fi

    if [ -d $WORKSPACE/$AdditionalFolderName/resources/dependencies/MRA2/BSP/KernelIntegrity/MRA2H2/bin ]; then
        tar -xvf $WORKSPACE/$AdditionalFolderName/resources/dependencies/MRA2/BSP/KernelIntegrity/MRA2H2/bin/*tar.gz
        if [ $? -ne 0 ]; then
			echo "Something went wrong with extracting!!!"
			exit 1
		fi
    fi

    python ${WORKSPACE}/$AdditionalFolderName/CI.BuildSystem/bspos_exec.py "true"
    if [ $? -ne 0 ]; then
		echo "Something went wrong  after bspos_exec.py true!!!"
		exit 1
	fi


elif [ "$1" = "monolith" ]; then
    echo "###### Build Monolith for Variant:$Variant ... ######"
    python ${WORKSPACE}/${AdditionalFolderName}/CI.BuildSystem/MRA2/perform_build.py "monolith"
    if [ $? -ne 0 ]; then
		echo "Something went wrong with extracting!!!"
		exit 1
    fi

elif [ "$1" = "export_workspace" ]; then
    echo "###### Exporting workspace in text file ... ######"
    python ${WORKSPACE}/${AdditionalFolderName}/CI.BuildSystem/scripts/export_workspace_path.py
    if [ $? -ne 0 ]; then
		echo "Something went wrong with extracting!!!"
		exit 1
    fi

elif [ "$1" = "archive_os_workspace" ]; then
    echo "###### Archiving os workspace... ######"
    python ${WORKSPACE}/${AdditionalFolderName}/CI.BuildSystem/scripts/archive_os_workspace.py
    if [ $? -ne 0 ]; then
		echo "Something went wrong with extracting!!!"
		exit 1
    fi

elif [ "$1" = "archive_workspace" ]; then
    echo "###### Archiving workspace... ######"
    python ${WORKSPACE}/${AdditionalFolderName}/CI.BuildSystem/scripts/archive_workspace.py
    if [ $? -ne 0 ]; then
		echo "Something went wrong with extracting!!!"
		exit 1
    fi

elif [ "$1" = "archive_additional_resources" ]; then
    echo "###### Archiving additional resources ... ######"
    python ${WORKSPACE}/${AdditionalFolderName}/CI.BuildSystem/scripts/archive_additional_resources.py
    if [ $? -ne 0 ]; then
		echo "Something went wrong with extracting!!!"
		exit 1
    fi

elif [ "$1" = "archive_bsp_workspace" ]; then
    echo "###### Archiving bsp workspace ... ######"
    python ${WORKSPACE}/${AdditionalFolderName}/CI.BuildSystem/scripts/archive_bsp_workspace.py
    if [ $? -ne 0 ]; then
		echo "Something went wrong with extracting!!!"
		exit 1
    fi

elif [ "$1" = "copy_workspace_files" ]; then
    echo "###### Copying workspace files from OS builds ... ######"
    python ${WORKSPACE}/${AdditionalFolderName}/CI.BuildSystem/scripts/copy_workspace_files.py
    if [ $? -ne 0 ]; then
		echo "Something went wrong with extracting!!!"
		exit 1
    fi

elif [ "$1" = "daily_archives" ]; then
    echo "###### Copying workspace files from OS builds ... ######"
    python ${WORKSPACE}/${AdditionalFolderName}/CI.BuildSystem/plugins/MRA2/DailyArchives.py
    if [ $? -ne 0 ]; then
		echo "Something went wrong with extracting!!!"
		exit 1
	fi

elif [ "$1" = "APIBuns" ]; then
    echo "####### APIBUNS BUILD .................. #######"
    ${WORKSPACE}/${AdditionalFolderName}/CI.BuildSystem/scripts/MRA2_APIBuns_build.sh
    if [ $? -ne 0 ]; then
	    echo "Something went wrong with the build!!!"
	    exit 1
	fi

elif [ "$1" = "ADSP" ]; then
    echo "####### ADSP BUILD .................. #######"
    ${WORKSPACE}/${AdditionalFolderName}/SourceSpace/scripts/buildNvfxAdsp.sh
    if [ $? -ne 0 ]; then
	    echo "Something went wrong with the build!!!"
	    exit 1
	fi

elif [ "$1" = "source_code_delivery" ]; then
    echo "####### SOURCE CODE DELIVERY ....... #######"  
    python ${WORKSPACE}/${AdditionalFolderName}/CI.BuildSystem/source_code/source_code_delivery.py $2 $3 $4
    if [ $? -ne 0 ]; then
	    echo "Something went wrong with the build!!!"
	    exit 1
	fi

else
    python $WORKSPACE/${AdditionalFolderName}/CI.BuildSystem/bspos_exec.py "$1"
    if [ $? -ne 0 ]; then
		echo "Something went wrong with the build!!!"
		exit 1
	fi
fi

