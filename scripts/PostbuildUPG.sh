#!/bin/sh
if [ ! -z $1 ]; then
    export Variant=$1
fi

if [ -d ${BS_WORKSPACE}/cards/ ]; then
    export BS_VERSION=$(ls -l ${BS_WORKSPACE}/cards/ | grep -o -e '[0-9]*\.[0-9]*\.[0-9]*' | head -1 ) 
fi

if [[ $Variant = *"B1hw.C5.MRA2"* ]]; then
    echo "===================================== HW variant B1hw.C5.MRA2 ============================================================="
    export pref="-b1"
    export post="-b1"
    export HW_PREFIX="B1"
    export VAR="C5"
    export _MIC="micc"
    export _linux="-linux"
    export _var="c5"
    export _SoC_Application="Cars_C5_SoC_IC_Application.odx-f"
    export PATH_TO_VIP_BootLoader="${BS_WORKSPACE}/cards/Mra2-VIP-${VAR}v${BS_VERSION}/VIP/bin/bootloader_b1"
    export VIP_FBL_Updater_Location="${PATH_TO_VIP_BootLoader}/MRA2Fbl-B1_Updater.srec"
    export VIP_SREC_BootLoader_Location="${PATH_TO_VIP_BootLoader}/MRA2Fbl-B1.srec"

elif [[ $Variant = *"B1hw.IC_H.MRA2"* ]]; then
    echo "================================ HW variant B1hw.IC_H.MRA2 ================================================================"
    export pref=""
    export post="-b1"
    export HW_PREFIX="B1"
    export VAR="IC-H"
    export _MIC="mich"
    export _linux=""
    export _var="ich"
    export _SoC_Application="Cars_IC-H_SoC_IC_Application.odx-f"
    export PATH_TO_VIP_BootLoader="${BS_WORKSPACE}/cards/Mra2-VIP-${VAR}v${BS_VERSION}/VIP/bin/bootloader"
    export VIP_FBL_Updater_Location="${PATH_TO_VIP_BootLoader}/MRA2Fbl_Updater.srec"
    export VIP_SREC_BootLoader_Location="${PATH_TO_VIP_BootLoader}/MRA2Fbl.srec"

elif [[ $Variant = *"C2hw.IC_H.MRA2"* ]]; then
    echo "================================ HW variant C2hw.IC_H.MRA2 ================================================================"
    export pref=""
    export post="-c2"
    export HW_PREFIX="C2"
    export VAR="IC-H"
    export _MIC="mich"
    export _linux=""
    export _var="ich"
    export _SoC_Application="Cars_IC-H_SoC_IC_Application.odx-f"
    export PATH_TO_VIP_BootLoader="${BS_WORKSPACE}/cards/Mra2-VIP-${VAR}v${BS_VERSION}/VIP/bin/bootloader"
    export VIP_FBL_Updater_Location="${PATH_TO_VIP_BootLoader}/MRA2Fbl_Updater.srec"
    export VIP_SREC_BootLoader_Location="${PATH_TO_VIP_BootLoader}/MRA2Fbl.srec"

elif [[ $Variant = *"B1hw.IC_E.MRA2-hud"* ]]; then
    echo "================================== HW variant B1hw.IC_E.MRA2-hud ============================================================="
    export pref=""
    export post="-b1-hud"
    export HW_PREFIX="B1"
    export VAR="IC-E"
    export _MIC="mice"
    export _linux=""
    export _var="ice"
    export _SoC_Application="Cars_IC-E_SoC_IC_Application.odx-f"
    export PATH_TO_VIP_BootLoader="${BS_WORKSPACE}/cards/Mra2-VIP-${VAR}v${BS_VERSION}/VIP/bin/bootloader"
    export VIP_FBL_Updater_Location="${PATH_TO_VIP_BootLoader}/MRA2Fbl_Updater.srec"
    export VIP_SREC_BootLoader_Location="${PATH_TO_VIP_BootLoader}/MRA2Fbl.srec"

