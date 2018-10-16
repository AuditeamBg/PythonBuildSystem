#!/bin/sh

# Enter into build root folder
cd  ${WORKSPACE}/${AdditionalFolderName}

# Find and remove all project settings
find -name ProjectSettings.set -exec rm {} \;
find -name WorkspaceSettings.set -exec rm {} \;

if [ -f ${WORKSPACE}/${AdditionalFolderName}/CI.BuildSystem/scripts/MRA2_APIBuns_build.sh ]; then
    chmod +x ${WORKSPACE}/${AdditionalFolderName}/CI.BuildSystem/scripts/MRA2_APIBuns_build.sh
fi

echo 'visteon' | sudo -S rm -f ${WORKSPACE}/${AdditionalFolderName}/artifacts/*_Sources.7z || true
echo 'visteon' | sudo -S rm -f ${WORKSPACE}/${AdditionalFolderName}/artifacts/*_Sources.txt || true

if [ -f ${WORKSPACE}/${AdditionalFolderName}/SourceSpace/scripts/buildNvfxAdsp.sh ]; then
    chmod +x  ${WORKSPACE}/${AdditionalFolderName}/SourceSpace/scripts/buildNvfxAdsp.sh
fi

# Create Bunny workspace
if [ -d ./BunnyBuildingWorkspace ]; then
    cp ./BunnyBuildingWorkspace/WorkspaceSettings.txt ./BunnyBuildingWorkspace/WorkspaceSettings.set
    cp ./BunnyBuildingWorkspace/SourceSpace/ProjectSettings.txt ./BunnyBuildingWorkspace/SourceSpace/ProjectSettings.set
    cp -rpf ./BunnyBuildingWorkspace/* ./
else
    # Still keep this for the old builds
    echo "No such file or directory ${WORKSPACE}/${AdditionalFolderName}/BunnyBuildingWorkspace "
fi

if [ -d ./BunnyBuildScripts ]; then
    cp -rpf ./BunnyBuildScripts/* ./SourceSpace/
fi

