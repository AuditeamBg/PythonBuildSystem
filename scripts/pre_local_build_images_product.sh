#!/bin/sh

filename="environment_vars_for_product.txt"
export WORKSPACE=$(dirname $(dirname $(dirname "$PWD")))
export BUILD_NUMBER=$(basename $(dirname $(dirname "$PWD")))
export SCRIPT_ROOT="$WORKSPACE/$BUILD_NUMBER/CI.BuildSystem"
export PLUGINS_MRA2_ROOT="$SCRIPT_ROOT/plugins/MRA2/"
export AdditionalFolderName=$BUILD_NUMBER
export LOCAL_IMAGE_CREATE=True

cd $SCRIPT_ROOT/scripts

while read -r line

do
    IN="$line"
    source ./$filename
    export $(cut -d= -f1 ./$filename)
done < "./$filename"

python pre_local_build_images_product.py