elif [[ $Variant = *"C2hw.IC_E.MRA2-hud"* ]]; then
    echo "================================== HW variant C2hw.IC_E.MRA2-hud ==========================================================="
    export pref=""
    export post="-c2-hud"
    export HW_PREFIX="C2"
    export VAR="IC-E"
    export _MIC="mice"
    export _linux=""
    export _var="ice"
    export _SoC_Application="Cars_IC-E_SoC_IC_Application.odx-f"
    export PATH_TO_VIP_BootLoader="${BS_WORKSPACE}/cards/Mra2-VIP-${VAR}v${BS_VERSION}/VIP/bin/bootloader"
    export VIP_FBL_Updater_Location="${PATH_TO_VIP_BootLoader}/MRA2Fbl_Updater.srec"
    export VIP_SREC_BootLoader_Location="${PATH_TO_VIP_BootLoader}/MRA2Fbl.srec"

elif [[ $Variant = *"B1hw.IC_E.MRA2" ]]; then
    echo "======================================== HW variant B1hw.IC_E.MRA2 ========================================================"
    export pref=""
    export post="-b1"
    export HW_PREFIX="B1"
    export VAR="IC-E"
    export _MIC="mice"
    export _linux=""
    export _var="ice"
    export _SoC_Application="Cars_IC-E_SoC_IC_Application.odx-f"
    export PATH_TO_VIP_BootLoader="${BS_WORKSPACE}/cards/Mra2-VIP-${VAR}v${BS_VERSION}/VIP/bin/bootloader"
    export VIP_FBL_Updater_Location="${PATH_TO_VIP_BootLoader}/MRA2Fbl_Updater.srec"
    export VIP_SREC_BootLoader_Location="${PATH_TO_VIP_BootLoader}/MRA2Fbl.srec"

elif [[ $Variant = *"C2hw.IC_E.MRA2" ]]; then
    echo "========================================== HW variant C2hw.IC_E.MRA2 ======================================================="
    export pref=""
    export post="-c2"
    export HW_PREFIX="C2"
    export VAR="IC-E"
    export _MIC="mice"
    export _linux=""
    export _var="ice"
    export _SoC_Application="Cars_IC-E_SoC_IC_Application.odx-f"
    export PATH_TO_VIP_BootLoader="${BS_WORKSPACE}/cards/Mra2-VIP-${VAR}v${BS_VERSION}/VIP/bin/bootloader"
    export VIP_FBL_Updater_Location="${PATH_TO_VIP_BootLoader}/MRA2Fbl_Updater.srec"
    export VIP_SREC_BootLoader_Location="${PATH_TO_VIP_BootLoader}/MRA2Fbl.srec"

else
    echo "============================================== Unknown Hardware variant ======================================================"
    export pref="-b1"
    export post="-b1"
    export HW_PREFIX="B1"
    export VAR="C5"
    export _MIC="micc"
    export _linux="-linux"
    export _var="c5"
    export _SoC_Application="Cars_C5_SoC_IC_Application.odx-f"
    export PATH_TO_VIP_BootLoader="${BS_WORKSPACE}/cards/Mra2-VIP-${VAR}v${BS_VERSION}/VIP/bin/bootloader_b1"
    export VIP_FBL_Updater_Location="${PATH_TO_VIP_BootLoader}/MRA2Fbl-B1_Updater.srec"
    export VIP_SREC_BootLoader_Location="${PATH_TO_VIP_BootLoader}/MRA2Fbl-B1.srec"
fi

