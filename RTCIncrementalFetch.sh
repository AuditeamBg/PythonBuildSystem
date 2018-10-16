#!/bin/sh

KillRTCDeamon()
{

	CHECK_DAEMON_L=$*
	
  	# find the port on which the daemon is running
    DAEMON_PORT=`egrep -o ' [0-9]+' <<< "$CHECK_DAEMON_L" | sed -e 's/^[[:space:]]*//'`
    
    # kill the deamon
    lsof -i | grep $DAEMON_PORT | awk '{print $2}' | xargs kill -9
}


JAZZ_SERVER="https://jazz.sofia.visteon.com:9443/ccm"
LSCM='/home/visteon/jazz_4.0.2.1/scmtools/eclipse'
CREDENTIALS='/opt/credentials/rtc.yaml'
LOAD_RULES="LoadRuleFiles/Streams/1C.MFA2.IC-C5.B1.Linux/1C.MFA2.IC-C5.B1.Linux.loadrule"
JAZZ_USER="KARLSRCI"

REPOSITORY_WORKSPACE=$1
STREAM=$2

CHANGES_AVAILABLE=0
FETCH_FAILED=1
ACCEPT_FAILED=1

time ${LSCM}/lscm login -r ${JAZZ_SERVER} -n local -u $JAZZ_USER -P $JAZZ_PASS
if [ ! -d ${WORKSPACE}/$AdditionalFolderName ]; then
	mkdir ${WORKSPACE}/$AdditionalFolderName
fi
if [ ! -d ${WORKSPACE}/$AdditionalFolderName/accept ]; then
	mkdir ${WORKSPACE}/$AdditionalFolderName/accept
fi
cd ${WORKSPACE}/$AdditionalFolderName
if [ ! -d "./.jazz5" ]; then
  echo "jazz folder does not exist"
  #Check load return value
  cd accept
 time ${LSCM}/lscm accept -r local -s $STREAM -t "$REPOSITORY_WORKSPACE" --no-merge --flow-components --overwrite-uncommitted --verbose || true
  cd ..
  time ${LSCM}/lscm load -r local -R ${LOAD_RULES} -d ${WORKSPACE}/${AdditionalFolderName}/ "$REPOSITORY_WORKSPACE" 2>LOAD_RESULT.TXT || true
  LOAD_RESULT=`cat LOAD_RESULT.TXT | grep -e "Problem running "` || LOAD_RESULT=1
  CHECK_DAEMON=`cat LOAD_RESULT.TXT | grep -e "already owned by daemon running on port"` || CHECK_DAEMON=1
  
  # We have deamon lock need to kill the process
  if [[ $CHECK_DAEMON != "1" ]]; then

	#Kill the deamon
    KillRTCDeamon $CHECK_DAEMON
    
    # Daemon is killed try to download again
    time ${LSCM}/lscm load -r local -R ${LOAD_RULES} -d ${WORKSPACE}/${AdditionalFolderName}/ "$REPOSITORY_WORKSPACE" 2>LOAD_RESULT.TXT || true 
    # If fail again don't recover
    LOAD_RESULT=`cat LOAD_RESULT.TXT | grep -e "Problem running "` || LOAD_RESULT=1
  fi  
  
  if [[ $LOAD_RESULT != "1" ]]; then
  	exit 1
  fi
  CHANGES_AVAILABLE=1
else
  ACCEPT_RESULT=$(${LSCM}/lscm accept -r local -s $STREAM --no-merge --flow-components --overwrite-uncommitted --verbose || true) 
  CHANGES_AVAILABLE=`echo -e "$ACCEPT_RESULT" | grep -e "Workspace unchanged."` || CHANGES_AVAILABLE=1
  ACCEPT_FAILED=`echo -e "$ACCEPT_RESULT" | grep -e "Update failed" -e "Problem running "` || ACCEPT_FAILED=1
  CHECK_DAEMON=`echo -e "$ACCEPT_RESULT" | grep -e "already owned by daemon running on port"` || CHECK_DAEMON=1
  # We have deamon lock need to kill the process
  if [[ $CHECK_DAEMON != "1" ]]; then  
    #Kill the deamon
    KillRTCDeamon $CHECK_DAEMON
    
    # Clean dir
    cd ..
    rm -rf ./$AdditionalFolderName/.jazz5
    rm -rf ./$AdditionalFolderName
    mkdir -p ./$AdditionalFolderName
    cd ./$AdditionalFolderName
  fi
  echo -e "$ACCEPT_RESULT" > RTC_FETCH_RESULT.txt
  echo -e "$ACCEPT_RESULT"
fi

# In case accept failed try to recover with reload
if [[ $ACCEPT_FAILED != "1" ]]; then
	# Delete current workspace
    cd ..
    rm -rf ./$AdditionalFolderName/.jazz5
    rm -rf ./$AdditionalFolderName
    mkdir -p ./$AdditionalFolderName/accept
    cd ./$AdditionalFolderName/accept    
    time ${LSCM}/lscm accept -r local -s $STREAM -t "$REPOSITORY_WORKSPACE" --no-merge --flow-components --overwrite-uncommitted --verbose || true
    cd ..
    time ${LSCM}/lscm load -r local -R ${LOAD_RULES} -d ${WORKSPACE}/${AdditionalFolderName}/ "$REPOSITORY_WORKSPACE" 2>LOAD_RESULT.TXT || true
    #Check load return value
    LOAD_RESULT=`cat LOAD_RESULT.TXT | grep -e "Problem running "` || LOAD_RESULT=1
    CHECK_DAEMON=`cat LOAD_RESULT.TXT | grep -e "already owned by daemon running on port"` || CHECK_DAEMON=1
    
  	# We have deamon lock need to kill the process
  	if [[ $CHECK_DAEMON != "1" ]]; then    
      #Kill the deamon
      KillRTCDeamon $CHECK_DAEMON
      
      # Clean dir
      cd ..
      rm -rf ./$AdditionalFolderName/.jazz5
      rm -rf ./$AdditionalFolderName
      mkdir -p ./$AdditionalFolderName
      cd ./$AdditionalFolderName
      
      # Daemon is killed try to download again
      time ${LSCM}/lscm load -r local -R ${LOAD_RULES} -d ${WORKSPACE}/${AdditionalFolderName}/ "$REPOSITORY_WORKSPACE" 2>LOAD_RESULT.TXT || true 
      # If fail again don't recover
      LOAD_RESULT=`cat LOAD_RESULT.TXT | grep -e "Problem running "` || LOAD_RESULT=1
  	fi      
    
    
    if [[ $LOAD_RESULT != "1" ]]; then
  		exit 1
    fi
    CHANGES_AVAILABLE=1
fi

if [[ $CHANGES_AVAILABLE == "1" ]]; then
	# Create snapshot
    time ${LSCM}/lscm create snapshot -r local -n $BUILD_NAME "$STREAM"
    echo -e "\n\nSNAPSHOT : $BUILD_NAME" >> RTC_FETCH_RESULT.txt
    # Execute build
	${WORKSPACE}/${AdditionalFolderName}/CI.BuildSystem/perform_build.sh "false"
fi

echo "CHANGES_AVAILABLE=$CHANGES_AVAILABLE" > env_config
cat env_config