#!/bin/bash

if [ "$(echo $FolderPath |grep "workspace"|wc -w)" == 1 ]; then
    FolderPath="/workspace/"${FolderPath##*workspace/}
    echo "Following Folder will be deleted"
    echo "$FolderPath"
    if [ "$ServerAddress" != "10.185.4.91" ]; then
        /usr/bin/sshpass -p 'visteon' ssh visteon@$ServerAddress 'echo "visteon" | sudo -S rm -rf' $FolderPath

        /usr/bin/sshpass -p 'visteon' ssh visteon@$ServerAddress "[ -d $FolderPath ]" && echo "Some problem was occured.Please, try again." || echo "The folder was deleted succesfully"
    else
        rm -rf $FolderPath
        [ -d "$FolderPath" ] && echo "Some problem was occured.Please, try again." || echo "The folder was deleted succesfully"
    fi
else
    echo "Folder does not exists or is denied for deletion"
fi


 
