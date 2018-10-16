#!/bin/sh
# Integrity Integrate script
# integrate a monolith out of binaries
# Parameter
# $1 variant, e.g. mfa2_b1

# Parameter check
DRIVE_INTEGRITY=$3/ghs.nvidia.int1144/drive-t186ref-integrity/bin
TEGRAMOD_BIN_PATH=$3/visteon.drivers/bin/mra
TOOLS_PATH=$3/ghs.comp_201714_linux
INTEX_EXE=$3/ghs.nvidia.int1144/drive-t186ref-integrity/integrity-11.4.4-arm64/multi/bin/linux86/intex
GHS_INT_PATH=$3/ghs.nvidia.int1144/drive-t186ref-integrity/integrity-11.4.4-arm64/
PLATFORM_BIN_PATH=$5
PLATFORM_BIN_UPDATE_PATH=$6
MONOLITH_PATH=$2
STARTER_BIN_PATH=$MONOLITH_PATH/../../../../ProductSpace/$1/Starter/Starter/bin
MKIMAGE_OUT_DIR=$MONOLITH_PATH/img
MONOLITH_INCLUDE_PATH=$4/Tools/IntegrityBSP/visteon.drivers/mra_monolith
COMPRESSED_MKIMAGE_OUT_DIR=$MONOLITH_PATH/NOR;
WD_PATH=$3/visteon.drivers/bin/mra

if [[ $1 == *TegraP1*IC_E* ]]; then
  MRA2_MONOLITH_INT_FILE=$MONOLITH_PATH/mra2_monolith_ic_e.int
fi
if [[ $1 == *TegraP1*IC_H* ]]; then
  MRA2_MONOLITH_INT_FILE=$MONOLITH_PATH/mra2_monolith_ic_h.int
fi
if [[ $1 == *TegraP1*C5* ]]; then
  MRA2_MONOLITH_INT_FILE=$MONOLITH_PATH/mra2_monolith_c5.int
fi


OUT_DIR=$2/bin

#clean the env
rm -rf $OUT_DIR
mkdir -p $OUT_DIR


tar -xvf $4/resources/dependencies/MRA2/BSP/ApplicationsIntegrity/MRA2H2/bin/applications.tar.gz --strip 1 -C $MONOLITH_PATH
tar -xvf $4/resources/dependencies/MRA2/BSP/ApplicationsIntegrity/MRA2H2/bin/applications.tar.gz --strip 2 -C $MONOLITH_PATH


  $INTEX_EXE \
  -integrity_version 11.4.4 -alt_tools_path $TOOLS_PATH \
    -bsp devtree-arm64 -os_dir $GHS_INT_PATH -gstack_options \
    -intexoption -no_shared_libs -intexoption -no_shared_libs_quiet \
    -intexoption -allocate_initialized_together \
    -intexoption -includefiledir $VIP_PROXY_INCLUDE_PATH \
    -intexoption -allowsetinitialtaskpriority \
    -intfile $MRA2_MONOLITH_INT_FILE \
    $PLATFORM_BIN_PATH/mra_kernel \
    $PLATFORM_BIN_PATH/osal_shm_manager \
    $PLATFORM_BIN_PATH/osal_res_manager \
    $PLATFORM_BIN_PATH/iftpserver_module \
    $PLATFORM_BIN_PATH/ser_des_module \
    $TEGRAMOD_BIN_PATH/tegra_ip4server_module \
    $TEGRAMOD_BIN_PATH/rpcbind_module \
    $TEGRAMOD_BIN_PATH/net_server_module \
    $TEGRAMOD_BIN_PATH/mixer_ctrl \
    $TEGRAMOD_BIN_PATH/des_pwrup_rgmii_as0 \
    $TEGRAMOD_BIN_PATH/touch_srv_as0 \
    $DRIVE_INTEGRITY/nvrm_as0 \
    $DRIVE_INTEGRITY/nvvicsi_as0 \
    $DRIVE_INTEGRITY/dispinit \
    $DRIVE_INTEGRITY/nvevent_logger \
    $DRIVE_INTEGRITY/nvclock_server \
    $DRIVE_INTEGRITY/nvpowergate_server \
    $DRIVE_INTEGRITY/nvtherm_server \
    $DRIVE_INTEGRITY/nvi2c_server \
    $DRIVE_INTEGRITY/nvspi_server \
    $DRIVE_INTEGRITY/nvgpio_server \
    $DRIVE_INTEGRITY/displayserver \
    $DRIVE_INTEGRITY/nvaudio_client_server \
    $DRIVE_INTEGRITY/nvvse_server \
    $DRIVE_INTEGRITY/nvtrusty_server \
    $DRIVE_INTEGRITY/nvtrusty_storage \
    $WD_PATH/watchdog \
    $WD_PATH/ivfsserver_module \
    $WD_PATH/iftpserver_module \
    $STARTER_BIN_PATH/Starter.elf \
  $MONOLITH_PATH/smi130_gyro_example_as0 \
    -o $MONOLITH_PATH/integrity


