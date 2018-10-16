# use with sudo from the CI.BuildSystem folder for local builds
#<variant> <is_release_buid (True/False)>
#!/bin/bash
cd scripts;
if [ -f "./env_conf.sh" ]; then
    #generate
    if [[ $1 == *"Dbg"* ]]; then
        build_type="Dbg"
    else
        build_type="Rel"
    fi

    echo "Would you like to force override Really ? (y/n)"
    #read ans
    #if [[ $ans == *"y"* ]]; then
    #    really_override="True"
    #else
    really_override="False"
    #fi
    work_dir=`pwd`
    work_dir="$(dirname "$(dirname "$work_dir")")"
    #cat > $PWD/env_conf.sh << EOT
    chmod +x $PWD/env_conf.sh
    . ./env_conf.sh;
    export AdditionalFolderName=""
    export ROOT_BUILD_CAUSE="SCMTRIGGER"
    #export OSVariant="${1%.*}"
    export IS_PRODUCT_BUILD="True"
    export SCRIPT_ROOT="$(dirname "$PWD")"
    export BUILD_CAUSE="UPSTREAMTRIGGER"
    #export BaseVariant="$1"
    export HAS_REALLY="True"
    export IS_DAILY_Linux_BUILD="False"
    export IS_DAILY_Integrity_BUILD="False"
    export _="/usr/bin/python"
    export SHELL="/bin/bash"
    export IS_RELEASE_BUILD="False"
    export BuildType="${build_type^}"
    export CARD_VERSION="00_00_00"
    export ftp_proxy="ftp://10.131.182.105:8080/"
    export BUILD_NAME="example" #to do: make it abstract
    export NODE_LABELS="MRA2 Linux - Integrity 3 MRA2Linux64bit3"
    export BUILD_ID="1"
    export JOB_NAME="Linux build"
    export WORKSPACE="$work_dir"
    export HTTPS_PROXY="https://10.131.182.105:8080/"
    #export Variant="$1"
    export REALLY_OVERRIDE="$really_override"
    export UserSettings="--usersettings=$WORKSPACE/UserSettings.set"
	export NO_PROXY="ccs-sof.sofia.visteon.com,jazz.visteon.com:9443/ccm/,localhost,127.0.0.1,localaddress,192.168.106.96,192.168.106.98,192.168.106.99,192.168.106.100,10.185.4.252,10.142.144.96,10.185.4.98,10.185.4.99,10.185.4.100,.localdomain.com"
    export UPSTART_EVENTS="started xsession"
    export BUILD_TAG="jenkins-DAG_MRA2_MY20_DI_Integration-Build-7"
    export requestUUID="_LMqJMMLLEeeIIYbOmc_uVg"
    export SHELL="/bin/bash"
    export XDG_DATA_DIRS="/usr/share/xubuntu:/usr/share/xfce4:/usr/local/share/:/usr/share/:/usr/share"
    export MANDATORY_PATH="/usr/share/gconf/xubuntu.mandatory.path"
    export buildEngineHostName="visteon"
    export DBUS_SESSION_BUS_ADDRESS="unix:abstract=/tmp/dbus-EfjxkoPS7M"
    export UPSTART_INSTANCE=""
    export JOB="dbus"
    export SESSION="xubuntu"
    export BUILD_CAUSE_MANUALTRIGGER="true"
    export HUDSON_URL="http://jenkins-mra2.sofia.visteon.com/"
    export XMODIFIERS="@im=none"
    export ROOT_BUILD_CAUSE="SCMTRIGGER"
    export SELINUX_INIT="YES"
    export BUILD_NUMBER="7"
    export XDG_RUNTIME_DIR="/run/user/1000"
    export team_scm_componentLoadRules="component=_5DfwkAP9EeeQYNqC0IxPxw fileitem=_G3MvwMClEeeEUKWsrfaCQQ "
    export SESSIONTYPE=""
    export buildRequesterUserId="KARLSRCI"
    export JOB_BASE_NAME="Build"
    export XDG_SESSION_ID="1"
    export IS_PRODUCT_BUILD="False"
    export DEFAULTS_PATH="/usr/share/gconf/xubuntu.default.path"
    export buildLabel="#7"
    export DESKTOP_SESSION="xubuntu"
    export IS_Domain_BUILD="False"
    export IS_DAILY_BUILD="False"
    export EXECUTOR_NUMBER="0"
    export INSTANCE=""
    export ITERATION_NUMBER_CARS="0.0"
    export IS_RELEASE_BUILD="False"
    export team_scm_fetchDestination="./IncrementalBuild"
    export MAIL="/var/mail/visteon"
    export LS_COLORS="rs=0:di=01;34:ln=01;36:mh=00:pi=40;33:so=01;35:do=01;35:bd=40;33;01:cd=40;33;01:or=40;31;01:su=37;41:sg=30;43:ca=30;41:tw=30;42:ow=34;42:st=37;44:ex=01;32:*.tar=01;31:*.tgz=01;31:*.arj=01;31:*.taz=01;31:*.lzh=01;31:*.lzma=01;31:*.tlz=01;31:*.txz=01;31:*.zip=01;31:*.z=01;31:*.Z=01;31:*.dz=01;31:*.gz=01;31:*.lz=01;31:*.xz=01;31:*.bz2=01;31:*.bz=01;31:*.tbz=01;31:*.tbz2=01;31:*.tz=01;31:*.deb=01;31:*.rpm=01;31:*.jar=01;31:*.war=01;31:*.ear=01;31:*.sar=01;31:*.rar=01;31:*.ace=01;31:*.zoo=01;31:*.cpio=01;31:*.7z=01;31:*.rz=01;31:*.jpg=01;35:*.jpeg=01;35:*.gif=01;35:*.bmp=01;35:*.pbm=01;35:*.pgm=01;35:*.ppm=01;35:*.tga=01;35:*.xbm=01;35:*.xpm=01;35:*.tif=01;35:*.tiff=01;35:*.png=01;35:*.svg=01;35:*.svgz=01;35:*.mng=01;35:*.pcx=01;35:*.mov=01;35:*.mpg=01;35:*.mpeg=01;35:*.m2v=01;35:*.mkv=01;35:*.webm=01;35:*.ogm=01;35:*.mp4=01;35:*.m4v=01;35:*.mp4v=01;35:*.vob=01;35:*.qt=01;35:*.nuv=01;35:*.wmv=01;35:*.asf=01;35:*.rm=01;35:*.rmvb=01;35:*.flc=01;35:*.avi=01;35:*.fli=01;35:*.flv=01;35:*.gl=01;35:*.dl=01;35:*.xcf=01;35:*.xwd=01;35:*.yuv=01;35:*.cgm=01;35:*.emf=01;35:*.axv=01;35:*.anx=01;35:*.ogv=01;35:*.ogx=01;35:*.aac=00;36:*.au=00;36:*.flac=00;36:*.mid=00;36:*.midi=00;36:*.mka=00;36:*.mp3=00;36:*.mpc=00;36:*.ogg=00;36:*.ra=00;36:*.wav=00;36:*.axa=00;36:*.oga=00;36:*.spx=00;36:*.xspf=00;36:"
    export com_ibm_team_build_internal_engine_request_processing_disabled="true"
    export JENKINS_HOME="/var/lib/jenkins"
    export BUILD_CAUSE="UPSTREAMTRIGGER"
    export IS_DOMAIN_BUILD="True"
    export LESSOPEN="| /usr/bin/lesspipe %s"
    export FTP_PROXY="localhost:3128"
    export team_scm_acceptBeforeFetch="true"
    export HUDSON_SERVER_COOKIE="9f20395fbf752b38"
    export USER="visteon"
    export XDG_VTNR="7"
    export BUILD_NAME="example"
    export REALLY_OVERRIDE="False"
    export XAUTHORITY="/home/visteon/.Xauthority"
    export LANGUAGE="en_US"
    export SESSION_MANAGER="local/visteon:@/tmp/.ICE-unix/1961,unix/visteon:/tmp/.ICE-unix/1961"
    export SHLVL="3"
    export DISPLAY=":0.0"
    export CLUTTER_IM_MODULE="xim"
    export WINDOWID="44040277"
    export ROOT_BUILD_CAUSE_MANUALTRIGGER="true"
    export GPG_AGENT_INFO="/run/user/1000/keyring-TAFT1I/gpg:0:1"
    export IS_DAILY_Linux_BUILD="False"
    export SCRIPT_ROOT="."
    export GDMSESSION="xubuntu"
    export UPSTART_JOB="startxfce4"
    export XDG_MENU_PREFIX="xfce-"
    export XDG_SEAT_PATH="/org/freedesktop/DisplayManager/Seat0"
    export _="/usr/bin/python"
    export GTK_IM_MODULE="xim"
    export SSH_CONNECTION="10.185.2.135 52641 10.185.20.201 22"
    export XDG_CONFIG_DIRS="/etc/xdg/xdg-xubuntu:/usr/share/upstart/xdg:/etc/xdg:/etc/xdg"
    export team_scm_snapshotUUID="_MBKIQMLLEeeIIYbOmc_uVg"
    export COLORTERM="xfce4-terminal"
    export team_scm_createFoldersForComponents="false"
    export XDG_GREETER_DATA_DIR="/var/lib/lightdm-data/visteon"
    export QT4_IM_MODULE="xim"
    export IS_Nightly_Integrity_BUILD="False"
    export TODAY_DATE="20171106"
    export XDG_CURRENT_DESKTOP="XFCE"
    pushd `dirname $0` > /dev/null
    export WORKSPACE=`pwd`/../../..
    popd > /dev/null
    export HOME="/home/visteon"
    export JOB_NAME="Linux build"
    export LANG="en_US.UTF-8"
    export IS_Nightly_Linux_BUILD="False"
    export IS_DAILY_Integrity_BUILD="False"
    export HUDSON_HOME="/var/lib/jenkins"
    export com_ibm_team_build_internal_engine_template_id="com.ibm.rational.connector.hudson.engine.template"
    export TEXTDOMAIN="im-config"
    export BuildType="Rel"
    export CARD_VERSION="0.1.0"
    export com_ibm_team_build_internal_engine_monitoring_threshold="0"
    export HUDSON_COOKIE="f65c53bc-7893-4ad5-ad0e-323041eda38d"
    export team_scm_acceptPhaseOver="true"
    export UPSTART_SESSION="unix:abstract=/com/ubuntu/upstart-session/1000/1808"
    export team_scm_loadComponents="_5DfwkAP9EeeQYNqC0IxPxw"
    export NLSPATH="/usr/dt/lib/nls/msg/%L/%N.cat"
    export com_ibm_rational_connector_hudson_connectionTimeout="300"
    export LESSCLOSE="/usr/bin/lesspipe %s %s"
    export GNOME_KEYRING_PID="1925"
    export HAS_REALLY="False"
    export GLADE_PIXMAP_PATH=":"
    export AdditionalFolderName=""
    export buildEngineId="MRA2_Integration"
    export ARCHIVING="false"
    export ITERATION_NUMBER="0.0"
    export ITERATION="E001"
    export Machine="Linux"
    export SSH_CLIENT="10.185.2.135 52641 22"
    export JENKINS_URL="http://jenkins-mra2.sofia.visteon.com/"
    export LOGNAME="visteon"
    export XDG_SEAT="seat0"
    export GNOME_KEYRING_CONTROL="/run/user/1000/keyring-TAFT1I"
    export PATH="/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin:/usr/games:/usr/local/games:/opt/cov-analysis-linux64/bin/:/opt/cov-analysis-linux64-8.5.0/bin"
    export TERM="xterm"
    export XDG_SESSION_PATH="/org/freedesktop/DisplayManager/Session0"
    export no_proxy="ccs-sof.sofia.visteon.com,jazz.visteon.com:9443/ccm/,localhost,127.0.0.1,localaddress,192.168.106.96,192.168.106.98,192.168.106.99,192.168.106.100,10.185.4.252,10.142.144.96,10.185.4.98,10.185.4.99,10.185.4.100,.localdomain.com"
    export Variant="TegraP1Integrity.Dbg.B0hw.C5.MRA2"
    export repositoryAddress="https://jazz.sofia.visteon.com:9443/ccm2/"
    export NODE_LABELS="MRA2 Linux - Integrity 3 MRA2Linux64bit3"
    export team_scm_includeComponents="false"
    export team_scm_deleteDestinationBeforeFetch="false"
    export IM_CONFIG_PHASE="1"
    export GLADE_CATALOG_PATH=":"
    export BUILD_ID="1"
    export GLADE_MODULE_PATH=":"
    export SSH_AUTH_SOCK="/run/user/1000/keyring-TAFT1I/ssh"
    export TEXTDOMAINDIR="/usr/share/locale/"
    export team_scm_buildOnlyIfChanges="true"
    export com_ibm_team_build_internal_template_id="com.ibm.rational.connector.hudson.ui.buildDefinitionTemplate"
    export RTCBuildResultUUID="_LMqwQMLLEeeIIYbOmc_uVg"
    export OLDPWD="/workspace/workspace/DAG_MRA2_MY20_DI_Integration/Build/IncrementalBuild/CI.BuildSystem"
    export GDM_LANG="en_US"
    export team_scm_workspaceUUID="_I42pAMCmEeeIIYbOmc_uVg"
    export PWD="/home/visteon/workspace/DAG_MRA2_MY20_DI_Integration/Build/IncrementalBuild/CI.BuildSystem"
    export SDKType="TegraP1"
    export JENKINS_SERVER_COOKIE="9f20395fbf752b38"
    export BUILD_DISPLAY_NAME="20171106-DAG.MRA2.MY20.DI.Integration.7"
    export XFILESEARCHPATH="/usr/dt/app-defaults/%L/Dt"

else
        echo "****** ERROR! Missing env_conf. EXIT..."
        exit
fi

echo "****** Local build ******"
echo " Do you want clean build ? (y/n)"
read ans

if [ -d "../../ProductSpace" ]; then
    if [[ $ans == *"y"* ]]; then
        echo "Deleting ProductSpace..."
        sudo rm -rf ../ProductSpace
    fi
fi

if [ -d "../ReleaseSpace" ]; then
    if [[ $ans == *"y"* ]]; then
        echo "Deleting InterSpace..."
        sudo rm -rf ../InterSpace
    fi
fi

if [ -d "../../ReleaseSpace" ]; then
    if [[ $ans == *"y"* ]]; then
        echo "Deleting ReleaseSpace..."
        sudo rm -rf ../ReleaseSpace
    fi
fi

cd ..;
python ./bspos_exec.py "false"

