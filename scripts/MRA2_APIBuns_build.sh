#!/bin/bash
export AdditionalFolderName=IncrementalBuild

#change current directory
cd ${WORKSPACE}/${AdditionalFolderName}/Tools/ThriftMe/ThriftMe.Gen.bin

# Generate, build and release IF1
echo "Calling IF1_generate_all.sh from /Tools/ThriftMe/ThriftMe.Gen.bin folder"

./IF1_generate_all.sh

echo "Generation of IF1 completed!"