export BS_PN_PATCH_DOT=$VERSION_PATCH_LEVEL
export BS_ITERATION="E00${BS_VERSION:0:3}" 
export BS_DATE=`date +"%Y-%m-%dT%T"`
export BS_UP_OUT_PATH="${BS_WORKSPACE}/UPG_Output-${Variant}"
export BS_CARDS_PATH="${BS_WORKSPACE}/cards/"
export TemplatesLocation="${BS_WORKSPACE}/MRA2.Reflash.ConfigTemplates"
export ConfigLocation="${BS_WORKSPACE}/MRA2.Reflash.Config-${Variant}"
export BS_CARDS="${BS_WORKSPACE}/cards/Mra2-SOC-${VAR}v${BS_VERSION}/"
export DRIVE_FOUNDATION_PATH="${BS_WORKSPACE}/cards/Mra2-SOC-${VAR}v${BS_VERSION}/drive-t186ref-foundation/"
export INPUT_BINARIES_LOCATION="${DRIVE_FOUNDATION_PATH}tools/host/flashtools/bootburn/images-${_var}/699-62382-0010-100_BB/flash-images"
export OUTPUT_BINARIES_LOCATION="${DRIVE_FOUNDATION_PATH}tools/host/flashtools/bootburn/images-${_var}/"
export INPUT_NOR="${DRIVE_FOUNDATION_PATH}tools/host/flashtools/bootburn/NOR/699-62382-0010-100_BB/flash-images"
export OUTPUT_NOR="${DRIVE_FOUNDATION_PATH}tools/host/flashtools/bootburn/NOR/"
export GEN_TUT_IMAGE_PATH="${BS_WORKSPACE}/cards/Mra2-SOC-${VAR}v${BS_VERSION}/drive-t186ref-foundation/tools/host/flashtools/bootburn"
export PATH_TO_VIP_APP="${BS_WORKSPACE}/cards/Mra2-VIP-${VAR}v${BS_VERSION}/VIP/bin/rel-mra2_${_var:0:2}$pref-default"
export ConfigPath="${ConfigLocation}/Cars_${VAR}-$HW_PREFIX"
export VIP_SREC_FILES="${PATH_TO_VIP_APP}/rel-mra2_${_var:0:2}$pref-default_app_only.srec"

/usr/bin/python ${SCRIPT_ROOT}/scripts/parseVIP.py

