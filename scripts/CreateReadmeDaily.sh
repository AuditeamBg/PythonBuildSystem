#!/bin/sh

N=`echo $BUILD_NUMBER | sed -r ":L;s=\b([0-9]+)([0-9]{3})\b=\1,\2=g;t L"`
cd ${WORKSPACE}/$AdditionalFolderName
echo "" > ${WORKSPACE}/$AdditionalFolderName/artifacts/readme.txt
echo "SNAPSHOTS" >> ${WORKSPACE}/$AdditionalFolderName/artifacts/readme.txt
echo "" >> ${WORKSPACE}/$AdditionalFolderName/artifacts/readme.txt
awk -f ${WORKSPACE}/$AdditionalFolderName/CI.BuildSystem/scripts/key-content-get.awk -v key=SNAPSHOT ${WORKSPACE}/$AdditionalFolderName/*_resources/*/readme.txt | sed 's/^/    /' >> ${WORKSPACE}/$AdditionalFolderName/artifacts/readme.txt
awk -f ${WORKSPACE}/$AdditionalFolderName/CI.BuildSystem/scripts/key-content-get.awk -v key=SNAPSHOT ${WORKSPACE}/$AdditionalFolderName/*_resources/*/*/readme.txt | sed 's/^/    /' >> ${WORKSPACE}/$AdditionalFolderName/artifacts/readme.txt

if [ *"RB"* = $WORKSPACE ]; then
    echo "    ${BUILD_NAME}" >> ${WORKSPACE}/$AdditionalFolderName/artifacts/readme.txt
else
    echo "    ${buildDefinitionId}_#${N}" >> ${WORKSPACE}/$AdditionalFolderName/artifacts/readme.txt
fi

echo "" >> ${WORKSPACE}/$AdditionalFolderName/artifacts/readme.txt
echo "LINKS" >> ${WORKSPACE}/$AdditionalFolderName/artifacts/readme.txt
echo "" >> ${WORKSPACE}/$AdditionalFolderName/artifacts/readme.txt

awk -f ${WORKSPACE}/$AdditionalFolderName/CI.BuildSystem/scripts/key-content-get.awk -v key=LINKS ${WORKSPACE}/$AdditionalFolderName/*_resources/*/readme.txt | sed 's/^/    /' >> ${WORKSPACE}/$AdditionalFolderName/artifacts/readme.txt
awk -f ${WORKSPACE}/$AdditionalFolderName/CI.BuildSystem/scripts/key-content-get.awk -v key=LINKS ${WORKSPACE}/$AdditionalFolderName/*_resources/*/*/readme.txt | sed 's/^/    /' >> ${WORKSPACE}/$AdditionalFolderName/artifacts/readme.txt

echo "" >> ${WORKSPACE}/$AdditionalFolderName/artifacts/readme.txt
echo "VERSIONS" >> ${WORKSPACE}/$AdditionalFolderName/artifacts/readme.txt
echo "" >> ${WORKSPACE}/$AdditionalFolderName/artifacts/readme.txt

awk -f ${WORKSPACE}/$AdditionalFolderName/CI.BuildSystem/scripts/key-content-get.awk -v key=VERSIONS ${WORKSPACE}/$AdditionalFolderName/*_resources/*/readme.txt >> tmp.txt
awk -f ${WORKSPACE}/$AdditionalFolderName/CI.BuildSystem/scripts/key-content-get.awk -v key=VERSIONS ${WORKSPACE}/$AdditionalFolderName/*_resources/*/*/readme.txt >> tmp.txt
awk 'seen[$0]++==0' tmp.txt | sed 's/^/    /' >> ${WORKSPACE}/$AdditionalFolderName/artifacts/readme.txt
rm -f tmp.txt

if [[ $Variant = *"C5"* ]]; 
then
	for d in ${WORKSPACE}/$AdditionalFolderName/Tools/drive-t*ref-linux/RootfsLinux/targetfs/opt/qt*;
	do
	  for f in $d/lib/pkgconfig/Qt?Core.pc;
	  do
	  	if [ -f $f ]; then
	    	echo -n "    Qt Core " >> ${WORKSPACE}/$AdditionalFolderName/artifacts/readme.txt
	    	grep Version $f >> ${WORKSPACE}/$AdditionalFolderName/artifacts/readme.txt
	    fi
	  done
	done
