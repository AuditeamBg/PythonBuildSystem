#!/bin/sh
echo "#################### PrebuildBSPMRA.sh ########################"

Project_Variant_lores="none"
if [[ $Variant == *C5* ]]; then
    Project_Variant="c5"
    Board_Variant="TegraP1"
    export __VARIANT="VARIANT_C5"
elif [[ $Variant == *IC_H* ]]; then
    Project_Variant="ic-h-hires"
    Project_Variant_lores="ic-h-lores"
    Board_Variant="TegraP1"
    export __VARIANT="VARIANT_IC_H"
elif [[ $Variant == *IC_E* ]]; then
    Project_Variant="ic-e"
    Board_Variant="TegraP1"
    export __VARIANT="VARIANT_IC_E"
else
    Board_Variant="TegraP1"
fi


if [[ $Board_Variant == M2 ]]; then
    mosx_Variant=`echo _$Board_Variant | tr '[:upper:]' '[:lower:]'`
else
    mosx_Variant=""
fi
echo ${mosx_Variant}

HW_Var=($HW_Variant)
arraylength=${#HW_Var[@]}

build_Kernel_App_Lib()
{
    rm -rf ${WORKSPACE}/${AdditionalFolderName}/resources/dependencies/MRA2/BSP/ApplicationsIntegrity/MRA2H2/bin/*
    rm -rf ${WORKSPACE}/${AdditionalFolderName}/resources/dependencies/MRA2/BSP/KernelIntegrity/MRA2H2/bin/*
    #---- build and deploy Kernel in Normal mode ----
    python ${WORKSPACE}/${AdditionalFolderName}/Tools/IntegrityBSP/scripts/Build.Integrity.Normal.py ${WORKSPACE}/${AdditionalFolderName}/resources/dependencies/MRA2/BSP/KernelIntegrity/MRA2H2/bin/
    if [[ ! -e ${WORKSPACE}/${AdditionalFolderName}/resources/dependencies/MRA2/BSP/KernelIntegrity/MRA2H2/bin/integrity.tar.gz ]]; then
        echo "================== ERROR: Build and deploy Kernel in Normal mode is not as expected. Missing KernelIntegrity files =================="
        exit 1
    fi

    #---- build and deploy Applications ----
    python ${WORKSPACE}/${AdditionalFolderName}/Tools/IntegrityBSP/scripts/Build.IntegrityApps.py ${WORKSPACE}/${AdditionalFolderName}/resources/dependencies/MRA2/BSP/ApplicationsIntegrity/MRA2H2/bin/
    if [[ ! -e ${WORKSPACE}/${AdditionalFolderName}/resources/dependencies/MRA2/BSP/ApplicationsIntegrity/MRA2H2/bin/applications.tar.gz ]]; then
            echo "================== ERROR: Build and deploy Applications is not as expected. Missing applications.tar.gz files =================="
        exit 1
    fi

    #---- deploy Libraries ----
    cd ${WORKSPACE}/${AdditionalFolderName}/Tools/IntegrityBSP/scripts
    ./deploy.sh Mra2_${mosx_Variant} ${WORKSPACE}/${AdditionalFolderName}/DeliSpace/${Variant}/BSP/LibsIntegrity/
    if [[ ! -e ${WORKSPACE}/${AdditionalFolderName}/resources/dependencies/MRA2/BSP/KernelIntegrity/MRA2H2/bin/integrity.tar.gz ]]; then
        echo "================== ERROR: Build and deploy Kernel in Normal mode is not as expected. Missing KernelIntegrity files =================="
        exit 1
    else
        if [[ ! -d ${WORKSPACE}/${AdditionalFolderName}/resources/dependencies/MRA2/MRA2_monolith/bin ]]; then
            mkdir -p ${WORKSPACE}/${AdditionalFolderName}/resources/dependencies/MRA2/MRA2_monolith/bin
        fi
        tar -xvf ${WORKSPACE}/${AdditionalFolderName}/resources/dependencies/MRA2/BSP/KernelIntegrity/MRA2H2/bin/integrity.tar.gz -C ${WORKSPACE}/${AdditionalFolderName}/resources/dependencies/MRA2/MRA2_monolith/bin/
    fi
    cd -
}


if [[ ${JOB_NAME} == *BSP510* ]]; then
    if [ -d ${WORKSPACE}/${AdditionalFolderName}/DeliSpace/${Variant}/BSP ]; then
        echo 'visteon' | sudo -S rm -fr ${WORKSPACE}/${AdditionalFolderName}/DeliSpace/${Variant}/BSP
    fi
    if [ -d ${WORKSPACE}/${AdditionalFolderName}/Tools/IntegrityBSP ]; then
        echo "=============== BUILD: Kernel_application_lib for ${JOB_NAME} =============================="
        build_Kernel_App_Lib
    else
        echo "================== ERROR: Build and deploy Kernel in Normal mode is not as expected. Missing KernelIntegrity files =================="
        exit 1
    fi

else
    if [ -d ${WORKSPACE}/${AdditionalFolderName}/Tools/IntegrityBSP ]; then
        echo "=============== BUILD: Kernel_application_lib for ${Variant} =============================="
        build_Kernel_App_Lib
    else
        echo "================== ERROR: Build and deploy Kernel in Normal mode is not as expected. Missing KernelIntegrity files =================="
        exit 1
    fi
fi