if [[ ! -d ${ConfigLocation} ]]; then
    mkdir -p ${ConfigLocation}
    cp -rp ${TemplatesLocation}/* ${ConfigLocation}/
fi

if [[ ! -d ${ConfigPath} ]]; then
    mv "${ConfigLocation}/Cars_${VAR}" "${ConfigLocation}/Cars_${VAR}-$HW_PREFIX"
fi

BS_PN_PATCH=$(echo "$BS_PN_PATCH_DOT" | sed 's/\.//g')
BS_PN_PATCH_SLASH=$(echo "$BS_PN_PATCH_DOT" | tr '.' '/')

RES_OK=0
RES_ERR=0
declare -a textToSearch=("\${BS_VERSION}" "\${BS_PN_PATCH}" "\${BS_PN_PATCH_DOT}" "\${BS_PN_PATCH_SLASH}" "\${BS_UP_OUT_PATH}" "\${BS_CARDS_PATH}" "\${BS_WORKSPACE}" "\${BS_DATE}" "\${BS_ITERATION}" "\${BS_END_ADDRESS}" "\${BS_CHECKSUM}")
arraylength=${#textToSearch[@]}

cd ${DRIVE_FOUNDATION_PATH}
make -f Makefile.bind PCT=integrity${_linux} BOARD=${_MIC}$post clean
make -f Makefile.bind PCT=integrity${_linux} BOARD=${_MIC}$post

${GEN_TUT_IMAGE_PATH}/create_bsp_images.sh -g images-${_var} -r 02 -D -b ${_MIC}$post -H -z "--skunum 699-62382-0010-100 --setskuversion BB  --setboardserial 1234 --setmacid eth0 0x3CCE15000107 --setprodinfo 699-62382-0010-100 BB" 2>&1 | tee log.create_bsp_images-${_var}.txt
echo "visteon" | sudo -S ${SCRIPT_ROOT}/scripts/GenerateSingleBinPerStorageDevice.sh ${INPUT_BINARIES_LOCATION} ${OUTPUT_BINARIES_LOCATION}

if [[ $Variant = *"IC_E"* ]]; then
    echo "++++++++++++++++++++++++++++++++++++"
    echo "Generating second NOR image for ic-e"
    echo "++++++++++++++++++++++++++++++++++++"
    make -f Makefile.bind PCT=integrity BOARD=mice-c2 clean
    make -f Makefile.bind PCT=integrity BOARD=mice-c2
    ${GEN_TUT_IMAGE_PATH}/create_bsp_images.sh -g NOR -r 02 -D -b ${_MIC}-c2 -H -z "--skunum 699-62382-0010-100 --setskuversion BB  --setboardserial 1234 --setmacid eth0 0x3CCE15000107 --setprodinfo 699-62382-0010-100 BB" 2>&1 | tee log.create_bsp_images-${_var}.txt
    echo "visteon" | sudo -S ${SCRIPT_ROOT}/scripts/GenerateSingleBinPerStorageDevice.sh ${INPUT_NOR} ${OUTPUT_NOR}

elif [[ $Variant = *"IC_H"* ]]; then
	echo "++++++++++++++++++++++++++++++++++++"
	echo "Generating second NOR image for ic-h"
	echo "++++++++++++++++++++++++++++++++++++"
    make -f Makefile.bind PCT=integrity BOARD=mich-c2 clean
    make -f Makefile.bind PCT=integrity BOARD=mich-c2
    ${GEN_TUT_IMAGE_PATH}/create_bsp_images.sh -g NOR -r 02 -D -b ${_MIC}-c2 -H -z "--skunum 699-62382-0010-100 --setskuversion BB  --setboardserial 1234 --setmacid eth0 0x3CCE15000107 --setprodinfo 699-62382-0010-100 BB" 2>&1 | tee log.create_bsp_images-${_var}.txt
    #${GEN_TUT_IMAGE_PATH}/create_bsp_images.sh -l -r 02 -b ${_MIC}-c2 -k $(readlink -f ${GEN_TUT_IMAGE_PATH}/quickboot_qspi_linux_factoryflash.cfg ) -D -g NOR -H -z "--skunum 699-62382-0010-100 --setskuversion BB  --setboardserial 1234 --setmacid eth0 0x3CCE15000107 --setprodinfo 699-62382-0010-100 BB" 2>&1 | tee log.create_bsp_images-NOR_c2.txt
    echo "visteon" | sudo -S ${SCRIPT_ROOT}/scripts/GenerateSingleBinPerStorageDevice.sh ${INPUT_NOR} ${OUTPUT_NOR}

elif [[ $Variant = *"C5"* ]]; then
	echo "++++++++++++++++++++++++++++++++++++"
	echo "Generating second NOR image for c5"
	echo "++++++++++++++++++++++++++++++++++++"
    ${GEN_TUT_IMAGE_PATH}/create_bsp_images.sh -g NOR -r 02 -D -b ${_MIC}-c2 -H -z "--skunum 699-62382-0010-100 --setskuversion BB  --setboardserial 1234 --setmacid eth0 0x3CCE15000107 --setprodinfo 699-62382-0010-100 BB" 2>&1 | tee log.create_bsp_images-${_var}.txt
    echo "visteon" | sudo -S ${SCRIPT_ROOT}/scripts/GenerateSingleBinPerStorageDevice.sh ${INPUT_NOR} ${OUTPUT_NOR}
fi

echo "visteon" | sudo -S rename -v 's/mtd0/mtd0-c2/' ${OUTPUT_NOR}/$(basename *mtd*)
echo "visteon" | sudo -S rename -v 's/mtd0/mtd0-b1/' ${OUTPUT_BINARIES_LOCATION}/$(basename *mtd*)
echo "visteon" | sudo -S mv ${OUTPUT_NOR}/$(basename *mtd*) ${OUTPUT_BINARIES_LOCATION}/

#Build the UPG
make clean -C ${BS_WORKSPACE}/SourceSpace/Reflash/UPG/private/src
make all -C ${BS_WORKSPACE}/SourceSpace/Reflash/UPG/private/src

make -C ${BS_WORKSPACE}/SourceSpace/SWUpdate/Security/tools/Signature
    
replace_strings()
{
echo "Replacing the ENVIRONMENT_VARIABLES in:"$1
textToReplace=(${BS_VERSION} ${BS_PN_PATCH} ${BS_PN_PATCH_DOT} ${BS_PN_PATCH_SLASH} ${BS_UP_OUT_PATH} ${BS_CARDS_PATH} ${BS_WORKSPACE} ${BS_DATE} ${BS_ITERATION} ${BS_END_ADDRESS} ${BS_CHECKSUM})
   for (( idx=0; idx<${arraylength}; idx++ )); do
       echo "TEXT_TO_SEARCH : ${textToSearch[idx]}"
       echo "TEXT_TO_REPLACE : ${textToReplace[idx]}"
       sed -i 's%'${textToSearch[idx]}'%'${textToReplace[idx]}'%g' $1
   done
}

generate_up_file()
{
    echo "############## BUILD configuration IS : $1 ##############"
    replace_strings $1
    echo "visteon" | sudo -S ${BS_WORKSPACE}/SourceSpace/Reflash/UPG/private/src/linux/upg -c $1
    if [ $? -eq 0 ] ; then
        ((RES_OK++))
    else
        ((RES_ERR++))
    fi
}

prepare_SOC_odx_file()
{
   cd $2
   
   BINNumber=${1#*"$BS_UP_OUT_PATH/"}
   BINNumber=${BINNumber#*/}
   BINNumber=${BINNumber%\_*}
   
   export BINFolder=${1%"/$BINNumber"*} 
   if [ $BINFolder == "" ]; then
       BINFolder=$BS_UP_OUT_PATH/
   fi
   
   ODXFile=($(grep -HRl "$BINNumber" *.odx-f))
   echo "[prepare_SOC_odx_file] Current ODX:"$ODXFile
   
   find $ConfigPath -iname "$ODXFile" -exec grep -oP "<SOURCE-START-ADDRESS>(.*)</SOURCE-START-ADDRESS>" {} \; > source_start_address.txt
   _start_address=`cat source_start_address.txt | cut -d ">" -f 2 | cut -d "<" -f 1`
     
   SizeInBytes=$(stat -c "%s" $1)
   BS_END_ADDRESS=`echo "ibase=10;obase=16;$[$SizeInBytes+$[0x$_start_address]-$[0x1]]"|bc`
   BS_CHECKSUM=`echo "$(crc32 $1)" | tr '[:lower:]' '[:upper:]'`
 
   replace_strings $ODXFile
   sudo cp -rp $ODXFile $BINFolder
	
   ${BS_WORKSPACE}/SourceSpace/SWUpdate/Security/tools/Signature/output/Signature ECC sign ${BS_WORKSPACE}/SourceSpace/SWUpdate/Security/tools/Signature/certificate/VisteonECC.private $BINFolder/$ODXFile
   ${BS_WORKSPACE}/SourceSpace/SWUpdate/Security/tools/Signature/output/Signature ECC test ${BS_WORKSPACE}/SourceSpace/SWUpdate/Security/tools/Signature/certificate/VisteonECC.public $BINFolder/$ODXFile
}