fi

python -c "import json;import sys;f=open(sys.argv[1]);s=f.read();j=json.loads(s);print j['sdk'].replace('.tar.gz','');print 'carbon-ui',j['githashes']['carbon-ui']" ${WORKSPACE}/$AdditionalFolderName/Tools/drive-t*ref-linux/RootfsLinux/targetfs/opt/hmi/ui/manifest.json | sed 's/^/    /' >> ${WORKSPACE}/$AdditionalFolderName/artifacts/readme.txt
sh ${WORKSPACE}/$AdditionalFolderName/CI.BuildSystem/scripts/software-version.sh | sed 's/^/    /' >> ${WORKSPACE}/$AdditionalFolderName/artifacts/readme.txt
echo "" >> ${WORKSPACE}/$AdditionalFolderName/artifacts/readme.txt
echo "BUNS" >> ${WORKSPACE}/$AdditionalFolderName/artifacts/readme.txt

awk -f ${WORKSPACE}/$AdditionalFolderName/CI.BuildSystem/scripts/key-content-get.awk -v key=BUNS ${WORKSPACE}/$AdditionalFolderName/*_resources/*/readme.txt | sed 's/^/    /' >> ${WORKSPACE}/$AdditionalFolderName/artifacts/readme.txt
awk -f ${WORKSPACE}/$AdditionalFolderName/CI.BuildSystem/scripts/key-content-get.awk -v key=BUNS ${WORKSPACE}/$AdditionalFolderName/*_resources/*/*/readme.txt | sed 's/^/    /' >> ${WORKSPACE}/$AdditionalFolderName/artifacts/readme.txt
sed 's/^/    /' ${WORKSPACE}/$AdditionalFolderName/artifacts/buns_included_log.txt >> ${WORKSPACE}/$AdditionalFolderName/artifacts/readme.txt

echo "" >> ${WORKSPACE}/$AdditionalFolderName/artifacts/readme.txt
echo "" >> ${WORKSPACE}/$AdditionalFolderName/artifacts/readme.txt
echo "LOC" >> ${WORKSPACE}/$AdditionalFolderName/artifacts/readme.txt
echo "" >> ${WORKSPACE}/$AdditionalFolderName/artifacts/readme.txt
python ${WORKSPACE}/$AdditionalFolderName/CI.BuildSystem/scripts/ClocParserSum.py ${WORKSPACE}/$AdditionalFolderName >> ${WORKSPACE}/$AdditionalFolderName/artifacts/readme.txt

if [[ $Variant = *"IC_E"* ]]; 
then
    variant_ff="IC-E"
    variant_img="ice"
fi

if [[ $Variant = *"IC_H"* ]];
then
    variant_ff="IC-H"
    variant_img="ich"
fi

if [[ $Variant = *"C5"* ]];
then
    variant_ff="C5"
    variant_img="c5"
fi

echo "visteon" | sudo -S bash -c 'printf "\n\nSOC IMAGES\n" >> artifacts/readme.txt'

hostname=`hostname`
current_dir=`pwd`
printf_c='printf "    %s %s %s %s %s\n"'
for file in `ls  ${WORKSPACE}/$AdditionalFolderName/cards/Mra2-SOC-${variant_ff}v${ITERATION_NUMBER}.${BUILD_NUMBER}/drive-t186ref-foundation/tools/host/flashtools/bootburn/images-${variant_img}/*.bin`; do
    filesize=`stat -c %s $file`
    checksum=`md5sum $file | cut -d " " -f1`
    echo "visteon" | sudo -S bash -c "$printf_c $hostname $current_dir $file $filesize $checksum >> artifacts/readme.txt"
done

cd ${WORKSPACE}/$AdditionalFolderName/artifacts

7zr x *FULL.7z e di-vip-tools -xr!.project
7z a ${BUILD_NAME}_di-vip-tools.7z di-vip-tools
echo 'visteon' | sudo -S rm -f -r di-vip-tools
echo 'visteon' | sudo -S rm -f -v buns_included_log.txt *FULL.7z
echo 'visteon' | sudo -S  md5sum -b *.7z > MD5 || true 
echo 'visteon' | sudo -S  md5sum -b *.tar* >> MD5 || true
