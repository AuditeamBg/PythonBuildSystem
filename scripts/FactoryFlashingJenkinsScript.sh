#ATTENTION - clean up unnecessary time consuming copy operations!!!
cd ${WORKSPACE}

#Workaround - copy predefined NOR and NAND images from /home/visteon/FactoryFlashing
#cp /home/visteon/FactoryFlashing/*.bin ${WORKSPACE}/resources

#Copy Image files with scp. Run this as a backgroung process to save time with parallel jobs - downloading image and extracting the archive
filename=${WORKSPACE}/resources/readme.txt
lines=`wc -l  $filename | cut -d ' ' -f1`
b_line=`grep -n "SOC IMAGES" $filename | cut -d':' -f 1`
from_line=$((lines - b_line))
e_line=`tail -n $from_line $filename | grep -n '^$' | cut -d':' -f 1`
if [ "$e_line" = "" ]; then
		e_line=$from_line
	else
			(( e_line-- ))
		fi

		echo "Reading $e_line lines from file $filename from line $b_line"

		echo "tail -n $from_line $filename | head -n $e_line"

		tail -n $from_line $filename | head -n $e_line > tmp.txt

		j=0

		while IFS='' read -r line || [[ -n "$line" ]]; do
				echo "Line $(( j+ 1 ))"
				    hostname=`echo $line | cut -d " " -f 1`
				    	folder=`echo $line | cut -d " " -f 2`
						filename=`echo $line | cut -d " " -f 3`
							file_names[$j]=`echo $line | cut -d " " -f 3 | rev | cut -d "/" -f1 | rev`
								file_size[$j]=`echo $line | cut -d " " -f 4`
									file_checksums[$j]=`echo $line | cut -d " " -f 5`
										file_prev_size[$j]=0
											file_download_finished[$j]=false
												
												echo ""
													echo "Starting download of ${file_names[j]} - ${file_size[j]} bytes (${file_checksums[j]})"
														
														#echo "sshpass -p "visteon" scp visteon@${hostname}:${filename} ${WORKSPACE}/resources/"
															#echo ""
																
																sshpass -p "visteon" scp visteon@${hostname}:${filename} ${WORKSPACE}/resources/ &
																	(( j++ ))
																done < tmp.txt

																echo "===================================="
																echo  ${file_names[*]}
																echo  ${file_size[*]}
																echo  ${file_checksums[*]}
																echo "===================================="
																echo ""

																echo "And on we go..."

																HW_VARIANT=`echo ${Hardware} | tr [a-z] [A-Z]`
																SW_VARIANT=`echo ${Variant} | tr [a-z] [A-Z]`
																S_SW_VARIANT=`echo ${SW_VARIANT} | tr [A-Z] [a-z] | tr - _`
																U_SW_VARIANT=`echo ${SW_VARIANT} | tr - _`
																V_SW_VARIANT=`echo ${SW_VARIANT} | tr [A-Z] [a-z]`
																case $S_SW_VARIANT in
																		ic_h)
																			    	bsp_s_variant="mich"
																				        ;;
																					    ic_e)
																						        	bsp_s_variant="mice"
																								        ;;
																									    c5)
																										        	bsp_s_variant="micc"
																												        ;;
																											esac

																											FOLDER=${WORKSPACE}/${BUILD_NAME}
																											ST1_FOLDER=${FOLDER}/stage1
																											ST2_FOLDER=${FOLDER}/stage2
																											CHUNKS_SIZE="100M"

																											#Extract parent job archives - Images
																											for archive in resources/*.7z; do
																													7z x $archive
																												done

																												#build Factory Flashing Micro Linux
																												cd cards/Mra2-SOC-${SW_VARIANT}v${RELEASE_VERSION}/drive-t186ref-foundation/tools/host/flashtools/bootburn/

																												mkdir ${S_SW_VARIANT}

																												echo "visteon" | sudo -S ./create_bsp_images.sh -l -r 02 -b ${bsp_s_variant}-${Hardware} -k $(readlink -f quickboot_qspi_linux_factoryflash_${V_SW_VARIANT}.cfg) -g ${S_SW_VARIANT}

																												#Create Factory Flashing archive package structure
																												mkdir -p ${ST1_FOLDER}
																												mkdir -p ${ST2_FOLDER}

																												#Manifest file line format
																												manifest_format="%-40s %-20s %-18s %-34s %-15s %-15s\n"

																												#Add Manifest files header line
																												echo "Creating Stage1 & Stage2 manifest files with their headers"
																												printf "$manifest_format" "#Filename" "Filetype" "FileSize(MB)" "MD5Checksum" "StartOffset" "EndOffset" > ${ST1_FOLDER}/st1-manifest
																												printf "$manifest_format" "#Filename" "Filetype" "FileSize(MB)" "MD5Checksum" "StartOffset" "EndOffset" > ${ST2_FOLDER}/st2-manifest

																												#Copy Factory Flashing Micro Linux binaries to stage1 directory
																												echo "Add stage1 images to ${ST1_FOLDER} folder "
																												sudo mv ${S_SW_VARIANT}/* ${ST1_FOLDER}

																												cd ${WORKSPACE}

																												#Check if images have been downloaded!
																												#Wait until they are! And verify that they are still downloading

																												echo "Verifying download progress..."
																												while true; do
																														all_finished=true
																															
																															for i in ${!file_names[*]}; do
																																		
																																		if ! ${file_download_finished[i]}; then
																																						echo "Checking file ${file_names[i]}..."
																																									if [ ! -f ${WORKSPACE}/resources/${file_names[i]} ]; then
																																														echo "File ${WORKSPACE}/resources/${file_names[i]} was not created!"
																																																		exit 1
																																																					fi
																																																								filesize=`stat -c %s ${WORKSPACE}/resources/${file_names[i]}`
																																																											if (( $filesize == ${file_size[i]} )); then
																																																																echo "File seems to have been downloaded. Verifying checksum..."
																																																																				checksum=`md5sum ${WORKSPACE}/resources/${file_names[i]} | cut -d " " -f1`
																																																																								#echo "? $checksum == ${file_checksums[i]}"
																																																																												if [ "$checksum"  = "${file_checksums[i]}" ]; then
																																																																																		file_download_finished[$i]=true
																																																																																							echo "File download has finished"
																																																																																											fi
																																																																																														elif (( $filesize == ${file_prev_size[i]} )); then
																																																																																																			echo "File ${WORKSPACE}/resources/${file_names[i]} download seems to have been interupted!"
																																																																																																							exit 1
																																																																																																										else
																																																																																																															file_prev_size[$i]=$filesize
																																																																																																																			p=$(( filesize * 100 / file_size[i] ))
																																																																																																																							echo "Downloading ${WORKSPACE}/resources/${file_names[i]}... $p %"
																																																																																																																										fi
																																																																																																																												fi
																																																																																																																														
																																																																																																																														#echo "all_finished: *${all_finished}* and current is *${file_download_finished[i]}* ; becomes: "
																																																																																																																																#echo [ "$all_finished" = true ]&& [ "${file_download_finished[i]}" = true ]
																																																																																																																																		
																																																																																																																																		if [ "$all_finished" = true ]&& [ "${file_download_finished[i]}" = true ]; then
																																																																																																																																						all_finished=true
																																																																																																																																									#echo "T"
																																																																																																																																											else
																																																																																																																																															all_finished=false
																																																																																																																																																		#echo "F"
																																																																																																																																																				fi
																																																																																																																																																						
																																																																																																																																																						echo ""
																																																																																																																																																								echo ""
																																																																																																																																																									done
																																																																																																																																																										
																																																																																																																																																										if [ $all_finished = true ]; then
																																																																																																																																																													echo "All downloads finished!"
																																																																																																																																																															break;
																																																																																																																																																																fi
																																																																																																																																																																	echo "Waiting for 30 seconds..."
																																																																																																																																																																		sleep 30
																																																																																																																																																																	done

																																																																																																																																																																	#Rename SoC Images:
																																																																																																																																																																	NOR_IMAGE_FILE=${ST2_FOLDER}/MRA2_${SW_VARIANT}_${RELEASE_VERSION}_NORContent.bin
																																																																																																																																																																	echo "Copy SoC images to ${ST2_FOLDER} folder"
																																																																																																																																																																	cp ${WORKSPACE}/resources/1-dev-mtd-mtd0-${Hardware}.bin ${NOR_IMAGE_FILE}

																																																																																																																																																																	#TODO: handle SOC images for IC-E and C5 variants
																																																																																																																																																																	cp ${WORKSPACE}/resources/2-dev-block-3460000-sdhci.bin ${ST2_FOLDER}/MRA2_${SW_VARIANT}_${RELEASE_VERSION}_SoC-DI.img

																																																																																																																																																																	if [[ $SW_VARIANT = *"C5"* ]];
																																																																																																																																																																	then
																																																																																																																																																																		cp ${WORKSPACE}/resources/3-dev-block-3440000-sdhci.bin ${ST2_FOLDER}/MRA2_${SW_VARIANT}_${RELEASE_VERSION}_SoC-IVI.img
																																																																																																																																																																	fi
																																																																																																																																																																	#Update manifest for NOR image file by adding a line for the file
																																																																																																																																																																	new_file_size=$(stat -c%s "${NOR_IMAGE_FILE}")
																																																																																																																																																																	printf "$manifest_format" "MRA2_${SW_VARIANT}_${RELEASE_VERSION}_NORContent.bin" "NORImage" `ls -l --block-size=M ${NOR_IMAGE_FILE} | cut -d' ' -f 5 | sed 's/.$//'` `md5sum ${NOR_IMAGE_FILE} | cut -d' ' -f 1` 0 ${new_file_size} >> ${ST2_FOLDER}/st2-manifest

																																																																																																																																																																	for board in DI IVI; do
																																																																																																																																																																			i=0
																																																																																																																																																																			    start_offset=0
																																																																																																																																																																			        
																																																																																																																																																																			        if [ -f ${ST2_FOLDER}/MRA2_${SW_VARIANT}_${RELEASE_VERSION}_SoC-${board}.img ]; then
																																																																																																																																																																					    
																																																																																																																																																																					    	#Split SoC image into $CHUNKS_SIZE chunks (default 100 MB - defined above)
																																																																																																																																																																								echo "Splitting MRA2_${SW_VARIANT}_${RELEASE_VERSION}_SoC-${board}.img image into chunks of size ${CHUNKS_SIZE}..."
																																																																																																																																																																								    	split -b ${CHUNKS_SIZE} ${ST2_FOLDER}/MRA2_${SW_VARIANT}_${RELEASE_VERSION}_SoC-${board}.img ${ST2_FOLDER}/MRA2_${SW_VARIANT}_${RELEASE_VERSION}_SoC-${board}.part_
																																																																																																																																																																									    
																																																																																																																																																																											for file in ${ST2_FOLDER}/MRA2_${SW_VARIANT}_${RELEASE_VERSION}_SoC-${board}.part_*; do
																																																																																																																																																																															printf -v j "%03d" $((i++))
																																																																																																																																																																															        	new_file=${ST2_FOLDER}/MRA2_${SW_VARIANT}_${RELEASE_VERSION}_SoC-${board}-$j.img
																																																																																																																																																																																	        
																																																																																																																																																																																	        	#Rename chunk file to compy with defined format
																																																																																																																																																																																			        	mv $file $new_file
																																																																																																																																																																																					        
																																																																																																																																																																																					        	new_file_size=$(stat -c%s "${new_file}")
																																																																																																																																																																																									
																																																																																																																																																																																							        	#Update manifest file by adding a line for the file
																																																																																																																																																																																												echo "Adding chunk $new_file to manifest"
																																																																																																																																																																																												        	printf "$manifest_format" "MRA2_${SW_VARIANT}_${RELEASE_VERSION}_SoC-${board}-$j.img" "SoC${board}Image" `ls -l --block-size=M ${new_file} | cut -d' ' -f 5 | sed 's/.$//'` `md5sum ${new_file} | cut -d' ' -f 1` ${start_offset} $((start_offset += new_file_size - 1)) >> ${ST2_FOLDER}/st2-manifest
																																																																																																																																																																																														        	((start_offset++))
																																																																																																																																																																																																		done
																																																																																																																																																																																																		    
																																																																																																																																																																																																		    	#Clean up - remove original image
																																																																																																																																																																																																			    	rm ${ST2_FOLDER}/MRA2_${SW_VARIANT}_${RELEASE_VERSION}_SoC-${board}.img
																																																																																																																																																																																																				    fi
																																																																																																																																																																																																			    done

																																																																																																																																																																																																			    cd ${WORKSPACE}

																																																																																																																																																																																																			    #Archive factory flashing package, store in artifacts folder for Jenkins archiving
																																																																																																																																																																																																			    echo "Archive factory flashing package, store in artifacts folder for Jenkins archiving"
																																																																																																																																																																																																			    echo "visteon" | sudo -S 7z a ${BUILD_NAME}.7z ${FOLDER}/*

																																																																																																																																																																																																			    mkdir -p ${WORKSPACE}/artifacts

																																																																																																																																																																																																			    mv ${BUILD_NAME}.7z ${WORKSPACE}/artifacts