prepare_VIP_odx_file()
{
   cd $1
   
   if [ $BINFolder == "" ]; then
       BINFolder=$BS_UP_OUT_PATH/
   fi
   
   for VIP_ODX_FILE in $(find $1  -name "*.odx-f" ! -name "*SoC_*"); do
       replace_strings $VIP_ODX_FILE
       sudo cp -rp $VIP_ODX_FILE $BINFolder
   done 

   if [ -f $VIP_SREC_FILES ]; then
       sudo cp -rp $VIP_SREC_FILES $BINFolder
   fi

   if [ -f $VIP_SREC_BootLoader_Location ]; then
       sudo cp -rp $VIP_SREC_BootLoader_Location $BINFolder
   else
       echo "No such path:\n $VIP_FBL_VIP_SREC_BootLoader_Location_Location"
   fi

   if [ -f $VIP_FBL_Updater_Location ]; then
	   echo  "-----------------------------------Updater Location Expected path: $VIP_FBL_Updater_Location"
       sudo cp -rp $VIP_FBL_Updater_Location $BINFolder
   else
       echo "=================================No such path:\n $VIP_FBL_Updater_Location  ==========================="
   fi
}

if [ -d ${BS_WORKSPACE}/SourceSpace/Reflash/UPG/private/src/linux ]; then
    for CONFIG_TARGET in $(find "$ConfigPath" -name "*.ini" -type f); do
        generate_up_file $CONFIG_TARGET
    done 
else
    echo "############## UPG was not built ##############"
    echo "[PostBuildUPG]:Total Fatals: 1"
    return -1
fi

for BIN_TARGET in $(find "$BS_UP_OUT_PATH/" -name "*.bin" -type f); do
   prepare_SOC_odx_file $BIN_TARGET $ConfigPath 
done

prepare_VIP_odx_file $ConfigPath 

echo "###################################################################################################################"

if [ $RES_ERR -eq 0 ] ; then
    echo "############## $Variant : Successfully generated '$RES_OK' Update Packages ####################################"
else
    echo "########### $Variant : Failed to generate '$RES_ERR' out of '$(($RES_OK+$RES_ERR))' Update Packages ###########"
fi

echo "###################################################################################################################"
echo TARGET_RESULT=$RES_ERR > variables.properties
