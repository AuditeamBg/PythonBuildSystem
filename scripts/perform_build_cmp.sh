#!/bin/sh

cd ${WORKSPACE}/${AdditionalFolderName}

if [[ -d ${WORKSPACE}/${AdditionalFolderName}/HMI/ ]]; then
	    export DIHMI_7Z=`ls ${WORKSPACE}/${AdditionalFolderName}/HMI/ | awk '/dihmi/' | awk '/int/' | awk '/7z/' | awk '!/md5/'`
	    export DIHMI_ZIP=`ls ${WORKSPACE}/${AdditionalFolderName}/HMI/ | awk '/dihmi/' | awk '/int/' | awk '/zip/' | awk '!/md5/'`
	    if [ -z ${DIHMI_7Z} ]; then
	       	export DIHMI=${DIHMI_ZIP::-4}
	    elif [ -z ${DIHMI_ZIP} ]; then
	       	export DIHMI=${DIHMI_7Z::-3}
	    else
	        echo "\n========= Luxsoft sent different archive again!!! Please check! =========\n"
	        exit 1
	    fi
	       
	    if [[ -f ${WORKSPACE}/${AdditionalFolderName}/HMI/${DIHMI}.7z ]]; then
	        7zr x ${WORKSPACE}/${AdditionalFolderName}/HMI/${DIHMI}.7z -aoa -o${WORKSPACE}/${AdditionalFolderName}/HMI/
	    elif [[ -f ${WORKSPACE}/${AdditionalFolderName}/HMI/${DIHMI}.zip ]]; then
	        unzip ${WORKSPACE}/${AdditionalFolderName}/HMI/${DIHMI}.zip -d ${WORKSPACE}/${AdditionalFolderName}/HMI/ -x
	    fi
	    export INTHMI=`ls ${WORKSPACE}/${AdditionalFolderName}/HMI/${DIHMI} | awk '/int/' | awk '/_e0/' | awk '/7z/'`
	    if [[ -f ${WORKSPACE}/${AdditionalFolderName}/HMI/${DIHMI}/${INTHMI} ]]; then
	        7zr x ${WORKSPACE}/${AdditionalFolderName}/HMI/${DIHMI}/${INTHMI} -aoa -o${WORKSPACE}/${AdditionalFolderName}/HMI/${DIHMI}/
	    fi
	    cp -r ${WORKSPACE}/${AdditionalFolderName}/HMI/${DIHMI}/${INTHMI::-3}/* ${WORKSPACE}/${AdditionalFolderName}/HMI/
fi


if [[ ${IS_PRODUCT_BUILD} == "True" ]] ; then
    mkdir -p ${WORKSPACE}/${AdditionalFolderName}/resources/configuration/
    echo "Copying Autogrator configuration from ${WORKSPACE}/${AdditionalFolderName}/Doc/IntegrationMra2H2/doc/Autogrator"
    cp -rp ${WORKSPACE}/Doc/IntegrationMra2H2/doc/Autogrator/* ${WORKSPACE}/resources/configuration/
else
    mkdir -p ${WORKSPACE}/${AdditionalFolderName}/resources/configuration/
    echo "Copying Autogrator configuration from ${WORKSPACE}/${AdditionalFolderName}/Doc/IntegrationMra2H2/doc/Autogrator"
    cp -rp ${WORKSPACE}/${AdditionalFolderName}/Doc/IntegrationMra2H2/doc/Autogrator/* ${WORKSPACE}/${AdditionalFolderName}/resources/configuration/
fi

# Trigger the build
echo "starting to build buns in workspace:"

if [[ ${IS_PRODUCT_BUILD} != "True" ]] ; then
    date3=$(date +"%s")

    # Remove top bun
    if [[ -d ./SourceSpace/Top ]]; then
        rm -rf ./SourceSpace/Top
    fi

    mkdir -p ./SourceSpace/Top/Bun/build
    mkdir -p ./SourceSpace/Top/Bun/private/build

    touch ./SourceSpace/Top/Bun/build/Bun.bunion
    touch ./SourceSpace/Top/Bun/private/build/Bun.bunion
    
    if [[ $WORKSPACE == *C5* ]] && [[ $WORKSPACE == *Integrity* ]]; then
        variantFile='$WORKSPACE/${AdditionalFolderName}/SourceSpace/UserVariants/UserVariants/plugins/C5.py'
        end=$(tail -n 1 $variantFile)
        if [[ "$end" != *"build.addDefines('BUNNY_BUILD')" ]]; then
            echo "        build.addDefines('BUNNY_BUILD')" >> $variantFile
        fi
    fi
    
	tail $WORKSPACE/${AdditionalFolderName}/SourceSpace/ProjectSettings.set -n 2 | grep "USE_COMA_GENSERVER"
	if [ $? -ne 0 ]; then
		# Add preventive new line in ProjectSettings.set
    	echo "" >> ./SourceSpace/ProjectSettings.set
        echo "USE_COMA_GENSERVER='true'" >> ./SourceSpace/ProjectSettings.set
        echo "COMA_GENSERVER_EXE='../Tools/ComaGen/GeneratorServer/GeneratorServer'" >> ./SourceSpace/ProjectSettings.set
	fi
	
    if [[ "$JOB_NAME" == *UnitTest ]]; then
        echo "build.addCompilerOptions('C++', '-fprofile-arcs', '-ftest-coverage', '-fPIC', '-O0')" >> ./SourceSpace/Top/Bun/build/Bun.bunion
        echo "build.addLinkerOptions('-lgcov', '-coverage')" >> ./SourceSpace/Top/Bun/build/Bun.bunion
    fi

    if [[ "${Variant}" == *Integrity* ]]; then
        echo "build.addLinkerOptions('-check_global_regs=1')" >> ./SourceSpace/Top/Bun/build/Bun.bunion
    fi
    
    if [[ "${Variant}" == *Linux* ]]; then
        echo "build.addCompilerOptions('fstack-protector', '-D_FORTIFY_SOURCE=2')" >> ./SourceSpace/Top/Bun/build/Bun.bunion
    fi

    echo "bun.setType(FACADE)" >> ./SourceSpace/Top/Bun/build/Bun.bunion
    echo "bun.requires(" >> ./SourceSpace/Top/Bun/build/Bun.bunion

    # fill the top bun with the MRA2 specific domains
    if [[ "$JOB_NAME" == *UnitTest ]]; then
        for BUILD_TARGET in $@; do
            if [[ "$BUILD_TARGET" == *UnitTest ]]; then
                a="'"
                a+=$BUILD_TARGET
                a+="',"
                echo $a >> ./SourceSpace/Top/Bun/build/Bun.bunion
            else
                echo "$BUILD_TARGET will not be included in UnitTest build"
            fi
        done
    else
        for BUILD_TARGET in $@; do
            echo -e "\n --------------- BUILD BUN IS : $BUILD_TARGET ------------------ \n"
            if [[ "$BUILD_TARGET" == *UnitTest ]]; then
                echo "$BUILD_TARGET will not be included in normal build"
            else
                a="'"
                a+=$BUILD_TARGET
                a+="',"
                echo $a >> ./SourceSpace/Top/Bun/build/Bun.bunion
            fi
        done
    fi

    echo ")" >> ./SourceSpace/Top/Bun/build/Bun.bunion

    if [[ -z "${LOCAL_CLEAN_REBUILD}" ]]; then
        ./Tools/Bunny/Bunny/bin/BunnyBuild Top.Bun ${Variant} ${UserSettings} -k 2>&1 | tee -a bunny_log.txt
        echo $PIPESTATUS > return_code_of_last_build.txt
    else
        ./Tools/Bunny/Bunny/bin/BunnyRebuild Top.Bun ${Variant} ${UserSettings} -k 2>&1 | tee -a bunny_log.txt 
        echo $PIPESTATUS > return_code_of_last_build.txt
    fi
    
    if [[ "${BUILD_NAME}" == *MRA2* && "${IS_PRODUCT_BUILD}" == False && ${Variant} == *IC-H* ]]; then
        echo "####################################################"
        echo "<!> STARTING BUILD WITH ADDITIONAL USER VARIANTS <!>"
        echo "####################################################"
        pathToAdditionalUserVariantsBuildScript=$SCRIPT_ROOT/scripts/perform_build_additional_user_variants.py
        python $pathToAdditionalUserVariantsBuildScript
    fi

    # Delete SourceSpace/Top and prepare it for archiving..

    if [[ -d ./Top ]]; then
        rm -rfv  ./Top
    fi
    cp -rpv ./SourceSpace/Top ./
    rm -rfv ./SourceSpace/Top

    date4=$(date +"%s")
    diff=$(($date4-$date3))
    echo "MRA2 components build tooks $(($diff / 60)) minutes and $(($diff % 60)) seconds."
fi

date1=$(date +"%s")
# Platform type of build
if [ -f ./SourceSpace/Build.sh ]; then
    if [[ "${Variant}" != X86Lin* ]]; then
        ./SourceSpace/Build.sh ${Variant} 2>&1 | tee -a bunny_log.txt
    fi
fi

date2=$(date +"%s")
diff=$(($date2-$date1))
echo "Platform build took $(($diff / 60)) minutes and $(($diff % 60)) seconds."
echo "all the buns are done"