$TOOLS_PATH/gmemfile  $MONOLITH_PATH/integrity -o $OUT_DIR/integrity.bin -map   $MONOLITH_PATH/integrity.map


## create the MKimage

LoadAdress=`echo $(( $(echo $(cat  $MONOLITH_PATH/integrity.map  | grep "Start Address" |  cut -d ":" -f2)) ))`
EntryPoint=`echo $(( $(echo $(cat  $MONOLITH_PATH/integrity.map  | grep "Start Address" |  cut -d ":" -f2)) + 0x1000 ))`


printf  -v "LoadAdress" "%x" "$LoadAdress"
printf  -v "EntryPoint" "%x" "$EntryPoint"


rm -rf $MKIMAGE_OUT_DIR
mkdir -p $MKIMAGE_OUT_DIR


$MONOLITH_PATH/mkimage \
   -A arm \
   -O integrity \
   -T kernel \
   -C none \
   -a $LoadAdress \
   -e $EntryPoint \
   -n "Integrity App Mode" \
   -d $OUT_DIR/integrity.bin \
   $MKIMAGE_OUT_DIR/Integrity.img

rm -rf $COMPRESSED_MKIMAGE_OUT_DIR
mkdir -p  $COMPRESSED_MKIMAGE_OUT_DIR

$MONOLITH_PATH/lz4 -9  $OUT_DIR/integrity.bin $OUT_DIR/integrity.bin.lz4

$MONOLITH_PATH/mkimage \
   -A arm \
   -O integrity \
   -T kernel \
   -C lz4 \
   -a $LoadAdress \
   -e $EntryPoint \
   -n "Integrity App Mode" \
   -d $OUT_DIR/integrity.bin.lz4 \
   $COMPRESSED_MKIMAGE_OUT_DIR/Integrity.img


if [ ! -f $OUT_DIR/integrity.bin ]; then
#tput setaf 1;
echo " _____       ___   _   _      "
echo "|  ___|     /   | | | | |     "
echo "| |__      / /| | | | | |     "
echo "|  __|    / / | | | | | |     "
echo "| |      / /__| | | | | |___  "
echo "|_|     /_/   |_| |_| |_____| "
echo "FATAL : integrity.bin not generated   :( "
#tput sgr0;
return -1

elif [ ! -f $MKIMAGE_OUT_DIR/Integrity.img ]; then
#tput setaf 1;
echo " _____       ___   _   _      "
echo "|  ___|     /   | | | | |     "
echo "| |__      / /| | | | | |     "
echo "|  __|    / / | | | | | |     "
echo "| |      / /__| | | | | |___  "
echo "|_|     /_/   |_| |_| |_____| "
echo "FATAL :  Integrity.img not generated   :( "
#tput sgr0;
return -1

else
#tput setaf 2;
echo " _____  __   __ "
echo "/  _  \ | | / / "
echo "| | | | | |/ /  "
echo "| | | | | |\\ \\  "
echo "| |_| | | | \\ \\ "
echo "\\_____/ |_|  \\_\\"
echo "All images are correctly created!    :) "
#tput sgr0;

fi